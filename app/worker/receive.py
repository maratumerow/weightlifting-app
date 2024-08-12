import logging

import pika
from pydantic import ValidationError

from app.schemas.email import MailBody


def get_channel(queue):
    connection=pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    # Create a channel
    channel=connection.channel()

    # Объявите очередь с именем hello
    channel.queue_declare(queue=queue)

    return channel

def msg_handler(ch, method, properties, body):
    """Callback function to receive messages"""
    try:
        msg = MailBody.parse_raw(body)
    except ValidationError as err:
        logging.error(
            f"Invalid message format for queue=hello, err={err}"
        )
    # -> отправляем сообщение

def main():
    queue = "hello"

    channel = get_channel(queue="hello")
    channel.basic_consume(
        queue=queue, on_message_callback=msg_handler, auto_ack=False
    )

    channel.start_consuming()


if __name__ == "__main__":
    main()

