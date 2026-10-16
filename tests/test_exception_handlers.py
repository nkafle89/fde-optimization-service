import pytest 
from fastapi import FastAPI
from fastapi.testclient import TestClient


from app.exceptions import (
    JobNotFoundError,
    OptimizationServiceError,
)


@pytest.fixture
def client():
    test_app = FastAPI()

    test_app.add_exception_handler(
        JobNotFoundError,
        test_job_not_found_handler
    )

    test_app.add_exception_handler(
        OptimizationServiceError,
        test_optimization_service_error_handler
    )

    @test_app.get("/test/job-not-found")
    def trigger_job_not_found():
        raise JobNotFoundError("job_999")

    @test_app.get("/test/service-error")
    def trigger_service_errror():
        raise OptimizationServiceError(
            "Database password leaked"
        )

    return TestClient(test_app)

def test_job_not_found_handler(client):
    response = client.get("/test/job-not-found")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "JOB_NOT_FOUND"
    assert "job_999" in response.json()["error"]["message"]


def test_optimization_service_error_handler(client):
    response = client.get("/test/service-error")

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "OPTIMIZATION_SERVICE_ERROR"

    assert "Database password leaked" not in response.text