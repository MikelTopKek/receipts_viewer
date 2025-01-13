from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, String

from app.models.base import BaseModel


class User(BaseModel):
    """Model with information about users"""

    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    receipts = relationship("Receipt", back_populates="user", cascade="all, delete-orphan")
