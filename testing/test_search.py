from fastapi.testclient import TestClient

from src.api.server import app

client = TestClient(app)

def test_search_fail():
    response = client.get("/search/?type=badtest")
    assert response.status_code == 422

def test_search_fail_2():
    response = client.get("/search/?type=artist&name=xXXXXXXXX____XXXXXXX")
    assert response.status_code == 422

def test_search_fail_3():
    response = client.get("/search/?type=artist&limit=-1")
    assert response.status_code == 422