from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


# example test for reference
def test_get_album_success():
    response = client.get("/albums/4")
    assert response.status_code == 200

    with open("test/albums/4.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_get_album_fail():
    response = client.get("/albums/-10000")
    assert response.status_code == 404
