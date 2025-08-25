# 🚀 COMO USAR A API - GUIA COMPLETO

## 📍 ENDPOINTS DISPONÍVEIS

### 1️⃣ DASHBOARDS E DOCUMENTAÇÃO

#### 📊 Swagger UI (Interface Visual):
```
http://104.238.222.79:8000/docs
```
ou se configurou domínio:
```
http://seu-dominio.com:8000/docs
```
**👉 ACESSE ESTE LINK NO NAVEGADOR para ver a interface visual!**

#### 📋 ReDoc (Documentação):
```
http://104.238.222.79:8000/redoc
```

#### ✅ Health Check:
```bash
curl http://104.238.222.79:8000/health
```

## 2️⃣ COMO INSERIR DADOS

### 🔑 API Key necessária:
```
Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4
```

### 📝 Exemplo 1: Inserir um documento simples
```bash
curl -X POST http://104.238.222.79:8000/api/index \
  -H "Content-Type: application/json" \
  -H "X-API-Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4" \
  -d '{
    "documents": [
      {
        "id": "doc1",
        "text": "Python é uma linguagem de programação de alto nível",
        "metadata": {"category": "programação", "language": "pt"}
      }
    ]
  }'
```

### 📝 Exemplo 2: Inserir múltiplos documentos
```bash
curl -X POST http://104.238.222.79:8000/api/index \
  -H "Content-Type: application/json" \
  -H "X-API-Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4" \
  -d '{
    "documents": [
      {
        "id": "doc1",
        "text": "Inteligência Artificial está revolucionando o mundo",
        "metadata": {"category": "tecnologia", "year": 2024}
      },
      {
        "id": "doc2",
        "text": "Machine Learning é um subcampo da IA",
        "metadata": {"category": "tecnologia", "topic": "ml"}
      },
      {
        "id": "doc3",
        "text": "Redes neurais são inspiradas no cérebro humano",
        "metadata": {"category": "tecnologia", "topic": "deep_learning"}
      }
    ]
  }'
```

## 3️⃣ COMO BUSCAR DADOS

### 🔍 Busca híbrida (dense + sparse):
```bash
curl -X POST http://104.238.222.79:8000/api/search \
  -H "Content-Type: application/json" \
  -H "X-API-Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4" \
  -d '{
    "query": "o que é inteligência artificial?",
    "limit": 5,
    "alpha": 0.5
  }'
```

### 🔍 Busca com filtros:
```bash
curl -X POST http://104.238.222.79:8000/api/search \
  -H "Content-Type: application/json" \
  -H "X-API-Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4" \
  -d '{
    "query": "machine learning",
    "limit": 10,
    "filters": {
      "category": "tecnologia"
    }
  }'
```

## 4️⃣ OUTROS ENDPOINTS ÚTEIS

### 📋 Listar coleções:
```bash
curl -H "X-API-Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4" \
     http://104.238.222.79:8000/api/collections
```

### 📊 Estatísticas da coleção:
```bash
curl -H "X-API-Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4" \
     http://104.238.222.79:8000/api/collections/hybrid_search/stats
```

### 🗑️ Deletar documento:
```bash
curl -X DELETE http://104.238.222.79:8000/api/documents/doc1 \
  -H "X-API-Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4"
```

## 5️⃣ SCRIPT PYTHON DE EXEMPLO

```python
import requests
import json

# Configuração
API_URL = "http://104.238.222.79:8000"
API_KEY = "Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# 1. Inserir documentos
documents = {
    "documents": [
        {
            "id": f"doc_{i}",
            "text": f"Documento de exemplo número {i}",
            "metadata": {"index": i}
        }
        for i in range(1, 11)
    ]
}

response = requests.post(
    f"{API_URL}/api/index",
    headers=headers,
    json=documents
)
print(f"Inserção: {response.status_code}")

# 2. Buscar
search_query = {
    "query": "documento exemplo",
    "limit": 5
}

response = requests.post(
    f"{API_URL}/api/search",
    headers=headers,
    json=search_query
)
print(f"Resultados: {response.json()}")
```

## 6️⃣ INTERFACE N8N

Se você tem n8n configurado, pode usar webhooks:
```bash
curl -X POST http://104.238.222.79:8000/api/n8n/webhook \
  -H "Content-Type: application/json" \
  -H "X-API-Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4" \
  -d '{
    "action": "index",
    "data": {
      "text": "Texto para indexar via n8n"
    }
  }'
```

## 🎯 DASHBOARD VISUAL

### Acesse no navegador:
👉 **http://104.238.222.79:8000/docs**

Lá você pode:
- ✅ Ver todos os endpoints
- ✅ Testar diretamente na interface
- ✅ Ver exemplos de requisições
- ✅ Inserir a API Key uma vez e testar tudo

### Como usar o Swagger UI:
1. Acesse http://104.238.222.79:8000/docs
2. Clique em "Authorize" 🔐
3. Digite a API Key: `Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4`
4. Clique em qualquer endpoint
5. Clique em "Try it out"
6. Edite os parâmetros
7. Clique em "Execute"

## 🔧 TROUBLESHOOTING

### Se a API não responder:
1. Verifique se está usando a API Key correta
2. Confirme a porta (8000)
3. Verifique se o container está rodando:
   ```bash
   docker ps | grep qdrant
   ```

### Se der erro de conexão com Qdrant:
O Qdrant precisa estar rodando na porta 6333

### Dashboard do Qdrant:
```
http://104.238.222.79:6333/dashboard
```

---

## 📌 RESUMO RÁPIDO:

1. **Dashboard API**: http://104.238.222.79:8000/docs
2. **API Key**: `Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4`
3. **Inserir dados**: POST `/api/index`
4. **Buscar dados**: POST `/api/search`
5. **Dashboard Qdrant**: http://104.238.222.79:6333/dashboard

**👉 ABRA http://104.238.222.79:8000/docs NO SEU NAVEGADOR AGORA!**