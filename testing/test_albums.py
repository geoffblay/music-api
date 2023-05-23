from fastapi.testclient import TestClient
from src.api.server import app


client = TestClient(app)


def test_get_album_fail():
    response = client.get("/albums/AF")
    assert response.status_code == 422


def test_get_album_fail2():
    response = client.get("/albums/-1")
    assert response.status_code == 404
