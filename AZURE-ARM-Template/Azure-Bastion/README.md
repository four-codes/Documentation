# ARM-Template

Bastion

    Requirements:

      minimum needed resource group with location

      Resource Group Name: ExampleGroup
  
  
  
Command:

    az group create --name ExampleGroup  --location "East US"

    az deployment group create --resource-group ExampleGroup --template-file azuredeploy.json --parameters azuredeploy.parameters.json
  
