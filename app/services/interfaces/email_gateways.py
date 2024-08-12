import abc

from app.schemas.email import MailBody


class IEmailGateway(abc.ABC):

    @abc.abstractmethod
    def send_email(self, body: MailBody) :
        ...