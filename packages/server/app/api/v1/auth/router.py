"""
This module defines the routes for Setup of the FastAPI App.
"""
from http.client import HTTPException

from api.v1.auth.controller import AuthController
from core import get_session, config, utils
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
    Request
)
from fastapi.responses import JSONResponse
from schemas import BaseResponse, SignupSchema
from crud import BaseCrud
from models import User
from passlib.context import CryptContext
from jose import jwt


auth_router = APIRouter(prefix="/auth")

control_obj = AuthController()


@auth_router.post("/login")
async def login(data: SignupSchema, session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    sub = await control_obj.user_verify(data, session)
    response = JSONResponse(content={"message": "correct user"},
                            status_code=200)
    token = utils.create_auth_token(sub)
    response.set_cookie(key="access_token",
                        value=token,
                        httponly=True,
                        secure=True,
                        samesite="lax")
    if(sub is not None):
        return response
        # user = user_object
    else:
        raise HTTPException()


    # auth_token = create_auth_token(user.id)

@auth_router.post("/signup")
async def signup(data: SignupSchema, session: AsyncSession = Depends(get_session)) -> dict[str,str]:

    await control_obj.add_user(data, session)

    return {"message":"Signup successful"}







