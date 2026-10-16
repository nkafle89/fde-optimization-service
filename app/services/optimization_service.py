from app.schemas import OptimizationRequest, OptimizationResponse


class OptimizationService:
    def submit(self, request: OptimizationRequest) -> OptimizationResponse:
        """
        Accept a validated optimization request.

        Week 2: Return a placeholder response.
        Week 3: Integrate the optimization solver.
        """

        # TODO 1:
        num_stores = len(request.demand)
        num_dcs = len(request.capacity)

        # TODO 2:
        message = f"There are 2 DCs and 3 stores"

        # TODO 3:
        status = "accepted"

        response = OptimizationResponse(status=status, message=message)

        return response
    