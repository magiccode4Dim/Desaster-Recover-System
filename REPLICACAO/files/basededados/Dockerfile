FROM postgres:14


#instalad dependencias
RUN apt-get update && apt-get install -y \
    wget unzip 


#vARIAVEIS DE AMBIENTE
ENV PG_MASTER_HOST="192.168.122.119"
ENV PG_MASTER_PORT="5432"
ENV PG_MASTER_DB="crudphp"
ENV PG_MASTER_USER="narciso"
ENV PG_MASTER_PASSWORD="2001"
ENV TABLENAME="mining_tb"
ENV TABLE_SQL="mining_tb(mine_id serial PRIMARY KEY,mine_color varchar(15) NOT NULL,install_date date,mine_owner varchar(20));"
ENV SUBSCRITION="crudphpsub799"
ENV PUBLICATION="crudphppub"

#CONFIGURACOES
RUN echo "wal_level = logical" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "max_replication_slots = 10" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "max_wal_senders = 10" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "listen_addresses = '*'" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "host    all             all             0.0.0.0/0            md5" >> /etc/postgresql/pg_hba.conf


#EXPOR A PORTA DA BASE DE DADOS
EXPOSE 5432

#baixa o script
RUN wget http://192.168.122.1:9000/basededados/init-replication.sh


# move
RUN mv init-replication.sh /docker-entrypoint-initdb.d/

