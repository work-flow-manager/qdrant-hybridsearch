#!/bin/bash

# Script de Deploy para Easypanel com Build Local
# Este script prepara os arquivos necessários para deploy no Easypanel

echo "🚀 Preparando deploy para Easypanel..."

# Criar arquivo ZIP com todos os arquivos necessários
echo "📦 Criando arquivo para upload..."

# Lista de arquivos necessários
FILES=(
    "Dockerfile.easypanel"
    "easypanel-build.yml"
    "requirements.txt"
    "app/"
)

# Verificar se os arquivos existem
for file in "${FILES[@]}"; do
    if [ ! -e "$file" ]; then
        echo "❌ Erro: $file não encontrado!"
        exit 1
    fi
done

# Criar arquivo tar.gz
tar -czf easypanel-deploy.tar.gz \
    Dockerfile.easypanel \
    easypanel-build.yml \
    requirements.txt \
    app/

echo "✅ Arquivo easypanel-deploy.tar.gz criado!"

echo ""
echo "📋 INSTRUÇÕES PARA DEPLOY NO EASYPANEL:"
echo "========================================"
echo ""
echo "1. FAZER UPLOAD DOS ARQUIVOS:"
echo "   - Faça upload do arquivo easypanel-deploy.tar.gz"
echo "   - Ou faça git clone do repositório"
echo ""
echo "2. NO EASYPANEL:"
echo "   a) Crie um novo projeto"
echo "   b) Escolha 'Docker Compose'"
echo "   c) Cole o conteúdo de easypanel-build.yml"
echo "   d) Configure a variável API_KEY com uma chave segura"
echo "   e) Clique em Deploy"
echo ""
echo "3. PRIMEIRO DEPLOY:"
echo "   - O build levará ~5-10 minutos (download dos modelos)"
echo "   - Builds posteriores serão mais rápidos (cache)"
echo ""
echo "4. VERIFICAR FUNCIONAMENTO:"
echo "   curl https://seu-dominio/health"
echo ""
echo "🎯 Arquivo pronto: easypanel-deploy.tar.gz"