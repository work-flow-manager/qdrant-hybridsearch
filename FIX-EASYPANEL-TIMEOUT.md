# 🔧 SOLUÇÃO PARA O ERRO DE TIMEOUT NO EASYPANEL

## ❌ Problema Identificado
```
ERROR: failed to do request: Head "https://registry-1.docker.io/v2/nvidia/cuda/manifests/12.1.0-cudnn8-runtime-ubuntu22.04": 
net/http: TLS handshake timeout
```

O Easypanel está com timeout ao baixar a imagem base da NVIDIA (2.24GB).

## ✅ SOLUÇÕES DISPONÍVEIS

### Solução 1: Use o Dockerfile.production (RECOMENDADO)
Este Dockerfile usa imagem Python slim que é menor e mais rápida:

```bash
# No Easypanel, configure:
Dockerfile: Dockerfile.production
```

**Vantagens:**
- Imagem base menor (150MB vs 2.24GB)
- Build mais rápido
- Funciona com CPU e GPU (se disponível)
- Sem dependência do registry NVIDIA

### Solução 2: Use o Dockerfile.easypanel
Versão alternativa com Ubuntu base:

```bash
# No Easypanel, configure:
Dockerfile: Dockerfile.easypanel
```

### Solução 3: Use Imagem Pré-construída do Docker Hub

1. **Build local e push para Docker Hub:**
```bash
# Build local
docker build -f Dockerfile.production -t qdrant-hybrid-search:latest .

# Tag para seu Docker Hub
docker tag qdrant-hybrid-search:latest SEU_USUARIO/qdrant-hybrid-search:latest

# Login no Docker Hub
docker login

# Push
docker push SEU_USUARIO/qdrant-hybrid-search:latest
```

2. **No Easypanel, use a imagem pronta:**
```yaml
image: SEU_USUARIO/qdrant-hybrid-search:latest
```

## 📝 CONFIGURAÇÃO COMPLETA NO EASYPANEL

### 1. Crie dois serviços no Easypanel:

#### Serviço 1: Qdrant
```yaml
Name: qdrant
Image: qdrant/qdrant:latest
Port: 6333 (interno, não expor)
Volume: /qdrant/storage
```

#### Serviço 2: Sua Aplicação
```yaml
Name: app
Build:
  Context: seu-repositorio
  Dockerfile: Dockerfile.production
Port: 8000 (expor externamente)
Environment:
  QDRANT_HOST: qdrant
  QDRANT_PORT: 6333
  USE_GPU: false
  BATCH_SIZE: 16
  CORS_ENABLED: true
```

### 2. OU use Docker Compose no Easypanel:

```yaml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      - QDRANT__LOG_LEVEL=INFO

  app:
    build:
      context: .
      dockerfile: Dockerfile.production
    ports:
      - "8000:8000"
    environment:
      - QDRANT_HOST=qdrant
      - QDRANT_PORT=6333
      - USE_GPU=false
    depends_on:
      - qdrant

volumes:
  qdrant_data:
```

## 🚀 DOCKERFILE RECOMENDADO

Use **`Dockerfile.production`** que:
- ✅ Não depende do registry NVIDIA
- ✅ Imagem base pequena (150MB)
- ✅ Build rápido
- ✅ Funciona com CPU
- ✅ Suporta GPU se disponível (use --gpus all)

## 📋 CHECKLIST PARA DEPLOY

1. [ ] Trocar `Dockerfile.gpu` por `Dockerfile.production`
2. [ ] Configurar variável `QDRANT_HOST=qdrant`
3. [ ] Expor porta 8000 (não 6333!)
4. [ ] Aguardar ~5min para download dos modelos
5. [ ] Acessar http://SEU_IP:8000/docs

## 🔍 TESTAR APÓS DEPLOY

```bash
# Health check
curl http://SEU_IP:8000/health

# Resposta esperada:
{
  "status": "healthy",
  "qdrant_connected": true,
  "gpu_available": false,
  "models_loaded": true
}
```

## 💡 DICAS IMPORTANTES

1. **Timeout no Easypanel:** Aumente o timeout de build nas configurações
2. **Memória:** Aloque pelo menos 4GB RAM
3. **Storage:** Reserve 10GB para modelos
4. **Network:** Use network bridge interno entre containers

## 🆘 SE AINDA TIVER PROBLEMAS

### Opção A: Build Local + Registry
```bash
# Build local onde tem boa conexão
docker build -f Dockerfile.production -t myapp:latest .
docker save myapp:latest | gzip > myapp.tar.gz

# Upload para servidor
scp myapp.tar.gz user@easypanel-server:/tmp/

# No servidor
docker load < /tmp/myapp.tar.gz
```

### Opção B: Use GitHub Actions
Configure CI/CD para build automático e push para registry.

---

## ✅ RESUMO: USE O `Dockerfile.production`

Ele resolve o problema de timeout e funciona perfeitamente no Easypanel!