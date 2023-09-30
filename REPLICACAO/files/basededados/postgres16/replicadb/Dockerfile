FROM postgres


#instalad dependencias
RUN apt-get update && apt-get install -y \
    wget unzip 


#vARIAVEIS DE AMBIENTE
ENV PG_MASTER_HOST="192.168.122.119"
ENV PG_MASTER_PORT="5433"
ENV PG_MASTER_DB="crudphp"
ENV PG_MASTER_USER="nany"
ENV PG_MASTER_PASSWORD="2001"
ENV MASTER_PUB="crudphppub"

#usuario root da base de dados
ENV ROOT_USER="narciso"
ENV ROOT_PASSWORD="2001"

#usuario de replicacao
ENV REP_USER="nany2"
ENV REP_PASS="2001"
ENV TABLENAME="mining_tb"
#ENV TABLENAME="pessoa"
ENV TABLE_SQL="mining_tb(mine_id serial PRIMARY KEY,mine_color varchar(15) NOT NULL,install_date date,mine_owner varchar(20));"
#ENV TABLE_SQL="pessoa(id serial PRIMARY KEY,nome varchar(15) NOT NULL);"
#ENV SUBSCRITION="replicasub" O nome da subscricao sera passada ao executar o container
ENV PUBLICATION="crudphppub2"

#CONFIGURACOES
RUN echo "wal_level = logical" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "max_replication_slots = 10" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "max_wal_senders = 10" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "listen_addresses = '*'" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "host    all             all             0.0.0.0/0            md5" >> /etc/postgresql/pg_hba.conf


#EXPOR A PORTA DA BASE DE DADOS
EXPOSE 5432

#COPY init-replication.sh /docker-entrypoint-initdb.d/
#baixa o script

RUN wget http://192.168.122.1:9000/init-replication.sh


# move
RUN mv init-replication.sh /docker-entrypoint-initdb.d/

#build and run
#sudo docker build -t postgresreplica .
#sudo docker run --name replicapostgres -e POSTGRES_PASSWORD=mysecretpassword -d postgresreplica

