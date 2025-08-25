# Dockerfile PRINCIPAL - Funciona com ou sem GPU
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Configurações
ENV NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    CUDA_VISIBLE_DEVICES=0 \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HF_HOME=/app/models \
    TRANSFORMERS_CACHE=/app/models \
    SENTENCE_TRANSFORMERS_HOME=/app/models

# Instalar Python 3.11
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    python3.11-distutils \
    git \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar PyTorch com CUDA 12.1
RUN python3 -m pip install --upgrade pip setuptools wheel && \
    python3 -m pip install torch==2.1.0+cu121 torchvision==0.16.0+cu121 --index-url https://download.pytorch.org/whl/cu121

# Instalar dependências
RUN python3 -m pip install --no-cache-dir \
    transformers==4.36.2 \
    sentence-transformers==2.2.2 \
    huggingface-hub==0.19.4 \
    qdrant-client==1.7.0 \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    pydantic==2.5.0 \
    pydantic-settings==2.1.0 \
    numpy==1.24.3 \
    scikit-learn==1.3.2 \
    python-multipart==0.0.6 \
    httpx==0.25.1 \
    python-jose[cryptography]==3.3.0 \
    passlib[bcrypt]==1.7.4 \
    aiofiles==23.2.1 \
    accelerate==0.25.0 \
    structlog==23.2.0 \
    uvloop==0.19.0 \
    scipy==1.11.4 \
    pillow==10.1.0

# Copiar código
COPY app/ /app/app/

# Criar diretórios
RUN mkdir -p /app/data /app/models

# Script de inicialização
RUN cat > /app/start.sh << 'EOF'
#!/bin/bash
echo "🚀 Iniciando Qdrant Hybrid Search..."
python3 -c "
import torch
import os
if torch.cuda.is_available():
    print(f'✅ GPU detectada: {torch.cuda.get_device_name(0)}')
    os.environ['USE_GPU'] = 'true'
else:
    print('⚠️ GPU não disponível - usando CPU')
    os.environ['USE_GPU'] = 'false'
"
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
EOF

RUN chmod +x /app/start.sh

HEALTHCHECK --interval=30s --timeout=10s --start-period=180s --retries=5 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["/app/start.sh"]