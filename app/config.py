"""Configuration settings for Qdrant Hybrid Search API"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings with GPU optimization for RTX 4000"""
    
    # API Configuration
    api_title: str = "Qdrant Hybrid Search API"
    api_version: str = "1.0.0"
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_key: Optional[str] = Field(default=None, env="API_KEY")
    
    # Qdrant Configuration
    qdrant_host: str = Field(default="localhost", env="QDRANT_HOST")
    qdrant_port: int = Field(default=6333, env="QDRANT_PORT")
    qdrant_api_key: Optional[str] = Field(default=None, env="QDRANT_API_KEY")
    qdrant_collection: str = Field(default="hybrid_search", env="QDRANT_COLLECTION")
    
    # Model Configuration with GPU optimization
    dense_model: str = Field(
        default="intfloat/multilingual-e5-large",
        env="DENSE_MODEL"
    )
    sparse_model: str = Field(
        default="prithivida/Splade_PP_en_v1", 
        env="SPARSE_MODEL"
    )
    
    # GPU Settings for RTX 4000
    use_gpu: bool = Field(default=True, env="USE_GPU")
    cuda_device: int = Field(default=0, env="CUDA_DEVICE")
    batch_size: int = Field(default=32, env="BATCH_SIZE")  # Optimized for 8GB VRAM
    max_sequence_length: int = Field(default=512, env="MAX_SEQUENCE_LENGTH")
    
    # Performance Settings
    num_workers: int = Field(default=4, env="NUM_WORKERS")
    cache_embeddings: bool = Field(default=True, env="CACHE_EMBEDDINGS")
    embedding_cache_size: int = Field(default=10000, env="EMBEDDING_CACHE_SIZE")
    
    # Search Settings
    default_limit: int = Field(default=10, env="DEFAULT_LIMIT")
    max_limit: int = Field(default=100, env="MAX_LIMIT")
    fusion_weight: float = Field(default=0.5, env="FUSION_WEIGHT")  # Balance between dense and sparse
    
    # n8n Integration
    n8n_webhook_enabled: bool = Field(default=True, env="N8N_WEBHOOK_ENABLED")
    n8n_webhook_timeout: int = Field(default=30, env="N8N_WEBHOOK_TIMEOUT")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # CORS Settings
    cors_enabled: bool = Field(default=True, env="CORS_ENABLED")
    cors_origins: list[str] = Field(
        default=["*"],
        env="CORS_ORIGINS"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()