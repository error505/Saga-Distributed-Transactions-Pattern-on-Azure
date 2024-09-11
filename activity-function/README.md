# Activity Function for Saga Distributed Transactions Pattern

This folder contains the Python code for the **Activity Function**. The Activity Function performs individual steps of the transaction, such as processing a part of the business logic and writing to Cosmos DB.

## 📑 Files

- **`activity_function.py`**: Python code for the Activity Function.
- **`requirements.txt`**: Lists the dependencies required by the Activity Function.
- **`deploy-activity.yml`**: GitHub Action workflow to automate the deployment of the Activity Function.

## 🚀 How to Deploy the Activity Function

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
   - Push your changes to the `main` branch or manually trigger the **Deploy Activity Function** workflow from the **Actions** tab.

3. **Monitor the Deployment**:
   - Go to the **Actions** tab in your GitHub repository.
   - Select the **Deploy Activity Function** workflow to monitor the deployment progress.

### 📝 How the Activity Function Works

1. **Listen for Messages**:
   - The Activity Function is triggered when it receives a message from the **Service Bus Topic** (`sagaServiceBusTopic`).
   - This message contains order details, such as `orderId`, `customerName`, and `items`.

2. **Process the Transaction**:
   - The function writes the order details to **Azure Cosmos DB**.
   - If successful, the data is stored in the Cosmos DB container; otherwise, it logs an error.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.