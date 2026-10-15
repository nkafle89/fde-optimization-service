from fastapi import FastAPI
from app.routers.optimization import router as optimization_router

app = FastAPI(
    title="Optimization-as-a-Service",
    description="Transportation optimization API",
    version="0.1.0",
)


@app.get("/health")
def health():
    return{"status":"healthy"}


app.include_router(optimization_router)