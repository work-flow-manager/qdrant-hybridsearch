# GitHub Setup Instructions

## 🔑 SSH Deploy Key

### Chave Pública (adicionar no GitHub):
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBSybvT1hKOjBaZ2uB585alGRbNbONVN6W+cXgA+AXuk qdrant-hybrid-search@github
```

### Como adicionar no GitHub:

1. **Acesse seu repositório no GitHub**
2. **Vá em Settings → Deploy keys**
3. **Clique em "Add deploy key"**
4. **Título:** `Qdrant Hybrid Search Server`
5. **Key:** Cole a chave pública acima
6. **Marque:** "Allow write access" (se quiser fazer push)
7. **Clique em "Add key"**

## 📦 Configurar Git Localmente

```bash
# Configurar Git para usar a chave SSH
eval $(ssh-agent -s)
ssh-add github_deploy_key

# Inicializar repositório
git init
git add .
git commit -m "Initial commit: Qdrant Hybrid Search with GPU support"

# Adicionar remote (substitua pelo seu repositório)
git remote add origin git@github.com:SEU_USUARIO/qdrant-hybrid-search.git

# Fazer push
git push -u origin main
```

## 🚀 Clone com Deploy Key

Para clonar em outro servidor:

```bash
# Criar arquivo de configuração SSH
cat > ~/.ssh/config << EOF
Host github-qdrant
    HostName github.com
    User git
    IdentityFile ~/github_deploy_key
EOF

# Clonar usando a configuração
git clone github-qdrant:SEU_USUARIO/qdrant-hybrid-search.git
```

## 📝 Arquivos de Chave

- **Chave Privada:** `github_deploy_key` (manter segura!)
- **Chave Pública:** `github_deploy_key.pub` (adicionar no GitHub)

⚠️ **IMPORTANTE:** Nunca commite a chave privada `github_deploy_key` no repositório!