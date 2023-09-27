#!/bin/bash

# Lista de diretórios onde estão localizados os Dockerfiles
microservices_directories=(
  "USERSERVICE"
  "STATUSSERVICE"
  "MANAGERSERVICE"
  "IMAGESERVICE"
  "FAILOVERSERVICE"
  "BACKUPSERVICE"
  "DRS_EUREKA_SERVER"
)

# Loop para percorrer os diretórios
for directory in "${microservices_directories[@]}"; do
  ldirectory=$(echo "$directory" | tr '[:upper:]' '[:lower:]')
  echo "Building Docker image for microservice in directory: $directory"
  
  # Verificar se o ficheiro existe
  if [ -f "$directory/Dockerfile" ]; then
    # Executar o comando 'docker build' no diretório
    docker build -t "$ldirectory-wars" "$directory"
  else
    echo "Dockerfile not found in directory: $directory"
  fi
done
