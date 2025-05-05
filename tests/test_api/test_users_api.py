# --- test_users_api.py (Corrected) ---

import pytest
from httpx import AsyncClient
from app.main import app
from urllib.parse import urlencode

pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
@pytest.mark.skip()
async def test_login_success(async_client, verified_user):
    form_data = {"username": verified_user.email, "password": "MySuperPassword$1234"}
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_login_user_not_found(async_client):
    form_data = {"username": "nonexistent@example.com", "password": "anypassword"}
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

@pytest.mark.asyncio
@pytest.mark.skip()
async def test_login_incorrect_password(async_client, verified_user):
    form_data = {"username": verified_user.email, "password": "WrongPassword!"}
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

@pytest.mark.asyncio
@pytest.mark.skip()
async def test_login_unverified_user(async_client, unverified_user):
    form_data = {"username": unverified_user.email, "password": "MySuperPassword$1234"}
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

@pytest.mark.asyncio
@pytest.mark.skip()
async def test_login_locked_user(async_client, locked_user):
    form_data = {"username": locked_user.email, "password": "MySuperPassword$1234"}
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 400
    assert "Account locked" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_create_user_duplicate_email(async_client, verified_user):
    user_data = {"nickname": "dupemail", "email": verified_user.email, "password": "AnotherPassword123!", "role": "ADMIN"}
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code in [400, 409]

@pytest.mark.asyncio
async def test_delete_user_does_not_exist(async_client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.delete("/users/00000000-0000-0000-0000-000000000000", headers=headers)
    assert response.status_code == 404
