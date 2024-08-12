import os
import sys

import pika


def main():
    """Receive messages from the queue named hello """

    # Create a connection to the RabbitMQ server running on rabbitmq
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    # Create a channel
    channel = connection.channel()

    # Объявите очередь с именем hello
    channel.queue_declare(queue="hello")

    # Определите функцию обратного вызова для получения сообщений
    def callback(ch, method, properties, body):
        """Callback function to receive messages"""
        print(f" [x] Received {body}")

    # Потреблять сообщения из очереди с именем hello
    channel.basic_consume(
        queue="hello", on_message_callback=callback, auto_ack=True
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    # Start consuming messages
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
