import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.fixture
def valid_problem():
    return {
        "demand": [100, 150, 80],
        "capacity": [200, 150],
        "cost": [
            [2, 4, 5],
            [3, 1, 2],
        ]
    }

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_valid_optimiztion_request(valid_problem):
    response = client.post(
        "/api/v1/optimize",
        json=valid_problem,
    )

    assert response.status_code == 202
    assert response.json()["status"] == "accepted"


def test_negative_demand(valid_problem):
    valid_problem["demand"][0] = -100

    response = client.post(
        "/api/v1/optimize",
        json=valid_problem,
    )

    assert response.status_code == 422


def test_insufficient_capacity(valid_problem):
    valid_problem["capacity"] = [100, 100]

    response = client.post(
        "/api/v1/optimize",
        json=valid_problem,
    )

    assert response.status_code == 422


def test_wrong_cost_dimensions(valid_problem):
    valid_problem["cost"] = [[2, 4, 5]]

    response = client.post(
        "/api/v1/optimize",
        json=valid_problem,
    )

    assert response.status_code == 422


def test_negative_capacity(valid_problem):
    valid_problem['capacity'][0] = -100
    
    response = client.post(
        "/api/v1/optimize",
        json=valid_problem,
    )

    assert response.status_code == 422

def test_negative_transportation_cost(valid_problem):
    valid_problem['cost'][0][0] =  -1

    response = client.post(
        "/api/v1/optimize",
        json=valid_problem,
    )

    assert response.status_code == 422


def test_empty_demand_list(valid_problem):
    valid_problem['demand'] = []

    response = client.post(
        "/api/v1/optimize",
        json=valid_problem,
    )

    assert response.status_code == 422


def test_missing_required_field(valid_problem):
    valid_problem.pop('cost')

    response = client.post(
        "/api/v1/optimize",
        json=valid_problem,
    )

    assert response.status_code == 422

def test_matrix_dimension(valid_problem):
    valid_problem['cost'] = [[2,1,3], [2,3]]

    response = client.post(
        "/api/v1/optimize",
        json=valid_problem,
    )

    assert response.status_code == 422