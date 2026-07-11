from fastapi import APIRouter

from app.core.exceptions import ResourceNotFoundException


def test_app_exception_handler(app, client):
    router = APIRouter()

    @router.get("/test-error")
    async def test_error():
        raise ResourceNotFoundException("Test resource not found")

    app.include_router(router)

    response = client.get("/test-error")

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False

    assert body["error"]["code"] == "RESOURCE_NOT_FOUND"

    assert body["error"]["message"] == "Test resource not found"

    assert body["request_id"] is not None
