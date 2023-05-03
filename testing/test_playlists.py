from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


# example test for reference
def test_get_character():
    response = client.get("/characters/7421")
    assert response.status_code == 200

    with open("test/characters/7421.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)
