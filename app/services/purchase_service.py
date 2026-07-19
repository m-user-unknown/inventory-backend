from datetime import date
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.purchase import Purchase
from app.schemas.purchase import PurchaseCreate
from app.services.product_service import get_product_or_404
from app.utils.helper import compute_total
from app.utils.validation import parse_date_range, start_of_day, end_of_day


def create_purchase(db: Session, payload: PurchaseCreate, created_by: Optional[int]) -> Purchase:
    """
    Record a stock-in event: creates a Purchase row, increments product stock,
    and updates the product's cost_price to reflect the latest purchase cost.
    All three changes happen in a single DB transaction.
    """
    product = get_product_or_404(db, payload.product_id)

    total_cost = compute_total(payload.quantity, payload.unit_cost)
    purchase = Purchase(
        product_id=payload.product_id,
        supplier_name=payload.supplier_name,
        quantity=payload.quantity,
        unit_cost=payload.unit_cost,
        total_cost=total_cost,
        reference_no=payload.reference_no,
        notes=payload.notes,
        created_by=created_by,
    )

    product.quantity_in_stock += payload.quantity
    product.cost_price = payload.unit_cost  # latest cost becomes the standing cost basis

    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase


def get_purchase_or_404(db: Session, purchase_id: int) -> Purchase:
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found.")
    return purchase


def list_purchases(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    product_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> list[Purchase]:
    parse_date_range(start_date, end_date)
    query = db.query(Purchase)
    if product_id:
        query = query.filter(Purchase.product_id == product_id)
    if start_date:
        query = query.filter(Purchase.purchase_date >= start_of_day(start_date))
    if end_date:
        query = query.filter(Purchase.purchase_date <= end_of_day(end_date))
    return query.order_by(Purchase.purchase_date.desc()).offset(skip).limit(limit).all()
