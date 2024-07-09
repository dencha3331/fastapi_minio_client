from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_memes():
    response = client.get("/apis/v1/memes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_meme():
    response = client.post("/apis/v1/memes", json={"title": "Test Meme", "description": "This is a test meme"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Meme"