from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SaleCreate(BaseModel):
    product_id: int
    customer_name: Optional[str] = Field(None, max_length=150)
    quantity: int = Field(..., gt=0)
    unit_price: Optional[float] = Field(None, ge=0)  # if omitted, uses product's current unit_price
    reference_no: Optional[str] = Field(None, max_length=80)
    notes: Optional[str] = Field(None, max_length=500)


class SaleOut(BaseModel):
    id: int
    product_id: int
    customer_name: Optional[str]
    quantity: int
    unit_price: float
    total_price: float
    reference_no: Optional[str]
    notes: Optional[str]
    sale_date: datetime
    created_by: Optional[int]

    model_config = {"from_attributes": True}
