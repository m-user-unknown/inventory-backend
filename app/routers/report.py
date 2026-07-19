from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.schemas.report import ProfitReportOut, PurchaseReportOut, SalesReportOut
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/sales", response_model=SalesReportOut)
def get_sales_report(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return report_service.sales_report(db, start_date=start_date, end_date=end_date)


@router.get("/purchases", response_model=PurchaseReportOut)
def get_purchase_report(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return report_service.purchase_report(db, start_date=start_date, end_date=end_date)


@router.get("/profit", response_model=ProfitReportOut)
def get_profit_report(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return report_service.profit_report(db, start_date=start_date, end_date=end_date)
