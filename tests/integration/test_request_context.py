def test_health_returns_request_id_header(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert "x-request-id" in response.headers
