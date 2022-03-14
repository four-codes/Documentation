```Jenkinsfile
pipeline {
    agent any
    parameters {
        choice(name: 'GROUP_AND_REPO_NAME', choices: ['A', 'B', 'C'], description: '') 
        choice(name: 'SINCE', choices: ['1 month ago', '2 months ago', '3 months ago'], description: '')
     }

    stages {
        stage('CLEAN THE BRANCHES') {
            steps {
                sh '''
                    bash branch-deletion.sh ${params.GROUP_AND_REPO_NAME} ${params.SINCE}
                '''
            }
        }
    }












}
```
