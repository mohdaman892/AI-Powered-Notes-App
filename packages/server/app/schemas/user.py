"""
All schemas related to User and Auth
"""


from pydantic import BaseModel


class SignupSchema(BaseModel):
    """Schema for sign-up of a User"""
    email: str
    password: str
