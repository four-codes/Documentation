```yml

image:
  name: python:3.8


unit-test: &unit-test
  parallel:
    - step:
        name: Unit tests
        script:
          - pip install -r test/requirements.txt
          - python -m pytest --verbose --capture=no test/test_pipe_unit.py
          - flake8 --ignore E501,E125,F541
        services:
          - docker
    - step:
        name: Lint the Dockerfile
        image: hadolint/hadolint:latest-debian
        script:
          - hadolint Dockerfile


integration-test: &integration-test
  step:
    name: Integration tests
    script:
      - pip install -r test/requirements.txt
      - python -m pytest --verbose --capture=no test/test_pipe_integration.py
    services:
      - docker


release-dev: &release-dev
  step:
    name: Release development version
    trigger: manual
    image: python:3.7
    script:
      - pip install semversioner
      - VERSION=$(semversioner current-version).${BITBUCKET_BUILD_NUMBER}-dev
      - pipe: atlassian/bitbucket-pipe-release:4.0.1
        variables:
          DOCKERHUB_USERNAME: $DOCKERHUB_USERNAME
          DOCKERHUB_PASSWORD: $DOCKERHUB_PASSWORD
          IMAGE: bitbucketpipelines/$BITBUCKET_REPO_SLUG
          GIT_PUSH: 'false'
          VERSION: ${VERSION}
    services:
      - docker


push: &push
  step:
    name: Push and Tag
    image: python:3.7
    script:
      - pipe: atlassian/bitbucket-pipe-release:4.0.1
        variables:
          DOCKERHUB_USERNAME: $DOCKERHUB_USERNAME
          DOCKERHUB_PASSWORD: $DOCKERHUB_PASSWORD
          IMAGE: bitbucketpipelines/$BITBUCKET_REPO_SLUG
    services:
      - docker


pipelines:
  default:
    - <<: *unit-test
    - <<: *integration-test
    - <<: *release-dev
  branches:
    master:
      - <<: *unit-test
      - <<: *integration-test
      - <<: *push


```
