from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_role
from app.models.user import UserRole
from app.schemas.report import InventoryValuationOut, StockAdjustRequest, StockItemOut
from app.schemas.product import ProductOut
from app.services import stock_service

router = APIRouter(prefix="/stock", tags=["Stock"])


@router.get("", response_model=list[StockItemOut])
def get_stock_overview(low_stock_only: bool = False, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return stock_service.get_stock_overview(db, low_stock_only=low_stock_only)


@router.get("/low-stock", response_model=list[StockItemOut])
def get_low_stock(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return stock_service.get_stock_overview(db, low_stock_only=True)


@router.get("/valuation", response_model=InventoryValuationOut)
def get_inventory_valuation(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return stock_service.get_inventory_valuation(db)


@router.post("/{product_id}/adjust", response_model=ProductOut)
def adjust_stock(
    product_id: int,
    payload: StockAdjustRequest,
    db: Session = Depends(get_db),
    _user=Depends(require_role(UserRole.admin, UserRole.manager)),
):
    return stock_service.adjust_stock(db, product_id, payload.quantity_delta, payload.reason)
