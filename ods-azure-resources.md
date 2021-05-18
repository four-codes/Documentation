```json

{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "environmentName": {
            "type": "string",
            "defaultValue": "dev",
            "allowedValues": [ "dev", "qa", "stage", "prod" ],
            "metadata": {
                "description": "Enter your environment name"
            }
        },
        "createdBy": {
            "type": "string",
            "defaultValue": "j",
            "metadata": {
                "description": "Enter your name"
            }
        },

        "clientGroup": {
            "type": "string",
            "defaultValue": "if",
            "metadata": {
                "description": "Enter servicenow group names"
            }
        },

        "managedByGroup": {
            "type": "string",
            "defaultValue": "wbg",
            "metadata": {
                "description": "Enter servicenow group names"
            }
        },

        "project": {
            "type": "string",
            "defaultValue": "ods",
            "metadata": {
                "description": "Enter project name"
            }
        },

        "ioCode": {
            "type": "string",
            "defaultValue": "77",
            "metadata": {
                "description": "Enter IO code"
            }
        },
        "accreditationNumber": {
            "type": "string",
            "defaultValue": "12",
            "metadata": {
                "description": "Enter accreditationNumber code"
            }
        },
        "administratorLogin": {
            "type": "string",
            "defaultValue": "user",
            "metadata": {
                "description": "Enter administratorLogin number"
            }
        },
        "administratorLoginPassword": {
            "type": "string",
            "defaultValue": "Password@1234",
            "metadata": {
                "description": "Enter administratorLoginPassword number"
            }
        },
        "version": {
            "type": "string",
            "defaultValue": "12.0",
            "metadata": {
                "description": "Enter SQL version number"
            }
        }
    },
    "functions": [],
    "variables": {
        "sqlServerName": "[concat(parameters('project'), '-', parameters('environmentName'), '-sql')]",
        "sqlDatabaseName": "[concat(parameters('project'), '-', parameters('environmentName'), '-sqldb')]",
        "storageAccountName": "[concat(parameters('project'), parameters('environmentName'), 'str')]",
        "dataFactoryName": "[concat(parameters('project'), '-', parameters('environmentName'), '-adf')]"
    },
    "resources": [
        {
            "name": "[variables('sqlServerName')]",
            "type": "Microsoft.Sql/servers",
            "apiVersion": "2020-11-01-preview",
            "location": "[resourceGroup().location]",
            "tags": {
                "Created BY": "[parameters('createdBy')]",
                "Project": "[parameters('project')]",
                "Client Group": "[parameters('clientGroup')]",
                "Managed By Group": "[parameters('managedByGroup')]",
                "IO Code": "[parameters('ioCode')]",
                "Accreditation Number": "[parameters('accreditationNumber')]"
            },
            "properties": {
                "administratorLogin": "[parameters('administratorLogin')]",
                "administratorLoginPassword": "[parameters('administratorLoginPassword')]",
                "version": "[parameters('version')]"
            }
        },
        {
            "type": "Microsoft.Sql/servers/databases",
            "apiVersion": "2020-08-01-preview",
            "location": "[resourceGroup().location]",
            "tags": {
                "Created BY": "[parameters('createdBy')]",
                "Project": "[parameters('project')]",
                "Client Group": "[parameters('clientGroup')]",
                "Managed By Group": "[parameters('managedByGroup')]",
                "IO Code": "[parameters('ioCode')]",
                "Accreditation Number": "[parameters('accreditationNumber')]"
            },
            "name": "[concat(variables('sqlServerName'), '/', variables('sqlDatabaseName'))]",
            "sku": {
                "name": "Standard",
                "tier": "Standard",
                "capacity": "[if(equals(parameters('environmentName'),'prod'), 100, 50)]"
            }
        },
        {
            "name": "[variables('storageAccountName')]",
            "type": "Microsoft.Storage/storageAccounts",
            "apiVersion": "2019-06-01",
            "location": "[resourceGroup().location]",
            "tags": {
                "Created BY": "[parameters('createdBy')]",
                "Project": "[parameters('project')]",
                "Client Group": "[parameters('clientGroup')]",
                "Managed By Group": "[parameters('managedByGroup')]",
                "IO Code": "[parameters('ioCode')]",
                "Accreditation Number": "[parameters('accreditationNumber')]"
            },
            "properties": {
                "accessTier": "Hot",
                "minimumTlsVersion": "TLS1_2",
                "supportsHttpsTrafficOnly": true,
                "allowBlobPublicAccess": false,
                "allowSharedKeyAccess": true,
                "networkAcls": {
                    "bypass": "AzureServices",
                    "defaultAction": "Deny",
                    "ipRules": []
                },
                "isHnsEnabled": true
            },
            "dependsOn": [],
            "sku": {
                "name": "Standard_LRS"
            },
            "kind": "StorageV2"
        },
        {
            "apiVersion": "2018-06-01",
            "name": "[variables('dataFactoryName')]",
            "location": "[resourceGroup().location]",
            "tags": {
                "Created BY": "[parameters('createdBy')]",
                "Project": "[parameters('project')]",
                "Client Group": "[parameters('clientGroup')]",
                "Managed By Group": "[parameters('managedByGroup')]",
                "IO Code": "[parameters('ioCode')]",
                "Accreditation Number": "[parameters('accreditationNumber')]"
            },
            "type": "Microsoft.DataFactory/factories",
            "identity": {
                "type": "SystemAssigned"
            },
            "properties": {}
        }
    ],
    "outputs": {}
}

```
