```json

{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environmentName": {
      "type": "string",
      "defaultValue": "dev",
      "allowedValues": ["dev", "qa", "stage", "prod"],
      "metadata": {
        "description": "Enter your environment name"
      }
    },

    "clientId": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Specifies the client id for aks."
      }
    },

    "clientSecret": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Specifies the client secret for aks."
      }
    },
    "resourceSPObjectID": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Specify the aks service principal object ID"
      }
    },
    "webApiSPObjectID": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Specify the web api service principal object ID"
      }
    },

    "tenantID": {
      "defaultValue": "",
      "type": "string",
      "metadata": {
        "description": "Specifies the tenant id of the Azure Active Directory used by the AKS cluster for authentication."
      }
    },
    "subscriptionID": {
      "defaultValue": "",
      "type": "string",
      "metadata": {
        "description": "Specifies the tenant id of the Azure Active Directory used by the AKS cluster for authentication."
      }
    },

    "aksAdminGroupObjectID": {
      "defaultValue": [""],
      "type": "array",
      "metadata": {
        "description": "Specifies the AAD group object IDs that will have admin role of the cluster."
      }
    },

    "virtual-network-appgateway-ip-address": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Enter a network appgateway private address space"
      }
    },

    "aksClusterServiceCidr": {
      "defaultValue": "",
      "type": "string",
      "metadata": {
        "description": "A CIDR notation IP range from which to assign service cluster IPs. It must not overlap with any Subnet IP ranges."
      }
    },

    "aksClusterDnsServiceIP": {
      "defaultValue": "",
      "type": "string",
      "metadata": {
        "description": "Specifies the IP address assigned to the Kubernetes DNS service. It must be within the Kubernetes service address range specified in serviceCidr."
      }
    },

    "logAnalyticsSku": {
      "type": "string",
      "allowedValues": ["Free", "Standalone", "PerNode", "PerGB2018"],
      "defaultValue": "PerGB2018",
      "metadata": {
        "description": "Specifies the service tier of the workspace: Free, Standalone, PerNode, Per-GB."
      }
    },

    "aksClusterKubernetesVersion": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Specifies the version of Kubernetes specified when creating the managed cluster."
      }
    },

    "nodePoolVmSize": {
      "defaultValue": "Standard_DS3_v2",
      "type": "string",
      "metadata": {
        "description": "Specifies the vm size of nodes in the node pool."
      }
    },

    "nodePoolOsDiskSizeGB": {
      "defaultValue": 100,
      "type": "int",
      "metadata": {
        "description": "Specifies the OS Disk Size in GB to be used to specify the disk size for every machine in this master/agent pool. If you specify 0, it will apply the default osDisk size according to the vmSize specified.."
      }
    },

    "nodePoolVmCount": {
      "defaultValue": 1,
      "type": "int",
      "metadata": {
        "description": "Specifies the number of instance"
      }
    },

    "aksClusterAdminUsername": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Specifies the administrator username of Linux virtual machines."
      }
    },

    "aksClusterSshPublicKey": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Specifies the SSH RSA public key string for the Linux nodes."
      }
    },

    "psqlUserName": {
      "type": "string",
      "defaultValue": "pgadmin",
      "metadata": {
        "description": "Specifies the administrator username of Linux virtual machines."
      }
    },

    "psqlPassword": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Specifies the SSH RSA public key string for the Linux nodes."
      }
    },

    "createdBy": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Enter your name"
      }
    },

    "clientGroup": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Enter servicenow group names"
      }
    },

    "managedByGroup": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Enter servicenow group names"
      }
    },

    "project": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Enter project name"
      }
    },

    "ioCode": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Enter IO code"
      }
    },

    "accreditationNumber": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Enter Accreditation number"
      }
    },

    "networking-resourceGroup": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Enter networking resources group"
      }
    },

    "networking-vnetName": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Enter networking vnet Name"
      }
    },

    "networking-apgSubnet": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Enter networking app gateway Subnet"
      }
    },

    "networking-aksSubnet": {
      "type": "string",
      "defaultValue": "",
      "metadata": {
        "description": "Enter networking AKS Subnet"
      }
    }
  },

  "functions": [],
  "variables": {
    "applicationGatewayName": "[concat(parameters('project'), '-', parameters('environmentName'), '-alb')]",
    "aksClusterName": "[concat(parameters('project'), '-', parameters('environmentName'), '-aks')]",
    "aksnodeResourceGroup": "[concat(parameters('project'), '-', parameters('environmentName'), '-aks-node-rg')]",
    "nodePoolName": "[concat('miga', parameters('environmentName'))]",
    "psql-service-name": "[concat(parameters('project'), '-', parameters('environmentName'), '-psql')]",
    "KeyVaultName": "[concat(parameters('project'), '-', parameters('environmentName'), '-kv' )]",
    "serviceBusName": "[concat(parameters('project'), '-', parameters('environmentName'), '-sb1' )]",
    "logAnalyticsWorkspaceName": "[concat(parameters('project'), '-', parameters('environmentName'),'-log')]",
    "appInsightsName": "[concat(parameters('project'), '-', parameters('environmentName'), '-appi')]",
    "cosmosdbName": "[concat(parameters('project'), '-', parameters('environmentName'),'-cosmos')]",
    "acrName": "[concat(parameters('project'), parameters('environmentName'),'acr')]",
    "appgatewaypublicipname": "[concat(parameters('project'), '-', parameters('environmentName'),'-lbe' )]",
    "storageAccountName": "[concat(parameters('project'), parameters('environmentName'),'strg')]",
    "applicationGatewayId": "[resourceId('Microsoft.Network/applicationGateways', variables('applicationGatewayName'))]",
    "logAnalyticsWorkspaceResourceID": "[resourceId('Microsoft.OperationalInsights/workspaces/', variables('logAnalyticsWorkspaceName'))]",
    "identityName": "[concat(parameters('project'),parameters('environmentName'), '-id' )]",
    "identityID": "[resourceId('Microsoft.ManagedIdentity/userAssignedIdentities', variables('identityName'))]",
    "kubernetesSubnetID": "[concat('/subscriptions/',parameters('subscriptionID'),'/resourceGroups/',parameters('networking-resourceGroup'),'/providers/Microsoft.Network/virtualNetworks/',parameters('networking-vnetName'),'/subnets/',parameters('networking-aksSubnet'))]",
    "appGateWaySubnetID": "[concat('/subscriptions/',parameters('subscriptionID'),'/resourceGroups/',parameters('networking-resourceGroup'),'/providers/Microsoft.Network/virtualNetworks/',parameters('networking-vnetName'),'/subnets/',parameters('networking-apgSubnet'))]",
    "networkDeploymentName": "[concat('network-section-',parameters('environmentName'))]"
  },
  "resources": [
    {
      "type": "Microsoft.OperationalInsights/workspaces",
      "apiVersion": "2020-03-01-preview",
      "name": "[variables('logAnalyticsWorkspaceName')]",
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
        "sku": {
          "name": "[parameters('logAnalyticsSku')]"
        },
        "retentionInDays": 120,
        "features": {
          "searchVersion": 1,
          "legacy": 0,
          "enableLogAccessUsingOnlyResourcePermissions": true
        }
      }
    },
    {
      "name": "[variables('appInsightsName')]",
      "type": "Microsoft.Insights/components",
      "apiVersion": "2020-02-02-preview",
      "dependsOn": [
        "[resourceId('Microsoft.OperationalInsights/workspaces', variables('logAnalyticsWorkspaceName'))]"
      ],
      "tags": {
        "Created BY": "[parameters('createdBy')]",
        "Project": "[parameters('project')]",
        "Client Group": "[parameters('clientGroup')]",
        "Managed By Group": "[parameters('managedByGroup')]",
        "IO Code": "[parameters('ioCode')]",
        "Accreditation Number": "[parameters('accreditationNumber')]"
      },
      "location": "[resourceGroup().location]",
      "properties": {
        "Application_Type": "web",
        "WorkspaceResourceId": "[variables('logAnalyticsWorkspaceResourceID')]",
        "Flow_Type": "Redfield",
        "Request_Source": "rest"
      }
    },
    {
      "type": "Microsoft.Insights/components/providers/diagnosticSettings",
      "apiVersion": "2017-05-01-preview",
      "name": "[concat(variables('appInsightsName'), '/Microsoft.Insights/', 'diagnosticsettings')]",
      "dependsOn": [
        "[resourceId('Microsoft.Insights/components', variables('appInsightsName'))]"
      ],
      "properties": {
        "workspaceId": "[variables('logAnalyticsWorkspaceResourceID')]",
        "logs": [
          {
            "category": "AppAvailabilityResults",
            "enabled": true
          },
          {
            "category": "AppBrowserTimings",
            "enabled": true
          },
          {
            "category": "AppEvents",
            "enabled": true
          },
          {
            "category": "AppMetrics",
            "enabled": true
          },
          {
            "category": "AppDependencies",
            "enabled": true
          },
          {
            "category": "AppExceptions",
            "enabled": true
          },
          {
            "category": "AppPageViews",
            "enabled": true
          },
          {
            "category": "AppPerformanceCounters",
            "enabled": true
          },
          {
            "category": "AppRequests",
            "enabled": true
          },
          {
            "category": "AppSystemEvents",
            "enabled": true
          },
          {
            "category": "AppTraces",
            "enabled": true
          }
        ],
        "metrics": [
          {
            "category": "AllMetrics",
            "enabled": true
          }
        ]
      }
    },
    {
      "name": "[variables('psql-service-name')]",
      "type": "Microsoft.DBforPostgreSQL/servers",
      "dependsOn": [
        "[resourceId('Microsoft.Insights/components', variables('appInsightsName'))]"
      ],
      "apiVersion": "2017-12-01",
      "identity": {
        "type": "SystemAssigned"
      },
      "sku": {
        "name": "GP_Gen5_4",
        "tier": "GeneralPurpose",
        "family": "Gen5",
        "capacity": 4
      },
      "properties": {
        "version": "11",
        "sslEnforcement": "Enabled",
        "minimalTlsVersion": "TLS1_2",
        "infrastructureEncryption": "Enabled",
        "publicNetworkAccess": "Enabled",
        "createMode": "Default",
        "administratorLogin": "[parameters('psqlUserName')]",
        "administratorLoginPassword": "[parameters('psqlPassword')]",
        "storageProfile": {
          "storageMB": "[if(equals(parameters('environmentName'),'prod'), 102400, 51200)]",
          "backupRetentionDays": "[if(equals(parameters('environmentName'),'prod'), 180, 30)]",
          "geoRedundantBackup": "Disabled",
          "storageAutogrow": "Enabled"
        }
      },
      "location": "[resourceGroup().location]",
      "tags": {
        "Created BY": "[parameters('createdBy')]",
        "Project": "[parameters('project')]",
        "Client Group": "[parameters('clientGroup')]",
        "Managed By Group": "[parameters('managedByGroup')]",
        "IO Code": "[parameters('ioCode')]",
        "Accreditation Number": "[parameters('accreditationNumber')]"
      },
      "resources": []
    },
    {
      "name": "[concat(variables('psql-service-name'), '/networks')]",
      "type": "Microsoft.DBforPostgreSQL/servers/virtualNetworkRules",
      "apiVersion": "2017-12-01",
      "dependsOn": [
        "[resourceId('Microsoft.DBforPostgreSQL/servers', variables('psql-service-name'))]"
      ],
      "properties": {
        "virtualNetworkSubnetId": "[variables('kubernetesSubnetID')]",
        "ignoreMissingVnetServiceEndpoint": true
      }
    },
    {
      "name": "[concat(variables('psql-service-name'), '/pg_qs.query_capture_mode')]",
      "type": "Microsoft.DBforPostgreSQL/servers/configurations",
      "apiVersion": "2017-12-01",
      "properties": {
        "value": "TOP",
        "source": "user-override"
      },
      "dependsOn": [
        "[resourceId('Microsoft.DBforPostgreSQL/servers', variables('psql-service-name'))]"
      ]
    },
    {
      "name": "[concat(variables('psql-service-name'), '/pgms_wait_sampling.query_capture_mode')]",
      "type": "Microsoft.DBforPostgreSQL/servers/configurations",
      "apiVersion": "2017-12-01",
      "properties": {
        "value": "ALL",
        "source": "user-override"
      },
      "dependsOn": [
        "[resourceId('Microsoft.DBforPostgreSQL/servers', variables('psql-service-name'))]"
      ]
    },
    {
      "type": "Microsoft.DBforPostgreSQL/servers/providers/diagnosticSettings",
      "apiVersion": "2017-05-01-preview",
      "name": "[concat(variables('psql-service-name'), '/Microsoft.Insights/', 'diagnosticsettings')]",
      "dependsOn": [
        "[resourceId('Microsoft.DBforPostgreSQL/servers', variables('psql-service-name'))]"
      ],
      "properties": {
        "workspaceId": "[variables('logAnalyticsWorkspaceResourceID')]",
        "logs": [
          {
            "category": "PostgreSQLLogs",
            "enabled": true
          },
          {
            "category": "QueryStoreRuntimeStatistics",
            "enabled": true
          },
          {
            "category": "QueryStoreWaitStatistics",
            "enabled": true
          }
        ],
        "metrics": [
          {
            "category": "AllMetrics",
            "enabled": true
          }
        ]
      }
    },
    {
      "type": "Microsoft.Network/privateEndpoints",
      "apiVersion": "2020-05-01",
      "name": "[variables('psql-service-name')]",
      "location": "[resourceGroup().location]",
      "tags": {
        "Created BY": "[parameters('createdBy')]",
        "Project": "[parameters('project')]",
        "Client Group": "[parameters('clientGroup')]",
        "Managed By Group": "[parameters('managedByGroup')]",
        "IO Code": "[parameters('ioCode')]",
        "Accreditation Number": "[parameters('accreditationNumber')]"
      },
      "dependsOn": [
        "[resourceId('Microsoft.DBforPostgreSQL/servers', variables('psql-service-name'))]"
      ],
      "properties": {
        "privateLinkServiceConnections": [
          {
            "name": "[concat(variables('psql-service-name'), substring(uniqueString(resourceGroup().id),0,6))]",
            "properties": {
              "privateLinkServiceId": "[resourceId('Microsoft.DBforPostgreSQL/servers', variables('psql-service-name'))]",
              "groupIds": ["postgresqlServer"],
              "privateLinkServiceConnectionState": {
                "status": "Approved",
                "description": "Auto-Approved",
                "actionsRequired": "None"
              }
            }
          }
        ],
        "manualPrivateLinkServiceConnections": [],
        "subnet": {
          "id": "[variables('kubernetesSubnetID')]"
        },
        "customDnsConfigs": []
      }
    },
    {
      "name": "[variables('serviceBusName')]",
      "type": "Microsoft.ServiceBus/namespaces",
      "apiVersion": "2017-04-01",
      "dependsOn": [
        "[resourceId('Microsoft.DBforPostgreSQL/servers', variables('psql-service-name'))]"
      ],
      "location": "[resourceGroup().location]",
      "tags": {
        "Created BY": "[parameters('createdBy')]",
        "Project": "[parameters('project')]",
        "Client Group": "[parameters('clientGroup')]",
        "Managed By Group": "[parameters('managedByGroup')]",
        "IO Code": "[parameters('ioCode')]",
        "Accreditation Number": "[parameters('accreditationNumber')]"
      },
      "sku": {
        "name": "Premium",
        "tier": "Premium",
        "capacity": 1
      },
      "properties": {
        "zoneRedundant": false
      },
      "resources": []
    },
    {
      "type": "Microsoft.ServiceBus/namespaces/AuthorizationRules",
      "apiVersion": "2017-04-01",
      "name": "[concat(variables('serviceBusName'), '/RootManageSharedAccessKey')]",
      "dependsOn": [
        "[resourceId('Microsoft.ServiceBus/namespaces', variables('serviceBusName'))]"
      ],
      "location": "[resourceGroup().location]",
      "properties": {
        "rights": ["Listen", "Manage", "Send"]
      }
    },
    {
      "type": "Microsoft.ServiceBus/namespaces/networkRuleSets",
      "apiVersion": "2018-01-01-preview",
      "name": "[concat(variables('serviceBusName'), '/default')]",
      "location": "[resourceGroup().location]",
      "dependsOn": [
        "[resourceId('Microsoft.ServiceBus/namespaces', variables('serviceBusName'))]"
      ],
      "properties": {
        "defaultAction": "Deny",
        "virtualNetworkRules": [
          {
            "subnet": {
              "id": "[variables('kubernetesSubnetID')]"
            },
            "ignoreMissingVnetServiceEndpoint": false
          }
        ],
        "ipRules": []
      }
    },
    {
      "type": "Microsoft.ServiceBus/namespaces/providers/diagnosticSettings",
      "apiVersion": "2017-05-01-preview",
      "name": "[concat(variables('serviceBusName'), '/Microsoft.Insights/', 'diagnosticsettings')]",
      "dependsOn": [
        "[resourceId('Microsoft.ServiceBus/namespaces', variables('serviceBusName'))]"
      ],
      "properties": {
        "workspaceId": "[variables('logAnalyticsWorkspaceResourceID')]",
        "logs": [
          {
            "category": "OperationalLogs",
            "enabled": true
          }
        ],
        "metrics": [
          {
            "category": "AllMetrics",
            "enabled": true
          }
        ]
      }
    },
    {
      "type": "Microsoft.ServiceBus/namespaces/queues",
      "apiVersion": "2018-01-01-preview",
      "name": "[concat(variables('serviceBusName'), '/miga-servicebus-queue')]",
      "location": "[resourceGroup().location]",
      "dependsOn": [
        "[resourceId('Microsoft.ServiceBus/namespaces', variables('serviceBusName'))]"
      ],
      "properties": {
        "lockDuration": "PT30S",
        "maxSizeInMegabytes": 1024,
        "requiresDuplicateDetection": false,
        "requiresSession": false,
        "defaultMessageTimeToLive": "P14D",
        "deadLetteringOnMessageExpiration": false,
        "enableBatchedOperations": true,
        "duplicateDetectionHistoryTimeWindow": "PT10M",
        "maxDeliveryCount": 10,
        "status": "Active",
        "autoDeleteOnIdle": "P10675199DT2H48M5.4775807S",
        "enablePartitioning": false,
        "enableExpress": false
      }
    },
    {
      "type": "Microsoft.ServiceBus/namespaces/topics",
      "apiVersion": "2018-01-01-preview",
      "name": "[concat(variables('serviceBusName'), '/miga-servicebus-topic')]",
      "location": "[resourceGroup().location]",
      "dependsOn": [
        "[resourceId('Microsoft.ServiceBus/namespaces', variables('serviceBusName'))]"
      ],
      "properties": {
        "defaultMessageTimeToLive": "P14D",
        "maxSizeInMegabytes": 1024,
        "requiresDuplicateDetection": false,
        "duplicateDetectionHistoryTimeWindow": "PT10M",
        "enableBatchedOperations": true,
        "status": "Active",
        "supportOrdering": true,
        "autoDeleteOnIdle": "P10675199DT2H48M5.4775807S",
        "enablePartitioning": false,
        "enableExpress": false
      }
    },
    {
      "type": "Microsoft.ServiceBus/namespaces/topics/subscriptions",
      "apiVersion": "2018-01-01-preview",
      "name": "[concat(variables('serviceBusName'), '/miga-servicebus-topic/miga-sb-crr-subscription')]",
      "location": "East US",
      "dependsOn": [
        "[resourceId('Microsoft.ServiceBus/namespaces/topics', variables('serviceBusName'), 'miga-servicebus-topic')]",
        "[resourceId('Microsoft.ServiceBus/namespaces', variables('serviceBusName'))]"
      ],
      "properties": {
        "lockDuration": "PT30S",
        "requiresSession": false,
        "defaultMessageTimeToLive": "P14D",
        "deadLetteringOnMessageExpiration": false,
        "deadLetteringOnFilterEvaluationExceptions": false,
        "maxDeliveryCount": 10,
        "status": "Active",
        "enableBatchedOperations": true,
        "autoDeleteOnIdle": "P14D"
      }
    },
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2019-06-01",
      "name": "[variables('storageAccountName')]",
      "dependsOn": [
        "[resourceId('Microsoft.ServiceBus/namespaces', variables('serviceBusName'))]"
      ],
      "tags": {
        "Created BY": "[parameters('createdBy')]",
        "Project": "[parameters('project')]",
        "Client Group": "[parameters('clientGroup')]",
        "Managed By Group": "[parameters('managedByGroup')]",
        "IO Code": "[parameters('ioCode')]",
        "Accreditation Number": "[parameters('accreditationNumber')]"
      },
      "location": "[resourceGroup().location]",
      "sku": {
        "name": "Standard_LRS",
        "tier": "Standard"
      },
      "kind": "StorageV2",
      "properties": {
        "minimumTlsVersion": "TLS1_2",
        "allowBlobPublicAccess": false,
        "networkAcls": {
          "bypass": "AzureServices",
          "virtualNetworkRules": [
            {
              "id": "[variables('kubernetesSubnetID')]",
              "action": "Allow",
              "state": "Succeeded"
            }
          ],
          "ipRules": [],
          "defaultAction": "Deny"
        },
        "supportsHttpsTrafficOnly": true,
        "encryption": {
          "services": {
            "file": {
              "keyType": "Account",
              "enabled": true
            },
            "blob": {
              "keyType": "Account",
              "enabled": true
            }
          },
          "keySource": "Microsoft.Storage"
        },
        "accessTier": "Hot"
      }
    },
    {
      "type": "Microsoft.Storage/storageAccounts/blobServices/containers",
      "apiVersion": "2020-08-01-preview",
      "name": "[concat(variables('storageAccountName'), '/default/', 'miga-storage-ac-blob')]",
      "dependsOn": [
        "[resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName'))]"
      ],
      "properties": {
        "defaultEncryptionScope": "$account-encryption-key",
        "denyEncryptionScopeOverride": false,
        "publicAccess": "None"
      }
    },
    {
      "type": "Microsoft.Storage/storageAccounts/providers/diagnosticsettings",
      "apiVersion": "2017-05-01-preview",
      "name": "[concat(variables('storageAccountName'),'/Microsoft.Insights/', 'diagnosticsettings')]",
      "dependsOn": [
        "[resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName'))]"
      ],
      "properties": {
        "workspaceId": "[variables('logAnalyticsWorkspaceResourceID')]",
        "storageAccountId": "[resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName'))]",
        "metrics": [
          {
            "category": "Transaction",
            "enabled": true
          }
        ]
      }
    },
    {
      "type": "Microsoft.Network/publicIPAddresses",
      "name": "[variables('appgatewaypublicipname')]",
      "apiVersion": "2018-08-01",
      "dependsOn": [
        "[resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName'))]"
      ],
      "tags": {
        "Created BY": "[parameters('createdBy')]",
        "Project": "[parameters('project')]",
        "Client Group": "[parameters('clientGroup')]",
        "Managed By Group": "[parameters('managedByGroup')]",
        "IO Code": "[parameters('ioCode')]",
        "Accreditation Number": "[parameters('accreditationNumber')]"
      },
      "location": "[resourceGroup().location]",
      "sku": {
        "name": "Standard"
      },
      "properties": {
        "publicIPAllocationMethod": "Static"
      }
    },
    {
      "type": "Microsoft.Network/applicationGateways",
      "name": "[variables('applicationGatewayName')]",
      "apiVersion": "2018-08-01",
      "dependsOn": [
        "[resourceId('Microsoft.Network/publicIPAddresses/', variables('appgatewaypublicipname'))]"
      ],
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
        "sku": {
          "name": "Standard_v2",
          "tier": "Standard_v2",
          "capacity": 1
        },
        "gatewayIPConfigurations": [
          {
            "name": "appgatewayipconfig",
            "properties": {
              "subnet": {
                "id": "[variables('appGateWaySubnetID')]"
              }
            }
          }
        ],
        "frontendIPConfigurations": [
          {
            "name": "appGatewayFrontendIP",
            "properties": {
              "PublicIPAddress": {
                "id": "[resourceId('Microsoft.Network/publicIPAddresses', variables('appgatewaypublicipname'))]"
              }
            }
          },
          {
            "name": "FrontendPrivate",
            "properties": {
              "privateIPAddress": "[parameters('virtual-network-appgateway-ip-address')]",
              "privateIPAllocationMethod": "Static",
              "subnet": {
                "id": "[variables('appGateWaySubnetID')]"
              }
            }
          }
        ],
        "frontendPorts": [
          {
            "name": "httpport",
            "properties": {
              "Port": 80
            }
          },
          {
            "name": "httpsPort",
            "properties": {
              "Port": 443
            }
          }
        ],
        "backendAddressPools": [
          {
            "name": "backendpool",
            "properties": {
              "backendAddresses": []
            }
          }
        ],
        "httpListeners": [
          {
            "name": "httpListener",
            "properties": {
              "protocol": "Http",
              "frontendPort": {
                "id": "[concat(variables('applicationGatewayId'), '/frontendPorts/httpport')]"
              },
              "frontendIPConfiguration": {
                "id": "[concat(variables('applicationGatewayId'), '/frontendIPConfigurations/appGatewayFrontendIP')]"
              }
            }
          }
        ],
        "backendHttpSettingsCollection": [
          {
            "name": "setting",
            "properties": {
              "port": 80,
              "protocol": "Http"
            }
          }
        ],
        "requestRoutingRules": [
          {
            "name": "BasicRule",
            "properties": {
              "httpListener": {
                "id": "[concat(variables('applicationGatewayId'), '/httpListeners/httpListener')]"
              },
              "backendAddressPool": {
                "id": "[concat(variables('applicationGatewayId'), '/backendAddressPools/backendpool')]"
              },
              "backendHttpSettings": {
                "id": "[concat(variables('applicationGatewayId'), '/backendHttpSettingsCollection/setting')]"
              }
            }
          }
        ]
      },
      "zones": ["1", "2", "3"]
    },
    {
      "type": "Microsoft.Network/applicationGateways/providers/diagnosticsettings",
      "apiVersion": "2017-05-01-preview",
      "name": "[concat(variables('applicationGatewayName'),'/Microsoft.Insights/', 'diagnosticsettings')]",
      "dependsOn": [
        "[resourceId('Microsoft.Network/applicationGateways', variables('applicationGatewayName'))]"
      ],
      "properties": {
        "workspaceId": "[variables('logAnalyticsWorkspaceResourceID')]",
        "logs": [
          {
            "category": "ApplicationGatewayAccessLog",
            "enabled": true
          },
          {
            "category": "ApplicationGatewayPerformanceLog",
            "enabled": true
          },
          {
            "category": "ApplicationGatewayFirewallLog",
            "enabled": true
          }
        ],
        "metrics": [
          {
            "category": "AllMetrics",
            "enabled": true
          }
        ]
      }
    },
    {
      "name": "[variables('acrName')]",
      "type": "Microsoft.ContainerRegistry/registries",
      "apiVersion": "2019-12-01-preview",
      "dependsOn": [
        "[resourceId('Microsoft.Network/applicationGateways', variables('applicationGatewayName'))]"
      ],
      "location": "[resourceGroup().location]",
      "comments": "Container registry for storing docker images",
      "tags": {
        "Created BY": "[parameters('createdBy')]",
        "Project": "[parameters('project')]",
        "Client Group": "[parameters('clientGroup')]",
        "Managed By Group": "[parameters('managedByGroup')]",
        "IO Code": "[parameters('ioCode')]",
        "Accreditation Number": "[parameters('accreditationNumber')]"
      },
      "sku": {
        "name": "Premium",
        "tier": "Premium"
      },
      "properties": {
        "adminUserEnabled": false,
        "networkRuleSet": {
          "defaultAction": "Allow",
          "virtualNetworkRules": [],
          "ipRules": []
        },
        "publicNetworkAccess": "disabled",
        "dataEndpointEnabled": false,
        "policies": {
          "quarantinePolicy": {
            "status": "disabled"
          },
          "trustPolicy": {
            "type": "Notary",
            "status": "disabled"
          },
          "retentionPolicy": {
            "days": 7,
            "status": "disabled"
          }
        }
      }
    },
    {
      "type": "Microsoft.ContainerRegistry/registries/providers/diagnosticSettings",
      "apiVersion": "2017-05-01-preview",
      "name": "[concat(variables('acrName'), '/Microsoft.Insights/', 'diagnosticsettings')]",
      "dependsOn": [
        "[resourceId('Microsoft.ContainerRegistry/registries', variables('acrName'))]"
      ],
      "properties": {
        "workspaceId": "[variables('logAnalyticsWorkspaceResourceID')]",
        "logs": [
          {
            "category": "ContainerRegistryRepositoryEvents",
            "enabled": true
          },
          {
            "category": "ContainerRegistryLoginEvents",
            "enabled": true
          }
        ],
        "metrics": [
          {
            "category": "AllMetrics",
            "enabled": true
          }
        ]
      }
    },
    {
      "type": "Microsoft.Network/privateEndpoints",
      "apiVersion": "2020-05-01",
      "name": "[variables('acrName')]",
      "location": "[resourceGroup().location]",
      "tags": {
        "Created BY": "[parameters('createdBy')]",
        "Project": "[parameters('project')]",
        "Client Group": "[parameters('clientGroup')]",
        "Managed By Group": "[parameters('managedByGroup')]",
        "IO Code": "[parameters('ioCode')]",
        "Accreditation Number": "[parameters('accreditationNumber')]"
      },
      "dependsOn": [
        "[resourceId('Microsoft.ContainerRegistry/registries', variables('acrName'))]"
      ],
      "properties": {
        "privateLinkServiceConnections": [
          {
            "name": "[concat(variables('acrName'), substring(uniqueString(resourceGroup().id),0,6))]",
            "properties": {
              "privateLinkServiceId": "[resourceId('Microsoft.ContainerRegistry/registries', variables('acrName'))]",
              "groupIds": ["registry"],
              "privateLinkServiceConnectionState": {
                "status": "Approved",
                "description": "Auto-Approved",
                "actionsRequired": "None"
              }
            }
          }
        ],
        "manualPrivateLinkServiceConnections": [],
        "subnet": {
          "id": "[variables('kubernetesSubnetID')]"
        },
        "customDnsConfigs": []
      }
    },
    {
      "type": "Microsoft.ManagedIdentity/userAssignedIdentities",
      "name": "[variables('identityName')]",
      "apiVersion": "2015-08-31-PREVIEW",
      "dependsOn": [
        "[resourceId('Microsoft.ContainerRegistry/registries', variables('acrName'))]"
      ],
      "tags": {
        "Created BY": "[parameters('createdBy')]",
        "Project": "[parameters('project')]",
        "Client Group": "[parameters('clientGroup')]",
        "Managed By Group": "[parameters('managedByGroup')]",
        "IO Code": "[parameters('ioCode')]",
        "Accreditation Number": "[parameters('accreditationNumber')]"
      },
      "location": "[resourceGroup().location]"
    },
    {
      "name": "[variables('KeyVaultName')]",
      "type": "Microsoft.KeyVault/vaults",
      "apiVersion": "2019-09-01",
      "location": "[resourceGroup().location]",
      "dependsOn": [
        "[resourceId('Microsoft.ManagedIdentity/userAssignedIdentities', variables('identityName'))]"
      ],
      "tags": {
        "Created BY": "[parameters('createdBy')]",
        "Project": "[parameters('project')]",
        "Client Group": "[parameters('clientGroup')]",
        "Managed By Group": "[parameters('managedByGroup')]",
        "IO Code": "[parameters('ioCode')]",
        "Accreditation Number": "[parameters('accreditationNumber')]"
      },
      "properties": {
        "tenantId": "[parameters('tenantID')]",
        "sku": {
          "family": "A",
          "name": "standard"
        },
        "accessPolicies": [
          {
            "tenantId": "[reference(variables('identityID')).tenantId]",
            "objectId": "[reference(variables('identityID')).principalId]",
            "permissions": {
              "secrets": [
                  "Get",
                  "List",
                  "Set"
              ],
              "keys": [
                  "Get",
                  "List",
                  "Update",
                  "Create",
                  "Decrypt",
                  "Encrypt",
                  "UnwrapKey",
                  "WrapKey"
              ],
              "certificates": [
                  "Get",
                  "List",
                  "Update",
                  "Create",
                  "Import",
                  "Delete"
              ]
          }
          },
          {
            "tenantId": "[subscription().tenantId]",
            "objectId": "[parameters('webApiSPObjectID')]",
            "permissions": {
              "secrets": [
                "Get",
                "List",
                "Set",
                "Delete",
                "Recover",
                "Backup",
                "Restore"
              ]
            }
          },
          {
            "tenantId": "[subscription().tenantId]",
            "objectId": "[parameters('resourceSPObjectID')]",
            "permissions": {
              "secrets": [
                "Get",
                "List",
                "Set",
                "Delete",
                "Recover",
                "Backup",
                "Restore",
                "Purge"
              ]
            }
          }
        ],
        "enabledForDeployment": false,
        "enabledForDiskEncryption": false,
        "enabledForTemplateDeployment": false,
        "enableSoftDelete": true,
        "enablePurgeProtection": true,
        "networkAcls": {
          "bypass": "None",
          "defaultAction": "Deny",
          "virtualNetworkRules": [
            {
              "id": "[variables('kubernetesSubnetID')]"
            }
          ]
        }
      },
      "resources": []
    },
    {
      "type": "Microsoft.KeyVault/vaults/secrets",
      "apiVersion": "2019-09-01",
      "name": "[concat(variables('keyVaultName'), '/', 'psql-password')]",
      "location": "[resourceGroup().location]",
      "dependsOn": [
        "[resourceId('Microsoft.KeyVault/vaults', variables('KeyVaultName'))]"
      ],
      "properties": {
        "value": "[parameters('psqlPassword')]"
      }
    },
    {
      "type": "Microsoft.KeyVault/vaults/secrets",
      "apiVersion": "2019-09-01",
      "name": "[concat(variables('keyVaultName'), '/', 'psql-username')]",
      "location": "[resourceGroup().location]",
      "dependsOn": [
        "[resourceId('Microsoft.KeyVault/vaults', variables('KeyVaultName'))]"
      ],
      "properties": {
        "value": "[parameters('psqlUserName')]"
      }
    },
    {
      "type": "Microsoft.KeyVault/vaults/secrets",
      "apiVersion": "2019-09-01",
      "name": "[concat(variables('keyVaultName'), '/', 'tenantId')]",
      "location": "[resourceGroup().location]",
      "dependsOn": [
        "[resourceId('Microsoft.KeyVault/vaults', variables('KeyVaultName'))]"
      ],
      "properties": {
        "value": "[parameters('tenantID')]"
      }
    },
    {
      "type": "Microsoft.KeyVault/vaults/secrets",
      "apiVersion": "2019-09-01",
      "name": "[concat(variables('keyVaultName'), '/', 'rp-clientId')]",
      "location": "[resourceGroup().location]",
      "dependsOn": [
        "[resourceId('Microsoft.KeyVault/vaults', variables('KeyVaultName'))]"
      ],
      "properties": {
        "value": "[parameters('clientId')]"
      }
    },
    {
      "type": "Microsoft.KeyVault/vaults/secrets",
      "apiVersion": "2019-09-01",
      "name": "[concat(variables('keyVaultName'), '/', 'rp-clientSecret')]",
      "location": "[resourceGroup().location]",
      "dependsOn": [
        "[resourceId('Microsoft.KeyVault/vaults', variables('KeyVaultName'))]"
      ],
      "properties": {
        "value": "[parameters('clientSecret')]"
      }
    },
    {
      "type": "Microsoft.KeyVault/vaults/secrets",
      "apiVersion": "2019-09-01",
      "name": "[concat(variables('keyVaultName'), '/', 'aks-username')]",
      "location": "[resourceGroup().location]",
      "dependsOn": [
        "[resourceId('Microsoft.KeyVault/vaults', variables('KeyVaultName'))]"
      ],
      "properties": {
        "value": "[parameters('aksClusterAdminUsername')]"
      }
    },
    {
      "type": "Microsoft.KeyVault/vaults/providers/diagnosticSettings",
      "apiVersion": "2017-05-01-preview",
      "name": "[concat(variables('KeyVaultName'), '/Microsoft.Insights/', 'diagnosticsettings')]",
      "dependsOn": [
        "[resourceId('Microsoft.KeyVault/vaults', variables('KeyVaultName'))]"
      ],
      "properties": {
        "workspaceId": "[variables('logAnalyticsWorkspaceResourceID')]",
        "logs": [
          {
            "category": "AuditEvent",
            "enabled": true
          }
        ],
        "metrics": [
          {
            "category": "AllMetrics",
            "enabled": true
          }
        ]
      }
    },
    {
      "type": "Microsoft.DocumentDB/databaseAccounts",
      "apiVersion": "2020-06-01-preview",
      "name": "[variables('cosmosdbName')]",
      "location": "[resourceGroup().location]",
      "tags": {
        "Created BY": "[parameters('createdBy')]",
        "Project": "[parameters('project')]",
        "Client Group": "[parameters('clientGroup')]",
        "Managed By Group": "[parameters('managedByGroup')]",
        "IO Code": "[parameters('ioCode')]",
        "Accreditation Number": "[parameters('accreditationNumber')]"
      },

      "kind": "GlobalDocumentDB",
      "identity": {
        "type": "None"
      },
      "properties": {
        "publicNetworkAccess": "Enabled",
        "enableAutomaticFailover": false,
        "enableMultipleWriteLocations": false,
        "isVirtualNetworkFilterEnabled": true,
        "virtualNetworkRules": [
          {
            "id": "[variables('kubernetesSubnetID')]",
            "ignoreMissingVNetServiceEndpoint": false
          }
        ],
        "disableKeyBasedMetadataWriteAccess": false,
        "enableFreeTier": true,
        "enableAnalyticalStorage": false,
        "createMode": "Default",
        "databaseAccountOfferType": "Standard",
        "consistencyPolicy": {
          "defaultConsistencyLevel": "Session",
          "maxIntervalInSeconds": 5,
          "maxStalenessPrefix": 100
        },
        "locations": [
          {
            "locationName": "[resourceGroup().location]",
            "failoverPriority": 0,
            "isZoneRedundant": true
          }
        ],
        "cors": [],
        "capabilities": [],
        "ipRules": [],
        "backupPolicy": {
          "type": "Periodic",
          "periodicModeProperties": {
            "backupIntervalInMinutes": 1440,
            "backupRetentionIntervalInHours": 192
          }
        }
      }
    },
    {
      "type": "Microsoft.DocumentDB/databaseAccounts/providers/diagnosticSettings",
      "apiVersion": "2017-05-01-preview",
      "name": "[concat(variables('cosmosdbName'), '/Microsoft.Insights/', 'diagnosticsettings')]",
      "dependsOn": [
        "[resourceId('Microsoft.DocumentDB/databaseAccounts', variables('cosmosdbName'))]"
      ],
      "properties": {
        "workspaceId": "[variables('logAnalyticsWorkspaceResourceID')]",
        "logs": [
          {
            "category": "DataPlaneRequests",
            "enabled": true
          },
          {
            "category": "MongoRequests",
            "enabled": true
          },
          {
            "category": "QueryRuntimeStatistics",
            "enabled": true
          },
          {
            "category": "PartitionKeyStatistics",
            "enabled": true
          },
          {
            "category": "PartitionKeyRUConsumption",
            "enabled": true
          },
          {
            "category": "ControlPlaneRequests",
            "enabled": true
          },
          {
            "category": "CassandraRequests",
            "enabled": true
          },
          {
            "category": "GremlinRequests",
            "enabled": true
          }
        ]
      }
    },
    {
      "name": "[variables('aksClusterName')]",
      "type": "Microsoft.ContainerService/managedClusters",
      "dependsOn": [
        "[resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName'))]"
      ],
      "apiVersion": "2020-07-01",
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
        "kubernetesVersion": "[parameters('aksClusterKubernetesVersion')]",
        "dnsPrefix": "aks",
        "agentPoolProfiles": [
          {
            "count": "[parameters('nodePoolVmCount')]",
            "vmSize": "[parameters('nodePoolVmSize')]",
            "osDiskSizeGB": "[parameters('nodePoolOsDiskSizeGB')]",
            "vnetSubnetID": "[variables('kubernetesSubnetID')]",
            "maxPods": 30,
            "osType": "Linux",
            "enableAutoScaling": false,
            "type": "VirtualMachineScaleSets",
            "mode": "System",
            "orchestratorVersion": "[parameters('aksClusterKubernetesVersion')]",
            "enableNodePublicIP": false,
            "tags": {},
            "nodeLabels": {},
            "name": "[variables('nodePoolName')]",
            "availabilityZones": ["1", "2", "3"]
          }
        ],
        "linuxProfile": {
          "adminUsername": "[parameters('aksClusterAdminUsername')]",
          "ssh": {
            "publicKeys": [
              {
                "keyData": "[parameters('aksClusterSshPublicKey')]"
              }
            ]
          }
        },
        "servicePrincipalProfile": {
          "clientId": "[parameters('clientId')]",
          "secret": "[parameters('clientSecret')]"
        },
        "addonProfiles": {
          "azurePolicy": {
            "enabled": true
          },
          "httpapplicationrouting": {
            "enabled": false
          },
          "kubedashboard": {
            "enabled": false
          },
          "omsagent": {
            "enabled": true,
            "config": {
              "logAnalyticsWorkspaceResourceID": "[variables('logAnalyticsWorkspaceResourceID')]"
            }
          }
        },
        "aadProfile": {
          "managed": true,
          "enableAzureRBAC": false,
          "adminGroupObjectIDs": "[parameters('aksAdminGroupObjectID')]",
          "clientAppID": "",
          "serverAppID": "",
          "serverAppSecret": "",
          "tenantID": "[parameters('tenantID')]"
        },
        "enableRBAC": true,
        "nodeResourceGroup": "[variables('aksnodeResourceGroup')]",
        "enablePodSecurityPolicy": false,
        "networkProfile": {
          "networkPlugin": "azure",
          "networkPolicy": "azure",
          "serviceCidr": "[parameters('aksClusterServiceCidr')]",
          "dnsServiceIP": "[parameters('aksClusterDnsServiceIP')]",
          "dockerBridgeCidr": "172.17.0.1/16",
          "outboundType": "loadBalancer",
          "loadBalancerSku": "standard"
        },
        "apiServerAccessProfile": {
          "enablePrivateCluster": true
        }
      },
      "resources": []
    }
  ],
  "outputs": {}
}



```
