"""
Activity Function for processing messages from Azure Service Bus and storing them in Azure Cosmos DB.
"""

import logging
import os
import json
from azure.functions import FunctionApp, ServiceBusMessage
from azure.cosmos import CosmosClient, exceptions

# Get environment variables
cosmos_db_conn_str = os.getenv('CosmosDBConnectionString')
cosmos_db_database_name = os.getenv('cosmosDbDatabaseName', 'myDatabase')
cosmos_db_container_name = os.getenv('cosmosDbContainerName', 'myContainer')

app = FunctionApp()

@app.function_name(name="ActivityFunction")
@app.service_bus_topic_trigger(
    connection="ServiceBusConnection",
    topic_name="sagaServiceBusTopic",
    subscription_name="activitySubscription",
)
def run_activity(message: ServiceBusMessage):
    """
    Processes a message from Azure Service Bus and stores it in Azure Cosmos DB.
    """
    logging.info('Activity Function: Processing message...')

    try:
        order_data = json.loads(message.get_body().decode('utf-8'))
        logging.info("Processing order data: %s", order_data)

        cosmos_client = CosmosClient.from_connection_string(cosmos_db_conn_str)
        database = cosmos_client.get_database_client(cosmos_db_database_name)
        container = database.get_container_client(cosmos_db_container_name)

        # Upsert order data to Cosmos DB
        container.upsert_item(order_data)
        logging.info("Order data stored in Cosmos DB: %s", order_data.get('orderId'))

    except exceptions.CosmosHttpResponseError as cosmos_error:
        logging.error("Cosmos DB error: %s", cosmos_error)
    except ValueError as json_error:
        logging.error("JSON decoding error: %s", json_error)
    except Exception as general_error:
        logging.error("Unexpected error in Activity Function: %s", general_error)
