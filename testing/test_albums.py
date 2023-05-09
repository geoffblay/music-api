from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


# example test for reference
def test_get_album_success():
    response = client.get("/albums/5")
    assert response.status_code == 200

    with open("testing/albums/5.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_get_album_fail():
    response = client.get("/albums/-10000")
    assert response.status_code == 404


def test_post_album_fail():
    response = client.post(
        "/albums",
        json={
            "title": "Station to Station",
            "release_date": "1976-01-23",
            "artists": [{"artist_id": -1}],
            "tracks": [
                {"title": "Station to Station", "artists": [{}], "runtime": 617},
            ],
            "genre_id": 3,
        },
    )
    assert response.status_code == 422


def test_post_album_fail_2():
    response = client.post(
        "/albums",
        json={
            "title": "Station to Station",
            "release_date": None,
            "artists": [{"artist_id": -1}],
            "tracks": [
                {
                    "title": "test_post_3",
                    "artists": [{"artist_id": -1}],
                    "runtime": 617,
                },
            ],
            "genre_id": 3,
        },
    )
    assert response.status_code == 422
