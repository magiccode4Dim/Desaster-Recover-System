FROM openjdk:8-jdk-alpine
WORKDIR /app
COPY target/USERSERVICE-1.0.jar service.jar
EXPOSE 8087
CMD ["java", "-jar", "service.jar"]
