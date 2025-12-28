"""
App wide configuration for all the environments.
This module handles loading of environment variables for the application.
"""

import os
from typing import cast

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Configurations class that loads environment variables.
    Provides type-safe access to environment variables used across the application.
    """

    ENV: str = cast(str, os.getenv("ENV", "development"))
    POSTGRES_CONNECTION_URL:str = cast(str, os.getenv("POSTGRES_CONNECTION_URL", ""))
    SECRET_KEY:str = cast(str, os.getenv("SECRET_KEY", ""))
    ACCESS_TOKEN_EXPIRY_MINUTES: int = cast(int, os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES",0))
    JWT_ALGORITHM: str = cast(int, os.getenv("JWT_ALGORITHM",""))

    class Config:
        """
        Load env from .env file and ignore extra env variables.
        """

        env_file = ".env"
        extra = "ignore"


config = Config()
