[Documentation](https://www.oracle.com/webfolder/technetwork/tutorials/obe/oci/registry/index.html)



```jenkinsfile

pipeline {
    agent any 
    environment {
        REPOSITORY_NAME="fra.ocir.io"
        OCR_NAME="xxxx-staging"
        IMAGE_NAME="node-api"
        NAMESPACE=credentials('ocr-tscout-staging-namespace')
        USERNAME=credentials('ocr-tscout-staging-username')
        PASSWORD=credentials('ocr-tscout-staging-password')
    }
    stages {
      stage('docker build') {   
        steps {
            sh'''
              docker build -t ${REPOSITORY_NAME}/${NAMESPACE}/${OCR_NAME}:${IMAGE_NAME}-${BUILD_ID} .
            '''
        }
      }
      
      stage('Docker image push') {   
        steps {
            sh'''
              RUNTIME_PASSWORD=${NAMESPACE}/${USERNAME}
              echo ${PASSWORD} | docker login ${REPOSITORY_NAME} --username  $RUNTIME_PASSWORD --password-stdin
              docker push ${REPOSITORY_NAME}/${NAMESPACE}/${OCR_NAME}:${IMAGE_NAME}-${BUILD_ID}
              docker logout ${REPOSITORY_NAME}
            '''
        }
      }
      stage('Delete last build docker image') {   
        steps {
            sh'''
              docker rmi ${REPOSITORY_NAME}/${NAMESPACE}/${OCR_NAME}:${IMAGE_NAME}-${BUILD_ID}
            '''
        }
      }
  }
}


```
