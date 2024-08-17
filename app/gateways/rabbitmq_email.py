import logging

import pika
from pika.exceptions import AMQPChannelError, AMQPConnectionError

from app.schemas.email import MailBody
from app.services.interfaces.email_gateways import IEmailGateway


class RabbitMqEmail(IEmailGateway):
    """RabbitMQ email gateway."""

    def __init__(self, host: str = "rabbitmq", queue: str = "email_queue"):
        """Initialize the RabbitMQ email gateway."""

        self.queue = queue
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host)
            )
        except AMQPConnectionError as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")

    def send_email(self, body: MailBody):
        """Send an email using RabbitMQ."""

        try:
            channel = self.connection.channel()
            channel.queue_declare(queue=self.queue)
            channel.basic_publish(
                exchange="",
                routing_key="email_queue",
                body=body.model_dump_json().encode(),
            )
            logging.info(
                f"TO:{body.to} SUBJECT:{body.subject} BODY:{body.body}"
            )
        except AMQPChannelError as e:
            logging.error(f"Failed to send email via RabbitMQ: {e}")
        finally:
            self.connection.close()
