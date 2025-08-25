#!/bin/bash

# Deploy script for Qdrant Hybrid Search

echo "🚀 Starting Qdrant Hybrid Search Deployment..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi

# Check for NVIDIA GPU
if ! nvidia-smi &> /dev/null; then
    echo "⚠️ NVIDIA GPU not detected. Running in CPU mode..."
    sed -i 's/USE_GPU=true/USE_GPU=false/' .env
fi

# Create necessary directories
mkdir -p data/qdrant models

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created .env file from example. Please configure your settings."
fi

# Build Docker images
echo "🔨 Building Docker images..."
docker compose build

# Start services
echo "🚀 Starting services..."
docker compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
docker compose ps

# Display access information
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📍 Access Points:"
echo "  - API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Qdrant UI: http://localhost:6333/dashboard"
echo ""
echo "🔑 Default API Key: Check your .env file"
echo ""
echo "📊 View logs:"
echo "  docker compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "  docker compose down"