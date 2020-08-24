FROM maven:3.6.3-jdk-11 AS build
LABEL stage=builder

# Copy deps and source over
COPY pom.xml /usr/src/app/  
COPY src /usr/src/app/src/
COPY target /usr/src/app/target/
COPY lib /usr/src/app/lib/
WORKDIR /usr/src/app

# Compile and package into jar
RUN mvn -f /usr/src/app/pom.xml -DskipTests package

# Run from slim java container
FROM gcr.io/distroless/java
COPY --from=build /usr/src/app/target/metamap-1.0-SNAPSHOT.jar /usr/app/metamap-1.0-SNAPSHOT.jar 
COPY resources /usr/app/resources
WORKDIR /usr/app
ENTRYPOINT ["java","-XX:+UnlockExperimentalVMOptions", "-XX:+UseCGroupMemoryLimitForHeap","-jar","/usr/app/metamap-1.0-SNAPSHOT.jar"]

#COPY resources /usr/app/resources
#RUN ls -a /usr/src/app/lib
#ENTRYPOINT ["java","-XX:+UnlockExperimentalVMOptions", "-XX:+UseCGroupMemoryLimitForHeap","-jar","/usr/src/app/target/metamap-1.0-SNAPSHOT.jar"]