from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from typing import List, Optional
from ..models import Sweet
from ..schemas import SweetCreate, SweetUpdate, SweetResponse


def create_sweet(db: Session, sweet_data: SweetCreate) -> SweetResponse:
    db_sweet = Sweet(
        name=sweet_data.name,
        category=sweet_data.category,
        price=sweet_data.price,
        quantity=sweet_data.quantity
    )
    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)
    return SweetResponse(
        id=db_sweet.id,
        name=db_sweet.name,
        category=db_sweet.category,
        price=db_sweet.price,
        quantity=db_sweet.quantity
    )


def get_all_sweets(db: Session) -> List[SweetResponse]:
    sweets = db.query(Sweet).all()
    return [
        SweetResponse(
            id=sweet.id,
            name=sweet.name,
            category=sweet.category,
            price=sweet.price,
            quantity=sweet.quantity
        )
        for sweet in sweets
    ]


def search_sweets(db: Session, query: str) -> List[SweetResponse]:
    sweets = db.query(Sweet).filter(
        or_(
            Sweet.name.ilike(f"%{query}%"),
            Sweet.category.ilike(f"%{query}%")
        )
    ).all()
    return [
        SweetResponse(
            id=sweet.id,
            name=sweet.name,
            category=sweet.category,
            price=sweet.price,
            quantity=sweet.quantity
        )
        for sweet in sweets
    ]


def get_sweet_by_id(db: Session, sweet_id: int) -> Sweet:
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    return sweet


def update_sweet(db: Session, sweet_id: int, sweet_data: SweetUpdate) -> SweetResponse:
    sweet = get_sweet_by_id(db, sweet_id)
    
    if sweet_data.name is not None:
        sweet.name = sweet_data.name
    if sweet_data.category is not None:
        sweet.category = sweet_data.category
    if sweet_data.price is not None:
        sweet.price = sweet_data.price
    if sweet_data.quantity is not None:
        sweet.quantity = sweet_data.quantity
    
    db.commit()
    db.refresh(sweet)
    
    return SweetResponse(
        id=sweet.id,
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity
    )


def delete_sweet(db: Session, sweet_id: int) -> dict:
    sweet = get_sweet_by_id(db, sweet_id)
    db.delete(sweet)
    db.commit()
    return {"message": "Sweet deleted successfully"}

