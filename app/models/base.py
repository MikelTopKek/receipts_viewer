from sqlalchemy import Column, Integer, MetaData, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)


class BaseModel(Base):
    """Base class for all models"""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(postgresql.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated = Column(
        postgresql.TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
