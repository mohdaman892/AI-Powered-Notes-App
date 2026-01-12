"""
Module defines a `UserCrud` by inheriting the `BaseCrud` to add CRUD operation
for the `User` model.
"""

from models import User
from schemas import SignupSchema

from .base import BaseCrud


class UserCrud(BaseCrud[User, SignupSchema, SignupSchema]):
    """
    This class is responsible for all CRUD operations for the `User` model.
    """

    def __init__(self):
        """
        Initializes the UserCrud instance with the `User` model.
        """
        super().__init__(model=User)
