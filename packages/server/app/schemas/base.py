"""
Base response model definition.
"""

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseResponse(BaseModel, Generic[T]):
    """
    Base pydantic model for all responses.
    """

    message: str
    success: bool
    details: Optional[T] = None
