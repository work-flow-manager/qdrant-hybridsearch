# 🎮 O QUE PRECISA INSTALAR PARA GPU NVIDIA FUNCIONAR

## 📋 REQUISITOS NO SERVIDOR

### 1️⃣ SEM GPU (Apenas CPU)
**NÃO PRECISA INSTALAR NADA DA NVIDIA!** ✅

A aplicação funciona perfeitamente apenas com CPU:
- Use `Dockerfile.production`
- Configure `USE_GPU=false`
- Pronto! Não precisa de nada da NVIDIA

### 2️⃣ COM GPU NVIDIA (RTX 4000, etc)

Se o servidor TEM uma GPU NVIDIA, você precisa:

#### A. Driver NVIDIA (OBRIGATÓRIO)
```bash
# Verificar se já tem driver instalado
nvidia-smi

# Se não tiver, instalar:
sudo apt update
sudo apt install nvidia-driver-525  # ou versão mais recente

# Reiniciar
sudo reboot

# Verificar após reiniciar
nvidia-smi
```

#### B. NVIDIA Container Toolkit (OBRIGATÓRIO para Docker)
```bash
# 1. Adicionar repositório
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# 2. Instalar nvidia-docker2
sudo apt update
sudo apt install nvidia-docker2

# 3. Reiniciar Docker
sudo systemctl restart docker

# 4. Testar
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

## 🤔 COMO SABER SE PRECISA?

### No Easypanel/Servidor, execute:
```bash
# Teste 1: Tem GPU?
lspci | grep -i nvidia

# Se retornar algo como:
# 01:00.0 VGA compatible controller: NVIDIA Corporation Device...
# ✅ TEM GPU - precisa instalar drivers

# Se não retornar nada:
# ❌ NÃO TEM GPU - não precisa instalar nada
```

## 💡 RESUMO RÁPIDO

| Situação | O que fazer | Dockerfile | Configuração |
|----------|------------|------------|--------------|
| **Servidor SEM GPU** | Nada! | `Dockerfile.production` | `USE_GPU=false` |
| **Servidor COM GPU** | Instalar driver + nvidia-docker2 | `Dockerfile.gpu` | `USE_GPU=true` + `--gpus all` |
| **Easypanel na nuvem** | Geralmente não tem GPU | `Dockerfile.production` | `USE_GPU=false` |

## 🚀 PARA EASYPANEL (Maioria dos casos)

**99% dos servidores Easypanel NÃO têm GPU**, então:

```yaml
# Use este Dockerfile (já está no GitHub)
Dockerfile: Dockerfile.production

# Configure assim
Environment:
  USE_GPU: false
  BATCH_SIZE: 16  # Menor para CPU
```

## ✅ A APLICAÇÃO FUNCIONA PERFEITAMENTE SEM GPU!

Diferenças de performance:
- **COM GPU**: Processa 32 documentos em ~50ms
- **SEM GPU**: Processa 16 documentos em ~800ms

Ambos funcionam bem! A GPU apenas acelera o processamento.

## 🔍 VERIFICAR NO EASYPANEL

SSH no servidor e execute:
```bash
# Verificar se tem GPU
nvidia-smi

# Se der erro "command not found":
# = Não tem GPU ou driver não instalado
# = Use modo CPU (USE_GPU=false)

# Se mostrar uma tabela com GPU:
# = Tem GPU e driver instalado
# = Pode usar modo GPU (USE_GPU=true)
```

## 📝 CONCLUSÃO

### Para Easypanel comum (sem GPU):
- ✅ **NÃO precisa instalar nada da NVIDIA**
- ✅ Use `Dockerfile.production`
- ✅ Configure `USE_GPU=false`
- ✅ Vai funcionar perfeitamente!

### Só precisa NVIDIA se:
- Servidor tem GPU física
- Você quer acelerar processamento
- Tem acesso root para instalar drivers

---

**NA DÚVIDA: Use modo CPU que funciona em qualquer lugar!**