from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr

from app.services.auth.tools import check_token_exp, decode_token

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login/", scheme_name="JWT")


def get_token_subject(
    token: str = Depends(reuseable_oauth),
) -> EmailStr:
    """Get the subject of the token, which is the user's email address."""

    token_data = decode_token(token)
    check_token_exp(token_data)
    token_subject = token_data.sub
    return token_subject
