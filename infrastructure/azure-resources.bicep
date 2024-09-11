// Parameters
param location string = resourceGroup().location
param serviceBusNamespaceName string = 'myServiceBusNamespace'
param serviceBusTopicName string = 'sagaServiceBusTopic'
param cosmosDbAccountName string = 'myCosmosDbAccount'
param cosmosDbDatabaseName string = 'myDatabase'
param cosmosDbContainerName string = 'myContainer'
param appInsightsName string = 'sagaAppInsights'
param functionAppPlanName string = 'myFunctionAppPlan'
param orchestratorFunctionName string = 'orchestratorFunctionApp'
param activityFunctionName string = 'activityFunctionApp'
param compensatorFunctionName string = 'compensatorFunctionApp'

// Azure Service Bus Namespace
resource serviceBusNamespace 'Microsoft.ServiceBus/namespaces@2021-06-01-preview' = {
  name: serviceBusNamespaceName
  location: location
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
}

// Azure Service Bus Topic
resource serviceBusTopic 'Microsoft.ServiceBus/namespaces/topics@2021-06-01-preview' = {
  parent: serviceBusNamespace
  name: serviceBusTopicName
}

// Azure Cosmos DB Account
resource cosmosDb 'Microsoft.DocumentDB/databaseAccounts@2023-05-15' = {
  name: cosmosDbAccountName
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: location
        failoverPriority: 0
      }
    ]
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
  }
}

// Azure Cosmos DB SQL Database
resource cosmosDbDatabase 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2023-05-15' = {
  parent: cosmosDb
  name: cosmosDbDatabaseName
  properties: {
    resource: {
      id: cosmosDbDatabaseName
    }
  }
}

// Azure Cosmos DB SQL Container
resource cosmosDbContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2023-05-15' = {
  parent: cosmosDbDatabase
  name: cosmosDbContainerName
  properties: {
    resource: {
      id: cosmosDbContainerName
      partitionKey: {
        paths: ['/partitionKey']
        kind: 'Hash'
      }
      defaultTtl: -1
    }
  }
}

// Application Insights
resource appInsights 'Microsoft.Insights/components@2022-07-01' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    RetentionInDays: 30
  }
}

// Azure Function App Plan
resource functionAppPlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: functionAppPlanName
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
}

// Orchestrator Function App
resource orchestratorFunctionApp 'Microsoft.Web/sites@2022-03-01' = {
  name: orchestratorFunctionName
  location: location
  kind: 'functionapp'
  properties: {
    serverFarmId: functionAppPlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'ServiceBusConnection'
          value: listKeys(resourceId('Microsoft.ServiceBus/namespaces/authorizationRules', serviceBusNamespace.name, 'RootManageSharedAccessKey'), '2021-06-01-preview').primaryConnectionString
        }
        {
          name: 'CosmosDBConnectionString'
          value: cosmosDb.listKeys().primaryMasterKey
        }
      ]
    }
  }
}

// Activity Function App
resource activityFunctionApp 'Microsoft.Web/sites@2022-03-01' = {
  name: activityFunctionName
  location: location
  kind: 'functionapp'
  properties: {
    serverFarmId: functionAppPlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'ServiceBusConnection'
          value: listKeys(resourceId('Microsoft.ServiceBus/namespaces/authorizationRules', serviceBusNamespace.name, 'RootManageSharedAccessKey'), '2021-06-01-preview').primaryConnectionString
        }
        {
          name: 'CosmosDBConnectionString'
          value: cosmosDb.listKeys().primaryMasterKey
        }
      ]
    }
  }
}

// Compensator Function App
resource compensatorFunctionApp 'Microsoft.Web/sites@2022-03-01' = {
  name: compensatorFunctionName
  location: location
  kind: 'functionapp'
  properties: {
    serverFarmId: functionAppPlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'ServiceBusConnection'
          value: listKeys(resourceId('Microsoft.ServiceBus/namespaces/authorizationRules', serviceBusNamespace.name, 'RootManageSharedAccessKey'), '2021-06-01-preview').primaryConnectionString
        }
        {
          name: 'CosmosDBConnectionString'
          value: cosmosDb.listKeys().primaryMasterKey
        }
      ]
    }
  }
}
