from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PurchaseCreate(BaseModel):
    product_id: int
    supplier_name: Optional[str] = Field(None, max_length=150)
    quantity: int = Field(..., gt=0)
    unit_cost: float = Field(..., ge=0)
    reference_no: Optional[str] = Field(None, max_length=80)
    notes: Optional[str] = Field(None, max_length=500)


class PurchaseOut(BaseModel):
    id: int
    product_id: int
    supplier_name: Optional[str]
    quantity: int
    unit_cost: float
    total_cost: float
    reference_no: Optional[str]
    notes: Optional[str]
    purchase_date: datetime
    created_by: Optional[int]

    model_config = {"from_attributes": True}
