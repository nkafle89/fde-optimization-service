import pytest
from pydantic import ValidationError
from app.schemas import (
    JobStatus,
    SolverStatus,
    OptimizationRequest,
    OptimizationResult,
    JobResponse
)


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


def test_optimal_result():
    result = OptimizationResult(
        solver_status=SolverStatus.OPTIMAL,
        objective_value=12000.0,
        best_bound=12000.0,
        optimality_gap=0.0,
        solve_time_seconds=2.5
    )

    assert result.objective_value == 12000.0
    assert result.solver_status == SolverStatus.OPTIMAL


def test_optimal_requires_objective():
    with pytest.raises(ValidationError):
        OptimizationResult(
            solver_status=SolverStatus.OPTIMAL,
            objective_value=None
        )

def test_infeasible_result():
    result = OptimizationResult(
        solver_status=SolverStatus.INFEASIBLE
    )

    assert result.objective_value is None


def test_finished_job():
    job = JobResponse(
        job_id="job_12345",
        status=JobStatus.FINISHED,
        message="Optimization completed",
        result=OptimizationResult(
            solver_status=SolverStatus.OPTIMAL,
            objective_value=12000.0
        )
    )

    assert job.status == JobStatus.FINISHED
    assert job.result.objective_value == 12000.0


def test_running_job_without_result():
    job = JobResponse(
        job_id="job_12345",
        status=JobStatus.RUNNING,
        message="Optimization in progress"
    )

    assert job.result is None