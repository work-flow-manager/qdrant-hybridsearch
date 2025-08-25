"""FastAPI application for Qdrant Hybrid Search"""

from fastapi import FastAPI, HTTPException, Depends, Security, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch
import time
import logging
import structlog
from typing import Optional, List
from contextlib import asynccontextmanager

from app.config import settings
from app.models import (
    DocumentBatch, SearchRequest, SearchResponse, SearchResult,
    CollectionInfo, HealthStatus, IndexingResponse,
    WebhookRequest, WebhookResponse
)
from app.search_engine import HybridSearchEngine

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Global search engine instance
search_engine: Optional[HybridSearchEngine] = None

# Security
security = HTTPBearer(auto_error=False)

def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify API key if configured"""
    if settings.api_key:
        if not credentials or credentials.credentials != settings.api_key:
            raise HTTPException(status_code=403, detail="Invalid API key")
    return True

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global search_engine
    
    # Startup
    logger.info("Starting Qdrant Hybrid Search API", gpu_available=torch.cuda.is_available())
    
    search_engine = HybridSearchEngine()
    success = search_engine.load_models()
    
    if not success:
        logger.error("Failed to load models")
    else:
        # Create default collection
        search_engine.create_collection()
        logger.info("Search engine initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Qdrant Hybrid Search API")

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    lifespan=lifespan
)

# Configure CORS
if settings.cors_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/health", response_model=HealthStatus)
async def health_check():
    """Health check endpoint"""
    gpu_name = None
    gpu_available = torch.cuda.is_available()
    
    if gpu_available:
        gpu_name = torch.cuda.get_device_name(0)
    
    try:
        # Check Qdrant connection
        collections = search_engine.qdrant_client.get_collections()
        qdrant_connected = True
    except:
        qdrant_connected = False
    
    models_loaded = (
        search_engine.dense_model is not None and 
        search_engine.sparse_model is not None
    )
    
    return HealthStatus(
        status="healthy" if models_loaded and qdrant_connected else "degraded",
        qdrant_connected=qdrant_connected,
        gpu_available=gpu_available,
        gpu_name=gpu_name,
        models_loaded=models_loaded,
        version=settings.api_version
    )

@app.post("/index", response_model=IndexingResponse)
async def index_documents(
    batch: DocumentBatch,
    background_tasks: BackgroundTasks,
    authorized: bool = Depends(verify_api_key)
):
    """Index documents into the search engine"""
    if not search_engine or not search_engine.dense_model:
        raise HTTPException(status_code=503, detail="Search engine not initialized")
    
    start_time = time.time()
    
    # Convert to dict format
    documents = [
        {
            "id": doc.id,
            "text": doc.text,
            "metadata": doc.metadata or {}
        }
        for doc in batch.documents
    ]
    
    # Index documents
    indexed_count, errors = search_engine.index_documents(
        documents,
        batch.collection_name
    )
    
    processing_time = (time.time() - start_time) * 1000
    
    return IndexingResponse(
        indexed_count=indexed_count,
        failed_count=len(documents) - indexed_count,
        collection_name=batch.collection_name or settings.qdrant_collection,
        processing_time_ms=processing_time,
        errors=errors if errors else None
    )

@app.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    authorized: bool = Depends(verify_api_key)
):
    """Perform hybrid search"""
    if not search_engine or not search_engine.dense_model:
        raise HTTPException(status_code=503, detail="Search engine not initialized")
    
    start_time = time.time()
    
    # Perform search
    results = search_engine.search(
        query=request.query,
        mode=request.mode.value,
        limit=request.limit,
        filters=request.filters,
        collection_name=request.collection_name
    )
    
    processing_time = (time.time() - start_time) * 1000
    
    # Convert to response format
    search_results = [
        SearchResult(
            id=r["id"],
            score=r["score"],
            text=r["text"],
            metadata=r["metadata"]
        )
        for r in results
    ]
    
    return SearchResponse(
        query=request.query,
        mode=request.mode.value,
        results=search_results,
        total=len(search_results),
        processing_time_ms=processing_time
    )

@app.get("/collections", response_model=List[str])
async def list_collections(authorized: bool = Depends(verify_api_key)):
    """List all collections"""
    if not search_engine:
        raise HTTPException(status_code=503, detail="Search engine not initialized")
    
    try:
        collections = search_engine.qdrant_client.get_collections()
        return [c.name for c in collections.collections]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collections/{name}", response_model=CollectionInfo)
async def get_collection_info(
    name: str,
    authorized: bool = Depends(verify_api_key)
):
    """Get collection information"""
    if not search_engine:
        raise HTTPException(status_code=503, detail="Search engine not initialized")
    
    info = search_engine.get_collection_info(name)
    if not info:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    return CollectionInfo(**info)

@app.delete("/collections/{name}")
async def delete_collection(
    name: str,
    authorized: bool = Depends(verify_api_key)
):
    """Delete a collection"""
    if not search_engine:
        raise HTTPException(status_code=503, detail="Search engine not initialized")
    
    if name == settings.qdrant_collection:
        raise HTTPException(status_code=400, detail="Cannot delete default collection")
    
    success = search_engine.delete_collection(name)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete collection")
    
    return {"message": f"Collection {name} deleted successfully"}

@app.post("/webhook", response_model=WebhookResponse)
async def webhook_handler(
    request: WebhookRequest,
    background_tasks: BackgroundTasks
):
    """Handle n8n webhook requests"""
    if not settings.n8n_webhook_enabled:
        raise HTTPException(status_code=404, detail="Webhook endpoint disabled")
    
    try:
        # Handle different webhook actions
        if request.action == "search":
            # Perform search
            search_req = SearchRequest(**request.data)
            results = await search(search_req, authorized=True)
            return WebhookResponse(
                success=True,
                data=results.dict(),
                webhook_id=request.webhook_id
            )
            
        elif request.action == "index":
            # Index documents
            batch = DocumentBatch(**request.data)
            result = await index_documents(batch, background_tasks, authorized=True)
            return WebhookResponse(
                success=True,
                data=result.dict(),
                webhook_id=request.webhook_id
            )
            
        else:
            return WebhookResponse(
                success=False,
                error=f"Unknown action: {request.action}",
                webhook_id=request.webhook_id
            )
            
    except Exception as e:
        logger.error("Webhook error", error=str(e))
        return WebhookResponse(
            success=False,
            error=str(e),
            webhook_id=request.webhook_id
        )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.api_title,
        "version": settings.api_version,
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "Not available",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower()
    )