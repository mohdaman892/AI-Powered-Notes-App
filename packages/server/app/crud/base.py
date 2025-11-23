"""
This module defines a generic `BaseCrud` class that provides common CRUD operations
for any SQLAlchemy model. It includes methods for retrieving, creating, updating,
and deleting records in the database, with support for soft deletion.

The `BaseCrud` class is designed to work with any model that inherits from the `Base`
class and includes an `is_deleted` field for soft deletion.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.engine.base import Engine
# from ..models.base import Base
from typing import Any
# from ..models.test import Test
from packages.server.app.core.session import Session



class BaseCrud:

    def __init__(self,model_type):
        self.model_type = model_type

    async def insert_record(self, session: AsyncSession, response: dict) -> str:
        in_object = self.model_type(**response)
        id = in_object.id
        in_object.created_by = "axsaxx"
        in_object.updated_by = "bhhhb"
        session.add(in_object)
        await session.commit()

        return f"Record inserted for id {id}"

    async def update_record(self, session: AsyncSession, old_object, new_object: dict) -> str:
        model_columns = [col.name for col in self.model_type.__table__.columns]
        for key, value in new_object.items():
            if key in model_columns:
                setattr(old_object, key, value)
        print(old_object.name)
        await session.commit()
        await session.refresh(old_object)

        return f"Record updated for id {new_object.get("id")}"

    async def get_records(self, session: AsyncSession, column_name: str, value:str) -> list[Any]:
        column = getattr(self.model_type, column_name)
        is_deleted = getattr(self.model_type, "is_deleted")
        fetched_objects = list(await session
                               .execute(select(self.model_type)
                               .where(column == value and is_deleted == False)))

        return fetched_objects

    async def delete_record(self, session: AsyncSession, db_object) -> str:
        setattr(db_object, "is_deleted", True)
        await session.commit()
        return f"Record deleted for id {id}"

    async def get_multi(self, session: AsyncSession, offset:int, limit:int) -> list[Any]:
        column = getattr(self.model_type, "is_deleted")
        fetched_objects = list(await session.execute(select(self.model_type).where(column == False).offset(offset).limit(limit)))
        return fetched_objects
