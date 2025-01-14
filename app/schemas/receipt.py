from datetime import datetime
from decimal import Decimal
import enum
from pydantic import BaseModel


class PaymentType(str, enum.Enum):
    """Possible types for product payment"""
    CASH = "cash"
    CASHLESS = "cashless"


class ProductCreate(BaseModel):
    """Model for receipt`s product"""
    name: str
    price: Decimal
    quantity: int


class ProductData(ProductCreate):
    """Model with product info"""
    total: Decimal


class PaymentCreate(BaseModel):
    """Model with payment info"""
    payment_type: PaymentType
    amount: Decimal


class ReceiptCreateDTO(BaseModel):
    """DTO for receipt"""
    products: list[ProductCreate]
    payment: PaymentCreate


class ReceiptResponse(BaseModel):
    """Model for selected receipt info response"""
    id: int
    products: list[ProductData]
    payment_type: PaymentType
    payment_amount: Decimal
    total_amount: Decimal
    rest_amount: Decimal
    created: datetime
