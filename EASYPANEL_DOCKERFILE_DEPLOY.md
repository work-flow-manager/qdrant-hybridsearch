# 🐳 Deploy no Easypanel com Dockerfile (Build Local)

## ✅ Solução para o Erro de Autorização

Como a imagem no GitHub Container Registry está com problema de acesso, vamos fazer o **build local** diretamente no Easypanel usando Dockerfile.

## 📁 Arquivos Criados

### 1. `Dockerfile.easypanel`
- Dockerfile otimizado para CPU (mais rápido)
- Instala todas as dependências necessárias
- Baixa os modelos na primeira execução
- Configurado para ambiente de produção

### 2. `easypanel-build.yml`
- Docker Compose que faz build local
- Não depende de imagem externa
- Configuração completa do ambiente

### 3. `deploy-easypanel.sh`
- Script para preparar arquivos para deploy
- Cria arquivo compactado para upload

## 🚀 Como Fazer Deploy no Easypanel

### Método 1: Upload de Arquivos (Recomendado)

1. **Preparar arquivos localmente:**
   ```bash
   ./deploy-easypanel.sh
   ```
   Isso criará `easypanel-deploy.tar.gz`

2. **No Easypanel:**
   - Criar novo projeto
   - Escolher "Docker Compose"
   - Fazer upload do arquivo `easypanel-deploy.tar.gz`
   - Ou fazer upload individual dos arquivos:
     - `Dockerfile.easypanel`
     - `easypanel-build.yml`
     - `requirements.txt`
     - Pasta `app/` completa

3. **Configurar e Deploy:**
   - Cole o conteúdo de `easypanel-build.yml`
   - Ajuste `API_KEY` para uma chave segura
   - Clique em "Deploy"

### Método 2: Git Clone no Easypanel

1. **No Easypanel Terminal:**
   ```bash
   git clone https://github.com/work-flow-manager/qdrant-hybridsearch.git
   cd qdrant-hybridsearch
   ```

2. **Usar o docker-compose de build:**
   ```bash
   docker-compose -f easypanel-build.yml up -d
   ```

## ⚙️ Configurações Importantes

### Variáveis de Ambiente
```yaml
API_KEY: "sua-chave-segura-aqui"  # MUDE ISSO!
USE_GPU: "false"                   # Mude para "true" se tiver GPU
BATCH_SIZE: "32"                   # Reduza se tiver pouca memória
```

### Requisitos Mínimos
- **RAM:** 4GB (8GB recomendado)
- **Disco:** 10GB (para modelos e dados)
- **CPU:** 2 cores (4 cores recomendado)

## 📊 Tempo de Deploy

### Primeiro Deploy
- **Build da imagem:** ~5-10 minutos
- **Download dos modelos:** ~5 minutos
- **Total:** ~15 minutos

### Deploys Posteriores
- **Com cache:** ~2-3 minutos
- Os modelos ficam salvos no volume

## 🧪 Verificar Funcionamento

```bash
# Health Check
curl http://seu-dominio:8000/health

# Teste com API Key
curl -H "X-API-Key: sua-api-key" \
     http://seu-dominio:8000/api/collections
```

## 🐛 Troubleshooting

### Build falha com "out of memory"
**Solução:** Aumente a memória do Docker ou reduza workers:
```yaml
NUM_WORKERS: "2"  # Reduza de 4 para 2
```

### Modelos demoram muito para baixar
**Solução:** Normal na primeira vez. Use volumes persistentes:
```yaml
volumes:
  models-cache:  # Mantém modelos entre deploys
```

### API não responde após deploy
**Checklist:**
1. Verifique logs: `docker logs app`
2. Confirme que Qdrant está rodando: `docker ps`
3. Teste conexão interna: `docker exec app curl qdrant:6333`

### Erro "torch not compiled with CUDA"
**Solução:** Está configurado para CPU. Se tiver GPU:
1. Use o `Dockerfile` original (não o .easypanel)
2. Configure `USE_GPU: "true"`
3. Adicione runtime NVIDIA no Easypanel

## 🔄 Atualizar Código

Para atualizar após mudanças:
```bash
# No Easypanel
git pull
docker-compose -f easypanel-build.yml up -d --build
```

## 💡 Dicas de Performance

1. **Cache de Modelos:** Sempre use volumes para `/app/models`
2. **Multi-stage Build:** O Dockerfile já está otimizado
3. **Health Checks:** Configurados para auto-restart
4. **Logs:** Use `LOG_LEVEL: "WARNING"` em produção

## 📝 Exemplo Completo no Easypanel

```yaml
# Este é o conteúdo do easypanel-build.yml
# Cole isso no Easypanel após upload dos arquivos
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant-storage:/qdrant/storage
    environment:
      QDRANT__SERVICE__HTTP_PORT: "6333"

  app:
    build:
      context: .
      dockerfile: Dockerfile.easypanel
    ports:
      - "8000:8000"
    volumes:
      - models-cache:/app/models
    environment:
      API_KEY: "MUDE-ESTA-CHAVE"
      QDRANT_HOST: "qdrant"
    depends_on:
      - qdrant

volumes:
  qdrant-storage:
  models-cache:
```

## ✅ Vantagens do Build Local

1. **Independente:** Não depende de registro externo
2. **Customizável:** Pode modificar o Dockerfile
3. **Seguro:** Código fonte no seu controle
4. **Flexível:** Ajuste conforme necessidade

## 🆘 Suporte

- **Logs:** `docker logs app` ou `docker logs qdrant`
- **Status:** `docker ps` para ver containers
- **Recursos:** `docker stats` para monitorar uso

---

**Nota:** Este método resolve o problema de autorização fazendo build local. O Easypanel compilará a imagem diretamente dos seus arquivos.