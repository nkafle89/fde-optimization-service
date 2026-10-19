import math


def sum_nonnegative_values(
    values: list[float],
    field_name: str,
) -> float:
    if not values:
        raise ValueError(f"{field_name} cannot be empty")

    if any(not math.isfinite(v) for v in values):
        raise ValueError(f"{field_name} must be finite")

    if any(v < 0 for v in values):
        raise ValueError(f"{field_name} cannot be negative")

    return sum(values)


def calculate_total_demand(demand: list[float]) -> float:
    return sum_nonnegative_values(demand, "Demand")


def check_capacity_feasibility(
    demand: list[float],
    capacity: list[float],
) -> dict:
    total_demand = calculate_total_demand(demand)
    total_capacity = sum_nonnegative_values(
        capacity, "Capacity"
    )

    return {
        "total_demand": total_demand,
        "total_capacity": total_capacity,
        "is_feasible": total_capacity >= total_demand,
        "capacity_shortfall": max(
            0, total_demand - total_capacity
        ),
        "remaining_capacity": max(
            0, total_capacity - total_demand
        ),
    }
