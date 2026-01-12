from core import config
from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware

exclude_paths = [
    "/docs",
    "/openapi.json",
    "/v1/auth/login",
    "/v1/auth/signup",
]


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if path in exclude_paths:
            return await call_next(request)

        token = request.cookies.get("access_token")

        if not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Not Authenticated"},
            )

        try:
            payload = jwt.decode(
                token,
                config.SECRET_KEY,
                algorithms=[config.JWT_ALGORITHM],
            )
            expiry_timestamp = payload.get("exp")
            current_timestamp = datetime.now().timestamp()
            if current_timestamp >= expiry_timestamp:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid or Expired Token"},
                )
            request.state.session_data = {"user_id": payload.get("sub")}
        except JWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or Expired Token"},
            )

        return await call_next(request)
