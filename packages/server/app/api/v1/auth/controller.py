"""
This module defines the `AuthController` class, which is just for testing the setup of the FastAPI App.
"""

from typing import Any, Dict

from core import setup_logger
from crud import UserCrud
from fastapi import HTTPException
from models import User
from schemas import SignupSchema
from sqlalchemy.ext.asyncio import AsyncSession
from utils import token

logger = setup_logger()


class AuthController:
    """
      Controller class for handling all operations related to Auth.
    """

    def __init__(self):
        """
          Initializing Constructor method for defining crud variables etc.
        """
        self.user_crud = UserCrud()

    async def user_verify(
        self, data: SignupSchema, session: AsyncSession
    ) -> tuple[Dict[str, Any], Any]:
        """
        Function for handling the log-in of a new user and creating the cookies.
        Cookies would contain the jwt access token.

        Args:
            data: login data from the user
            session: Async DB session

        Returns:
            Cookies dict and Dictionary Response

        """
        logger.info("Inside Auth Controller, Logging in a user.")
        existing_user = await self.user_crud.get(
            session=session, field=User.email, value=data.email
        )
        if not existing_user:
            logger.info("User trying to sign-in does not exists.")
            raise HTTPException(
                status_code=503, detail="Internal Server Error. Something went wrong."
            )

        if not existing_user.verify_password(data.password):
            logger.info("User trying to sign-in has entered incorrect password.")
            raise HTTPException(
                status_code=503, detail="Internal Server Error. Something went wrong."
            )
        jwt_token = token.create_auth_token(existing_user.id)
        cookies = {"access_token": jwt_token}
        login_response = {"id": existing_user.id}
        return login_response, cookies

    async def add_user(
        self, data: SignupSchema, session: AsyncSession
    ) -> Dict[str, Any]:
        """
        Function for creating a new user in our App.

        Args:
            data: Sing-up data from the user
            session: Async DB session

        Returns:
            Sign-Up Response dictionary
        """
        logger.info("Inside Auth Controller, Creating a new user.")
        existing_user = await self.user_crud.get(
            session=session, field=User.email, value=data.email
        )
        if existing_user:
            logger.info("User trying to sign-up already exists.")
            raise HTTPException(
                status_code=503, detail="Internal Server Error. Something went wrong."
            )
        new_user_data = {"email": data.email, "password": data.password, "role": "User"}
        user_obj = await self.user_crud.insert(
            session=session, create_obj=new_user_data, unique_identifier="System"
        )
        create_user_response = {"id": user_obj.id}
        return create_user_response
