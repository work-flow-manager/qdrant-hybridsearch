#!/bin/bash

# ========================================
# BUILD E PUSH PARA DOCKER HUB
# Para deploy no Easypanel
# ========================================

# Configurações (MUDE AQUI!)
DOCKER_USERNAME="seu_usuario"  # <- MUDE PARA SEU USUÁRIO DO DOCKER HUB
IMAGE_NAME="qdrant-hybrid-gpu"
TAG="latest"

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   🚀 BUILD E PUSH PARA DOCKER HUB                        ║"
echo "╚══════════════════════════════════════════════════════════╝"

# Verificar se usuário foi configurado
if [ "$DOCKER_USERNAME" == "seu_usuario" ]; then
    echo -e "${RED}❌ Configure seu DOCKER_USERNAME no script!${NC}"
    echo "   Edite a linha 9 deste arquivo"
    exit 1
fi

# Login no Docker Hub
echo ""
echo -e "${BLUE}1. Fazendo login no Docker Hub...${NC}"
docker login || {
    echo -e "${RED}❌ Falha no login${NC}"
    exit 1
}

# Build da imagem all-in-one
echo ""
echo -e "${BLUE}2. Building imagem all-in-one (Qdrant + App)...${NC}"
docker build -f Dockerfile.all-in-one -t ${IMAGE_NAME}:${TAG} . || {
    echo -e "${RED}❌ Falha no build${NC}"
    exit 1
}
echo -e "${GREEN}✅ Build concluído${NC}"

# Tag para Docker Hub
echo ""
echo -e "${BLUE}3. Criando tag para Docker Hub...${NC}"
docker tag ${IMAGE_NAME}:${TAG} ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}
echo -e "${GREEN}✅ Tag criada: ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}${NC}"

# Push para Docker Hub
echo ""
echo -e "${BLUE}4. Fazendo push para Docker Hub...${NC}"
echo "   Isso pode demorar alguns minutos..."
docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG} || {
    echo -e "${RED}❌ Falha no push${NC}"
    exit 1
}
echo -e "${GREEN}✅ Push concluído${NC}"

# Build alternativo (apenas app)
echo ""
echo -e "${BLUE}5. Building imagem da app separada...${NC}"
docker build -f Dockerfile.gpu -t ${IMAGE_NAME}-app:${TAG} . || {
    echo -e "${YELLOW}⚠️ Falha no build da app separada${NC}"
}

# Push da app separada
if [ $? -eq 0 ]; then
    docker tag ${IMAGE_NAME}-app:${TAG} ${DOCKER_USERNAME}/${IMAGE_NAME}-app:${TAG}
    docker push ${DOCKER_USERNAME}/${IMAGE_NAME}-app:${TAG}
    echo -e "${GREEN}✅ App separada também disponível${NC}"
fi

# Instruções para Easypanel
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   📋 CONFIGURAÇÃO NO EASYPANEL                           ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "1. NO EASYPANEL, USE:"
echo "   ${GREEN}Image: ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}${NC}"
echo ""
echo "2. CONFIGURE AS PORTAS:"
echo "   - 8000 (API)"
echo "   - 6333 (Qdrant)"
echo ""
echo "3. ADICIONE NO RUN COMMAND:"
echo "   ${YELLOW}--gpus all${NC}"
echo ""
echo "4. ENVIRONMENT VARIABLES (copie do .env.gpu):"
echo "   USE_GPU=true"
echo "   BATCH_SIZE=64"
echo "   CUDA_VISIBLE_DEVICES=0"
echo "   NVIDIA_VISIBLE_DEVICES=all"
echo ""
echo "5. VOLUMES (opcional):"
echo "   /app/models -> para cachear modelos"
echo "   /qdrant/storage -> para persistir dados"
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   🎯 IMAGENS DISPONÍVEIS                                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "ALL-IN-ONE (Qdrant + App):"
echo "  ${GREEN}${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}${NC}"
echo ""
echo "Apenas App (precisa Qdrant separado):"
echo "  ${GREEN}${DOCKER_USERNAME}/${IMAGE_NAME}-app:${TAG}${NC}"
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   ✅ PRONTO PARA DEPLOY NO EASYPANEL!                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "URL da imagem no Docker Hub:"
echo "${BLUE}https://hub.docker.com/r/${DOCKER_USERNAME}/${IMAGE_NAME}${NC}"