# 🔧 SOLUÇÃO: Forçar GPU no Easypanel

## ❌ Problema:
GPU não está sendo detectada dentro do container no Easypanel, mesmo com NVIDIA Container Toolkit instalado.

## ✅ Solução Criada:

### 1. **Novo Dockerfile**: `Dockerfile.easypanel-gpu`
- FORÇA detecção de GPU
- Instala nvidia-ml-py3 para detecção alternativa
- Configura todas as variáveis NVIDIA
- Script de inicialização com diagnóstico completo

### 2. **Novo Docker Compose**: `easypanel-gpu-force.yml`
- Mapeia dispositivos NVIDIA diretamente
- Adiciona `privileged: true` para acesso ao hardware
- Configura runtime: nvidia
- Força todas as variáveis de GPU

## 🚀 COMO USAR NO EASYPANEL:

### Opção 1: Rebuild com novo Dockerfile
```bash
# No Easypanel, faça rebuild com:
Dockerfile: Dockerfile.easypanel-gpu
Docker Compose: easypanel-gpu-force.yml
```

### Opção 2: Configuração Manual no Easypanel

No seu serviço "app" no Easypanel, adicione estas configurações:

#### Variáveis de Ambiente:
```yaml
USE_GPU: "true"
FORCE_CUDA: "1"
CUDA_VISIBLE_DEVICES: "0"
NVIDIA_VISIBLE_DEVICES: "all"
NVIDIA_DRIVER_CAPABILITIES: "compute,utility"
```

#### Volumes (IMPORTANTE!):
```yaml
/dev/nvidia0:/dev/nvidia0
/dev/nvidiactl:/dev/nvidiactl
/dev/nvidia-uvm:/dev/nvidia-uvm
/dev/nvidia-modeset:/dev/nvidia-modeset
```

#### Configurações Avançadas:
```yaml
privileged: true
runtime: nvidia
```

## 🔍 DIAGNÓSTICO:

O novo Dockerfile fará 3 tentativas de detectar GPU:
1. **nvidia-smi** - Comando direto
2. **PyTorch CUDA** - Detecção Python
3. **nvidia-ml-py** - Biblioteca alternativa

## ⚠️ SE AINDA NÃO FUNCIONAR:

### No Easypanel UI:
1. Vá em **Settings** do serviço
2. Procure por **"GPU"** ou **"Device"** options
3. Ative qualquer opção relacionada a GPU
4. Adicione **"privileged: true"** nas configurações avançadas

### Teste Manual:
```bash
# SSH no servidor Easypanel
docker exec SEU_CONTAINER nvidia-smi

# Se falhar, tente:
docker run --rm --privileged --gpus all nvidia/cuda:12.1.0-runtime-ubuntu22.04 nvidia-smi
```

## 📝 ALTERNATIVA FINAL:

Se o Easypanel não suportar GPU nativamente, você pode:

1. **Deploy manual com Docker**:
```bash
docker run -d \
  --name hybrid-search \
  --gpus all \
  --privileged \
  -p 8000:8000 \
  -v $(pwd):/app \
  -e USE_GPU=true \
  --build -f Dockerfile.easypanel-gpu .
```

2. **Usar Docker Compose direto** (fora do Easypanel):
```bash
docker-compose -f easypanel-gpu-force.yml up -d
```

## 🎯 CHECKLIST:

- [ ] Use `Dockerfile.easypanel-gpu`
- [ ] Use `easypanel-gpu-force.yml`
- [ ] Adicione volumes /dev/nvidia*
- [ ] Configure privileged: true
- [ ] Force variáveis USE_GPU=true
- [ ] Verifique logs para diagnóstico

## 💡 NOTA IMPORTANTE:

Alguns painéis como Easypanel podem ter limitações com GPU. Se não funcionar:
1. A API funciona PERFEITAMENTE com CPU (só mais lenta)
2. Considere deploy direto com Docker (fora do painel)
3. Use um serviço cloud com suporte GPU nativo (AWS ECS, GCP, etc.)

---

**API Key**: `Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4`

A API está funcionando! GPU é opcional para melhor performance.