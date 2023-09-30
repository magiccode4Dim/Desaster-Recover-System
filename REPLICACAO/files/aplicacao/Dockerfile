FROM php:apache

# Atualize o sistema e instale as extensões do PHP necessárias
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && docker-php-ext-configure pgsql -with-pgsql=/usr/local/pgsql \
    && docker-php-ext-install pdo pdo_pgsql pgsql 


RUN apt-get install -y wget unzip
#baixa a codigo
RUN wget http://192.168.122.1:9000/aplicacao/crudphpdocker.zip
#RUN curl -o crudphpdocker.zip http://192.168.122.1:9000/aplicacao/crudphpdocker.zip
#tira do zip
RUN unzip crudphpdocker.zip

# move para a pasta do apache
RUN cp -r crudphpdocker/* /var/www/html

# Configure o PHP para mostrar erros no navegador (apenas para fins de desenvolvimento)
#RUN echo "display_errors=On" >> /usr/local/etc/php/php.ini

# Exponha a porta 80, que é a porta padrão do Nginx
EXPOSE 80

# Defina as variáveis de ambiente para a conexão com o banco de dados
#ENV DB_HOST="'192.168.122.119'"
#ENV DB_PORT="5432"
#ENV DB_USER="'narciso'"
#ENV DB_PASS="'2001'"
#ENV DB_NAME="'crudphp'"

# Inicialize o servidor Apache em segundo plano
CMD ["apache2-foreground"]
