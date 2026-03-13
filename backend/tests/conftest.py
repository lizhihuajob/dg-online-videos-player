import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

from app.main import app
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    from app.main import app
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def test_user(client, db):
    response = client.post(
        "/register",
        json={"username": "testuser", "email": "test@example.com", "password": "testpass123"}
    )
    assert response.status_code == 200
    return response.json()

@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
