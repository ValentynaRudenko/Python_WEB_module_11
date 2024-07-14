from unittest.mock import MagicMock, patch
from datetime import datetime
from sqlalchemy.orm import Session, sessionmaker

import pytest
from fastapi.testclient import TestClient
from main import app

from src.database.models import User, Contact
from src.services.auth import auth_service
from src.database.db import get_db, SessionLocal
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis


# # Initialize FastAPILimiter with test Redis instance
# @pytest.fixture(scope="module", autouse=True)
# async def initialize_limiter():
#     r = await redis.Redis(
#         host="localhost",
#         port=6379,
#         db=1,  # Use a different Redis DB for testing
#         encoding="utf-8",
#         decode_responses=True
#     )
#     await FastAPILimiter.init(r)

# # Fixture to create test client
# @pytest.fixture(scope="module")
# def client():
#     return TestClient(app)

# # Fixture to create a test session
# @pytest.fixture(scope="module")
# def session():
#     engine = SessionLocal()
#     TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(
        User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def test_create_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/contacts",
            json={
                "first_name": "test_first_name",
                "last_name": "test_last_name",
                "email": "test_email@example.com",
                "phone": 111111111,
                "birth_date": "2020-07-13",
                "additional_data": "test_additional_data",
                "created_at": "2024-07-13"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["first_name"] == "test_first_name"
        assert "id" in data


def test_get_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        # Assuming the contact with ID 1 exists
        response = client.get(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["first_name"] == "test_first_name"
        assert "id" in data


def test_get_contact_not_found(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/999",  # Using an ID that does not exist
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"


def test_get_contacts(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        if data:  # If there are contacts
            assert data[0]["first_name"] == "test_first_name"
            assert "id" in data[0]


def test_update_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/1",
            json={
                "first_name": "test_first_name",
                "last_name": "test_last_name",
                "email": "test_email@example.com",
                "phone": 222222222,
                "birth_date": "2020-08-13",
                "additional_data": "test_additional_data",
                "created_at": "2024-07-13"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["phone"] == 222222222
        assert "id" in data


def test_update_contact_not_found(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/999",  # Using an ID that does not exist
            json={
                "first_name": "test_first_name",
                "last_name": "test_last_name",
                "email": "testemail@example.com",
                "phone": 222222222,
                "birth_date": "2020-08-13",
                "additional_data": "updated_additional_data",
                "created_at": "2024-07-13"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"


def test_delete_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",  # Assuming the contact with ID 1 exists
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["first_name"] == "test_first_name"
        assert "id" in data


def test_repeat_delete_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",  # Using the same ID again
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"
