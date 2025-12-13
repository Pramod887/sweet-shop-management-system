import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base, get_db
from ..main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
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


def test_register_success(client):
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_email(client):
    client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_fail_wrong_password(client):
    client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_login_fail_user_not_found(client):
    response = client.post(
        "/api/auth/login",
        data={"username": "nonexistent@example.com", "password": "testpass123"}
    )
    assert response.status_code == 401

