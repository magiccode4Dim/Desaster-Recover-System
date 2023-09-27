# Use a imagem openjdk:8-jdk-alpine como imagem base
FROM openjdk:8-jdk-alpine

# Atualize e instale as dependências necessárias para o Python 3
RUN apk update && apk add --no-cache python3 py3-pip

# Crie um link simbólico para 'python' apontando para 'python3'
RUN ln -s /usr/bin/python3 /usr/bin/python

# Atualize o pip para a versão mais recente
RUN python -m pip install --upgrade pip

# Adicione os comandos ou instruções adicionais aqui, se necessário

# Define o diretório de trabalho padrão
WORKDIR /app

#sudo docker build -t openjdk8-and-python3 .
