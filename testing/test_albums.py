from fastapi.testclient import TestClient
from src.api.server import app

from src.api.albums import get_score

client = TestClient(app)

def test_get_score_1():
    result = get_score("Moderate rain", "19:00", 50, "FoCUS")
    assert result == 132.75

def test_get_score_2():
    result = get_score("Sunny", "12:00", 95, "Happy")
    assert result == 380.75

def test_list_albums_fail():
    response = client.get("/albums?name=badtest11111")
    assert response.status_code == 200
    assert response.json() == []


def test_get_album_fail():
    response = client.get("/albums/AF")
    assert response.status_code == 422


def test_get_album_fail2():
    response = client.get("/albums/-1")
    assert response.status_code == 404
