# 🚀 GUIA DEFINITIVO - Deploy no Easypanel

## ⚠️ PROBLEMA ATUAL
Você está tentando acessar `http://104.238.222.79:6333/dashboard` mas:
1. **Porta 6333 = Qdrant Database** (NÃO tem dashboard web!)
2. **Porta 8000 = Sua API** (ESTA é que você deve acessar!)

## ✅ SOLUÇÃO COMPLETA

### Opção A: Deploy com Docker Compose (MAIS FÁCIL)

1. **No Easypanel:**
   - Clique em **"+ Create App"**
   - Escolha **"Docker Compose"**
   - Nome: `qdrant-hybrid-search`

2. **Cole este docker-compose.yml:**

```yaml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    restart: unless-stopped
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      - QDRANT__LOG_LEVEL=INFO
    networks:
      - internal

  app:
    image: rreis22/hybrid-search:latest
    restart: unless-stopped
    ports:
      - "3000:8000"
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - QDRANT_HOST=qdrant
      - QDRANT_PORT=6333
      - USE_GPU=false
      - BATCH_SIZE=16
      - CORS_ENABLED=true
    depends_on:
      - qdrant
    networks:
      - internal

volumes:
  qdrant_data:

networks:
  internal:
```

3. **Configure no Easypanel:**
   - **Port Mapping**: `3000` → `8000`
   - **Domain**: Configure se quiser um domínio customizado
   - **Deploy**: Clique em Deploy

### Opção B: Build da Imagem Localmente e Push

1. **Build local:**
```bash
cd /root/home/qdrant-hybrid-search

# Build da imagem
docker build -t qdrant-hybrid-search:latest .

# Tag para seu registry
docker tag qdrant-hybrid-search:latest YOUR_DOCKER_USERNAME/qdrant-hybrid-search:latest

# Push para Docker Hub
docker push YOUR_DOCKER_USERNAME/qdrant-hybrid-search:latest
```

2. **Use a imagem no Easypanel**

### Opção C: Deploy Direto do GitHub

1. **Faça push do código para GitHub:**
```bash
git add .
git commit -m "Deploy ready for Easypanel"
git push origin main
```

2. **No Easypanel:**
   - Create App → GitHub
   - Conecte seu repositório
   - Use o Dockerfile existente

## 📍 URLS CORRETAS APÓS DEPLOY

Após o deploy bem-sucedido, acesse:

| O que você quer | URL Correta | Descrição |
|-----------------|-------------|-----------|
| **Documentação API** | `http://104.238.222.79:8000/docs` | Interface Swagger interativa |
| **Status do Sistema** | `http://104.238.222.79:8000/health` | Verifica se tudo está OK |
| **API Root** | `http://104.238.222.79:8000/` | Informações básicas |
| **Fazer Buscas** | `http://104.238.222.79:8000/search` | Endpoint de busca (POST) |

## 🧪 TESTE RÁPIDO

Execute este comando para testar:

```bash
# Teste de saúde
curl http://104.238.222.79:8000/health

# Se funcionar, você verá:
{
  "status": "healthy",
  "qdrant_connected": true,
  "models_loaded": true
}
```

## 🔍 COMO USAR A API

### 1. Indexar documentos:
```bash
curl -X POST "http://104.238.222.79:8000/index" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [{
      "id": "doc1",
      "text": "Seu texto aqui",
      "metadata": {}
    }]
  }'
```

### 2. Fazer buscas:
```bash
curl -X POST "http://104.238.222.79:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "sua busca",
    "mode": "hybrid",
    "limit": 10
  }'
```

## 🔧 CONFIGURAÇÃO NO EASYPANEL

### Settings Importantes:
```
App Name: qdrant-hybrid-search
Port: 8000 (externa) → 8000 (interna)
Health Check: /health
Restart Policy: unless-stopped
```

### Environment Variables:
```
QDRANT_HOST=localhost (se mesmo container) ou qdrant (se docker-compose)
QDRANT_PORT=6333
USE_GPU=false
CORS_ENABLED=true
```

## 🐛 TROUBLESHOOTING

### "Connection refused" no log:
```bash
# Solução: Garantir que Qdrant está rodando
# No docker-compose, use: depends_on: - qdrant
```

### "GPU não disponível":
```bash
# Normal em servidores sem GPU
# A aplicação funciona perfeitamente com CPU
```

### Aplicação não inicia:
```bash
# Verifique os logs no Easypanel
# Procure por: "Application startup complete"
```

## ✅ CHECKLIST FINAL

- [ ] Deploy feito no Easypanel
- [ ] Porta 8000 exposta (NÃO 6333!)
- [ ] Health check retorna "healthy"
- [ ] Docs acessível em /docs
- [ ] Teste de busca funcionando

## 📞 SUPORTE

Se ainda tiver problemas:
1. Verifique os logs no Easypanel
2. Teste com: `curl http://seu-ip:8000/health`
3. Confirme que AMBOS containers estão rodando (app + qdrant)

---
💡 **LEMBRE-SE**: O Qdrant NÃO tem interface web! Use sua API na porta 8000!