sonar-scanner installation

```bash
wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.2.0.1873-linux.zip
unzip sonar-scanner-cli-4.2.0.1873-linux.zip
mv sonar-scanner-4.2.0.1873-linux /opt/sonar-scanner
sudo mv sonar-scanner-4.2.0.1873-linux /opt/sonar-scanner
export PATH=$PATH:/opt/sonar-scanner/bin
```

```Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Code Quality') {
        steps {
            sh '''
                export PATH=$PATH:/opt/sonar-scanner/bin
                sonar-scanner \
                    -Dsonar.projectKey=demo \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://35.172.236.123:9000 \
                    -Dsonar.login=sqp_d22a74f08467d7b552d06760e65ea6bfc000181a
                '''
            }
        }
    }    
}
```
