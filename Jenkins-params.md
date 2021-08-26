```Jenkinsfile

def jobName = env.JOB_BASE_NAME

if (jobName == 'staging-deployment') {
    nameSpace = 'STAGE_NS'
} else if (jobName == 'production-deployment') {
    nameSpace = 'PROD_NS'        
} else {
    nameSpace = "unknown"
}


pipeline {
    agent any
    environment {
        AWS_ACCESS_KEY_ID = credentials('jenkins-aws-secret-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
        REGION = credentials('REGION')
        ECR_REPO = credentials('ECR_REPO')
        ECR_REPO_URL = credentials('ECR_REPO_URL')
        EKS_CLUTER_NAME = credentials('EKS_CLUTER_NAME')
        NAME_SPACE = credentials("${nameSpace}") 
        EMAIL_INFORM ='krishna.raj@tisteps.co;'
    }
    stages {
        stage('IMAGE BUILD') {
        steps {
            sh '''
                export BranchName=$( git rev-parse HEAD | xargs git name-rev | cut -d' ' -f2)
                git checkout ${BranchName}
                export IMAGE_NAME=api-$(git rev-parse --short HEAD)
                docker build -t $ECR_REPO:${IMAGE_NAME} -f Dockerfile .
            '''
            }
        }
        stage('IMAGE PUSH') {
        steps {
            sh '''
                export IMAGE_NAME=api-$(git rev-parse --short HEAD)
                aws configure set region $REGION
                $(aws ecr get-login --region $REGION --no-include-email)
                docker push $ECR_REPO:$IMAGE_NAME
                docker logout $ECR_REPO_URL
                docker rmi $ECR_REPO:$IMAGE_NAME
            '''
            }
        }
    stage('DEPLOYMENT') {
        steps {
            sh '''
                export IMAGE_NAME=api-$(git rev-parse --short HEAD)
                export imageNameandversion=$ECR_REPO:$IMAGE_NAME
                sed -i "s|containerImageName|$imageNameandversion|" kube-deployment/api-server.yml
                sed -i "s|containerImageName|$imageNameandversion|" kube-deployment/worker.yml
                aws eks --region $REGION update-kubeconfig --name $EKS_CLUTER_NAME
                /usr/local/bin/kubectl apply -f kube-deployment/ -n ${NAME_SPACE}
                unset imageNameandversion
                unset IMAGE_NAME
                unset BranchName
            '''
            }
        }
    stage('WORKSPACE CLEAN'){
        steps{
                cleanWs()
            }
        }
    }
    
    post {
        success {  
            emailext body: 'Check console output at $BUILD_URL to view the results.', 
                to: "${EMAIL_INFORM}", 
                subject: 'SUCCESS KUBERNETES DEPLOYMENT - $PROJECT_NAME - #$BUILD_NUMBER'
        }
        failure {
            emailext body: 'Check console output at $BUILD_URL to view the results.', 
                    to: "${EMAIL_INFORM}", 
                    subject: 'FAILURE KUBERNETES DEPLOYMENT - $PROJECT_NAME - #$BUILD_NUMBER'
        }
    }
}


```
