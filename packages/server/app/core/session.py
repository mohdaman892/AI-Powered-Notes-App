"""
Database session management module.
Handles creation and lifecycle of async SQLAlchemy database sessions.
"""

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from .config import config


def create_async_postgres_engine() -> AsyncEngine:
    postgres_conn: AsyncEngine = create_async_engine(config.POSTGRES_CONNECTION_URL)
    return postgres_conn


def create_async_session() -> AsyncSession:
    postgres_async_session = async_sessionmaker(
        bind=create_async_postgres_engine(), expire_on_commit=False
    )
    return postgres_async_session()


async def get_session():
    async with create_async_session() as session:
        try:
            yield session
            await session.commit()

        except:
            await session.rollback()
            raise
        finally:
            await session.close()
