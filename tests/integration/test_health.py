from fastapi.testclient import TestClient

from app.factory import create_application


app = create_application()

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }
