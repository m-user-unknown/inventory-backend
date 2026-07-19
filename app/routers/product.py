from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_role
from app.models.user import UserRole
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductOut])
def list_products(
    skip: int = 0,
    limit: int = Query(default=50, le=200),
    search: Optional[str] = None,
    category: Optional[str] = None,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return product_service.list_products(
        db, skip=skip, limit=limit, search=search, category=category, active_only=not include_inactive
    )


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return product_service.get_product_or_404(db, product_id)


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _user=Depends(require_role(UserRole.admin, UserRole.manager)),
):
    return product_service.create_product(db, payload)


@router.patch("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_role(UserRole.admin, UserRole.manager)),
):
    return product_service.update_product(db, product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _user=Depends(require_role(UserRole.admin)),
):
    product_service.delete_product(db, product_id)
