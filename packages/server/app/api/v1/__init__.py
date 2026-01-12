"""
This module initializes and configures the API v1 routers.
"""

from fastapi import APIRouter

from .auth.router import auth_router
from .notes.router import note_router, notes_router
from .setup.router import setup_router

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(setup_router, tags=["Setup"])
api_v1_router.include_router(auth_router, tags=["Auth"])
api_v1_router.include_router(note_router, tags=["Note"])
api_v1_router.include_router(notes_router, tags=["Notes"])
