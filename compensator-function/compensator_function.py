import azure.functions as func
import logging
import os
import json
from azure.cosmos import CosmosClient, exceptions

# Get environment variables
cosmos_db_conn_str = os.getenv('CosmosDBConnectionString')
cosmos_db_database_name = os.getenv('cosmosDbDatabaseName', 'myDatabase')
cosmos_db_container_name = os.getenv('cosmosDbContainerName', 'myContainer')

app = func.FunctionApp()

@app.function_name(name="CompensatorFunction")
@app.service_bus_topic_trigger(
    connection="ServiceBusConnection",
    topic_name="sagaServiceBusTopic",
    subscription_name="compensatorSubscription",
)
def run_compensation(message: func.ServiceBusMessage):
    logging.info('Compensator Function: Processing compensation...')

    try:
        order_data = json.loads(message.get_body().decode('utf-8'))
        logging.info(f"Compensating for order: {order_data['orderId']}")

        cosmos_client = CosmosClient.from_connection_string(cosmos_db_conn_str)
        database = cosmos_client.get_database_client(cosmos_db_database_name)
        container = database.get_container_client(cosmos_db_container_name)

        # Here we simulate compensation by deleting the item from Cosmos DB
        container.delete_item(order_data['orderId'], partition_key=order_data['orderId'])
        logging.info(f"Order data deleted from Cosmos DB: {order_data['orderId']}")

    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Cosmos DB error during compensation: {e}")
    except Exception as e:
        logging.error(f"Unexpected error in Compensation Function: {e}")
