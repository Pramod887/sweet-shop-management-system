from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Sweet
from ..schemas import PurchaseRequest, RestockRequest, SweetResponse
from ..sweets.service import get_sweet_by_id


def purchase_sweet(db: Session, sweet_id: int, purchase_data: PurchaseRequest) -> SweetResponse:
    sweet = get_sweet_by_id(db, sweet_id)
    
    if sweet.quantity == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sweet is out of stock"
        )
    
    if purchase_data.quantity > sweet.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {sweet.quantity}, Requested: {purchase_data.quantity}"
        )
    
    sweet.quantity -= purchase_data.quantity
    db.commit()
    db.refresh(sweet)
    
    return SweetResponse(
        id=sweet.id,
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity
    )


def restock_sweet(db: Session, sweet_id: int, restock_data: RestockRequest) -> SweetResponse:
    sweet = get_sweet_by_id(db, sweet_id)
    
    sweet.quantity += restock_data.quantity
    db.commit()
    db.refresh(sweet)
    
    return SweetResponse(
        id=sweet.id,
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity
    )

