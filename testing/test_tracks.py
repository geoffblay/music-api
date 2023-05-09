from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


# example test for reference
def test_get_track_success():
    response = client.get("/tracks/9")
    assert response.status_code == 200

    with open("testing/tracks/9.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_get_track_fail():
    response = client.get("/tracks/badtest")
    assert response.status_code == 422


# runtime less than 1
def test_post_track_fail():
    response = client.post(
        "/tracks",
        json={
            "title": "bad_post_test",
            "album_id": 0,
            "genre_id": 0,
            "runtime": -5,
            "release_date": "2023-05-09",
            "artist_ids": [0],
        },
    )
    assert response.status_code == 422


# missing release date
def test_post_track_fail_2():
    response = client.post(
        "/tracks",
        json={
            "title": "bad_post_test",
            "album_id": 0,
            "genre_id": 0,
            "runtime": -5,
            "artist_ids": [0],
        },
    )
    assert response.status_code == 422
