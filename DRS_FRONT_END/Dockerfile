FROM python:3

WORKDIR /app/

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8000

#CMD ["python","manage.py","runserver","0.0.0.0:8000"]

COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

# Comando para executar o script personalizado 
#CMD ["/app/start.sh"]

#sudo docker build -t aaeewarsfrontend .
