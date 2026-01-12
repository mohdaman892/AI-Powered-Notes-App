"""
This module defines the routes for Auth Service of the FastAPI App.
"""

from api.v1.auth.controller import AuthController
from core import Response, config, get_session
from fastapi import APIRouter, Depends
from schemas import BaseResponse, SignupSchema
from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login", response_model=BaseResponse)
async def login(data: SignupSchema, session: AsyncSession = Depends(get_session)):
    """

    Router method for Login of any user.

    Args:

        data: Payload containing the user sing-in data.
        session: Async DB session.

    Returns:

        HTTP Response containing success message and cookies.
    """
    response, cookies = await AuthController().user_verify(data, session)
    return Response.success(
        message="User Logged-In Successfully.",
        status_code=200,
        body=response,
        cookies=cookies,
    )


@auth_router.post("/logout", response_model=BaseResponse)
async def logout():
    """

    Router method for Log-out of any user.

    Returns:

        HTTP Response containing success message and no cookies
    """
    response = Response.success(message="Signed out successfully.")
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return response


@auth_router.post("/signup", response_model=BaseResponse)
async def signup(data: SignupSchema, session: AsyncSession = Depends(get_session)):
    """

    Router method for creating a new user.

    Args:

        data: Payload containing the user sing-up data.
        session: Async DB session.

    Returns:

        HTTP Response containing success message and user_id.
    """

    response = await AuthController().add_user(data, session)
    return Response.success(
        message="User Sign-Up was Successful.", status_code=200, body=response
    )
