from contextlib import asynccontextmanager
from time import time
from typing import Any, ClassVar, TypeVar

from sqlalchemy import BinaryExpression, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.logger import BaseLogger
from app.models.base import Base


Model = TypeVar("Model", bound=Base) # type: ignore


class Singleton(type):
    """Singleton metaclass"""

    _instances: ClassVar[dict] = {}

    def __call__(cls, *args, **kwargs):  # noqa: D102
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):
    """Interface for interacting with postgres db"""

    __engine_created = False

    def __init__(self, logger: BaseLogger, connection_string: str):
        self.logger = logger

        if not Database.__engine_created:
            self.engine = create_async_engine(
                connection_string,
                pool_recycle=3600,
                pool_size=400,
                max_overflow=100,
                pool_pre_ping=True,
                echo=False,
            )

            self.session = sessionmaker(
                class_=AsyncSession,
                bind=self.engine,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )

            Database.__engine_created = True

    @asynccontextmanager
    async def _async_session_scope(self, table_name: str, operation: str):
        """Context manager for handling database sessions"""

        async_session = self.session()
        start_time = time()

        try:
            yield async_session
            await async_session.commit()
        except Exception as e:
            await async_session.rollback()
            self.logger.log(
                {
                    "text": f"Error in {operation}",
                    "error": str(e),
                    "object": table_name,
                },
                level="error",
            )
            raise
        finally:
            await async_session.close()
            self.logger.log(
                {
                    "text": operation,
                    "time": time() - start_time,
                    "object": table_name,
                },
                level="info",
            )

    async def update(
        self,
        table: Model,
        obj_id: int,
        values: dict,
    ) -> Model | None:
        """Update object in db"""

        async with self._async_session_scope(table.__tablename__, "async_update") as session:
            query = select(table).where(table.id == obj_id)
            result = await session.execute(query)
            obj = result.scalar_one_or_none()

            if obj:
                for key, value in values.items():
                    setattr(obj, key, value)

                await session.flush()
                await session.refresh(obj)
                return obj

            return None

    async def create(self, obj: Model) -> Model:
        """Creating record in db"""

        async with self._async_session_scope(obj.__tablename__, "async_create") as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
        return obj

    async def get_or_create(
        self,
        table: type[Model],
        keys: dict[str, Any],
        defaults: dict[str, Any],
    ) -> Model | None:
        """Get existing object or create new one"""

        async with self._async_session_scope(table.__tablename__, "async_get_or_create") as session:
            query = select(table).filter_by(**keys)
            result = await session.execute(query)
            obj = result.scalars().first()

            if not obj:
                obj = table(**{**keys, **defaults})
                session.add(obj)
                await session.flush()
                await session.refresh(obj)

            return obj

    async def get(self, table: Model, *keys: BinaryExpression) -> Model | None:
        """Get object from db using expressions"""

        async with self._async_session_scope(table.__tablename__, "async_get") as session:
            query = select(table).where(*keys)
            result = await session.execute(query)
        return result.scalar()

    async def get_all(
        self,
        table: Model,
        *keys: BinaryExpression,
        orders=None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Model | None:
        """Get all objects from db using expressions"""

        async with self._async_session_scope(table.__tablename__, "async_get_all") as session:
            query = select(table).where(*keys)
            if orders is not None:
                query = query.order_by(orders)
            if limit is not None:
                query = query.limit(limit)
            if offset is not None:
                query = query.offset(offset)

            result = await session.execute(query)
        return result.scalars().all()
