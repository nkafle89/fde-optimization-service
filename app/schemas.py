from pydantic import BaseModel, Field, model_validator
import math
from enum import Enum


class OptimizationRequest(BaseModel):
    demand: list[float] = Field(min_length=1)
    capacity: list[float] = Field(min_length=1)
    cost: list[list[float]]

    @model_validator(mode="after")
    def validate_problem(self):
        """
        1. Check that all demand values are nonnegative.
        2. Check that all capacity values are nonnegative.
        3. Check that all costs are finite and nonnegative.
        4. Check cost matrix dimensions.
        5. Check total capacity >= total demand.
        6. Reject NaN and infinity in all numeric inputs.
        """

        if any(d < 0 for d in self.demand):
            raise ValueError("Demand cannot be negative")

        if any(not math.isfinite(v) for v in self.demand):
            raise ValueError("Demand cannot be inifnite")

        if any(c < 0 for c in self.capacity):
            raise ValueError("Capacity cannot be negative")

        if any(not math.isfinite(c) for c in self.capacity):
            raise ValueError("Capacity must be finite")

        if any( not math.isfinite(v) for row in self.cost for v in row):
            raise ValueError("Cost must be finite")

        if any(v < 0 for row in self.cost for v in row):
            raise ValueError("Cost cannot be negative")

        num_dcs = len(self.capacity)
        num_stores = len(self.demand)

        if len(self.cost) != num_dcs:
            raise ValueError("Cost matix dont have cost from all DC")

        if any(len(v) != num_stores for v in self.cost):
            raise ValueError("Cost matrix dont have cost to all stores")


        if sum(self.capacity) < sum(self.demand):
            raise ValueError("Capacity is less than total demand")

        return self

class JobStatus(str, Enum):
    ACCEPTED = "accepted"
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"


class SolverStatus(str, Enum):
    OPTIMAL = "optimal"
    FEASIBLE_TIME_LIMIT = "feasible_time_limit"
    INFEASIBLE = "infeasible"
    NO_SOLUTION = "no_solution"
    ERROR = "error"


class OptimizationResult(BaseModel):
    solver_status: SolverStatus

    objective_value: float | None = None
    best_bound: float | None = None
    optimality_gap: float | None = Field(default=None, ge=0)
    solve_time_seconds: float | None = Field(default=None, ge=0)

    @model_validator(mode='after')
    def validate_solver_result(self):
        if self.solver_status == SolverStatus.OPTIMAL:
            if self.objective_value is None:
                raise ValueError("An Optimal solution must have a objective value")

        return self



class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    message: str
    result: OptimizationResult | None = None

    
class OptimizationResponse(BaseModel):
    status: str
    message: str

