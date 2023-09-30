#!/bin/bash
set -e

# Inicie o PostgreSQL
pg_ctl restart -D /var/lib/postgresql/data

# Espera até que o PostgreSQL esteja pronto para aceitar conexões
#until pg_isready -h localhost -p 5432; do
#    echo "Aguardando o PostgreSQL iniciar..."
#    sleep 2
#done

# Crie um novo usuário administrador (substitua "new_admin_user" e "new_admin_password" pelos valores desejados)
psql -U postgres -c "CREATE USER ${PG_MASTER_USER} WITH PASSWORD '${PG_MASTER_PASSWORD}';"

# Conceda privilégios de superusuário ao novo usuário (opcional, se necessário)
psql -U postgres -c "ALTER USER ${PG_MASTER_USER} WITH SUPERUSER;"


# Crie a base de dados, se ela não existir
psql -U postgres -c "CREATE DATABASE ${PG_MASTER_DB};"

# Conecte-se à base de dados recém-criada
psql -U postgres -d ${PG_MASTER_DB} -c "CREATE TABLE ${TABLE_SQL};"

# Crie uma Publicação (Publication) para a tabela
#psql -U postgres -d ${PG_MASTER_DB}  -c "CREATE PUBLICATION ${PUBLICATION} FOR TABLE ${TABLENAME};"

# Configure a replicação lógica
psql -U postgres -d ${PG_MASTER_DB} -c "CREATE SUBSCRIPTION ${SUBSCRITION} CONNECTION 'host=${PG_MASTER_HOST} port=${PG_MASTER_PORT} user=${PG_MASTER_USER} password=${PG_MASTER_PASSWORD} dbname=${PG_MASTER_DB}' PUBLICATION ${PUBLICATION}"


