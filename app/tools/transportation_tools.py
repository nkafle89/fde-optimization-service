import math


def calculate_total_demand(demand: list[float]) -> float:
    if not demand:
        raise ValueError("Demand cannot be empty")
    if any(d < 0 for d in demand):
        raise ValueError("Demand cannot be negative")

    return sum(demand)


def check_capacity_feasibility(
        demand: list[float],
        capacity: list[float],
) -> dict:
    total_demand = calculate_total_demand(demand)
    total_capacity = sum(capacity)
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