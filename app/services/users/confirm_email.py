import logging

from jose import JWTError

from app.services.auth.tools.token import check_token_exp, decode_token
from app.services.interfaces.users import IConfirmEmailService


class ConfirmEmailService(IConfirmEmailService):
    """Service to confirm a user email."""

    def __call__(self, token: str) -> dict[str, str]:
        """Confirm a user email."""

        try:
            token_data = decode_token(token)
            check_token_exp(token_data)
            email: str = token_data.sub
        except JWTError:
            logging.error(f"Token={token} is invalid")
            return {"message": "Invalid token"}

        success = self.user_repo.activate_user(email=email)

        if success:
            logging.info(f"User with EMAIL={email} confirmed")
            return {"message": "Email confirmed"}
        else:
            logging.info(f"User with EMAIL={email} not confirmed")
            return {"message": "Email not confirmed"}
