"""FastAPI application entrypoint for PolicyLens AI."""

from fastapi import FastAPI
from pydantic import BaseModel

from policylens.analysis.unemployment import analyze_unemployment_change
from policylens.models.unemployment import BriefingResponse, UnemploymentChangeRequest


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    service: str


app = FastAPI(title="PolicyLens AI", version="0.1.0")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return service health for local and CI checks."""

    return HealthResponse(status="ok", service="policylens-api")


@app.post("/api/v1/analysis/unemployment-change", response_model=BriefingResponse)
def unemployment_change(request: UnemploymentChangeRequest) -> BriefingResponse:
    """Return a deterministic unemployment-change briefing from local/mock input."""

    return analyze_unemployment_change(request.unemployment, request.evidence_metadata)
