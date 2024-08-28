import logging
import re

import pika
from pika.exceptions import AMQPChannelError, AMQPConnectionError

from app.schemas.email import MailBody
from app.services.interfaces.email_gateways import IEmailGateway


class RabbitMqEmail(IEmailGateway):
    def __init__(
        self, host: str = "localhost", message_queue: str = "email_queue"
    ):
        """Initialize the RabbitMQ email gateway."""
        self.message_queue = message_queue
        self.connection = None
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host)
            )
        except (AMQPConnectionError, AMQPChannelError) as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")

    def send_email(self, body: MailBody) -> None:
        """Send an email using RabbitMQ."""
        if not self.connection or self.connection.is_closed:
            logging.error("No connection to RabbitMQ.")
            return

        try:
            channel = self.connection.channel()
            channel.queue_declare(queue=self.message_queue)
            channel.basic_publish(
                exchange="",
                routing_key=self.message_queue,
                body=str(body).encode(),
            )
            logging.info("Email sent successfully.")
        except (AMQPConnectionError, AMQPChannelError) as e:
            logging.error(f"Failed to send email: {e}")
