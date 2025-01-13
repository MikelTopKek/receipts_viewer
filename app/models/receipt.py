
from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.models.base import BaseModel


class PaymentType(str, PyEnum):
    """Payment type"""
    CASH = "cash"
    CASHLESS = "cashless"


class Receipt(BaseModel):

    __tablename__ = "receipts"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    payment_type = Column(Enum(PaymentType), nullable=False, default=PaymentType.CASH.value)
    payment_amount = Column(DECIMAL(10, 2), nullable=False)
    rest_amount = Column(DECIMAL(10, 2), nullable=False)

    products = Column(JSON, nullable=False)

    user = relationship("User", back_populates="receipts")
