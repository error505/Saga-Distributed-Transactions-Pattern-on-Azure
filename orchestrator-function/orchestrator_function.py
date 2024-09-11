import azure.functions as func
import logging
import os
import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage

# Get environment variables
servicebus_connection_str = os.getenv('ServiceBusConnection')
topic_name = os.getenv('sagaServiceBusTopic', 'sagaServiceBusTopic')
cosmos_db_conn_str = os.getenv('CosmosDBConnectionString')
cosmos_db_database_name = os.getenv('cosmosDbDatabaseName', 'myDatabase')
cosmos_db_container_name = os.getenv('cosmosDbContainerName', 'myContainer')

app = func.FunctionApp()

@app.route(route="startSaga", auth_level=func.AuthLevel.ANONYMOUS)
def start_saga(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Orchestrator Function: Starting Saga...')

    try:
        # Simulate starting the saga
        order_data = req.get_json()
        logging.info(f"Received order data: {order_data}")

        # Call Activity Function (could be synchronous or via another Azure Function)
        # Here, we'll just simulate the call and result
        activity_result = call_activity_function(order_data)
        
        if activity_result['status'] == 'success':
            return func.HttpResponse(
                "Saga completed successfully.",
                status_code=200
            )
        else:
            # If something fails, trigger the compensating transaction
            trigger_compensation(order_data)
            return func.HttpResponse(
                "Saga failed. Compensation triggered.",
                status_code=500
            )
    except Exception as e:
        logging.error(f"Unexpected error in Saga: {e}")
        return func.HttpResponse(
            "Unexpected error occurred.",
            status_code=500
        )

def call_activity_function(order_data):
    logging.info('Calling Activity Function...')
    # Here, you would normally call another Azure Function or perform a task
    # For simplicity, we simulate a successful task
    # Return a simulated result
    return {
        'status': 'success',
        'message': 'Activity Function completed successfully.'
    }

def trigger_compensation(order_data):
    logging.info('Triggering Compensation Function...')
    try:
        # Send a message to the compensator via Service Bus
        servicebus_client = ServiceBusClient.from_connection_string(servicebus_connection_str)
        sender = servicebus_client.get_topic_sender(topic_name=topic_name)

        with sender:
            message = ServiceBusMessage(body=json.dumps(order_data))
            sender.send_messages(message)
        
        logging.info('Compensation Function triggered successfully.')
    except Exception as e:
        logging.error(f"Failed to trigger Compensation Function: {e}")
