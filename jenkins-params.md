```Jenkins
pipeline {
    agent any 
        parameters {
            choice(name: 'CHOICE', choices: ['SanityTestRunner', 'Two'], description: 'Pick test case option')
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
                VALUES_SH = "${params.CHOICE}"
            }

        steps {
            sh'''
	            sshpass -p password ssh paywalletdevops@35.225.43.162 bash test-automation.sh $VALUES_SH
            '''

            }
        }
    }
}
```
