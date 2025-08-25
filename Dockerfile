# Multi-stage build for optimized image with GPU support
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04 AS base

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CUDA_VISIBLE_DEVICES=0 \
    TORCH_CUDA_ARCH_LIST="7.5;8.0;8.6;8.9" \
    HF_HOME=/app/models \
    TRANSFORMERS_CACHE=/app/models \
    SENTENCE_TRANSFORMERS_HOME=/app/models

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip first
RUN python3 -m pip install --upgrade pip setuptools wheel

# Install Python dependencies with CUDA support
RUN pip3 install --no-cache-dir -r requirements.txt

# Pre-download models during build
RUN python3 -c "from sentence_transformers import SentenceTransformer; \
    model = SentenceTransformer('intfloat/multilingual-e5-large'); \
    print('Dense model downloaded')"

RUN python3 -c "from transformers import AutoTokenizer, AutoModelForMaskedLM; \
    tokenizer = AutoTokenizer.from_pretrained('prithivida/Splade_PP_en_v1'); \
    model = AutoModelForMaskedLM.from_pretrained('prithivida/Splade_PP_en_v1'); \
    print('Sparse model downloaded')"

# Copy application code
COPY app/ /app/app/

# Create data directory
RUN mkdir -p /app/data

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run the application
CMD ["python3", "-m", "uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1", \
     "--loop", "uvloop"]