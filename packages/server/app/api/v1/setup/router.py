"""
This module defines the routes for Setup of the FastAPI App.
"""

from api.v1.setup.controller import SetupController
from core import config, get_session
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

setup_router = APIRouter(prefix="/setup")


@setup_router.get("")
async def test_setup(request: Request, session: AsyncSession = Depends(get_session)):
    """
    Testing Setup.

    Args:

        request: Incoming HTTP request object.

    Returns:

        String Response.
    """

    return SetupController().print_hello_world()
