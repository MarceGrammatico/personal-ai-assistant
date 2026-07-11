from datetime import datetime

from app.core.config import settings


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == settings.APP_NAME
    assert data["version"] == settings.APP_VERSION

    assert "timestamp" in data

    datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
