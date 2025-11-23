from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200

def test_best_seller_ratings():
    response = client.get("/best-seller/ratings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_user():
    response = client.post("/users/", json={"user_id": 999999})
    assert response.status_code in (200, 400)

def test_search_movie():
    response = client.get("/search/movie/toy")
    assert response.status_code == 200
