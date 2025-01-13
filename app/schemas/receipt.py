from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, validator

from app.models.receipt import PaymentType


class ProductCreate(BaseModel):
    name: str
    price: Decimal
    quantity: int


class ProductResponse(ProductCreate):
    total: Decimal


class PaymentCreate(BaseModel):
    type: str
    amount: Decimal

    @validator("type")
    def validate_type(cls, v):
        if v not in ["cash", "cashless"]:
            raise ValueError("Payment type must be either cash or cashless")
        return v


class ReceiptCreate(BaseModel):
    products: list[ProductCreate]
    payment: PaymentCreate


class ReceiptResponse(BaseModel):
    id: int
    products: list[ProductResponse]
    payment_type: PaymentType
    payment_amount: Decimal
    total_amount: Decimal
    rest_amount: Decimal
    created: datetime
