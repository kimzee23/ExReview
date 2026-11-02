from fastapi.testclient import TestClient

from exreview.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to ExReview API",
                               "status": "Application is running"}