# 📋 INSTRUÇÕES DEFINITIVAS PARA EASYPANEL

## ✅ ARQUIVOS CORRETOS A USAR:

### 1. PRINCIPAL (usar estes!):
- **`Dockerfile`** (arquivo principal, sem extensão)
- **`docker-compose.yml`** (arquivo principal, sem prefixo)

### 2. NÃO USAR:
- ❌ Dockerfile.gpu-ready
- ❌ docker-compose-gpu.yml
- ❌ Outros Dockerfiles com sufixo

## 🚀 COMO FAZER DEPLOY NO EASYPANEL:

### Método 1: Copiar e Colar (MAIS SIMPLES)

1. **No Easypanel, crie novo projeto**
2. **Escolha "Docker Compose"**
3. **Cole o conteúdo de `docker-compose.yml`**
4. **Clique em Deploy**

### Método 2: Git Clone

1. **No terminal do Easypanel:**
```bash
git clone https://github.com/work-flow-manager/qdrant-hybridsearch.git
cd qdrant-hybridsearch
```

2. **Use o docker-compose.yml padrão**

## ⚠️ IMPORTANTE:

### Se der erro "Dockerfile.gpu-ready not found":
- O Easypanel está tentando usar o arquivo errado
- Certifique-se de usar `docker-compose.yml` (sem sufixo)
- O Dockerfile correto é `Dockerfile` (sem extensão)

### Se GPU não for detectada:
- Normal no Easypanel sem configuração especial
- A API funcionará perfeitamente com CPU

## 🔑 CONFIGURAÇÕES:

```yaml
API_KEY: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4
Porta API: 8000
Porta Qdrant: 6333
```

## 📂 ESTRUTURA CORRETA:

```
qdrant-hybridsearch/
├── Dockerfile          ← USAR ESTE
├── docker-compose.yml  ← USAR ESTE
├── requirements.txt
└── app/
    └── (arquivos da aplicação)
```

## 🧪 TESTAR APÓS DEPLOY:

```bash
# Health check
curl http://seu-dominio:8000/health

# API docs
http://seu-dominio:8000/docs

# Teste com API key
curl -H "X-API-Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4" \
     http://seu-dominio:8000/api/collections
```

## 💡 DICAS:

1. **Sempre use os arquivos principais** (sem sufixo)
2. **Se der erro de build**, verifique se está usando `Dockerfile` (não `Dockerfile.gpu-ready`)
3. **A API funciona sem GPU** - não se preocupe se não detectar
4. **Qdrant precisa estar rodando** para a API funcionar 100%

## 🆘 SE NADA FUNCIONAR:

### Deploy Manual:
```bash
# Build
docker build -t hybrid-search .

# Run
docker run -d -p 8000:8000 \
  -e API_KEY=Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4 \
  hybrid-search
```

---

**USE OS ARQUIVOS PRINCIPAIS: `Dockerfile` e `docker-compose.yml`**