```bash
pipeline {
agent {label 'slave3'}

    stages {
        stage('ENV') {
            steps {
                echo bat(returnStdout: true, script: 'set')
            }
        }
        stage('TEST CASES') {
            steps {
                echo bat(returnStdout: true, script: 'mvn test')
            }
        }
    }
}
```
