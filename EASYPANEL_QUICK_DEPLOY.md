# 🚀 DEPLOY RÁPIDO NO EASYPANEL

## ✅ Imagem Docker Pronta para Usar:

```
ghcr.io/work-flow-manager/qdrant-hybridsearch:latest
```

> **Nota:** A imagem está sendo construída automaticamente no GitHub Actions. Aguarde ~10 minutos após o push para estar disponível.

## 📋 Copie e Cole no Easypanel:

### Opção 1: Docker Compose (RECOMENDADO)

No Easypanel, crie um novo serviço e use:
- **Tipo:** Docker Compose
- **Nome:** qdrant-hybrid-search
- **Compose File:** Use o conteúdo de `docker-compose.production.yml`

### Opção 2: Configuração Manual

1. **Serviço 1 - Qdrant:**
   - Image: `qdrant/qdrant:latest`
   - Port: 6333
   - Volume: `/qdrant/storage`

2. **Serviço 2 - API:**
   - Image: `ghcr.io/work-flow-manager/qdrant-hybridsearch:latest`
   - Port: 8000
   - Volumes:
     - `/app/models` (cache dos modelos)
     - `/app/data` (dados)
   - Environment:
     ```env
     API_KEY=sua-chave-segura-aqui
     QDRANT_HOST=qdrant
     USE_GPU=false
     ```

## 🔑 Variáveis IMPORTANTES:

```env
# MUDE ESTAS ANTES DO DEPLOY!
API_KEY=gere-uma-chave-segura-aqui
USE_GPU=false  # true se tiver GPU NVIDIA
```

## 📝 Comando Rápido para Testar:

Depois do deploy, teste com:

```bash
# Verificar saúde
curl http://seu-dominio:8000/health

# Ver documentação
http://seu-dominio:8000/docs
```

## ⚡ Deploy em 1 Minuto:

1. **No Easypanel:**
   - New App → Docker Compose
   - Cole o `docker-compose.production.yml`
   - Mude `API_KEY`
   - Deploy!

2. **Pronto!** Acesse:
   - API: `http://seu-app.easypanel.host:8000`
   - Docs: `http://seu-app.easypanel.host:8000/docs`

## 🆘 Problemas?

### Imagem não encontrada:
- Aguarde 10 min para o GitHub Actions construir
- Verifique: https://github.com/work-flow-manager/qdrant-hybridsearch/actions

### Out of Memory:
- Reduza `BATCH_SIZE=16`
- Configure `USE_GPU=false`

### Modelos demoram para carregar:
- Normal na primeira vez (download ~2GB)
- Aguarde ~5-10 minutos

---
**Imagem Docker:** `ghcr.io/work-flow-manager/qdrant-hybridsearch:latest`