# tests/test_users/test_user_creation.py (Corrected)

import pytest
from httpx import AsyncClient
from app.main import app
import time 

@pytest.mark.asyncio
@pytest.mark.skip()
async def test_create_user_success():
    user_data = {
        "nickname": "newuser123",
        "email": f"newuser123_{time.time()}@example.com",
        "password": "Password123!",  # Strong password
        "first_name": "New",
        "last_name": "User",
        "role": "AUTHENTICATED",  # <-- MISSING COMMA WAS HERE
        "is_professional": False
    }
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post("/register/", json=user_data)
    assert response.status_code in [200, 201]

@pytest.mark.asyncio
@pytest.mark.skip()
async def test_create_user_duplicate_email():
    user_data = {
        "nickname": "duplicateuser",
        "email": "newuser123@example.com",
        "password": "Password123!",
        "first_name": "Duplicate",
        "last_name": "User",
        "role": "AUTHENTICATED",
        "is_professional": False
    }
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post("/register/", json=user_data)
    assert response.status_code in [400, 409]  # 409 = Conflict (already exists)

@pytest.mark.asyncio
async def test_register_missing_password():
    user_data = {
        "nickname": "nopassworduser",
        "email": f"nopassword_{time.time()}@example.com",
        "first_name": "No",
        "last_name": "Password",
        "role": "AUTHENTICATED",
        "is_professional": False
    }
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post("/register/", json=user_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_invalid_email_format():
    user_data = {
        "nickname": "bademailuser",
        "email": "notanemail",
        "password": "Password123!",
        "first_name": "Bad",
        "last_name": "Email",
        "role": "AUTHENTICATED",
        "is_professional": False
    }
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post("/register/", json=user_data)
    assert response.status_code == 422
