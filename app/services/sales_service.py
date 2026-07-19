from datetime import date
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.sales import Sale
from app.schemas.sales import SaleCreate
from app.services.product_service import get_product_or_404
from app.utils.helper import compute_total
from app.utils.validation import ensure_positive_stock, parse_date_range, start_of_day, end_of_day


def create_sale(db: Session, payload: SaleCreate, created_by: Optional[int]) -> Sale:
    """
    Record a stock-out event: validates sufficient stock, creates a Sale row,
    and decrements product stock. All changes happen in a single DB transaction.
    """
    product = get_product_or_404(db, payload.product_id)
    ensure_positive_stock(product.quantity_in_stock, payload.quantity)

    unit_price = payload.unit_price if payload.unit_price is not None else product.unit_price
    total_price = compute_total(payload.quantity, unit_price)

    sale = Sale(
        product_id=payload.product_id,
        customer_name=payload.customer_name,
        quantity=payload.quantity,
        unit_price=unit_price,
        total_price=total_price,
        reference_no=payload.reference_no,
        notes=payload.notes,
        created_by=created_by,
    )

    product.quantity_in_stock -= payload.quantity

    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale


def get_sale_or_404(db: Session, sale_id: int) -> Sale:
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found.")
    return sale


def list_sales(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    product_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> list[Sale]:
    parse_date_range(start_date, end_date)
    query = db.query(Sale)
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    if start_date:
        query = query.filter(Sale.sale_date >= start_of_day(start_date))
    if end_date:
        query = query.filter(Sale.sale_date <= end_of_day(end_date))
    return query.order_by(Sale.sale_date.desc()).offset(skip).limit(limit).all()
