from jose import jwt
from core import config


class UtilFunctions:

    def create_auth_token(self, sub: str):
        return jwt.encode({"sub":sub}, config.SECRET_KEY ,algorithm="HS256")


utils = UtilFunctions()