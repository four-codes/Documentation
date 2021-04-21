------------

    name: Build and Deploy to GraphQL Gateway

    on:
      pull_request:
        types: [labeled]
      push:
        branches:
          - 'master'

    env:
      GITHUB_SHA: ${{ github.sha }}
      IMAGE: ${{ secrets.IMAGE }}
      GKE_IMAGE_PROJECT: ${{ secrets.GKE_STAGING_PROJECT }}
      GKE_IMAGE_PROJECT_KEY: ${{ secrets.GKE_STAGING_PROJECT_KEY }}
      GKE_IMAGE_PROJECT_EMAIL: ${{ secrets.GKE_STAGING_EMAIL }}
      REGISTRY_HOSTNAME: gcr.io

    jobs:
      deploy:
        name: Setup, Test, Build, Deploy, Notify
        if: github.event_name == 'push' || github.event.label.name == 'dev-sandbox-1' || github.event.label.name == 'prep' || github.event.label.name == 'staging' || github.event.label.name == 'prod'
        runs-on: ubuntu-latest
        steps:
          - name: Checkout
            uses: actions/checkout@v2

          ############## dev-sandbox-1 ##############
          - name: Set environment variables for dev-sandbox-1
            if: github.event.label.name == 'dev-sandbox-1'
            run: |
              echo "DEPLOYMENT_ENVIRONMENT=dev-sandbox-1" >> $GITHUB_ENV
              echo "GKE_PROJECT_CREDENTIALS=${{ secrets.dev_sandbox_1_google_service_account_key }}" >> $GITHUB_ENV
              echo "GKE_ZONE=${{ secrets.dev_sandbox_1_zone }}" >> $GITHUB_ENV
              echo "GKE_CLUSTER=${{ secrets.dev_sandbox_1_gke_cluster }}" >> $GITHUB_ENV
              echo "SLACK_WEBHOOK_URL=${{ secrets.dev_sandbox_1_slack_webhook_url }}" >> $GITHUB_ENV
          ############## prep ##############
          - name: Set environment variables for prep
            if: github.event.label.name == 'prep'
            run: |
              echo "DEPLOYMENT_ENVIRONMENT=prep" >> $GITHUB_ENV
              echo "GKE_PROJECT_CREDENTIALS=${{ secrets.prep_google_service_account_key }}" >> $GITHUB_ENV
              echo "GKE_ZONE=${{ secrets.prep_zone }}" >> $GITHUB_ENV
              echo "GKE_CLUSTER=${{ secrets.prep_gke_cluster }}" >> $GITHUB_ENV
              echo "SLACK_WEBHOOK_URL=${{ secrets.prep_slack_webhook_url }}" >> $GITHUB_ENV
          ############## staging ##############
          - name: Set environment variables for staging
            if: github.event.label.name == 'staging'
            run: |
              echo "DEPLOYMENT_ENVIRONMENT=staging" >> $GITHUB_ENV
              echo "GKE_PROJECT_CREDENTIALS=${{ secrets.staging_google_service_account_key }}" >> $GITHUB_ENV
              echo "GKE_ZONE=${{ secrets.staging_zone }}" >> $GITHUB_ENV
              echo "GKE_CLUSTER=${{ secrets.staging_gke_cluster }}" >> $GITHUB_ENV
              echo "SLACK_WEBHOOK_URL=${{ secrets.staging_slack_webhook_url }}" >> $GITHUB_ENV
          ############## prod ##############
          - name: Set environment variables for prod
            if: github.event.label.name == 'prod' || github.event_name == 'push'
            run: |
              echo "DEPLOYMENT_ENVIRONMENT=prod" >> $GITHUB_ENV
              echo "GKE_PROJECT_CREDENTIALS=${{ secrets.prod_google_service_account_key }}" >> $GITHUB_ENV
              echo "GKE_ZONE=${{ secrets.prod_zone }}" >> $GITHUB_ENV
              echo "GKE_CLUSTER=${{ secrets.prod_gke_cluster }}" >> $GITHUB_ENV
              echo "SLACK_WEBHOOK_URL=${{ secrets.prod_slack_webhook_url }}" >> $GITHUB_ENV
          # Setup gcloud CLI - Staging Creds for image access
          - name: Initialize GCloud
            uses: GoogleCloudPlatform/github-actions/setup-gcloud@master
            with:
              version: "290.0.1"
              service_account_email: ${{ env.GKE_IMAGE_PROJECT_EMAIL }}
              service_account_key: ${{ env.GKE_IMAGE_PROJECT_KEY }}

          # Configure docker to use the gcloud command-line tool as a credential helper
          # Set up docker to authenticate
          # via gcloud command-line tool.
          - name: "Configure docker to use GCloud CLI"
            run: |
              gcloud auth configure-docker
          # Build the Docker image
          - name: Build
            run: |
              docker build -t $REGISTRY_HOSTNAME/$GKE_IMAGE_PROJECT/$IMAGE:$GITHUB_SHA \
                -t $REGISTRY_HOSTNAME/$GKE_IMAGE_PROJECT/$IMAGE:$DEPLOYMENT_ENVIRONMENT \
                --build-arg GITHUB_SHA=$GITHUB_SHA \
                --build-arg GITHUB_REF=$GITHUB_REF .
          # Push the Docker image to Google Container Registry
          # REF: https://github.com/docker/cli/issues/267
          # Cannot Publish with multiple tags
          - name: Publish
            run: |
              docker push $REGISTRY_HOSTNAME/$GKE_IMAGE_PROJECT/$IMAGE:$GITHUB_SHA
              docker push $REGISTRY_HOSTNAME/$GKE_IMAGE_PROJECT/$IMAGE:$DEPLOYMENT_ENVIRONMENT
          # INFO(105): jq .project_id google-credentials.json -r to eliminate quotes in the output
          - name: Setup Additional ENV
            run: |
              echo $GKE_PROJECT_CREDENTIALS | base64 --decode >> google-credentials.json
              echo "GKE_PROJECT=$(jq .project_id google-credentials.json -r)" >> $GITHUB_ENV
          - name: Remove GKE_PROJECT_CREDENTIALS
            run: |
              rm google-credentials.json
          # Reinitialize with dev project creds because kustomize needs to work on dev.
          - name: Initialize GCloud For Dev Project
            uses: GoogleCloudPlatform/github-actions/setup-gcloud@master
            with:
              version: "290.0.1"
              service_account_key: ${{ env.GKE_PROJECT_CREDENTIALS }}

          # Set up kustomize
          - name: Set up Kustomize
            run: |
              cd deployments/$DEPLOYMENT_ENVIRONMENT
              curl -o kustomize --location https://github.com/kubernetes-sigs/kustomize/releases/download/v3.1.0/kustomize_3.1.0_linux_amd64
              chmod u+x ./kustomize
          # Deploy the Docker image to the GKE cluster
          - name: Deploy
            run: |
              cd deployments/$DEPLOYMENT_ENVIRONMENT
              gcloud container clusters get-credentials $GKE_CLUSTER --zone $GKE_ZONE --project $GKE_PROJECT
              ./kustomize edit set image $REGISTRY_HOSTNAME/$GKE_IMAGE_PROJECT/$IMAGE:$GITHUB_SHA
              ./kustomize build . | kubectl apply -f -
          - name: Deploy Success Notification to Slack Channel
            uses: 8398a7/action-slack@v2
            with:
              status: ${{ job.status }}
              text: ":rocket: [${{env.DEPLOYMENT_ENVIRONMENT}}] XSEED Gateway deployment Succeeded"
              fields: repo,message,commit,author,action,eventName,ref,workflow,job,took

          - name: Fallback - Failure Notification to Slack Channel
            if: failure()
            uses: 8398a7/action-slack@v2
            with:
              status: ${{ job.status }}
              text: ":no_entry_sign: [${{env.DEPLOYMENT_ENVIRONMENT}}] XSEED Gateway deployment Failed"
              fields: repo,message,commit,author,action,eventName,ref,workflow,job,took
          
 ------------
