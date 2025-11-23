"""
This module initializes core components and utilities for the application,
including configuration, exception handling, response formatting, and database session management.
"""
from .config import config as config
from .session import get_session