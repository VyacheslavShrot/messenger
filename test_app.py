import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_main_route():
    response = client.get("/app-status")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


@pytest.mark.asyncio
async def test_db_route():
    response = client.get("/db-status")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
