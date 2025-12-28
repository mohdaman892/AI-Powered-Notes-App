"""
App wide response handler for standardizing API responses.
This module provides a consistent response format across all API endpoints.
"""
from http.client import responses

from fastapi.responses import JSONResponse
from utils import token
from schemas import BaseResponse
from fastapi import Response
from core import config

class Responses():
    async def success_response(self,response:Response = None, token: str = None) -> BaseResponse:
        message = {"status_code":"200"}
        if token is not None and response is not None:
            response.set_cookie(key="access_token",
                                value=token,
                                httponly=True,
                                secure=True,
                                samesite="lax",
                                max_age=config.ACCESS_TOKEN_EXPIRY_MINUTES*60)
        return BaseResponse(message="Response send successfully", success=True)

    async def failed_response(self) -> BaseResponse:
        return BaseResponse(message="Response failed to be send", success=False)

response_func = Responses()
