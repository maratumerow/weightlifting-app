import abc

from app.schemas.email import MailBody


class IEmailGateway(abc.ABC):
    """Interface for sending emails."""

    @abc.abstractmethod
    def send_email(self, body: MailBody) -> None:
        """Send an email."""
