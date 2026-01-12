from datetime import datetime, timedelta, timezone

from core import config
from jose import jwt


class TokenFunctions:

    @staticmethod
    def create_auth_token(sub: str, expire_delta: timedelta | None = None) -> str:
        data: dict = {"sub": sub}
        time = datetime.now(timezone.utc) + (
                expire_delta or timedelta(minutes=config.ACCESS_TOKEN_EXPIRY_MINUTES)
        )
        data.update({"exp": time})
        return jwt.encode(data, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)


token = TokenFunctions()
