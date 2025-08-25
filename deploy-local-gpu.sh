#!/bin/bash

# Script para Deploy Local com GPU RTX 4000
# Acesso local e via URL externa

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   🚀 DEPLOY LOCAL COM GPU QUADRO RTX 4000                ║"
echo "╚══════════════════════════════════════════════════════════╝"

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Verificar GPU
echo ""
echo "🎮 Verificando GPU..."
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
echo -e "${GREEN}✅ GPU Quadro RTX 4000 detectada!${NC}"

# Parar containers antigos
echo ""
echo "🧹 Limpando containers antigos..."
docker-compose -f docker-compose.gpu.yml down 2>/dev/null
docker stop qdrant-server qdrant-hybrid-search 2>/dev/null
docker rm qdrant-server qdrant-hybrid-search 2>/dev/null

# Build da imagem com GPU
echo ""
echo "🔨 Building imagem com suporte GPU..."
docker build -f Dockerfile.gpu -t qdrant-hybrid-gpu:latest . || {
    echo -e "${RED}❌ Erro no build${NC}"
    exit 1
}
echo -e "${GREEN}✅ Imagem construída com sucesso${NC}"

# Iniciar com Docker Compose
echo ""
echo "🚀 Iniciando serviços com GPU..."
docker-compose -f docker-compose.gpu.yml up -d

# Aguardar serviços iniciarem
echo ""
echo "⏳ Aguardando serviços iniciarem (30 segundos)..."
for i in {30..1}; do
    echo -ne "\r   Aguardando: $i segundos..."
    sleep 1
done
echo ""

# Verificar GPU no container
echo ""
echo "🔍 Verificando GPU no container..."
docker exec qdrant-hybrid-search nvidia-smi --query-gpu=name,utilization.gpu,memory.used --format=csv,noheader || {
    echo -e "${YELLOW}⚠️  GPU não acessível no container${NC}"
}

# Verificar saúde
echo ""
echo "🏥 Verificando saúde da aplicação..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Aplicação respondendo!${NC}"
    echo "$HEALTH_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$HEALTH_RESPONSE"
else
    echo -e "${YELLOW}⚠️  Aplicação ainda iniciando...${NC}"
    echo "   Aguarde mais alguns minutos para download dos modelos"
fi

# Obter IPs
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   📍 URLS DE ACESSO                                       ║"
echo "╚══════════════════════════════════════════════════════════╝"

# IP Local
LOCAL_IP=$(hostname -I | awk '{print $1}')

# IP Externo
EXTERNAL_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null || echo "Não detectado")

echo ""
echo "🏠 ACESSO LOCAL:"
echo "   - http://localhost:8000/docs"
echo "   - http://localhost:8000/health"
echo "   - http://${LOCAL_IP}:8000/docs"
echo ""
echo "🌍 ACESSO EXTERNO (Internet):"
echo "   - http://${EXTERNAL_IP}:8000/docs"
echo "   - http://${EXTERNAL_IP}:8000/health"
echo ""
echo "🔧 COMANDOS ÚTEIS:"
echo "   - Logs: docker-compose -f docker-compose.gpu.yml logs -f"
echo "   - GPU: docker exec qdrant-hybrid-search nvidia-smi"
echo "   - Stop: docker-compose -f docker-compose.gpu.yml down"
echo "   - Restart: docker-compose -f docker-compose.gpu.yml restart"
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   ✅ DEPLOY CONCLUÍDO COM GPU!                           ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   1. Certifique-se que a porta 8000 está aberta no firewall"
echo "   2. Para acesso externo, configure port forwarding no roteador"
echo "   3. Os modelos levam ~5 min para baixar na primeira vez"
echo ""

# Monitorar logs em tempo real (opcional)
read -p "Deseja ver os logs em tempo real? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose -f docker-compose.gpu.yml logs -f
fi