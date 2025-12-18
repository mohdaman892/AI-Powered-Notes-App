"""
This module defines a generic `BaseCrud` class that provides common CRUD operations
for any SQLAlchemy model. It includes methods for retrieving, creating, updating,
and deleting records in the database, with support for soft deletion.

The `BaseCrud` class is designed to work with any model that inherits from the `Base`
class and includes an `is_deleted` field for soft deletion.
"""
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Any


logger = logging.getLogger(__name__)

class BaseCrud:

    def __init__(self,model_type):
        self.model_type = model_type

    async def insert(self, session: AsyncSession, in_obj) -> Any:
        session.add(in_obj)
        await session.commit()
        logger.info(f"Record inserted for id {id}")

        return in_obj

    async def update(self, session: AsyncSession, old_object, new_object: dict) -> Any:
        model_columns = [col.name for col in self.model_type.__table__.columns]
        for key, value in new_object.items():
            if key in model_columns:
                setattr(old_object, key, value)
        await session.commit()
        await session.refresh(old_object)
        logger.info(f"Record updated for id {new_object.get("id")}")
        return old_object

    async def get(self, session: AsyncSession, column_name: str, value:str) -> list[Any]:
        column = getattr(self.model_type, column_name)
        is_deleted = getattr(self.model_type, "is_deleted")
        fetched_objects = (await session
                               .execute(select(self.model_type)
                               .where(column == value and is_deleted == False)))

        return fetched_objects.scalars().first()

    async def delete(self, session: AsyncSession, db_object):
        setattr(db_object, "is_deleted", True)
        await session.commit()
        logger.info(f"Record deleted for id {id}")


    async def get_multi(self, session: AsyncSession, offset:int, limit:int) -> list[Any]:
        column = getattr(self.model_type, "is_deleted")
        fetched_objects = list(await session.execute(select(self.model_type).where(column == False).offset(offset).limit(limit)))
        return fetched_objects