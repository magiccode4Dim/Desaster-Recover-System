FROM openjdk8-and-python3
WORKDIR /app
COPY target/IMAGESERVICE-1.0.jar service.jar
COPY src/main/resources/scripts/* ./
RUN pip install -r requirements.txt
EXPOSE 8088
#cria um script e roda o script e o arquivo java ao mesmo tempo
RUN echo -e '#!/bin/sh\npython server.py &\njava -jar service.jar' > start.sh

RUN chmod +x start.sh


CMD ["./start.sh"]
