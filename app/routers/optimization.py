from fastapi import APIRouter, status
from app.schemas import OptimizationRequest, OptimizationResponse

router = APIRouter(prefix="/api/v1", tags=["Optimization"])


@router.post(
    "/optimize",
    response_model=OptimizationResponse,
    status_code=status.HTTP_202_ACCEPTED
)

def optimize(request: OptimizationRequest):
    return OptimizationResponse(
        status="accepted",
        message="Optimization request validated successfully"
    )