"""
This module initializes core components and utilities for the application,
including configuration, exception handling, response formatting, and database session management.
"""
from .config import config as config
from .session import get_session
from .logging_config import setup_logger
from .response import response_func as response_func
from .middlewares import CustomMiddleware as CustomMiddleware