# Compensator Function for Saga Distributed Transactions Pattern

This folder contains the Python code for the **Compensator Function**. The Compensator Function reverts or compensates for any changes if a failure occurs in any part of the Saga.

## 📑 Files

- **`compensator_function.py`**: Python code for the Compensator Function.
- **`requirements.txt`**: Lists the dependencies required by the Compensator Function.
- **`deploy-compensator.yml`**: GitHub Action workflow to automate the deployment of the Compensator Function.

## 🚀 How to Deploy the Compensator Function

### Prerequisites

1. **Azure Subscription**: You need an active Azure account.
2. **Azure Function App**: Ensure the Azure Function App is created (using the Bicep template in the `/infrastructure` folder).
3. **GitHub Secrets Configuration**:
   - **`AZURE_CREDENTIALS`**: Azure service principal credentials in JSON format.
   - **`AZURE_FUNCTIONAPP_PUBLISH_PROFILE`**: Publish profile for the Azure Function App.
   - **`ServiceBusConnection`**: Connection string for the Azure Service Bus namespace.
   - **`CosmosDBConnectionString`**: Connection string for the Azure Cosmos DB account.

### Steps to Deploy

1. **Add Required Secrets to GitHub**:
   - Go to your repository's **Settings > Secrets and variables > Actions > New repository secret**.
   - Add the following secrets:
     - **`AZURE_CREDENTIALS`**: Your Azure service principal credentials.
     - **`AZURE_FUNCTIONAPP_PUBLISH_PROFILE`**: The publish profile for your Azure Function App.
     - **`ServiceBusConnection`**: The connection string for your Azure Service Bus namespace.
     - **`CosmosDBConnectionString`**: The connection string for your Azure Cosmos DB account.

2. **Run the GitHub Action**:
   - Push your changes to the `main` branch or manually trigger the **Deploy Compensator Function** workflow from the **Actions** tab.

3. **Monitor the Deployment**:
   - Go to the **Actions** tab in your GitHub repository.
   - Select the **Deploy Compensator Function** workflow to monitor the deployment progress.

### 📝 How the Compensator Function Works

1. **Listen for Compensation Requests**:
   - The Compensator Function is triggered when it receives a compensation request message from the **Service Bus Topic** (`sagaServiceBusTopic`).

2. **Revert or Compensate the Transaction**:
   - The function deletes the order details from **Azure Cosmos DB** based on the received order information.
   - If successful, the data is removed, achieving compensation; otherwise, it logs an error.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
