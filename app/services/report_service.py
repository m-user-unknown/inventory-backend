from datetime import date
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.purchase import Purchase
from app.models.sales import Sale
from app.schemas.report import (
    PurchaseReportOut,
    PurchaseReportRow,
    SalesReportOut,
    SalesReportRow,
    ProfitReportOut,
)
from app.utils.validation import parse_date_range, start_of_day, end_of_day


def sales_report(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> SalesReportOut:
    parse_date_range(start_date, end_date)
    query = (
        db.query(
            Sale.product_id,
            Product.name.label("product_name"),
            func.sum(Sale.quantity).label("total_quantity_sold"),
            func.sum(Sale.total_price).label("total_revenue"),
        )
        .join(Product, Product.id == Sale.product_id)
        .group_by(Sale.product_id, Product.name)
    )
    if start_date:
        query = query.filter(Sale.sale_date >= start_of_day(start_date))
    if end_date:
        query = query.filter(Sale.sale_date <= end_of_day(end_date))

    rows = [
        SalesReportRow(
            product_id=r.product_id,
            product_name=r.product_name,
            total_quantity_sold=r.total_quantity_sold or 0,
            total_revenue=round(r.total_revenue or 0.0, 2),
        )
        for r in query.all()
    ]
    return SalesReportOut(
        start_date=start_date,
        end_date=end_date,
        rows=rows,
        total_revenue=round(sum(r.total_revenue for r in rows), 2),
        total_quantity_sold=sum(r.total_quantity_sold for r in rows),
    )


def purchase_report(
    db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None
) -> PurchaseReportOut:
    parse_date_range(start_date, end_date)
    query = (
        db.query(
            Purchase.product_id,
            Product.name.label("product_name"),
            func.sum(Purchase.quantity).label("total_quantity_purchased"),
            func.sum(Purchase.total_cost).label("total_cost"),
        )
        .join(Product, Product.id == Purchase.product_id)
        .group_by(Purchase.product_id, Product.name)
    )
    if start_date:
        query = query.filter(Purchase.purchase_date >= start_of_day(start_date))
    if end_date:
        query = query.filter(Purchase.purchase_date <= end_of_day(end_date))

    rows = [
        PurchaseReportRow(
            product_id=r.product_id,
            product_name=r.product_name,
            total_quantity_purchased=r.total_quantity_purchased or 0,
            total_cost=round(r.total_cost or 0.0, 2),
        )
        for r in query.all()
    ]
    return PurchaseReportOut(
        start_date=start_date,
        end_date=end_date,
        rows=rows,
        total_cost=round(sum(r.total_cost for r in rows), 2),
        total_quantity_purchased=sum(r.total_quantity_purchased for r in rows),
    )


def profit_report(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> ProfitReportOut:
    """
    Approximates gross profit as revenue minus (quantity sold * product's CURRENT cost_price).
    NOTE: this is a simplification (not true FIFO/weighted-average COGS) — see caveats.
    """
    parse_date_range(start_date, end_date)
    query = (
        db.query(
            Sale.product_id,
            func.sum(Sale.quantity).label("qty"),
            func.sum(Sale.total_price).label("revenue"),
        )
        .group_by(Sale.product_id)
    )
    if start_date:
        query = query.filter(Sale.sale_date >= start_of_day(start_date))
    if end_date:
        query = query.filter(Sale.sale_date <= end_of_day(end_date))

    total_revenue = 0.0
    total_cogs = 0.0
    for row in query.all():
        product = db.query(Product).filter(Product.id == row.product_id).first()
        cost_price = product.cost_price if product else 0.0
        total_revenue += row.revenue or 0.0
        total_cogs += (row.qty or 0) * cost_price

    return ProfitReportOut(
        start_date=start_date,
        end_date=end_date,
        total_revenue=round(total_revenue, 2),
        total_cost_of_goods_sold=round(total_cogs, 2),
        gross_profit=round(total_revenue - total_cogs, 2),
    )
