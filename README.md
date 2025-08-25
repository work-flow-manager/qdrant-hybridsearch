# Qdrant Hybrid Search with GPU Acceleration

Sistema de busca híbrida otimizado para GPU RTX 4000, combinando embeddings densos multilinguais e esparsos para máxima precisão.

## 🚀 Características

- **Busca Híbrida**: Combina embeddings densos (semânticos) e esparsos (léxicos)
- **GPU Otimizado**: Configurado para RTX 4000 com 8GB VRAM
- **Modelos de Alta Qualidade**:
  - Dense: `intfloat/multilingual-e5-large` (suporta 100+ idiomas)
  - Sparse: `prithivida/Splade_PP_en_v1` (otimizado para precisão)
- **API REST**: FastAPI com documentação automática
- **Integração n8n**: Webhooks prontos para automação
- **Docker Ready**: Deploy fácil no Easypanel

## 📋 Requisitos

- Docker com suporte NVIDIA GPU
- NVIDIA Driver >= 525.60.13
- CUDA >= 12.0
- 8GB+ RAM
- 10GB+ espaço em disco

## 🛠️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/qdrant-hybrid-search.git
cd qdrant-hybrid-search
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite .env com suas configurações
```

### 3. Build e execute com Docker Compose

```bash
# Build da imagem
docker-compose build

# Iniciar serviços
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## 🔌 API Endpoints

### Health Check
```bash
GET /health
```

### Indexar Documentos
```bash
POST /index
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "documents": [
    {
      "id": "doc1",
      "text": "Seu texto aqui",
      "metadata": {"category": "example"}
    }
  ]
}
```

### Busca Híbrida
```bash
POST /search
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "query": "sua consulta de busca",
  "mode": "hybrid",  # ou "dense" ou "sparse"
  "limit": 10
}
```

### Listar Coleções
```bash
GET /collections
Authorization: Bearer YOUR_API_KEY
```

## 🔧 Integração com n8n

### Webhook para Busca

1. No n8n, adicione um node "Webhook"
2. Configure o método como POST
3. URL: `http://seu-servidor:8000/webhook`
4. Body:
```json
{
  "action": "search",
  "data": {
    "query": "busca texto",
    "limit": 5
  }
}
```

### Webhook para Indexação

```json
{
  "action": "index",
  "data": {
    "documents": [
      {
        "text": "Documento para indexar",
        "metadata": {}
      }
    ]
  }
}
```

## 🚀 Deploy no Easypanel

### Via Interface Web

1. Acesse o Easypanel em `http://seu-servidor:3000`
2. Crie um novo projeto
3. Escolha "Docker Compose"
4. Cole o conteúdo do `docker-compose.yml`
5. Configure as variáveis de ambiente
6. Deploy!

### Via CLI

```bash
# Na pasta do projeto
easypanel deploy --compose docker-compose.yml
```

## 📊 Performance

Com RTX 4000 (8GB VRAM):
- **Indexação**: ~500 docs/segundo
- **Busca**: <50ms latência média
- **Batch Size Ótimo**: 32 documentos
- **Uso de VRAM**: ~3-4GB com modelos carregados

## 🔍 Modos de Busca

### Hybrid (Padrão)
Combina resultados densos e esparsos usando Reciprocal Rank Fusion (RRF).
Melhor para: Consultas gerais com alta precisão.

### Dense
Usa apenas embeddings semânticos multilinguais.
Melhor para: Busca por significado, cross-lingual.

### Sparse
Usa apenas embeddings léxicos esparsos.
Melhor para: Correspondência exata de termos, nomes próprios.

## 🛡️ Segurança

- API Key obrigatória para endpoints sensíveis
- CORS configurável
- Rate limiting disponível
- Logs estruturados em JSON

## 📝 Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `API_KEY` | Chave de API para autenticação | - |
| `USE_GPU` | Habilitar aceleração GPU | true |
| `BATCH_SIZE` | Tamanho do batch para GPU | 32 |
| `QDRANT_HOST` | Host do Qdrant | qdrant |
| `N8N_WEBHOOK_ENABLED` | Habilitar webhooks | true |

## 🐛 Troubleshooting

### GPU não detectada
```bash
# Verificar NVIDIA drivers
nvidia-smi

# Verificar Docker GPU support
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### Out of Memory (OOM)
- Reduza `BATCH_SIZE` no `.env`
- Aumente `MAX_SEQUENCE_LENGTH` gradualmente

### Modelos não carregando
```bash
# Limpar cache e re-download
docker-compose down
rm -rf models/*
docker-compose up --build
```

## 📚 Documentação da API

Após iniciar, acesse:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contribuindo

Pull requests são bem-vindos! Para mudanças maiores, abra uma issue primeiro.

## 📄 Licença

MIT

## 🆘 Suporte

- Issues: GitHub Issues
- Email: seu-email@example.com
- Discord: [Link do Discord]
