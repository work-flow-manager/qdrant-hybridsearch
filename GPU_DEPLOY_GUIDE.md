# 🎮 Deploy com GPU no Easypanel - Guia Completo

## 🔑 API KEY GERADA
```
API_KEY: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4
```
**⚠️ IMPORTANTE: Guarde esta chave com segurança! Você precisará dela para acessar a API.**

## 📁 Arquivos para Deploy GPU

### 1. `Dockerfile.gpu` 
- Baseado em NVIDIA CUDA 12.1
- PyTorch com suporte CUDA
- Otimizado para GPU RTX 4000 ou similar

### 2. `easypanel-gpu.yml`
- Docker Compose com configurações GPU
- API Key já configurada
- Runtime NVIDIA configurado

### 3. `.env.gpu`
- Todas as variáveis de ambiente
- GPU ativada por padrão
- Batch size otimizado (64)

## 🚀 Como Fazer Deploy no Easypanel

### Passo 1: Preparar Arquivos
```bash
# Criar arquivo compactado com tudo necessário
tar -czf gpu-deploy.tar.gz \
    Dockerfile.gpu \
    easypanel-gpu.yml \
    .env.gpu \
    requirements.txt \
    app/
```

### Passo 2: No Easypanel
1. Criar novo projeto
2. Escolher "Docker Compose"
3. Fazer upload dos arquivos ou clonar do GitHub
4. Colar conteúdo de `easypanel-gpu.yml`
5. Clicar em Deploy

### Passo 3: Verificar GPU
Após deploy, verificar se GPU está ativa:
```bash
docker exec app nvidia-smi
```

## ⚙️ Variáveis de Ambiente Principais

| Variável | Valor | Descrição |
|----------|-------|-----------|
| `API_KEY` | `Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4` | Chave de autenticação |
| `USE_GPU` | `true` | GPU ativada |
| `CUDA_DEVICE` | `0` | GPU 0 (primeira) |
| `BATCH_SIZE` | `64` | Tamanho do batch (GPU) |
| `DENSE_MODEL` | `intfloat/multilingual-e5-large` | Modelo denso |
| `SPARSE_MODEL` | `prithivida/Splade_PP_en_v1` | Modelo esparso |

## 🧪 Testar Instalação

### 1. Health Check
```bash
curl http://seu-dominio:8000/health
```

### 2. Verificar GPU
```bash
curl -H "X-API-Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4" \
     http://seu-dominio:8000/api/system/gpu
```

### 3. Testar Busca
```bash
curl -X POST http://seu-dominio:8000/api/search \
     -H "X-API-Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4" \
     -H "Content-Type: application/json" \
     -d '{"query": "teste", "collection": "hybrid_search"}'
```

## 📊 Performance Esperada com GPU

### RTX 4000 (ou similar)
- **Embeddings/seg:** ~1000-2000
- **Batch processing:** 64 documentos
- **Latência de busca:** < 100ms
- **Uso de VRAM:** ~4-6GB

### Comparação CPU vs GPU
| Operação | CPU | GPU | Speedup |
|----------|-----|-----|---------|
| Embedding (1000 docs) | ~60s | ~5s | 12x |
| Busca híbrida | ~500ms | ~50ms | 10x |
| Batch processing | 32 | 64 | 2x |

## 🐛 Troubleshooting GPU

### GPU não detectada
```bash
# Verificar NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:12.1.0-base nvidia-smi
```

### Out of Memory (OOM)
Reduza o batch size:
```yaml
BATCH_SIZE: "32"  # ou até 16 se necessário
```

### CUDA version mismatch
Verifique sua versão CUDA:
```bash
nvidia-smi
# Use a imagem Docker correspondente
```

## 🔧 Configurações Avançadas

### Multi-GPU (se disponível)
```yaml
CUDA_VISIBLE_DEVICES: "0,1"  # Usar 2 GPUs
```

### Precision reduzida (mais rápido)
```yaml
MIXED_PRECISION: "true"
TORCH_DTYPE: "float16"
```

### Cache maior (mais RAM)
```yaml
EMBEDDING_CACHE_SIZE: "50000"
```

## 📝 Comandos Docker Úteis

```bash
# Ver logs
docker logs app -f

# Estatísticas GPU
docker exec app nvidia-smi

# Python interativo com GPU
docker exec -it app python3
>>> import torch
>>> torch.cuda.is_available()
>>> torch.cuda.get_device_name(0)

# Monitorar uso GPU em tempo real
watch -n 1 docker exec app nvidia-smi
```

## ⚡ Otimizações Recomendadas

1. **Persistent Volumes**: Sempre use volumes para `/app/models`
2. **Health Checks**: Configurados para auto-restart
3. **Logging**: Use `WARNING` em produção para menos I/O
4. **VRAM**: Monitore uso para evitar OOM
5. **Batch Size**: Ajuste baseado na sua GPU

## 🎯 Checklist de Deploy

- [ ] Arquivo `Dockerfile.gpu` presente
- [ ] Arquivo `easypanel-gpu.yml` presente
- [ ] API Key anotada: `Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4`
- [ ] NVIDIA Docker runtime instalado no servidor
- [ ] GPU disponível e funcionando
- [ ] Pelo menos 8GB RAM
- [ ] Pelo menos 10GB espaço disco

## 🆘 Suporte

Se tiver problemas:
1. Verifique logs: `docker logs app`
2. Confirme GPU: `docker exec app nvidia-smi`
3. Teste API: `curl http://localhost:8000/health`
4. Verifique Qdrant: `docker logs qdrant`

---

**🎮 GPU Ativada e Pronta para Deploy!**

API Key gerada e configurada. Use `easypanel-gpu.yml` para deploy com GPU.