
import pytest

from app.tools.transportation_tools import (
    calculate_total_demand,
    check_capacity_feasibility,
)


def test_calculate_total_demand():
    assert calculate_total_demand([100, 150, 80]) == 330


def test_calculate_total_demand_empty():
    with pytest.raises(ValueError, match="cannot be empty"):
        calculate_total_demand([])


def test_calculate_total_demand_negative():
    with pytest.raises(ValueError, match="cannot be negative"):
        calculate_total_demand([100, -50])


def test_calculate_total_demand_nan():
    with pytest.raises(ValueError, match="must be finite"):
        calculate_total_demand([100, float("nan")])


def test_calculate_total_demand_infinity():
    with pytest.raises(ValueError, match="must be finite"):
        calculate_total_demand([100, float("inf")])


def test_check_capacity_feasibility_sufficient():
    result = check_capacity_feasibility(
        demand=[100, 150, 80],
        capacity=[200, 200],
    )

    assert result == {
        "total_demand": 330,
        "total_capacity": 400,
        "is_feasible": True,
        "capacity_shortfall": 0,
        "remaining_capacity": 70,
    }


def test_check_capacity_feasibility_insufficient():
    result = check_capacity_feasibility(
        demand=[100, 150, 80],
        capacity=[200, 100],
    )

    assert result == {
        "total_demand": 330,
        "total_capacity": 300,
        "is_feasible": False,
        "capacity_shortfall": 30,
        "remaining_capacity": 0,
    }


def test_check_capacity_feasibility_exact():
    result = check_capacity_feasibility(
        demand=[100, 150, 80],
        capacity=[200, 130],
    )

    assert result["is_feasible"] is True
    assert result["capacity_shortfall"] == 0
    assert result["remaining_capacity"] == 0


def test_check_capacity_feasibility_negative_capacity():
    with pytest.raises(ValueError, match="cannot be negative"):
        check_capacity_feasibility(
            demand=[100],
            capacity=[200, -50],
        )


def test_check_capacity_feasibility_empty_capacity():
    with pytest.raises(ValueError, match="cannot be empty"):
        check_capacity_feasibility(
            demand=[100],
            capacity=[],
        )


def test_check_capacity_feasibility_nan_capacity():
    with pytest.raises(ValueError, match="must be finite"):
        check_capacity_feasibility(
            demand=[100],
            capacity=[float("nan")],
        )
