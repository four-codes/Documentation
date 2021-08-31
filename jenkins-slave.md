```Dockerfile

# jenkins-slave:alpine - awscli 
FROM jenkins/slave:alpine
USER root
RUN apk upgrade
RUN apk add aws-cli
RUN aws --version
USER jenkins

```

```Dockerfile

# jenkins-slave:alpine - helm client
FROM jenkins/slave:alpine
ARG HELM_VERSION=3.6.3
USER root
RUN apk upgrade
RUN wget https://get.helm.sh/helm-v$HELM_VERSION-linux-amd64.tar.gz
RUN tar -zxvf helm-v$HELM_VERSION-linux-amd64.tar.gz
RUN mv linux-amd64/helm /usr/local/bin/
RUN rm -rf helm-v$HELM_VERSION-linux-amd64.tar.gz && rm -rf linux-amd64
RUN helm version 
USER jenkins

```


```Dockerfile

# jenkins-slave:alpine - terraform & terragrunt
FROM jenkins/slave:alpine
ARG TERRAFORM_VERSION=1.0.5
ARG TERRAGRUNT_VERSION=0.31.8
USER root
RUN apk upgrade
RUN wget "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip"
RUN unzip "terraform_${TERRAFORM_VERSION}_linux_amd64.zip"
RUN mv terraform /usr/local/bin/
RUN rm -rf "terraform_${TERRAFORM_VERSION}_linux_amd64.zip"
RUN terraform -version
RUN wget "https://github.com/gruntwork-io/terragrunt/releases/download/v${TERRAGRUNT_VERSION}/terragrunt_linux_amd64"
RUN mv terragrunt_linux_amd64 /usr/local/bin/terragrunt
RUN chmod +x  /usr/local/bin/terragrunt
RUN  terragrunt --version
USER jenkins

```
