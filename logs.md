Commit: Add: Guia completo de uso da API e script de teste

Criado COMO_USAR_API.md com:
- Como acessar dashboards (Swagger UI e ReDoc)
- Exemplos de inserção de dados
- Exemplos de busca
- Todos os endpoints disponíveis
- Script Python de exemplo

Criado teste_api.py:
- Script completo para testar a API
- Insere dados de exemplo
- Faz buscas de teste
- Mostra como usar todos os endpoints

Dashboards disponíveis:
- API Swagger: http://IP:8000/docs
- API ReDoc: http://IP:8000/redoc
- Qdrant Dashboard: http://IP:6333/dashboard

API Key: Gw9iEdSGbAlsyoiT5YEJUbCy6O33bfxs9CV2-iZQjN4 
##########################################
### Download Github Archive Started...
### Mon, 25 Aug 2025 22:09:10 GMT
##########################################

#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile.production
#1 transferring dockerfile: 2B done
#1 DONE 0.0s
ERROR: failed to build: failed to solve: failed to read dockerfile: open Dockerfile.production: no such file or directory
##########################################
### Error
### Mon, 25 Aug 2025 22:09:10 GMT
##########################################

Command failed with exit code 1: docker buildx build --network host -f /etc/easypanel/projects/app/qdrant-hybrid/code/Dockerfile.production -t easypanel/app/qdrant-hybrid --label 'keep=true' --no-cache --build-arg 'GIT_SHA=d4279a8609358006ece1392896c48e1924c5e961' /etc/easypanel/projects/app/qdrant-hybrid/code/