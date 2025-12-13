from sqlalchemy import Column, Integer, String, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from .database import Base


class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)


class Sweet(Base):
    __tablename__ = "sweets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)

