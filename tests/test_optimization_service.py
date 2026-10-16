from app.schemas import OptimizationRequest
from app.services.optimization_service import OptimizationService
import pytest


@pytest.mark.parametrize(
        "num_dcs, num_stores",
        [(1, 1), (2, 3), (3, 4), (5, 10)]
)
def test_service_accepts_valid_problem(num_dcs, num_stores):

    request = OptimizationRequest(
        demand=[100] * num_stores,
        capacity=[100 * num_stores] * num_dcs,
        cost=[[100] * num_stores for _ in range(num_dcs)]
    )

    service = OptimizationService()
    response = service.submit(request)

    assert response.status == "accepted"
    assert f"{num_dcs} DCs" in response.message
    assert f"{num_stores} stores" in response.message

