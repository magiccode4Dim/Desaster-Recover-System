FROM openjdk:8-jdk-alpine
WORKDIR /app
COPY target/DRS_EUREKA_SERVER-1.0.jar service.jar
EXPOSE 8761
CMD ["java", "-jar", "service.jar"]
