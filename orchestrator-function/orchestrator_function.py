"""
Orchestrator Function for the Saga Distributed Transactions Pattern.

This function initiates the Saga, manages the workflow, and triggers compensating
actions if needed.
"""

import logging
import os
import json
import requests
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import azure.functions as func

# Get environment variables
servicebus_connection_str = os.getenv('ServiceBusConnection')
topic_name = os.getenv('sagaServiceBusTopic', 'sagaServiceBusTopic')
cosmos_db_conn_str = os.getenv('CosmosDBConnectionString')
cosmos_db_database_name = os.getenv('cosmosDbDatabaseName', 'myDatabase')
cosmos_db_container_name = os.getenv('cosmosDbContainerName', 'myContainer')
activity_function_url = os.getenv('ActivityFunctionUrl')  # URL of the Activity Function

app = func.FunctionApp()

@app.route(route="startSaga", auth_level=func.AuthLevel.ANONYMOUS)
def start_saga(req: func.HttpRequest) -> func.HttpResponse:
    """
    Entry point for starting the Saga process.

    This function receives an HTTP request with order data, processes it,
    and coordinates the Saga workflow.
    """
    logging.info('Orchestrator Function: Starting Saga...')

    try:
        order_data = req.get_json()
        logging.info("Received order data: %s", order_data)

        # Call Activity Function
        activity_result = call_activity_function(order_data)

        if activity_result['status'] == 'success':
            return func.HttpResponse(
                "Saga completed successfully.",
                status_code=200
            )

        # If something fails, trigger the compensating transaction
        trigger_compensation(order_data)
        return func.HttpResponse(
            "Saga failed. Compensation triggered.",
            status_code=500
        )
    except Exception as e:  # pylint: disable=broad-except
        logging.error("Unexpected error in Saga: %s", e)
        return func.HttpResponse(
            "Unexpected error occurred.",
            status_code=500
        )

def call_activity_function(order_data):
    """
    Calls the Activity Function to process the order data.

    This function sends an HTTP POST request to the Activity Function URL.
    """
    logging.info('Calling Activity Function...')

    try:
        response = requests.post(activity_function_url, json=order_data)
        response.raise_for_status()
        logging.info('Activity Function response: %s', response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error("Error calling Activity Function: %s", e)
        return {
            'status': 'failure',
            'message': str(e)
        }

def trigger_compensation(order_data):
    """
    Trigger the Compensation Function by sending a message to the Service Bus.

    This function sends a message to the compensator via Service Bus
    to undo any changes made by the Activity Function.
    """
    logging.info('Triggering Compensation Function...')
    try:
        servicebus_client = ServiceBusClient.from_connection_string(servicebus_connection_str)
        sender = servicebus_client.get_topic_sender(topic_name=topic_name)

        with sender:
            message = ServiceBusMessage(body=json.dumps(order_data))
            sender.send_messages(message)

        logging.info('Compensation Function triggered successfully.')
    except Exception as e:  # pylint: disable=broad-except
        logging.error("Failed to trigger Compensation Function: %s", e)
