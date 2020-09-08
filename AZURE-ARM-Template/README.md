[ARM-Template Reference](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/)
  
Ansible

  ---
    - hosts: localhost
      tasks:
    - name: Create Azure Resource Group deployment
      azure_rm_deployment:
        state: present
        resource_group_name: myResourceGroup
        name: myDeployment
        location: West Europe
        template: "{{ lookup('file', 'azuredeploy.json') }}"
        parameters:
          siteName:
            value: myWebApp
          hostingPlanName:
            value: myHostingPlan
          sku:
            value: Standard
            
Terraform

      resource "azurerm_template_deployment" "terraform-arm" {
      name                = "terraform-arm-01"
      resource_group_name = "MyResourceGroup"
      template_body       = file("resource.json")
      deployment_mode     = "Incremental"
    }




    https://azure.microsoft.com/en-in/resources/templates/101-logic-app-sendgrid/
    https://www.bruttin.com/2017/06/13/deploy-logic-app-with-arm.html



  Logic Connector 
  
    https://management.azure.com/subscriptions/1eccc4af-d37c-41ea-9978-5dafe23e5930/providers/Microsoft.Web/locations/eastus/managedApis/gmail?api-version=2016-06-01
    
     az login
     az account get-access-token
   
   
    # Find Access Token
    
   
    accessToken: "zzzz...xxxx"
   
    curl -X GET --header "Authorization: Bearer zzzz...xxxx" https://management.azure.com/subscriptions/1eccc4af-d37c-47ea-2978-5daf23e5930/providers/Microsoft.Web/locations/eastus/managedApis/gmail?api-version=2016-06-01
  
  
