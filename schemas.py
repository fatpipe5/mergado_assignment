from pydantic import BaseModel, Field, PositiveFloat
from typing import Literal

CurrencyCode = Literal["CZK", "USD", "EUR"] #povolene hodnoty

class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=120)
    price: PositiveFloat
    currency: CurrencyCode

class OrderOut(BaseModel):
    id: int
    customer_name: str
    price: float
    currency: CurrencyCode
