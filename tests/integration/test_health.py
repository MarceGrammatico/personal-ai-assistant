from datetime import datetime

from fastapi.testclient import TestClient

from app.core.config import settings
from app.factory import create_application

client = TestClient(create_application())


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == settings.APP_NAME
    assert data["version"] == settings.APP_VERSION

    assert "timestamp" in data

    datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
