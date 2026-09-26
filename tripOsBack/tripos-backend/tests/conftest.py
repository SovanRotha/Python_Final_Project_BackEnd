import os

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["JWT_SECRET_KEY"] = "test-only-secret-key-with-more-than-32-bytes"

import pytest
from fastapi.testclient import TestClient

from app.core.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "traveler@example.com", "password": "secure-pass-123", "full_name": "Traveler"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "traveler@example.com", "password": "secure-pass-123"},
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}