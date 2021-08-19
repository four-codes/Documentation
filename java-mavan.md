```DOckerfile
FROM openjdk:8-jdk-alpine as build
ARG VERSION=3.8.1
WORKDIR /app
RUN wget https://downloads.apache.org/maven/maven-3/$VERSION/binaries/apache-maven-$VERSION-bin.zip
RUN unzip apache-maven-$VERSION-bin.zip
RUN rm -rf apache-maven-$VERSION-bin.zip
ENV MAVEN_HOME=/app/apache-maven-$VERSION
ENV PATH="$MAVEN_HOME/bin:$PATH"
COPY . .
RUN mvn clean package


FROM openjdk:8-jre-alpine
WORKDIR /app
COPY --from=build /app/admin-backend/target/admin-module-2.4.2.jar .
EXPOSE 8082
CMD ["java","-jar","admin-module-2.4.2.jar"]
```
