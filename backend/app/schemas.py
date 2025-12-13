from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import UserRole


# User Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    role: UserRole

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Sweet Schemas
class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int = 0


class SweetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class SweetResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    quantity: int

    class Config:
        from_attributes = True


# Inventory Schemas
class PurchaseRequest(BaseModel):
    quantity: int = 1


class RestockRequest(BaseModel):
    quantity: int

