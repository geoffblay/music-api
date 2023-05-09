from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_artist():
    response = client.get("/artists/2")
    assert response.status_code == 200

    with open("testing/artists/get_artist2.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_artist_404():
    response = client.get("/artists/999999999")
    assert response.status_code == 404

    assert response.json() == {"detail": "Artist not found."}
