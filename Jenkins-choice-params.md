```Jenkinsfile
pipeline {
    agent any
    environment {
        REPO_USERNAME = credentials('git-username')
        REPO_TOKEN = credentials('git-token')
    }
    parameters {
        choice(name: 'GROUP_AND_REPO_NAME', choices: ['A', 'B', 'C'], description: '') 
        choice(name: 'SINCE', choices: ['1 month ago', '2 months ago', '3 months ago'], description: '')
     }

    stages {
        stage('CLEAN THE BRANCHES') {
           environment {
                REPOSITORY = "${params.GROUP_AND_REPO_NAME}"
                DURATION = "${params.SINCE}"
            }
            steps {
                sh '''
                    bash branch-deletion.sh ${REPOSITORY} ${DURATION} ${REPO_USERNAME} ${REPO_TOKEN}
                '''
            }
        }
    }
    post {
        always {
            cleanws()
        }
    }

}
```
