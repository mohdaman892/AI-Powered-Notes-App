"""
This module initializes and configures the API v1 routers.
"""

from fastapi import APIRouter

from .setup.router import setup_router

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(setup_router, tags=["Setup"])
