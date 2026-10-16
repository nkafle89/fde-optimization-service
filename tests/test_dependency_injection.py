
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.schemas import OptimizationResponse
from app.services.optimization_service import (
    get_optimization_service,
)


class FakeOptimizationService:
    def submit(self, request):
        return OptimizationResponse(
            status="accepted",
            message="Response from fake service",
        )


@pytest.fixture
def client():
    def override_optimization_service():
        return FakeOptimizationService()

    app.dependency_overrides[
        get_optimization_service
    ] = override_optimization_service

    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.pop(
            get_optimization_service,
            None,
        )


def test_optimize_uses_fake_service(client):
    request_data = {
        "demand": [100, 150],
        "capacity": [200, 100],
        "cost": [
            [2, 3],
            [4, 1],
        ],
    }

    response = client.post(
        "/api/v1/optimize",
        json=request_data,
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "accepted",
        "message": "Response from fake service",
    }
