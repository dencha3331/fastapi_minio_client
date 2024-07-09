from fastapi.testclient import TestClient
from media_service.main import app

client = TestClient(app)


def test_upload_file():
    with open("test_image.png", "rb") as f:
        response = client.post("/upload", files={"file": f})
    assert response.status_code == 200
    assert "url" in response.json()
