import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base, get_db
from ..models import User, UserRole, Sweet
from ..main import app
from ..core.security import create_access_token

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_inventory.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db):
    from ..core.security import get_password_hash
    user = User(
        email="admin@example.com",
        password=get_password_hash("admin123"),
        role=UserRole.ADMIN
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def regular_user(db):
    from ..core.security import get_password_hash
    user = User(
        email="user@example.com",
        password=get_password_hash("user123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_token(admin_user):
    return create_access_token(data={"sub": admin_user.email, "role": admin_user.role.value})


@pytest.fixture
def user_token(regular_user):
    return create_access_token(data={"sub": regular_user.email, "role": regular_user.role.value})


@pytest.fixture
def sweet_with_stock(db, admin_user, admin_token, client):
    response = client.post(
        "/api/sweets",
        json={"name": "Chocolate Bar", "category": "Chocolate", "price": 5.99, "quantity": 10},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    return response.json()


@pytest.fixture
def sweet_out_of_stock(db, admin_user, admin_token, client):
    response = client.post(
        "/api/sweets",
        json={"name": "Gummy Bears", "category": "Gummies", "price": 3.99, "quantity": 0},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    return response.json()


def test_purchase_reduces_quantity(client, user_token, sweet_with_stock):
    sweet_id = sweet_with_stock["id"]
    initial_quantity = sweet_with_stock["quantity"]
    
    response = client.post(
        f"/api/sweets/{sweet_id}/purchase",
        json={"quantity": 3},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == initial_quantity - 3


def test_cannot_purchase_when_quantity_zero(client, user_token, sweet_out_of_stock):
    sweet_id = sweet_out_of_stock["id"]
    
    response = client.post(
        f"/api/sweets/{sweet_id}/purchase",
        json={"quantity": 1},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 400
    assert "out of stock" in response.json()["detail"].lower()


def test_cannot_purchase_more_than_available(client, user_token, sweet_with_stock):
    sweet_id = sweet_with_stock["id"]
    
    response = client.post(
        f"/api/sweets/{sweet_id}/purchase",
        json={"quantity": 100},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 400
    assert "insufficient" in response.json()["detail"].lower()


def test_admin_restock_increases_quantity(client, admin_token, sweet_with_stock):
    sweet_id = sweet_with_stock["id"]
    initial_quantity = sweet_with_stock["quantity"]
    
    response = client.post(
        f"/api/sweets/{sweet_id}/restock",
        json={"quantity": 20},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == initial_quantity + 20


def test_user_cannot_restock(client, user_token, sweet_with_stock):
    sweet_id = sweet_with_stock["id"]
    
    response = client.post(
        f"/api/sweets/{sweet_id}/restock",
        json={"quantity": 20},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403

