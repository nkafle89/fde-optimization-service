from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import JobNotFoundError, OptimizationServiceError
from app.routers.optimization import router as optimization_router
import logging


app = FastAPI(
    title="Optimization-as-a-Service",
    description="Transportation optimization API",
    version="0.1.0",
)


logger = logging.getLogger(__name__)



@app.exception_handler(JobNotFoundError)
async def job_not_found_handler(
    request: Request, 
    exc: JobNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "JOB_NOT_FOUND",
                "message": str(exc)
            }
        }
    )


@app.exception_handler(OptimizationServiceError)
async def optimization_error_handler(
    request: Request,
    exc: OptimizationServiceError
):
    logger.error("Optimization service error", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "OPTIMIZATION_SERVICE_ERROR",
                "message": "ERROR. Check the internal logs"
            }
        }
    )


@app.get("/health")
def health():
    return{"status":"healthy"}


app.include_router(optimization_router)