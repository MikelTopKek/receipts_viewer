import enum
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, model_validator


class PaymentType(str, enum.Enum):
    """Possible types for product payment"""
    CASH = "cash"
    CASHLESS = "cashless"


class ProductCreate(BaseModel):
    """Model for receipt's product"""
    name: str
    price: Decimal
    quantity: int

    @model_validator(mode='after')
    def validate(self) -> 'ProductCreate':
        if self.price <= 0:
            raise ValueError("Price must be greater than 0")
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        return self


class ProductData(ProductCreate):
    """Model with product info"""
    total: Decimal


class PaymentCreate(BaseModel):
    """Model with payment info"""
    payment_type: PaymentType
    amount: Decimal

    @model_validator(mode='after')
    def validate(self) -> 'PaymentCreate':
        if self.amount <= 0:
            raise ValueError("Amount must be greater than 0")
        return self


class ReceiptCreateDTO(BaseModel):
    """DTO for receipt"""
    products: list[ProductCreate]
    payment: PaymentCreate


class ReceiptResponse(BaseModel):
    """Model for selected receipt info response"""
    id: int
    public_id: str
    products: list[ProductData]
    payment_type: PaymentType
    payment_amount: Decimal
    total_amount: Decimal
    rest_amount: Decimal
    created: datetime


class ReceiptFilter(BaseModel):
    """Filters for db request for getting receipts data"""
    date_from: date | None = None
    date_to: date | None = None
    min_amount: Decimal | None = None
    max_amount: Decimal | None = None
    payment_type: str | None = None
