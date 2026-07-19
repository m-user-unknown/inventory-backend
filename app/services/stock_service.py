from typing import Optional

from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.report import InventoryValuationOut, StockItemOut
from app.services.product_service import get_product_or_404


def get_stock_overview(db: Session, low_stock_only: bool = False) -> list[StockItemOut]:
    query = db.query(Product).filter(Product.is_active.is_(True))
    products = query.order_by(Product.name).all()

    result = []
    for p in products:
        is_low = p.quantity_in_stock <= p.reorder_level
        if low_stock_only and not is_low:
            continue
        result.append(
            StockItemOut(
                product_id=p.id,
                sku=p.sku,
                name=p.name,
                category=p.category,
                quantity_in_stock=p.quantity_in_stock,
                reorder_level=p.reorder_level,
                is_low_stock=is_low,
                stock_value=round(p.quantity_in_stock * p.cost_price, 2),
            )
        )
    return result


def adjust_stock(db: Session, product_id: int, quantity_delta: int, reason: Optional[str] = None) -> Product:
    """
    Manual stock correction (e.g. damage, recount, shrinkage) that is NOT a purchase or sale.
    Positive delta adds stock, negative delta removes it. Never allows stock to go negative.
    """
    from fastapi import HTTPException, status

    product = get_product_or_404(db, product_id)
    new_quantity = product.quantity_in_stock + quantity_delta
    if new_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Adjustment would result in negative stock ({new_quantity}).",
        )
    product.quantity_in_stock = new_quantity
    db.commit()
    db.refresh(product)
    return product


def get_inventory_valuation(db: Session) -> InventoryValuationOut:
    products = db.query(Product).filter(Product.is_active.is_(True)).all()
    total_units = sum(p.quantity_in_stock for p in products)
    total_cost_value = round(sum(p.quantity_in_stock * p.cost_price for p in products), 2)
    total_retail_value = round(sum(p.quantity_in_stock * p.unit_price for p in products), 2)
    return InventoryValuationOut(
        total_products=len(products),
        total_units=total_units,
        total_cost_value=total_cost_value,
        total_retail_value=total_retail_value,
    )
