import pika

# Establish a connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', port=5672, credentials=pika.credentials.PlainCredentials('guest', 'guest')))

# Create a channel
channel = connection.channel()

# Define the queue names
request_queue_name = "requestQueue"
response_queue_name = "responseQueue"

# Check if the request queue and response queue exist
try:
    channel.queue_declare(queue=request_queue_name, passive=True)
    channel.queue_declare(queue=response_queue_name, passive=True)
    print("Both Request and Response Queues are present.")
except pika.exceptions.ChannelClosedByBroker as e:
    print(f"Error: Queues are not present. Reason: {e}")
    connection.close()
    exit(1)

# Check if the queue has any consumers
request_consumers = channel.queue_declare(queue=request_queue_name).method.consumer_count
response_consumers = channel.queue_declare(queue=response_queue_name).method.consumer_count

# Assert that the number of consumers is greater than 0
assert request_consumers > 0, f"C++ S3 server is down.. Unable to consume request messages from {request_queue_name} (from C++ Client)"
assert response_consumers > 0, f"C++ Client is down.. Unable to consume response messages from {response_queue_name} (from C++ Server)"

# Close the connection
connection.close()
