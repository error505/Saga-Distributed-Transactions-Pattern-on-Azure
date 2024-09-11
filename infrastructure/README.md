# Infrastructure Deployment for Saga Distributed Transactions Pattern

This folder contains the **Bicep template** for deploying the required Azure resources for the **Saga Distributed Transactions Pattern**. The resources include an Azure Service Bus, Azure Cosmos DB, Application Insights, and Azure Function Apps.

## 📑 Files

- **`azure-resources.bicep`**: Bicep template file that defines all the necessary Azure resources.
- **`deploy-bicep.yml`**: GitHub Action workflow file to automate the deployment of the Azure infrastructure.

## 🚀 How to Deploy the Infrastructure

### Prerequisites

1. **Azure Subscription**: You need an active Azure account.
2. **Azure CLI**: Installed and configured.
3. **GitHub Secrets Configuration**:
   - **`AZURE_CLIENT_ID`**: Azure service principal client ID.
   - **`AZURE_CLIENT_SECRET`**: Azure service principal client secret.
   - **`AZURE_TENANT_ID`**: Azure tenant ID.

### Steps to Deploy

1. **Add Required Secrets to GitHub**:
   - Go to your repository's **Settings > Secrets and variables > Actions > New repository secret**.
   - Add the following secrets:
     - **`AZURE_CLIENT_ID`**: Your Azure service principal client ID.
     - **`AZURE_CLIENT_SECRET`**: Your Azure service principal client secret.
     - **`AZURE_TENANT_ID`**: Your Azure tenant ID.

2. **Run the GitHub Action**:
   - Push your changes to the `main` branch or manually trigger the **Deploy Azure Infrastructure with Bicep** workflow from the **Actions** tab.

3. **Monitor the Deployment**:
   - Go to the **Actions** tab in your GitHub repository.
   - Select the **Deploy Azure Infrastructure with Bicep** workflow to monitor the deployment progress.

### 📊 What Happens After Deployment

- The Bicep template will create the following resources:
  - **Azure Service Bus**: A messaging service that acts as the backbone for communication between the orchestrator, activity, and compensator functions.
  - **Azure Cosmos DB**: A globally distributed database that stores order details.
  - **Azure Function Apps**: Hosts for the Orchestrator, Activity, and Compensator Functions.
  - **Application Insights**: A monitoring tool that collects logs and telemetry data from all functions.

### 💡 Next Steps

Once the infrastructure is deployed, proceed to deploy each of the Azure Functions (Orchestrator, Activity, and Compensator) using their respective GitHub Actions.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
