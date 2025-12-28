"""
This module defines the routes for Setup of the FastAPI App.
"""
from http.client import HTTPException

from api.v1.auth.controller import AuthController
from core import get_session, config, response_func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response
)
from fastapi.responses import JSONResponse
from schemas import BaseResponse, SignupSchema
from crud import BaseCrud
from models import User


auth_router = APIRouter(prefix="/auth")

control_obj = AuthController()


@auth_router.post("/login")
async def login(response: Response, data: SignupSchema, session: AsyncSession = Depends(get_session)) -> BaseResponse:
    token = await control_obj.user_verify(data, session)
    if(token is not None):
        return await response_func.success_response(response,token)
        # user = user_object
    else:
        raise await response_func.failed_response

@auth_router.post("/signup")
async def signup(data: SignupSchema, session: AsyncSession = Depends(get_session)) -> BaseResponse:

    await control_obj.add_user(data, session)

    return await response_func.success_response()






