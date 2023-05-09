from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_search1():
    response = client.get("/search/?name=bowie")
    assert response.status_code == 200

    with open("testing/search/search_bowie.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_artist_404():
    response = client.get("/search/?name=skrillex")
    assert response.status_code == 404

    assert response.json() == {"detail": "No results."}
