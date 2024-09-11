# Orchestrator Function for Saga Distributed Transactions Pattern

This folder contains the Python code for the **Orchestrator Function**. The Orchestrator Function manages the flow of the Saga, coordinating multiple steps and triggering compensating actions if needed.

## 📑 Files

- **`orchestrator_function.py`**: Python code for the Orchestrator Function.
- **`requirements.txt`**: Lists the dependencies required by the Orchestrator Function.
- **`deploy-orchestrator.yml`**: GitHub Action workflow to automate the deployment of the Orchestrator Function.

## 🚀 How to Deploy the Orchestrator Function

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

### Required Environment Variables

Ensure the following environment variables are set in your Azure Function App configuration:

- **`ServiceBusConnection`**: Connection string for the Azure Service Bus namespace.
- **`CosmosDBConnectionString`**: Connection string for the Azure Cosmos DB account.
- **`ActivityFunctionUrl`**: URL of the deployed Activity Function endpoint.

2. **Run the GitHub Action**:
   - Push your changes to the `main` branch or manually trigger the **Deploy Orchestrator Function** workflow from the **Actions** tab.

3. **Monitor the Deployment**:
   - Go to the **Actions** tab in your GitHub repository.
   - Select the **Deploy Orchestrator Function** workflow to monitor the deployment progress.

### 📝 How to Use the Orchestrator Function

1. **Trigger the Orchestrator Function**:
   - The Orchestrator Function is triggered via an HTTP POST request to the `/startSaga` endpoint.
   - Use an HTTP client (such as Postman or `curl`) to send a request:

   ```bash
   curl -X POST https://<your-orchestrator-function-app-name>.azurewebsites.net/api/startSaga \
   -H "Content-Type: application/json" \
   -d '{
       "orderId": "12345",
       "customerName": "John Doe",
       "items": ["Laptop", "Smartphone"]
   }'
   ```

   Replace `<your-orchestrator-function-app-name>` with the name of your deployed Azure Function App.

2. **What Happens Next**:
   - The Orchestrator Function processes the request and calls the **Activity Function** to perform the transaction.
   - If the transaction is successful, a success response is returned.
   - If the transaction fails, the **Compensator Function** is triggered to revert or compensate for the failed transaction.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
