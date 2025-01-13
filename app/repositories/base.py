from typing import Generic, TypeVar

from app.db.base import Database

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """Base class for all repository-like classes"""

    def __init__(self, model: type[ModelType], db: Database):
        self.model = model
        self.db = db
