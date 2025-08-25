# 🚨 INSTALAÇÃO RÁPIDA GPU - PASSO A PASSO

## ✅ O QUE VOCÊ PRECISA INSTALAR:

### 1️⃣ NVIDIA Container Toolkit (NECESSÁRIO para GPU funcionar no Docker)

```bash
# COPIE E COLE ESTES COMANDOS NO TERMINAL:

# 1. Adicionar repositório NVIDIA
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# 2. Instalar NVIDIA Container Toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# 3. Configurar Docker para usar GPU
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# 4. TESTAR se funcionou
docker run --rm --gpus all nvidia/cuda:12.1.0-runtime-ubuntu22.04 nvidia-smi
```

Se o teste mostrar sua Quadro RTX 4000, está pronto! ✅

## 📦 QUAL DOCKERFILE E ENV USAR:

### USAR ESTES ARQUIVOS:
```
✅ Dockerfile.final        (USAR ESTE!)
✅ easypanel-final.yml     (USAR ESTE!)
✅ .env.gpu               (SIM, USAR ESTE!)
```

### NÃO USAR ESTES:
```
❌ Dockerfile.gpu
❌ Dockerfile.easypanel
❌ Dockerfile.fixed
❌ easypanel-gpu.yml
```

## 🚀 COMANDO PARA DEPLOY NO EASYPANEL:

```bash
# Com GPU ativada (após instalar NVIDIA Container Toolkit):
docker-compose -f easypanel-final.yml up -d --build
```

## 🔑 VARIÁVEIS DE AMBIENTE (.env.gpu):

```bash
# SIM, USE O .env.gpu! Estas são as configurações:
API_KEY=Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4
USE_GPU=true              # Será detectado automaticamente
CUDA_DEVICE=0
BATCH_SIZE=64             # Para sua RTX 4000
```

## 📝 NO EASYPANEL - CONFIGURAÇÃO FINAL:

### 1. Editar easypanel-final.yml e DESCOMENTAR estas linhas:
```yaml
app:
  # DESCOMENTE ESTAS LINHAS (remova o #):
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

### 2. Fazer upload dos arquivos:
- Dockerfile.final
- easypanel-final.yml
- .env.gpu
- requirements.txt
- pasta app/

## ✅ VERIFICAR SE GPU ESTÁ FUNCIONANDO:

```bash
# Após o deploy, teste:
docker exec app python3 -c "import torch; print(f'GPU: {torch.cuda.is_available()}')"

# Deve retornar: GPU: True
```

## 🎯 RESUMO - O QUE FAZER AGORA:

1. **INSTALAR** NVIDIA Container Toolkit (comandos acima)
2. **USAR** Dockerfile.final + easypanel-final.yml + .env.gpu
3. **DESCOMENTAR** linhas GPU no docker-compose
4. **DEPLOY** no Easypanel
5. **VERIFICAR** se GPU está ativa

## ⚠️ SE NÃO QUISER INSTALAR (funciona sem GPU):

O sistema funcionará perfeitamente só com CPU, apenas mais lento:
- Use os mesmos arquivos (Dockerfile.final + easypanel-final.yml)
- NÃO descomente as linhas GPU
- Pronto!

## 💬 RESPOSTA DIRETA:

**SIM, você precisa instalar o NVIDIA Container Toolkit** para a GPU funcionar no Docker.
- **Dockerfile**: usar `Dockerfile.final`
- **Docker Compose**: usar `easypanel-final.yml`
- **ENV**: SIM, usar `.env.gpu`
- **API Key**: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4

---
🚀 **Copie os comandos da seção 1️⃣ e execute no terminal agora!**