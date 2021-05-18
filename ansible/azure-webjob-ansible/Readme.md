# Requirements

    pip install requests

    
[BearerToken](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/aad/service-prin-aad-token)


Shell Script 

    #!/usr/bin/env bash

    tenantID="xxxxxx"
    clientID="xxxxxx"
    clientSecret="xxxxxx"
    appServiceName="jinojs"
    folderPath="/home/sepoy/Documents/ansible/index.zip"
    data="grant_type=client_credentials&client_id=$clientID&resource=https://management.core.windows.net/&client_secret=$clientSecret"
    TOKEN=$(curl -X POST -d $data https://login.microsoftonline.com/$tenantID/oauth2/token | jq '.access_token' | sed 's/"//g')

    # curl -H "Authorization: Bearer " --data-binary @"/home/sepoy/Documents/ansible/index.zip" https://$appServiceName.scm.azurewebsites.net/api/zipdeploy
    curl -H "Authorization: Bearer ${TOKEN}" --data-binary @$folderPath https://$appServiceName.scm.azurewebsites.net/api/zipdeploy
