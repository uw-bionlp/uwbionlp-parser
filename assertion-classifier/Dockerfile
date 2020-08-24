FROM maven:3.5-jdk-8 AS build
LABEL stage=builder

# Copy deps and source over
COPY pom.xml /usr/src/app/  
COPY src /usr/src/app/src/
COPY lib /usr/src/app/lib/
WORKDIR /usr/src/app

# Compile and package into jar
RUN mvn -f /usr/src/app/pom.xml -DskipTests package

# Run from slim java container
FROM gcr.io/distroless/java
COPY --from=build /usr/src/app/target/assertion-classifier-1.0-SNAPSHOT.jar /usr/app/assertion-classifier-1.0-SNAPSHOT.jar 
COPY resources /usr/app/resources
WORKDIR /usr/app
ENTRYPOINT ["java","-jar","/usr/app/assertion-classifier-1.0-SNAPSHOT.jar"]