#!/bin/bash

# Script de teste para verificar o deploy
API_URL="${1:-http://104.238.222.79:8000}"

echo "🔍 Testando deploy em: $API_URL"
echo "================================"

# Teste 1: Health Check
echo -e "\n1️⃣ Health Check..."
curl -s "$API_URL/health" | python3 -m json.tool
if [ $? -eq 0 ]; then
    echo "✅ Health check OK"
else
    echo "❌ Health check falhou"
    exit 1
fi

# Teste 2: API Root
echo -e "\n2️⃣ API Info..."
curl -s "$API_URL/" | python3 -m json.tool
if [ $? -eq 0 ]; then
    echo "✅ API info OK"
else
    echo "❌ API info falhou"
fi

# Teste 3: Listar Coleções
echo -e "\n3️⃣ Listando coleções..."
curl -s "$API_URL/collections" | python3 -m json.tool
if [ $? -eq 0 ]; then
    echo "✅ Listagem OK"
else
    echo "❌ Listagem falhou"
fi

# Teste 4: Criar documento de teste
echo -e "\n4️⃣ Indexando documento de teste..."
curl -s -X POST "$API_URL/index" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "id": "test-1",
        "text": "Este é um documento de teste para verificar a busca híbrida",
        "metadata": {"tipo": "teste", "data": "2025-01-08"}
      }
    ]
  }' | python3 -m json.tool

# Teste 5: Fazer busca
echo -e "\n5️⃣ Fazendo busca de teste..."
curl -s -X POST "$API_URL/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "documento teste",
    "mode": "hybrid",
    "limit": 5
  }' | python3 -m json.tool

echo -e "\n================================"
echo "✅ Testes concluídos!"
echo ""
echo "📝 Próximos passos:"
echo "1. Acesse a documentação em: $API_URL/docs"
echo "2. Use a API para indexar seus documentos"
echo "3. Faça buscas híbridas com dense + sparse vectors"
echo ""
echo "⚠️  LEMBRE-SE: A porta 6333 é INTERNA do Qdrant!"
echo "    Use sempre a porta 8000 para acessar sua API!"