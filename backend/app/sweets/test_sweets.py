import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base, get_db
from ..models import User, UserRole
from ..main import app
from ..core.security import create_access_token

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sweets.db"
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


def test_admin_can_add_sweet(client, admin_token):
    response = client.post(
        "/api/sweets",
        json={
            "name": "Chocolate Bar",
            "category": "Chocolate",
            "price": 5.99,
            "quantity": 10
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Chocolate Bar"
    assert data["price"] == 5.99
    assert data["quantity"] == 10


def test_user_cannot_add_sweet(client, user_token):
    response = client.post(
        "/api/sweets",
        json={
            "name": "Chocolate Bar",
            "category": "Chocolate",
            "price": 5.99,
            "quantity": 10
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403


def test_user_can_view_sweets(client, user_token, admin_token, db):
    # Admin adds a sweet
    client.post(
        "/api/sweets",
        json={
            "name": "Chocolate Bar",
            "category": "Chocolate",
            "price": 5.99,
            "quantity": 10
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # User views sweets
    response = client.get(
        "/api/sweets",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Chocolate Bar"


def test_user_can_search_sweets(client, user_token, admin_token):
    # Admin adds multiple sweets
    client.post(
        "/api/sweets",
        json={"name": "Chocolate Bar", "category": "Chocolate", "price": 5.99, "quantity": 10},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    client.post(
        "/api/sweets",
        json={"name": "Gummy Bears", "category": "Gummies", "price": 3.99, "quantity": 20},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # User searches by name
    response = client.get(
        "/api/sweets/search?query=Chocolate",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "Chocolate" in data[0]["name"]


def test_admin_can_update_sweet(client, admin_token):
    # Add sweet
    create_response = client.post(
        "/api/sweets",
        json={"name": "Chocolate Bar", "category": "Chocolate", "price": 5.99, "quantity": 10},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    sweet_id = create_response.json()["id"]
    
    # Update sweet
    response = client.put(
        f"/api/sweets/{sweet_id}",
        json={"price": 6.99, "quantity": 15},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 6.99
    assert data["quantity"] == 15


def test_admin_can_delete_sweet(client, admin_token):
    # Add sweet
    create_response = client.post(
        "/api/sweets",
        json={"name": "Chocolate Bar", "category": "Chocolate", "price": 5.99, "quantity": 10},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    sweet_id = create_response.json()["id"]
    
    # Delete sweet
    response = client.delete(
        f"/api/sweets/{sweet_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    
    # Verify deleted
    get_response = client.get(
        "/api/sweets",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert len(get_response.json()) == 0

