from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class StockItemOut(BaseModel):
    product_id: int
    sku: str
    name: str
    category: Optional[str]
    quantity_in_stock: int
    reorder_level: int
    is_low_stock: bool
    stock_value: float  # quantity_in_stock * cost_price

    model_config = {"from_attributes": True}


class StockAdjustRequest(BaseModel):
    quantity_delta: int  # positive to add, negative to remove
    reason: Optional[str] = None


class InventoryValuationOut(BaseModel):
    total_products: int
    total_units: int
    total_cost_value: float   # sum(quantity * cost_price)
    total_retail_value: float  # sum(quantity * unit_price)


class SalesReportRow(BaseModel):
    product_id: int
    product_name: str
    total_quantity_sold: int
    total_revenue: float


class PurchaseReportRow(BaseModel):
    product_id: int
    product_name: str
    total_quantity_purchased: int
    total_cost: float


class SalesReportOut(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    rows: list[SalesReportRow]
    total_revenue: float
    total_quantity_sold: int


class PurchaseReportOut(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    rows: list[PurchaseReportRow]
    total_cost: float
    total_quantity_purchased: int


class ProfitReportOut(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    total_revenue: float
    total_cost_of_goods_sold: float
    gross_profit: float
