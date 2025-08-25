# 🚀 Deploy no Easypanel

## Opção 1: Usar Imagem Pré-construída do Docker Hub

### 📦 Imagem Docker Recomendada:
```
qdrant/qdrant:latest
```

E para a API:
```
ghcr.io/work-flow-manager/qdrant-hybridsearch:latest
```

## Opção 2: Build a partir do GitHub

### 1. No Easypanel, crie um novo serviço:

**Configurações do Serviço:**
- **Nome**: qdrant-hybrid-search
- **Tipo**: Docker Compose
- **Source**: GitHub
- **Repository**: `https://github.com/work-flow-manager/qdrant-hybridsearch`
- **Branch**: main
- **Docker Compose File**: docker-compose.yml

### 2. Variáveis de Ambiente (Configure no Easypanel):

```env
# API Configuration
API_KEY=sua-chave-segura-aqui
API_HOST=0.0.0.0
API_PORT=8000

# Qdrant Configuration  
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION=hybrid_search

# Model Configuration
DENSE_MODEL=intfloat/multilingual-e5-large
SPARSE_MODEL=prithivida/Splade_PP_en_v1

# GPU Settings (se disponível)
USE_GPU=false  # Mude para true se tiver GPU
CUDA_DEVICE=0
BATCH_SIZE=32

# Performance
NUM_WORKERS=4
CACHE_EMBEDDINGS=true

# n8n Integration
N8N_WEBHOOK_ENABLED=true
```

### 3. Configuração de Portas:

- **8000**: API REST (Hybrid Search)
- **6333**: Qdrant HTTP
- **6334**: Qdrant gRPC

### 4. Volumes Persistentes:

```yaml
/app/models  # Cache dos modelos
/app/data    # Dados do Qdrant
```

## Opção 3: Deploy Manual via Docker Compose

### 1. Clone o repositório:
```bash
git clone https://github.com/work-flow-manager/qdrant-hybridsearch.git
cd qdrant-hybridsearch
```

### 2. Configure o .env:
```bash
cp .env.example .env
nano .env  # Edite suas configurações
```

### 3. Build e execute:
```bash
docker compose build
docker compose up -d
```

## 📊 Recursos Recomendados:

### Mínimo (CPU only):
- **CPU**: 2 cores
- **RAM**: 4GB
- **Disco**: 10GB

### Recomendado (com GPU):
- **CPU**: 4 cores
- **RAM**: 8GB
- **GPU**: NVIDIA com 4GB+ VRAM
- **Disco**: 20GB

## 🔧 Configuração GPU (Opcional):

Se você tem GPU no servidor Easypanel:

1. Instale NVIDIA Docker Runtime:
```bash
# No servidor do Easypanel
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

2. Edite o docker-compose.yml e descomente as linhas de GPU:
```yaml
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    runtime: nvidia
```

## 🌐 URLs de Acesso:

Após o deploy:
- **API**: `http://seu-dominio:8000`
- **API Docs**: `http://seu-dominio:8000/docs`
- **Qdrant Dashboard**: `http://seu-dominio:6333/dashboard`

## 🔐 Segurança:

1. **Sempre mude a API_KEY** padrão
2. Configure **HTTPS** via proxy reverso no Easypanel
3. Limite acesso ao Qdrant (porta 6333) apenas para localhost

## ✅ Verificar Deploy:

```bash
# Teste de saúde
curl http://seu-dominio:8000/health

# Teste de indexação
curl -X POST "http://seu-dominio:8000/index" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SUA_API_KEY" \
  -d '{"documents": [{"text": "Teste de deploy"}]}'
```

## 🐛 Troubleshooting:

### Erro de memória:
- Reduza `BATCH_SIZE` para 16 ou 8
- Desative `USE_GPU=false`

### Modelos não carregam:
- Verifique espaço em disco (precisa ~5GB)
- Aguarde download inicial (~10 min)

### API não responde:
- Check logs: `docker logs hybrid-search-api`
- Verifique se Qdrant está rodando: `docker ps`