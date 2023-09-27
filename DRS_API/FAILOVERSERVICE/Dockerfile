FROM openjdk:8-jdk-alpine
WORKDIR /app
COPY target/FAILOVERSERVICE-1.0.jar service.jar
EXPOSE 8091
CMD ["java", "-jar", "service.jar"]
