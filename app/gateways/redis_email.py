import logging

import redis

from app.schemas.email import MailBody
from app.services.interfaces.email_gateways import IEmailGateway


class RedisEmail(IEmailGateway):
    """Redis email gateway."""

    def __init__(
        self,
        host: str = "redis",
        port: int = 6379,
        message_queue: str = "email_queue",
    ):
        """Initialize the Redis email gateway."""

        self.message_queue = message_queue
        try:
            self.redis_client = redis.Redis(host=host, port=port)
        except redis.ConnectionError as e:
            logging.error(f"Failed to connect to Redis: {e}")

    def send_email(self, body: MailBody) -> None:
        """Send an email using Redis."""

        try:
            self.redis_client.lpush(
                self.message_queue, body.model_dump_json().encode()
            )
            logging.info(
                f"Processed email TO:{body.to} "
                f"SUBJECT:{body.subject} "
                f"BODY:{body.body}"
            )
        except redis.RedisError as e:
            logging.error(f"Failed to send email via Redis: {e}")
