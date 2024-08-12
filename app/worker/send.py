import pika

# Create a connection to the RabbitMQ server running on rabbitmq
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmq")
)
# Create a channel
channel = connection.channel()

# Объявите очередь с именем hello
channel.queue_declare(queue="hello")

# Publish a message to the queue named hello
channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
print(" [x] Sent 'Hello World!'")
# Close the connection
connection.close()
