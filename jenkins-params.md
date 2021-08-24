```Jenkins
pipeline {
    agent any 
        parameters {
        	string(name: 'RUNNER', defaultValue: 'SanityTestRunner', description: 'ENTER THE RUNNER VALUE?')
        	string(name: 'TAG', defaultValue: '@notification', description: 'ENTER THE TAG VALUE?')
        	string(name: 'ENV', defaultValue: 'dev', description: 'ENTER THE ENV VALUE?')
    }
    stages {
        stage('check version') {   
        steps {
            sh'''
                docker --version
            '''
            }
        }

        stage('Deploment state') {
            environment {
                RUNNER = "${params.RUNNER}"
                TAG = "${params.TAG}"
                ENV = "${params.ENV}"
            }

        steps {
            sh'''
	            sshpass -p password ssh user@ip bash test-automation.sh $RUNNER $TAG $ENV
            '''

            }
        }
    }
}
```


```Dockerfile
FROM openjdk:11 as build
ARG VERSION=3.6.3

WORKDIR /app
RUN wget https://downloads.apache.org/maven/maven-3/$VERSION/binaries/apache-maven-$VERSION-bin.zip
RUN unzip apache-maven-$VERSION-bin.zip
RUN rm -rf apache-maven-$VERSION-bin.zip
ENV MAVEN_HOME=/app/apache-maven-$VERSION
ENV PATH="$MAVEN_HOME/bin:$PATH"
COPY . .
RUN mvn clean install
RUN mvn test -Dtest=TEST_CASE "-Dkarate.options=--tags TAG_CASE" "-Dkarate.env=ENV_CASE"


FROM openjdk:11
WORKDIR /app
COPY --from=build /app/target/otp-service-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 9030
CMD ["java","-jar","app.jar"]
```



```sh
#!/usr/bin/env bash

REPOSITORYNAME=test-automation
BRANCHNAME=createOrder
TEST_CASE=$1
TAG_CASE=$2
ENV_CASE=$3

# Remove the existing directory

if [ -d "$REPOSITORYNAME" ]; then
    printf '%s\n' "Removing DIrectory ($REPOSITORYNAME)"
    rm -rf "$REPOSITORYNAME"
fi

# Clone the repository

git clone -b ${BRANCHNAME} git@github.com:repo-name/test-automation.git

# cd test-automation

sed -i 's/TEST_CASE/'$TEST_CASE'/g' Dockerfile
sed -i 's/TAG_CASE/'$TAG_CASE'/g' Dockerfile
sed -i 's/ENV_CASE/'$ENV_CASE'/g' Dockerfile

# docker build and update

docker-compose up --build -d



## bash test-automation.sh SanityTestRunner @notification dev
```


```yml
version: "3.6"
networks:
  backend-net:
    
services: 
  otp-service:
    image: test-automation
    container_name: test-automation_container
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "9030:9030"
    environment:
      MONGO_INITDB_DATABASE: user
      MONGO_INITDB_ROOT_USERNAME: user
    networks:
    - backend-net
    restart: unless-stopped
    volumes:
    - /data/backend-service-logs:/log
```
