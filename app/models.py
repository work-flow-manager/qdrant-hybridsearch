"""Data models for the Hybrid Search API"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class SearchMode(str, Enum):
    """Search modes available"""
    HYBRID = "hybrid"
    DENSE = "dense"
    SPARSE = "sparse"

class DocumentInput(BaseModel):
    """Model for document input"""
    id: Optional[str] = Field(default=None, description="Document ID")
    text: str = Field(..., description="Document text content")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Document metadata")
    
class DocumentBatch(BaseModel):
    """Model for batch document upload"""
    documents: List[DocumentInput] = Field(..., description="List of documents to index")
    collection_name: Optional[str] = Field(default=None, description="Target collection name")

class SearchRequest(BaseModel):
    """Model for search requests"""
    query: str = Field(..., description="Search query text")
    mode: SearchMode = Field(default=SearchMode.HYBRID, description="Search mode")
    limit: int = Field(default=10, ge=1, le=100, description="Number of results to return")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Metadata filters")
    collection_name: Optional[str] = Field(default=None, description="Collection to search")
    
class SearchResult(BaseModel):
    """Model for individual search result"""
    id: str = Field(..., description="Document ID")
    score: float = Field(..., description="Relevance score")
    text: str = Field(..., description="Document text")
    metadata: Dict[str, Any] = Field(default={}, description="Document metadata")
    dense_score: Optional[float] = Field(default=None, description="Dense embedding score")
    sparse_score: Optional[float] = Field(default=None, description="Sparse embedding score")

class SearchResponse(BaseModel):
    """Model for search response"""
    query: str = Field(..., description="Original query")
    mode: str = Field(..., description="Search mode used")
    results: List[SearchResult] = Field(..., description="Search results")
    total: int = Field(..., description="Total number of results")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    
class CollectionInfo(BaseModel):
    """Model for collection information"""
    name: str = Field(..., description="Collection name")
    vectors_count: int = Field(..., description="Number of vectors in collection")
    points_count: int = Field(..., description="Number of points in collection")
    config: Dict[str, Any] = Field(..., description="Collection configuration")
    
class HealthStatus(BaseModel):
    """Model for health check response"""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    qdrant_connected: bool = Field(..., description="Qdrant connection status")
    gpu_available: bool = Field(..., description="GPU availability")
    gpu_name: Optional[str] = Field(default=None, description="GPU device name")
    models_loaded: bool = Field(..., description="Models loading status")
    version: str = Field(..., description="API version")

class IndexingResponse(BaseModel):
    """Model for indexing response"""
    indexed_count: int = Field(..., description="Number of documents indexed")
    failed_count: int = Field(default=0, description="Number of failed documents")
    collection_name: str = Field(..., description="Collection name")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    errors: Optional[List[str]] = Field(default=None, description="List of errors if any")

class WebhookRequest(BaseModel):
    """Model for n8n webhook integration"""
    action: str = Field(..., description="Action to perform")
    data: Dict[str, Any] = Field(..., description="Action data")
    webhook_id: Optional[str] = Field(default=None, description="Webhook identifier")
    
class WebhookResponse(BaseModel):
    """Model for webhook response"""
    success: bool = Field(..., description="Operation success status")
    data: Optional[Any] = Field(default=None, description="Response data")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    webhook_id: Optional[str] = Field(default=None, description="Webhook identifier")