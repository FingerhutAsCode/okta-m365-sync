@description('Environment name (dev, staging, prod)')
param environment string = 'dev'

@description('Azure region for all resources')
param location string = resourceGroup().location

@description('Okta webhook secret')
@secure()
param oktaWebhookSecret string

@description('Azure AD Client Secret for Graph API')
@secure()
param azureClientSecret string

var prefix = 'okta-m365-sync-${environment}'

resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: replace('st${prefix}', '-', '')
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}

resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: 'asp-${prefix}'
  location: location
  sku: { name: 'Y1', tier: 'Dynamic' }
  properties: { reserved: true }
  kind: 'linux'
}

resource functionApp 'Microsoft.Web/sites@2022-03-01' = {
  name: 'func-${prefix}'
  location: location
  kind: 'functionapp,linux'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'Python|3.11'
      appSettings: [
        { name: 'AzureWebJobsStorage', value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net' }
        { name: 'FUNCTIONS_EXTENSION_VERSION', value: '~4' }
        { name: 'FUNCTIONS_WORKER_RUNTIME', value: 'python' }
        { name: 'OKTA_WEBHOOK_SECRET', value: oktaWebhookSecret }
        { name: 'AZURE_CLIENT_SECRET', value: azureClientSecret }
      ]
    }
  }
}

output functionAppName string = functionApp.name
output functionAppUrl string = 'https://${functionApp.properties.defaultHostName}'
