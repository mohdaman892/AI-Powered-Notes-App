"""
This module defines the `SetupController` class, which is just for testing the setup of the FastAPI App.
"""
from schemas import SignupSchema
from models import User
from crud import BaseCrud
from sqlalchemy.ext.asyncio import AsyncSession

class AuthController:

    @staticmethod
    def print_hello_world():
        return "Hello World!"

    async def user_verify(self, data: SignupSchema, session: AsyncSession):
        user_details = BaseCrud(User)
        user_object: list = await user_details.get(session, "email", data.email)
        user = None
        # print(user_objects.to_dict())
        if(user_object.verify_password(data.password)):
         return user_object.id
        else:
            return None
            # user = user_object

    async def add_user(self, data: SignupSchema, session: AsyncSession):
        user = User()
        user.email = data.email
        user.password = data.password
        user.role = "User"
        user.created_by = "System"
        user.updated_by = "System"
        crud_object = BaseCrud(User)
        object = await crud_object.insert(session, user)
