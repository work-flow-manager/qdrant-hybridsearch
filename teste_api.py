#!/usr/bin/env python3
"""
Script de teste para a API Qdrant Hybrid Search
"""

import requests
import json
from datetime import datetime

# Configuração
API_URL = "http://104.238.222.79:8000"  # Mude para seu domínio se configurou
API_KEY = "Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4"

# Headers padrão
headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def test_health():
    """Testa se a API está rodando"""
    print("🔍 Testando health check...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def insert_sample_data():
    """Insere dados de exemplo"""
    print("📝 Inserindo dados de exemplo...")
    
    documents = {
        "documents": [
            {
                "id": "python_intro",
                "text": "Python é uma linguagem de programação de alto nível, interpretada e de propósito geral. Foi criada por Guido van Rossum em 1991.",
                "metadata": {
                    "category": "programação",
                    "language": "pt-BR",
                    "topic": "python",
                    "year": 2024
                }
            },
            {
                "id": "ai_revolution",
                "text": "A Inteligência Artificial está transformando diversos setores, desde saúde até finanças, com aplicações de machine learning e deep learning.",
                "metadata": {
                    "category": "tecnologia",
                    "language": "pt-BR",
                    "topic": "IA",
                    "year": 2024
                }
            },
            {
                "id": "qdrant_intro",
                "text": "Qdrant é um banco de dados vetorial de alta performance, otimizado para busca por similaridade e aplicações de IA.",
                "metadata": {
                    "category": "banco de dados",
                    "language": "pt-BR",
                    "topic": "vector_db",
                    "year": 2024
                }
            },
            {
                "id": "ml_basics",
                "text": "Machine Learning é um ramo da inteligência artificial que permite que sistemas aprendam e melhorem com a experiência sem serem explicitamente programados.",
                "metadata": {
                    "category": "tecnologia",
                    "language": "pt-BR",
                    "topic": "machine_learning",
                    "year": 2024
                }
            },
            {
                "id": "nlp_overview",
                "text": "Processamento de Linguagem Natural (NLP) permite que computadores entendam, interpretem e gerem linguagem humana de forma útil.",
                "metadata": {
                    "category": "tecnologia",
                    "language": "pt-BR",
                    "topic": "NLP",
                    "year": 2024
                }
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/index",
            headers=headers,
            json=documents
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Documentos inseridos com sucesso!\n")
        else:
            print(f"❌ Erro: {response.text}\n")
    except Exception as e:
        print(f"❌ Erro ao inserir: {e}\n")

def search_documents(query, limit=3):
    """Busca documentos"""
    print(f"🔍 Buscando: '{query}'...")
    
    search_data = {
        "query": query,
        "limit": limit,
        "alpha": 0.5  # Balanço entre busca densa e esparsa
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/search",
            headers=headers,
            json=search_data
        )
        
        if response.status_code == 200:
            results = response.json()
            print(f"Encontrados {len(results.get('results', []))} resultados:\n")
            
            for i, result in enumerate(results.get('results', []), 1):
                print(f"  {i}. Score: {result.get('score', 0):.4f}")
                print(f"     ID: {result.get('id')}")
                print(f"     Texto: {result.get('text', '')[:100]}...")
                print(f"     Metadata: {result.get('metadata', {})}\n")
        else:
            print(f"❌ Erro na busca: {response.text}\n")
    except Exception as e:
        print(f"❌ Erro ao buscar: {e}\n")

def list_collections():
    """Lista coleções disponíveis"""
    print("📋 Listando coleções...")
    
    try:
        response = requests.get(
            f"{API_URL}/api/collections",
            headers=headers
        )
        
        if response.status_code == 200:
            collections = response.json()
            print(f"Coleções: {collections}\n")
        else:
            print(f"❌ Erro: {response.text}\n")
    except Exception as e:
        print(f"❌ Erro ao listar: {e}\n")

def main():
    """Função principal"""
    print("="*50)
    print("🚀 TESTE DA API QDRANT HYBRID SEARCH")
    print("="*50)
    print(f"API URL: {API_URL}")
    print(f"Timestamp: {datetime.now()}\n")
    
    # 1. Testar health
    if not test_health():
        print("❌ API não está respondendo!")
        return
    
    # 2. Listar coleções
    list_collections()
    
    # 3. Inserir dados
    insert_sample_data()
    
    # 4. Fazer buscas
    queries = [
        "o que é python?",
        "inteligência artificial e machine learning",
        "banco de dados vetorial",
        "processamento de linguagem"
    ]
    
    for query in queries:
        search_documents(query)
        print("-"*40)
    
    print("\n✅ Teste concluído!")
    print(f"\n👉 Acesse o dashboard em: {API_URL}/docs")
    print(f"👉 Dashboard Qdrant: http://104.238.222.79:6333/dashboard")

if __name__ == "__main__":
    main()