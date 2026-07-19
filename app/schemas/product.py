from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    sku: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=100)
    unit: str = Field(default="pcs", max_length=20)
    unit_price: float = Field(default=0.0, ge=0)
    cost_price: float = Field(default=0.0, ge=0)
    reorder_level: int = Field(default=10, ge=0)


class ProductCreate(ProductBase):
    quantity_in_stock: int = Field(default=0, ge=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=100)
    unit: Optional[str] = Field(None, max_length=20)
    unit_price: Optional[float] = Field(None, ge=0)
    cost_price: Optional[float] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class ProductOut(ProductBase):
    id: int
    quantity_in_stock: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
