import pika
from pika import connection

from app.schemas.email import MailBody
from app.services.interfaces.email_gateways import IEmailGateway


class RabbitMqEmail(IEmailGateway):
    def __init__(self, host: str="rabbitmq", queue: str = "hello" ):
        self.queue=queue
        self.connection=pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )

    def send_email(self, body: MailBody):
        channel= self.connection.channel()
        channel.queue_declare(queue=self.queue)
        channel.basic_publish(
            exchange="",
            routing_key="hello",
            body=body.json().encode()
        )
        connection.close()
