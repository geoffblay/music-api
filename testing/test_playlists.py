from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_playlist_fail():
    response = client.get("/playlists/badtest")
    assert response.status_code == 422


# missing title
def test_post_playlist_fail():
    response = client.post(
        "/playlists",
        json={
            "artist_ids": [1, 2, 3],
        },
    )
    assert response.status_code == 422


# missing track_ids
def test_post_playlist_fail_3():
    response = client.post(
        "/playlists",
        json={
            "title": "Test Playlist with Empty Track IDs",
        },
    )
    assert response.status_code == 422
