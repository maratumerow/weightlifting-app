import logging

from app.schemas.email import MailBody
from app.tools.mailer import send_email


def push_user_email_service(mail_body: MailBody) -> None:
    """Push email to the queue."""
    send_email(mail_body)
    logging.info(f"Push email for email={mail_body.to}")
