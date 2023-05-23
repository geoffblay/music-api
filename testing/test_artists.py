from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_artist():
    response = client.get("/artists/101")
    assert response.status_code == 200

    with open("testing/artists/get_artist101.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_get_artist_404():
    response = client.get("/artists/-5")
    assert response.status_code == 404

    assert response.json() == {"detail": "Artist not found"}


def test_get_artist2_404():
    # unprocessable entity
    response = client.get("/artists/af")
    assert response.status_code == 422
