from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_role
from app.models.user import User, UserRole
from app.schemas.purchase import PurchaseCreate, PurchaseOut
from app.services import purchase_service

router = APIRouter(prefix="/purchases", tags=["Purchases"])


@router.get("", response_model=list[PurchaseOut])
def list_purchases(
    skip: int = 0,
    limit: int = Query(default=50, le=200),
    product_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return purchase_service.list_purchases(
        db, skip=skip, limit=limit, product_id=product_id, start_date=start_date, end_date=end_date
    )


@router.get("/{purchase_id}", response_model=PurchaseOut)
def get_purchase(purchase_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return purchase_service.get_purchase_or_404(db, purchase_id)


@router.post("", response_model=PurchaseOut, status_code=status.HTTP_201_CREATED)
def create_purchase(
    payload: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin, UserRole.manager, UserRole.staff)),
):
    return purchase_service.create_purchase(db, payload, created_by=current_user.id)
