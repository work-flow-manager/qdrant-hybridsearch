# 🚀 Deploy no Easypanel - Instruções Completas

## ⚠️ IMPORTANTE: Formato Correto para Easypanel

O Easypanel requer um formato específico. **NÃO use o arquivo `easypanel.json` original**, ele está em formato incompatível.

## 📋 Opção 1: Deploy via Docker Compose (RECOMENDADO)

### Passo 1: Criar Novo Projeto
1. No Easypanel, clique em **"New Project"**
2. Escolha **"Docker Compose"**
3. Cole o conteúdo do arquivo `easypanel-docker-compose.yml`

### Passo 2: Configurar Variáveis
Antes de fazer deploy, ajuste estas variáveis no editor:
- `API_KEY`: Mude de "change-me-before-deploy" para uma chave segura
- `USE_GPU`: Mude para "true" se tiver GPU NVIDIA

### Passo 3: Deploy
1. Clique em **"Deploy"**
2. Aguarde os containers iniciarem
3. Configure os domínios para acesso externo

## 📋 Opção 2: Deploy Manual Service por Service

### Serviço 1: Qdrant Database
```yaml
Nome: qdrant
Imagem: qdrant/qdrant:latest
Portas: 6333, 6334
Volumes: /qdrant/storage
Environment:
  QDRANT__SERVICE__HTTP_PORT: 6333
  QDRANT__SERVICE__GRPC_PORT: 6334
  QDRANT__LOG_LEVEL: INFO
```

### Serviço 2: Hybrid Search API
```yaml
Nome: app
Imagem: ghcr.io/work-flow-manager/qdrant-hybridsearch:latest
Porta: 8000
Volumes: 
  - /app/models
  - /app/data
Environment:
  API_HOST: 0.0.0.0
  API_PORT: 8000
  API_KEY: [SUA-CHAVE-SEGURA]
  QDRANT_HOST: qdrant
  QDRANT_PORT: 6333
  QDRANT_COLLECTION: hybrid_search
  DENSE_MODEL: intfloat/multilingual-e5-large
  SPARSE_MODEL: prithivida/Splade_PP_en_v1
  USE_GPU: false
  BATCH_SIZE: 32
  N8N_WEBHOOK_ENABLED: true
```

## 🔧 Configuração de Domínio

1. No serviço `app`, vá em **Domains**
2. Adicione seu domínio customizado ou use o subdomínio do Easypanel
3. Configure SSL (automático com Let's Encrypt)

## 🧪 Testar Instalação

```bash
# Testar Health Check
curl https://seu-dominio.easypanel.host/health

# Testar API (com sua API key)
curl -H "X-API-Key: sua-api-key" https://seu-dominio.easypanel.host/api/collections
```

## ⚡ Performance com GPU

Se você tem GPU NVIDIA no servidor Easypanel:

1. Edite o serviço `app`
2. Mude `USE_GPU` para `true`
3. Adicione em **Advanced Settings**:
   ```yaml
   deploy:
     resources:
       reservations:
         devices:
           - driver: nvidia
             count: 1
             capabilities: [gpu]
   ```

## 🐛 Troubleshooting

### Erro "Minified React error #31"
- **Causa**: Formato JSON incorreto
- **Solução**: Use o arquivo `easypanel-docker-compose.yml` ao invés do `easypanel.json`

### API não responde
- Verifique se ambos os serviços estão rodando
- Confirme que `QDRANT_HOST` está configurado como `qdrant`
- Verifique os logs do container

### Modelos demoram para carregar
- Normal no primeiro deploy (download de ~2GB)
- Modelos são cacheados após primeiro download
- Use volumes persistentes para manter cache

## 📊 Monitoramento

No Easypanel, você pode:
- Ver logs em tempo real
- Monitorar uso de recursos
- Configurar alertas
- Fazer backup dos volumes

## 🔄 Atualização

Para atualizar para nova versão:
1. No serviço `app`, clique em **Redeploy**
2. Easypanel baixará a imagem mais recente
3. Zero downtime com rolling update

## 💡 Dicas

1. **API Key**: Sempre configure uma API key forte
2. **Volumes**: Use volumes nomeados para persistência
3. **Backup**: Configure backup automático dos volumes
4. **Monitoring**: Ative health checks para auto-restart
5. **Scaling**: Use replicas para alta disponibilidade

## 🆘 Suporte

- Documentação: [GitHub Repository](https://github.com/work-flow-manager/qdrant-hybridsearch)
- Issues: Abra uma issue no GitHub
- Easypanel Docs: [easypanel.io/docs](https://easypanel.io/docs)