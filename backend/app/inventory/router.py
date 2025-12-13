from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..core.dependencies import get_current_user, get_current_admin_user
from ..models import User
from ..schemas import PurchaseRequest, RestockRequest, SweetResponse
from .service import purchase_sweet, restock_sweet

router = APIRouter()


@router.post("/{sweet_id}/purchase", response_model=SweetResponse)
def purchase_sweet_endpoint(
    sweet_id: int,
    purchase_data: PurchaseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return purchase_sweet(db, sweet_id, purchase_data)


@router.post("/{sweet_id}/restock", response_model=SweetResponse)
def restock_sweet_endpoint(
    sweet_id: int,
    restock_data: RestockRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return restock_sweet(db, sweet_id, restock_data)

