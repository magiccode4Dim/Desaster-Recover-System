FROM openjdk:8-jdk-alpine
WORKDIR /app
COPY target/STATUSSERVICE-1.0.jar service.jar
EXPOSE 8086
CMD ["java", "-jar", "service.jar"]
