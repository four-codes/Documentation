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
	            sshpass -p password ssh user@ip bash test-automation.sh $VALUES_SH
            '''

            }
        }
    }
}
```
