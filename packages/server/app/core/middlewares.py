"""
This module defines all custom middlewares for the application.
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt,JWTError
from core import config

exclude_paths = ["/docs","/v1/auth/login","/v1/auth/signup"]
algorithm = "HS256"

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request: Request, call_next):
        path = request.url.path

        if path in exclude_paths:
            return await call_next(request)

        token = request.cookies.get("access_token")

        if not token:
            raise HTTPException(status_code=401,detail="Not Authenticated")

        try:
            payload = jwt.decode(token=token,key=config.SECRET_KEY,algorithms=config.JWT_ALGORITHM)
            request.state.user = payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or Expired Token")

        return await call_next(request)
