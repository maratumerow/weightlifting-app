import logging
from email.mime.text import MIMEText
from smtplib import SMTP
from ssl import create_default_context

from app.config import settings
from app.schemas.email import MailBody


def send_email(data: MailBody):
    """Send email."""

    msg = data.model_dump()
    message = MIMEText(msg["body"], "html")
    message["From"] = settings.email.username
    message["To"] = ",".join(msg["to"])
    message["Subject"] = msg["subject"]

    ctx = create_default_context()

    try:
        with SMTP(settings.email.host, settings.email.port) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(settings.email.username, settings.email.password)
            server.send_message(message)
            server.quit()
        logging.info("Push!!!")
        return {"status": 200, "errors": None}
    except Exception as e:
        logging.info(f"error!!! {e}")
        return {"status": 500, "errors": str(e)}
