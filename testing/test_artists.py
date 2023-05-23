from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_artist_404():
    response = client.get("/artists/-5")
    assert response.status_code == 404

    assert response.json() == {"detail": "Artist not found"}


def test_get_artist2_404():
    # unprocessable entity
    response = client.get("/artists/af")
    assert response.status_code == 422
