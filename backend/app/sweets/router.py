from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..core.dependencies import get_current_user, get_current_admin_user
from ..models import User
from ..schemas import SweetCreate, SweetUpdate, SweetResponse
from .service import (
    create_sweet,
    get_all_sweets,
    search_sweets,
    update_sweet,
    delete_sweet
)

router = APIRouter()


@router.post("", response_model=SweetResponse, status_code=201)
def add_sweet(
    sweet_data: SweetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return create_sweet(db, sweet_data)


@router.get("", response_model=List[SweetResponse])
def view_sweets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_sweets(db)


@router.get("/search", response_model=List[SweetResponse])
def search_sweets_endpoint(
    query: str = Query(..., description="Search term for name or category"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return search_sweets(db, query)


@router.put("/{sweet_id}", response_model=SweetResponse)
def update_sweet_endpoint(
    sweet_id: int,
    sweet_data: SweetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return update_sweet(db, sweet_id, sweet_data)


@router.delete("/{sweet_id}")
def delete_sweet_endpoint(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return delete_sweet(db, sweet_id)

