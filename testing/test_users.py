from fastapi.testclient import TestClient
from src.api.server import app


client = TestClient(app)


def test_validate_user_fail2():
    response = client.post("/users/validate", json={"username": "", "password": "test"})
    assert response.status_code == 422


def test_validate_user_fail():
    response = client.post(
        "/users/validate", json={"username": "badtest", "password": "badtest"}
    )
    assert response.status_code == 400


def test_create_user_fail():
    response = client.post("/users", json={"username": "testuser", "password": "bad"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": "Password must be at least 8 characters long and less than 72 characters long."
    }


def test_create_user_fail2():
    response = client.post("/users", json={"username": "", "password": "bad"})
    assert response.status_code == 422
