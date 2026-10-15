import pytest
from pydantic import ValidationError
from app.schemas import OptimizationRequest


@pytest.mark.parametrize(
    "invalid_value",
    [float("nan"), float("inf"), float("-inf")]
)
def test_non_finite_cost(invalid_value):
    problem = {
        "demand": [100, 150, 80],
        "capacity": [200, 150],
        "cost": [
            [2, 4, 5],
            [3, 1, 2]
        ]
    }

    problem["cost"][0][0] = invalid_value

    with pytest.raises(ValidationError):
        OptimizationRequest(**problem)