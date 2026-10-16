from app.schemas import OptimizationRequest
from app.services.optimization_service import OptimizationService


def test_service_accepts_valid_problem():
    request = OptimizationRequest(
        demand=[100, 150, 80],
        capacity=[200, 150],
        cost=[
            [2, 1, 5],
            [3, 1, 2]
        ]
    )

    service = OptimizationService()
    response = service.submit(request)

    assert response.status == "accepted"
    assert "2 DCs" in response.message
    assert "3 stores" in response.message

