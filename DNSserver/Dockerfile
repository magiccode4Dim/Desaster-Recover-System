# Use uma imagem base do Ubuntu
FROM ubuntu:latest

# Instale o BIND (servidor DNS)
RUN apt-get update && apt-get install -y bind9

# Copie o arquivo de configuração do BIND
COPY named.conf.local /etc/bind/
COPY db.rh.net /etc/bind/

# Exponha a porta DNS (53)
EXPOSE 53/udp

# Inicie o BIND como processo principal
CMD ["/usr/sbin/named", "-g", "-c", "/etc/bind/named.conf", "-u", "bind"]
