"""Hybrid Search Engine with GPU-accelerated embeddings"""

import torch
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForMaskedLM
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, VectorParams, PointStruct, SparseVector
import hashlib
import time
from functools import lru_cache
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class HybridSearchEngine:
    """GPU-optimized hybrid search engine for RTX 4000"""
    
    def __init__(self):
        """Initialize search engine with GPU support"""
        self.device = self._setup_device()
        self.qdrant_client = self._setup_qdrant()
        self.dense_model = None
        self.sparse_model = None
        self.sparse_tokenizer = None
        self._embedding_cache = {}
        
    def _setup_device(self) -> torch.device:
        """Setup CUDA device for RTX 4000"""
        if settings.use_gpu and torch.cuda.is_available():
            device = torch.device(f"cuda:{settings.cuda_device}")
            logger.info(f"Using GPU: {torch.cuda.get_device_name(settings.cuda_device)}")
            # Set memory optimization for RTX 4000 (8GB VRAM)
            torch.cuda.set_per_process_memory_fraction(0.9)
            torch.backends.cudnn.benchmark = True
            return device
        else:
            logger.warning("GPU not available, using CPU")
            return torch.device("cpu")
    
    def _setup_qdrant(self) -> QdrantClient:
        """Setup Qdrant client"""
        return QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            api_key=settings.qdrant_api_key,
            timeout=30
        )
    
    def load_models(self):
        """Load embedding models with GPU optimization"""
        try:
            # Load dense model (multilingual-e5-large)
            logger.info(f"Loading dense model: {settings.dense_model}")
            self.dense_model = SentenceTransformer(
                settings.dense_model,
                device=self.device
            )
            self.dense_model.max_seq_length = settings.max_sequence_length
            
            # Load sparse model (Splade)
            logger.info(f"Loading sparse model: {settings.sparse_model}")
            self.sparse_tokenizer = AutoTokenizer.from_pretrained(settings.sparse_model)
            self.sparse_model = AutoModelForMaskedLM.from_pretrained(settings.sparse_model)
            self.sparse_model.to(self.device)
            self.sparse_model.eval()
            
            # Optimize models for inference
            if settings.use_gpu:
                self.dense_model = self.dense_model.half()  # Use FP16 for faster inference
                self.sparse_model = self.sparse_model.half()
                
            logger.info("Models loaded successfully with GPU optimization")
            return True
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False
    
    def create_collection(self, collection_name: str = None) -> bool:
        """Create Qdrant collection with hybrid search configuration"""
        collection_name = collection_name or settings.qdrant_collection
        
        try:
            # Check if collection exists
            collections = self.qdrant_client.get_collections()
            if any(c.name == collection_name for c in collections.collections):
                logger.info(f"Collection {collection_name} already exists")
                return True
            
            # Create collection with dense and sparse vectors
            self.qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    "dense": VectorParams(
                        size=1024,  # multilingual-e5-large embedding size
                        distance=Distance.COSINE
                    )
                },
                sparse_vectors_config={
                    "sparse": models.SparseVectorParams(
                        index=models.SparseIndexParams(
                            on_disk=False  # Keep in RAM for RTX 4000 performance
                        )
                    )
                }
            )
            
            logger.info(f"Collection {collection_name} created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            return False
    
    @torch.no_grad()
    def encode_dense(self, texts: List[str]) -> np.ndarray:
        """Encode texts to dense embeddings with GPU acceleration"""
        # Prefix texts for e5-large model
        prefixed_texts = [f"passage: {text}" for text in texts]
        
        # Batch encoding with optimal batch size for RTX 4000
        embeddings = []
        for i in range(0, len(prefixed_texts), settings.batch_size):
            batch = prefixed_texts[i:i + settings.batch_size]
            batch_embeddings = self.dense_model.encode(
                batch,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False
            )
            embeddings.append(batch_embeddings)
        
        return np.vstack(embeddings) if embeddings else np.array([])
    
    @torch.no_grad()
    def encode_sparse(self, texts: List[str]) -> List[SparseVector]:
        """Encode texts to sparse embeddings with GPU acceleration"""
        sparse_vectors = []
        
        for text in texts:
            # Tokenize with max length constraint (24 for queries, 128 for docs)
            max_length = 24 if len(text) < 100 else 128
            inputs = self.sparse_tokenizer(
                text,
                return_tensors="pt",
                max_length=max_length,
                truncation=True,
                padding="max_length"
            ).to(self.device)
            
            # Get logits from model
            outputs = self.sparse_model(**inputs)
            logits = outputs.logits
            
            # Apply log-softmax and max pooling
            log_probs = torch.log_softmax(logits, dim=-1)
            pooled = log_probs.max(dim=1).values.squeeze()
            
            # Apply ReLU and get non-zero indices
            relu_probs = torch.relu(pooled)
            
            # Convert to sparse vector
            non_zero_indices = relu_probs.nonzero().squeeze().cpu().numpy()
            non_zero_values = relu_probs[non_zero_indices].cpu().numpy()
            
            if len(non_zero_indices) > 0:
                sparse_vector = SparseVector(
                    indices=non_zero_indices.tolist(),
                    values=non_zero_values.tolist()
                )
            else:
                sparse_vector = SparseVector(indices=[], values=[])
            
            sparse_vectors.append(sparse_vector)
        
        return sparse_vectors
    
    def index_documents(
        self,
        documents: List[Dict[str, Any]],
        collection_name: str = None
    ) -> Tuple[int, List[str]]:
        """Index documents with hybrid embeddings"""
        collection_name = collection_name or settings.qdrant_collection
        indexed_count = 0
        errors = []
        
        try:
            # Extract texts
            texts = [doc["text"] for doc in documents]
            
            # Generate embeddings in batches
            logger.info(f"Encoding {len(texts)} documents...")
            dense_embeddings = self.encode_dense(texts)
            sparse_embeddings = self.encode_sparse(texts)
            
            # Prepare points for Qdrant
            points = []
            for i, doc in enumerate(documents):
                doc_id = doc.get("id", hashlib.md5(doc["text"].encode()).hexdigest())
                
                point = PointStruct(
                    id=doc_id,
                    vector={
                        "dense": dense_embeddings[i].tolist()
                    },
                    payload={
                        "text": doc["text"],
                        "metadata": doc.get("metadata", {})
                    }
                )
                points.append(point)
            
            # Upload to Qdrant in batches
            batch_size = 100
            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                self.qdrant_client.upsert(
                    collection_name=collection_name,
                    points=batch
                )
                
                # Also upload sparse vectors
                sparse_batch = sparse_embeddings[i:i + batch_size]
                for j, point in enumerate(batch):
                    self.qdrant_client.update_vectors(
                        collection_name=collection_name,
                        points=[
                            models.PointVectors(
                                id=point.id,
                                vector={"sparse": sparse_batch[j]}
                            )
                        ]
                    )
                
                indexed_count += len(batch)
                logger.info(f"Indexed {indexed_count}/{len(documents)} documents")
            
        except Exception as e:
            logger.error(f"Error indexing documents: {e}")
            errors.append(str(e))
        
        return indexed_count, errors
    
    def search(
        self,
        query: str,
        mode: str = "hybrid",
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        collection_name: str = None
    ) -> List[Dict[str, Any]]:
        """Perform hybrid search with RRF fusion"""
        collection_name = collection_name or settings.qdrant_collection
        results = []
        
        try:
            # Encode query
            query_prefix = f"query: {query}"
            dense_query = self.encode_dense([query_prefix])[0]
            sparse_query = self.encode_sparse([query])[0]
            
            if mode == "hybrid":
                # Hybrid search with RRF fusion
                search_result = self.qdrant_client.query_points(
                    collection_name=collection_name,
                    query=models.FusionQuery(
                        fusion=models.Fusion.RRF
                    ),
                    prefetch=[
                        models.Prefetch(
                            query=dense_query.tolist(),
                            using="dense",
                            limit=limit * 2  # Fetch more for fusion
                        ),
                        models.Prefetch(
                            query=sparse_query,
                            using="sparse",
                            limit=limit * 2
                        )
                    ],
                    limit=limit,
                    with_payload=True
                )
                
            elif mode == "dense":
                # Dense-only search
                search_result = self.qdrant_client.search(
                    collection_name=collection_name,
                    query_vector=("dense", dense_query.tolist()),
                    limit=limit,
                    with_payload=True
                )
                
            elif mode == "sparse":
                # Sparse-only search
                search_result = self.qdrant_client.search(
                    collection_name=collection_name,
                    query_vector=("sparse", sparse_query),
                    limit=limit,
                    with_payload=True
                )
            
            # Format results
            for point in search_result:
                result = {
                    "id": point.id,
                    "score": point.score if hasattr(point, 'score') else 0.0,
                    "text": point.payload.get("text", ""),
                    "metadata": point.payload.get("metadata", {})
                }
                results.append(result)
                
        except Exception as e:
            logger.error(f"Error during search: {e}")
        
        return results
    
    def get_collection_info(self, collection_name: str = None) -> Dict[str, Any]:
        """Get collection statistics"""
        collection_name = collection_name or settings.qdrant_collection
        
        try:
            info = self.qdrant_client.get_collection(collection_name)
            return {
                "name": collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "config": {
                    "vector_size": info.config.params.vectors.get("dense").size,
                    "distance": str(info.config.params.vectors.get("dense").distance)
                }
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}
    
    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection"""
        try:
            self.qdrant_client.delete_collection(collection_name)
            logger.info(f"Collection {collection_name} deleted")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            return False