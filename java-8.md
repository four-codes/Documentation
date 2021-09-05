```Dockerfile
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

# Multistage

FROM openjdk:8-jre-alpine
RUN apk upgrade
WORKDIR /app
COPY --from=build /app/web-backend/target/web-backend-2.4.2.jar .
EXPOSE 8083
CMD ["java","-jar","web-backend-2.4.2.jar"]
```
