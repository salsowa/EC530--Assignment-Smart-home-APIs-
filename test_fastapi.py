from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"

def test_get_non_existent_user():
    response = client.get("/users/non-existing-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_house():
    response = client.post("/houses/", json={"name": "Smart Home", "metadata": {}})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Smart Home"
