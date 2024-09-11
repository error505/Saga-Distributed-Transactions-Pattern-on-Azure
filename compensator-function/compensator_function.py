"""
Compensator Function for handling distributed transactions using Azure Service Bus and Cosmos DB.
This function listens for compensation messages and reverts transactions as needed.
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

@app.function_name(name="CompensatorFunction")
@app.service_bus_topic_trigger(
    connection="ServiceBusConnection",
    topic_name="sagaServiceBusTopic",
    subscription_name="compensatorSubscription",
)
def run_compensation(message: ServiceBusMessage):
    """
    Compensator Function to handle transaction rollback in case of failure.

    This function listens to messages from a Service Bus topic and compensates for failed transactions
    by deleting relevant data from Cosmos DB.
    """
    logging.info('Compensator Function: Processing compensation...')

    try:
        order_data = json.loads(message.get_body().decode('utf-8'))
        logging.info('Compensating for order: %s', order_data['orderId'])

        cosmos_client = CosmosClient.from_connection_string(cosmos_db_conn_str)
        database = cosmos_client.get_database_client(cosmos_db_database_name)
        container = database.get_container_client(cosmos_db_container_name)

        # Simulate compensation by deleting the item from Cosmos DB
        container.delete_item(order_data['orderId'], partition_key=order_data['orderId'])
        logging.info('Order data deleted from Cosmos DB: %s', order_data['orderId'])

    except exceptions.CosmosHttpResponseError as ex:
        logging.error('Cosmos DB error during compensation: %s', ex)
    except Exception as ex:  # pylint: disable=broad-exception-caught
        logging.error('Unexpected error in Compensation Function: %s', ex)
