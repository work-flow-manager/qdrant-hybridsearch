# 🎮 Configuração GPU Quadro RTX 4000 no Easypanel

## 📊 Status da Sua Máquina

### ✅ GPU Detectada:
- **Modelo**: NVIDIA Quadro RTX 4000
- **Memória**: 8GB VRAM
- **Driver**: 575.64.03
- **CUDA**: 12.9

### ❌ Problema Atual:
- **NVIDIA Container Toolkit NÃO está instalado**
- Por isso a GPU não está sendo detectada dentro dos containers Docker

## 🔧 Como Resolver: Instalar NVIDIA Container Toolkit

### No Servidor Easypanel (Ubuntu/Debian):

```bash
# 1. Configurar repositório NVIDIA
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# 2. Instalar NVIDIA Container Toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# 3. Configurar Docker
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# 4. Testar
docker run --rm --gpus all nvidia/cuda:12.1.0-runtime-ubuntu22.04 nvidia-smi
```

## 🚀 Deploy no Easypanel (Solução Atual)

### Arquivos Prontos para Deploy:

1. **`Dockerfile.final`** - Funciona COM ou SEM GPU
2. **`easypanel-final.yml`** - Docker Compose inteligente
3. **API Key**: `Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4`

### Como Funciona:
- O Dockerfile.final **detecta automaticamente** se há GPU disponível
- Se GPU detectada: usa modo GPU (rápido)
- Se não detectada: usa modo CPU (funcional)

## 📝 Para Ativar GPU no Easypanel:

### Opção 1: Com NVIDIA Container Toolkit (Recomendado)

Após instalar o toolkit, edite `easypanel-final.yml`:

```yaml
app:
  # Descomente estas linhas:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

### Opção 2: Passthrough Manual (Alternativa)

Se não puder instalar o toolkit, adicione devices manualmente:

```yaml
app:
  devices:
    - /dev/nvidia0:/dev/nvidia0
    - /dev/nvidiactl:/dev/nvidiactl
    - /dev/nvidia-uvm:/dev/nvidia-uvm
    - /dev/nvidia-modeset:/dev/nvidia-modeset
```

## 🧪 Verificar se GPU Está Funcionando:

```bash
# 1. Dentro do container
docker exec app python3 -c "import torch; print(torch.cuda.is_available())"

# 2. Via API
curl -H "X-API-Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4" \
     http://localhost:8000/api/system/info
```

## 📊 Performance Esperada:

### Com GPU (Quadro RTX 4000):
- **Embeddings/seg**: ~800-1500
- **Batch size**: 64-128
- **Latência**: < 100ms
- **Uso VRAM**: 4-6GB

### Sem GPU (CPU):
- **Embeddings/seg**: ~50-100
- **Batch size**: 16-32
- **Latência**: 200-500ms

## ⚠️ Erro Atual nos Logs:

```
ModuleNotFoundError: No module named 'pydantic_settings'
```
**✅ RESOLVIDO**: Adicionado no Dockerfile.final

```
CUDA disponível: False
```
**⚠️ ESPERADO**: Até instalar NVIDIA Container Toolkit

## 🎯 Checklist de Deploy:

- [ ] Usar `Dockerfile.final` (já tem pydantic_settings)
- [ ] Usar `easypanel-final.yml`
- [ ] API Key: `Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4`
- [ ] (Opcional) Instalar NVIDIA Container Toolkit para GPU
- [ ] (Opcional) Descomentar linhas GPU no docker-compose

## 💡 Dica Importante:

**O sistema funcionará PERFEITAMENTE sem GPU!** A detecção é automática:
- Com GPU: 10x mais rápido
- Sem GPU: Totalmente funcional

## 🆘 Comandos de Debug:

```bash
# Ver logs completos
docker logs app -f

# Verificar se pydantic_settings está instalado
docker exec app pip list | grep pydantic

# Testar import dos módulos
docker exec app python3 -c "from pydantic_settings import BaseSettings; print('OK')"

# Ver uso de memória
docker stats app
```

## 📦 Para Fazer Deploy Agora:

```bash
# No Easypanel, use estes arquivos:
- Dockerfile.final
- easypanel-final.yml
- requirements.txt
- pasta app/

# O sistema detectará automaticamente se há GPU disponível!
```

---

**Sua Quadro RTX 4000 está pronta**, só precisa do NVIDIA Container Toolkit para o Docker acessá-la!