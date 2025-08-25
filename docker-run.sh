#!/bin/bash

# Script para executar container com GPU support usando --gpus all

echo "🚀 Iniciando Qdrant Hybrid Search com GPU Support"
echo "================================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker não está instalado${NC}"
    exit 1
fi

# Verificar NVIDIA Docker runtime
if ! docker info 2>/dev/null | grep -q nvidia; then
    echo -e "${YELLOW}⚠️  NVIDIA Docker runtime não detectado${NC}"
    echo "Para usar GPU, instale nvidia-docker2:"
    echo "  sudo apt-get install nvidia-docker2"
    echo "  sudo systemctl restart docker"
    echo ""
    read -p "Continuar sem GPU? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    GPU_FLAG=""
else
    echo -e "${GREEN}✅ NVIDIA Docker runtime detectado${NC}"
    GPU_FLAG="--gpus all"
fi

# Configurações
IMAGE_NAME="qdrant-hybrid-search"
CONTAINER_NAME="qdrant-hybrid-search"
QDRANT_CONTAINER="qdrant-server"

# Build da imagem
echo ""
echo "📦 Building Docker image..."
docker build -f Dockerfile.gpu -t ${IMAGE_NAME}:latest . || {
    echo -e "${RED}❌ Falha no build da imagem${NC}"
    exit 1
}

echo -e "${GREEN}✅ Imagem construída com sucesso${NC}"

# Parar containers antigos
echo ""
echo "🧹 Limpando containers antigos..."
docker stop ${CONTAINER_NAME} 2>/dev/null
docker rm ${CONTAINER_NAME} 2>/dev/null
docker stop ${QDRANT_CONTAINER} 2>/dev/null
docker rm ${QDRANT_CONTAINER} 2>/dev/null

# Criar network se não existir
echo "🌐 Configurando network..."
docker network create qdrant-network 2>/dev/null || true

# Iniciar Qdrant
echo ""
echo "🗄️  Iniciando Qdrant server..."
docker run -d \
    --name ${QDRANT_CONTAINER} \
    --network qdrant-network \
    -p 6333:6333 \
    -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    -e QDRANT__LOG_LEVEL=INFO \
    --restart unless-stopped \
    qdrant/qdrant:latest || {
        echo -e "${RED}❌ Falha ao iniciar Qdrant${NC}"
        exit 1
    }

echo -e "${GREEN}✅ Qdrant iniciado${NC}"

# Aguardar Qdrant ficar pronto
echo "⏳ Aguardando Qdrant ficar pronto..."
sleep 5

# Iniciar aplicação com GPU
echo ""
echo "🚀 Iniciando aplicação com GPU support..."
echo "Comando: docker run ${GPU_FLAG} ..."

docker run -d \
    --name ${CONTAINER_NAME} \
    --network qdrant-network \
    ${GPU_FLAG} \
    -p 8000:8000 \
    -v $(pwd)/models:/app/models \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/logs:/app/logs \
    -e QDRANT_HOST=${QDRANT_CONTAINER} \
    -e QDRANT_PORT=6333 \
    -e USE_GPU=true \
    -e CUDA_VISIBLE_DEVICES=0 \
    -e BATCH_SIZE=32 \
    -e MAX_SEQUENCE_LENGTH=512 \
    -e CORS_ENABLED=true \
    -e LOG_LEVEL=INFO \
    --restart unless-stopped \
    ${IMAGE_NAME}:latest || {
        echo -e "${RED}❌ Falha ao iniciar aplicação${NC}"
        echo "Verifique os logs com: docker logs ${CONTAINER_NAME}"
        exit 1
    }

echo -e "${GREEN}✅ Aplicação iniciada${NC}"

# Mostrar logs iniciais
echo ""
echo "📋 Logs iniciais:"
echo "================================================"
sleep 3
docker logs ${CONTAINER_NAME} 2>&1 | head -20

# Informações de acesso
echo ""
echo "================================================"
echo -e "${GREEN}✅ Deploy concluído com sucesso!${NC}"
echo "================================================"
echo ""
echo "📍 URLs de acesso:"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Health: http://localhost:8000/health"
echo "  - API Root: http://localhost:8000/"
echo ""
echo "🔧 Comandos úteis:"
echo "  - Ver logs: docker logs -f ${CONTAINER_NAME}"
echo "  - Parar: docker stop ${CONTAINER_NAME} ${QDRANT_CONTAINER}"
echo "  - Reiniciar: docker restart ${CONTAINER_NAME}"
echo "  - Status GPU: docker exec ${CONTAINER_NAME} nvidia-smi"
echo ""

# Verificar saúde
echo "🏥 Verificando saúde da aplicação..."
sleep 10

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Aplicação respondendo corretamente${NC}"
    echo ""
    echo "Resposta do health check:"
    curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8000/health
else
    echo -e "${YELLOW}⚠️  Aplicação ainda está iniciando...${NC}"
    echo "Aguarde alguns minutos para o download dos modelos"
    echo "Monitore com: docker logs -f ${CONTAINER_NAME}"
fi

echo ""
echo "================================================"