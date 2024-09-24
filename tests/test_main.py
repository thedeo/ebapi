import pytest
from fastapi.testclient import TestClient

from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_openapi_url():
    assert app.openapi_url == "/openapi.json"

def test_app_metadata(client):
    response = client.get("/docs")
    assert response.status_code == 200
    assert "EBapi - Swagger UI" in response.text