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

@app.function_name(name="ActivityFunction")
@app.service_bus_topic_trigger(
    connection="ServiceBusConnection",
    topic_name="sagaServiceBusTopic",
    subscription_name="activitySubscription",
)
def run_activity(message: func.ServiceBusMessage):
    logging.info('Activity Function: Processing message...')

    try:
        order_data = json.loads(message.get_body().decode('utf-8'))
        logging.info(f"Processing order data: {order_data}")

        cosmos_client = CosmosClient.from_connection_string(cosmos_db_conn_str)
        database = cosmos_client.get_database_client(cosmos_db_database_name)
        container = database.get_container_client(cosmos_db_container_name)

        # Upsert order data to Cosmos DB
        container.upsert_item(order_data)
        logging.info(f"Order data stored in Cosmos DB: {order_data['orderId']}")

    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Cosmos DB error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error in Activity Function: {e}")
