from fastapi.testclient import TestClient

from app.factory import create_application


def test_health_returns_request_id_header():
    app = create_application()

    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert "x-request-id" in response.headers
