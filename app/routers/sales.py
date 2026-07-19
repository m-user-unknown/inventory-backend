from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_role
from app.models.user import User, UserRole
from app.schemas.sales import SaleCreate, SaleOut
from app.services import sales_service

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.get("", response_model=list[SaleOut])
def list_sales(
    skip: int = 0,
    limit: int = Query(default=50, le=200),
    product_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return sales_service.list_sales(
        db, skip=skip, limit=limit, product_id=product_id, start_date=start_date, end_date=end_date
    )


@router.get("/{sale_id}", response_model=SaleOut)
def get_sale(sale_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return sales_service.get_sale_or_404(db, sale_id)


@router.post("", response_model=SaleOut, status_code=status.HTTP_201_CREATED)
def create_sale(
    payload: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin, UserRole.manager, UserRole.staff)),
):
    return sales_service.create_sale(db, payload, created_by=current_user.id)
