# 🔧 Correções para Deploy com GPU no Easypanel

## ❌ Problemas Identificados nos Logs

1. **GPU não detectada**: "WARNING: The NVIDIA Driver was not detected"
2. **Módulo structlog faltando**: "ModuleNotFoundError: No module named 'structlog'"
3. **Erro de sintaxe no script**: Problema com f-strings
4. **Incompatibilidade huggingface_hub**: "cannot import name 'cached_download'"
5. **Qdrant precisa imagem específica para GPU**

## ✅ Soluções Implementadas

### 1. Arquivos Corrigidos Criados:
- **`Dockerfile.fixed`** - Dockerfile corrigido com todas as dependências
- **`easypanel-gpu-fixed.yml`** - Docker Compose com Qdrant GPU

### 2. Principais Correções:

#### Qdrant com GPU:
```yaml
# Usar imagem específica para GPU NVIDIA
image: qdrant/qdrant:v1.13.0-gpu-nvidia

# Ativar GPU no Qdrant
QDRANT__GPU__INDEXING: "1"
```

#### Dependências Python Corrigidas:
- Adicionado `structlog==23.2.0`
- Versão compatível do `huggingface-hub==0.19.4`
- Python 3.11 instalado corretamente

#### Script de Inicialização Corrigido:
- Removido erro de sintaxe nas f-strings
- Melhor tratamento de erros
- Verificação de GPU aprimorada

## 🚀 Como Fazer Deploy no Easypanel

### Pré-requisitos no Servidor Easypanel:
```bash
# Verificar se NVIDIA Docker runtime está instalado
docker run --rm --gpus all nvidia/cuda:12.1.0-base nvidia-smi

# Se não funcionar, instalar:
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

### Deploy no Easypanel:

1. **Upload dos Arquivos:**
   - `Dockerfile.fixed`
   - `easypanel-gpu-fixed.yml`
   - `requirements.txt`
   - Pasta `app/`

2. **No Easypanel:**
   - Criar novo projeto
   - Escolher "Docker Compose"
   - Usar conteúdo de `easypanel-gpu-fixed.yml`
   - Deploy

3. **Configurar Runtime GPU no Easypanel:**
   ```json
   {
     "default-runtime": "nvidia",
     "runtimes": {
       "nvidia": {
         "path": "nvidia-container-runtime",
         "runtimeArgs": []
       }
     }
   }
   ```

## 🔍 Verificação Pós-Deploy

### 1. Verificar GPU no Container:
```bash
# Verificar GPU no Qdrant
docker exec qdrant nvidia-smi

# Verificar GPU na API
docker exec app nvidia-smi

# Verificar CUDA
docker exec app python3.11 -c "import torch; print(torch.cuda.is_available())"
```

### 2. Verificar Logs:
```bash
# Logs do Qdrant
docker logs qdrant

# Logs da API
docker logs app
```

### 3. Testar API:
```bash
# Health check
curl http://localhost:8000/health

# Info do sistema
curl -H "X-API-Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4" \
     http://localhost:8000/api/system/info
```

## ⚠️ Troubleshooting Adicional

### Se GPU ainda não funcionar:

1. **Verificar driver NVIDIA no host:**
   ```bash
   nvidia-smi
   # Deve mostrar driver >= 525.60.13 para CUDA 12.1
   ```

2. **Verificar Docker runtime:**
   ```bash
   docker info | grep -i runtime
   # Deve mostrar: nvidia
   ```

3. **Testar GPU com container simples:**
   ```bash
   docker run --rm --gpus all nvidia/cuda:12.1.0-base nvidia-smi
   ```

### Se Qdrant não iniciar:

1. **Usar versão sem GPU temporariamente:**
   ```yaml
   image: qdrant/qdrant:latest
   # Remover QDRANT__GPU__* variables
   ```

2. **Verificar memória disponível:**
   ```bash
   free -h
   # Precisa de pelo menos 4GB livres
   ```

## 📝 Variáveis de Ambiente Importantes

```bash
# Para Easypanel com GPU
NVIDIA_VISIBLE_DEVICES=all
NVIDIA_DRIVER_CAPABILITIES=compute,utility
CUDA_VISIBLE_DEVICES=0
```

## 🎯 Checklist Final

- [ ] NVIDIA Docker runtime instalado
- [ ] GPU detectada com `nvidia-smi`
- [ ] Arquivo `Dockerfile.fixed` presente
- [ ] Arquivo `easypanel-gpu-fixed.yml` presente
- [ ] Volumes criados para persistência
- [ ] API Key configurada: `Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4`

## 💡 Dica Importante

Se o Easypanel não suportar runtime GPU, use esta alternativa no docker-compose:

```yaml
# Em vez de runtime: nvidia
devices:
  - /dev/nvidia0:/dev/nvidia0
  - /dev/nvidiactl:/dev/nvidiactl
  - /dev/nvidia-uvm:/dev/nvidia-uvm
```

---

**Use `easypanel-gpu-fixed.yml` com `Dockerfile.fixed` para deploy corrigido!**