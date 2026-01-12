"""
This module initializes all database models for the application.

It imports all model classes to ensure they are registered with the SQLAlchemy Base.
These models define the schema for the application's database tables.
"""

from .base import Base as Base
from .multimedia import Multimedia as Multimedia
from .note import Note as Note
from .user import User as User
