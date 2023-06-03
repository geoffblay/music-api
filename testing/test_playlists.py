from fastapi.testclient import TestClient

from src.api.server import app

import json

from src.api.playlists import get_score

client = TestClient(app)

def test_generate_score():
    result = get_score("Clear", "13:00", 80, "chill")
    assert result == 308.5

def test_generate_score_2():
    result = get_score("Heavy snow", "01:00", 5, "heartbroken")
    assert result == 10


def test_get_playlist_fail():
    response = client.get("/playlists/badtest")
    assert response.status_code == 422

def test_get_playlist_fail_2():
    response = client.get("/playlists/-1")
    assert response.status_code == 422

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

def test_delete_playlist_fail():
    response = client.delete("/playlists/badtest")
    assert response.status_code == 422

def test_delete_track_from_playlist_fail():
    response = client.delete("/playlists/badtest/tracks/1")
    assert response.status_code == 422

def test_delete_track_from_playlist_fail_2():
    response = client.delete("/playlists/1/tracks/badtest")
    assert response.status_code == 422

def test_create_fail():
    response = client.get("/playlists/create/?location=xxxxxxxxxx")
    assert response.status_code == 422

def test_create_fail_2():
    response = client.get("/playlists/create/?location=New%20York&vibe=downbad")
    assert response.status_code == 422

def test_create_fail_3():
    response = client.get("/playlists/create/?location=New%20York&vibe=chill&num_tracks=-1")
    assert response.status_code == 422

def test_add_track_to_playlist_fail():
    response = client.put("/playlists/badtest/tracks/1")
    assert response.status_code == 405

def test_add_track_to_playlist_fail_2():
    response = client.put("/playlists/1/tracks/badtest")
    assert response.status_code == 405



