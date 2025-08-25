# Deploy no Easypanel - Guia Completo

## Problema Identificado
Você está tentando acessar `http://104.238.222.79:6333/dashboard` mas isso está errado porque:
- **Porta 6333**: É o Qdrant (banco de dados vetorial interno)
- **Porta 8000**: É sua aplicação (API de busca híbrida) - ESSA É A QUE VOCÊ DEVE ACESSAR!

## URLs Corretos para Acessar

### Após o deploy no Easypanel:
- **API Docs**: `http://104.238.222.79:8000/docs` ✅ (Interface Swagger)
- **API Root**: `http://104.238.222.79:8000/` ✅ (Informações da API)
- **Health Check**: `http://104.238.222.79:8000/health` ✅ (Status do sistema)

### O Qdrant NÃO tem dashboard público!
O Qdrant é apenas o banco de dados interno. Você acessa ele através da sua API na porta 8000.

## Como Fazer o Deploy no Easypanel

### Método 1: Deploy com Docker Compose (RECOMENDADO)

1. **No Easypanel, crie um novo App**
2. **Escolha "Docker Compose"**
3. **Cole este docker-compose.yml**:

```yaml
version: '3.8'

services:
  # Servidor Qdrant (banco de dados vetorial)
  qdrant:
    image: qdrant/qdrant:latest
    restart: unless-stopped
    volumes:
      - qdrant-storage:/qdrant/storage
    environment:
      QDRANT__SERVICE__HTTP_PORT: "6333"
      QDRANT__SERVICE__GRPC_PORT: "6334"
      QDRANT__LOG_LEVEL: "INFO"
    networks:
      - internal

  # Sua aplicação de busca híbrida
  app:
    image: ghcr.io/your-username/qdrant-hybrid-search:latest
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - models-cache:/app/models
      - app-data:/app/data
    environment:
      API_HOST: "0.0.0.0"
      API_PORT: "8000"
      QDRANT_HOST: "qdrant"
      QDRANT_PORT: "6333"
      QDRANT_COLLECTION: "hybrid_search"
      DENSE_MODEL: "intfloat/multilingual-e5-large"
      SPARSE_MODEL: "prithivida/Splade_PP_en_v1"
      USE_GPU: "false"
      BATCH_SIZE: "16"
      MAX_SEQUENCE_LENGTH: "512"
      NUM_WORKERS: "2"
      CACHE_EMBEDDINGS: "true"
      EMBEDDING_CACHE_SIZE: "5000"
      N8N_WEBHOOK_ENABLED: "true"
      LOG_LEVEL: "INFO"
      CORS_ENABLED: "true"
      CORS_ORIGINS: '["*"]'
    depends_on:
      - qdrant
    networks:
      - internal

volumes:
  qdrant-storage:
  models-cache:
  app-data:

networks:
  internal:
    driver: bridge
```

4. **Configure o domínio/porta**:
   - Domain: Deixe vazio ou configure seu domínio customizado
   - Port: `8000`
   - Mount Path: `/`

5. **Deploy!**

### Método 2: Deploy Separado (2 Apps)

#### App 1: Qdrant
1. Crie um app chamado "qdrant"
2. Use a imagem: `qdrant/qdrant:latest`
3. NÃO exponha porta externa (só interna)
4. Configure volume: `/qdrant/storage`

#### App 2: Sua Aplicação
1. Crie um app chamado "hybrid-search"
2. Use sua imagem Docker
3. Exponha porta: `8000`
4. Configure as variáveis de ambiente:
   ```
   QDRANT_HOST=qdrant.internal
   QDRANT_PORT=6333
   ```

## Testando o Deploy

### 1. Verificar se está funcionando:
```bash
curl http://104.238.222.79:8000/health
```

Resposta esperada:
```json
{
  "status": "healthy",
  "qdrant_connected": true,
  "gpu_available": false,
  "models_loaded": true,
  "version": "1.0.0"
}
```

### 2. Acessar a documentação interativa:
Abra no navegador: `http://104.238.222.79:8000/docs`

### 3. Fazer uma busca de teste:
```bash
curl -X POST "http://104.238.222.79:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "exemplo de busca",
    "mode": "hybrid",
    "limit": 5
  }'
```

## Troubleshooting

### Erro: "Connection refused" no log
- **Causa**: O Qdrant não está rodando ou não está acessível
- **Solução**: Certifique-se de que ambos os containers estão rodando

### Erro: "GPU não disponível"
- **Causa**: Normal em servidores sem GPU
- **Solução**: A aplicação funciona perfeitamente com CPU

### Aplicação demora para iniciar
- **Causa**: Download dos modelos (pode levar 5-10 minutos na primeira vez)
- **Solução**: Aguarde e monitore os logs

## Monitoramento

### Ver logs no Easypanel:
1. Vá para seu app
2. Clique em "Logs"
3. Procure por:
   - "Application startup complete" ✅
   - "Models loaded successfully" ✅
   - "Qdrant connected" ✅

### Logs importantes:
```
🚀 Iniciando Qdrant Hybrid Search...
✅ Models loaded successfully
✅ Qdrant connected
INFO: Application startup complete
INFO: Uvicorn running on http://0.0.0.0:8000
```

## URLs Finais

Após o deploy bem-sucedido, acesse:

| Endpoint | URL | Descrição |
|----------|-----|-----------|
| API Docs | http://104.238.222.79:8000/docs | Interface Swagger |
| API Root | http://104.238.222.79:8000/ | Informações da API |
| Health | http://104.238.222.79:8000/health | Status do sistema |
| Search | http://104.238.222.79:8000/search | Endpoint de busca |
| Collections | http://104.238.222.79:8000/collections | Listar coleções |

## ⚠️ IMPORTANTE
- **NÃO tente acessar a porta 6333** - É interna!
- **USE sempre a porta 8000** - Sua aplicação!
- O Qdrant não tem interface web pública
- Toda interação é feita através da sua API na porta 8000