from fastapi import APIRouter, status
from app.schemas import OptimizationRequest, OptimizationResponse
from app.services.optimization_service import OptimizationService


router = APIRouter(
    prefix="/api/v1", 
    tags=["Optimization"]
    )


service = OptimizationService()


@router.post(
    "/optimize",
    response_model=OptimizationResponse,
    status_code=status.HTTP_202_ACCEPTED
)
def optimize(request: OptimizationRequest):
    return service.submit(request)