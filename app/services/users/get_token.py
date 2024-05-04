from app.schemas.user import TokenInfo, UserLogin
from app.tools.security import encode_jwt


def get_token_service(user: UserLogin) -> TokenInfo:
    jwt_pyload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = encode_jwt(payload=jwt_pyload)

    return TokenInfo(access_token=token, token_type="Bearer")
