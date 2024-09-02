import logging
import time

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

        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                self.redis_client.lpush(
                    self.message_queue, body.model_dump_json().encode()
                )
                logging.info(f"Processed email TO:{body.to}")
                return
            except redis.RedisError as e:
                logging.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    logging.error(
                        f"Failed to send email via Redis"
                        f"after {max_retries} attempts: {e}"
                    )
