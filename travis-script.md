      
      
        sudo: required
        services:
          - docker
        env:
          global:
            - SHA=$(git rev-parse HEAD)
        before_install:
            - sudo apt update -qq && sudo apt install sshpass -y -qq
            - gem install bundler
            - echo "$dockerpassword" | docker login -u "$dockerusername" --password-stdin        
            - docker build -t $dockerusername/node-server:latest -f source/backend/Dockerfile source/backend/
            - docker push $dockerusername/node-server:latest
            - docker build -t $dockerusername/web-server:latest -f source/frontend/Dockerfile source/frontend/
            - docker push $dockerusername/web-server:latest
            - sshpass -p $sshpassword ssh -o StrictHostKeyChecking=no $username@$ipaddress 'bash custom.sh'
            - docker logout
        script:
            - echo "OH OH DONE"

        branches:
          only:
            - master
