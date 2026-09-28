"""FastAPI application entrypoint for PolicyLens AI."""

from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    service: str


app = FastAPI(title="PolicyLens AI", version="0.1.0")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return service health for local and CI checks."""

    return HealthResponse(status="ok", service="policylens-api")
