from jose import jwt
from core import config
from datetime import datetime, timezone, timedelta

class TokenFunctions:

    async def create_auth_token(self, sub: str, expire_delta: timedelta | None = None) -> str:
        data: dict = {"sub":sub}
        time = datetime.now(timezone.utc) + (expire_delta or timedelta(config.ACCESS_TOKEN_EXPIRY_MINUTES))
        data.update({"exp":time})
        return jwt.encode(data, config.SECRET_KEY ,algorithm=config.JWT_ALGORITHM)


token = TokenFunctions()