from app.schemas import OptimizationRequest, OptimizationResponse
from app.services.optimization_service import OptimizationService, get_optimization_service
from fastapi import APIRouter, Depends, status
from typing import Annotated


router = APIRouter(
    prefix="/api/v1", 
    tags=["Optimization"]
    )



@router.post(
    "/optimize",
    response_model=OptimizationResponse,
    status_code=status.HTTP_200_OK
)
def optimize(request: OptimizationRequest,
             service: Annotated[
                 OptimizationService, 
                 Depends(get_optimization_service)
                 ],
):
    return service.submit(request)