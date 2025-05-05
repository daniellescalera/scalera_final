import pytest
from httpx import AsyncClient
from app.main import app

# Test: Check if /analytics/retention returns 200 OK
@pytest.mark.asyncio
async def test_retention_status_code():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.get("/analytics/retention")
    assert response.status_code == 200

# Test: Check if the /docs endpoint is accessible (basic FastAPI health check)
@pytest.mark.asyncio
async def test_docs_accessible():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.get("/docs")
    assert response.status_code == 200

