"""Typed models for deterministic unemployment-change analysis."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, FiniteFloat

from policylens.models.briefing import Finding


class UnemploymentInput(BaseModel):
    """Structured unemployment-rate input for a single comparison."""

    previous_rate: FiniteFloat = Field(..., ge=0, le=100)
    current_rate: FiniteFloat = Field(..., ge=0, le=100)
    previous_period: str = Field(..., min_length=1)
    current_period: str = Field(..., min_length=1)
    geography: str = Field(..., min_length=1)


class EvidenceMetadata(BaseModel):
    """Minimal deterministic source metadata for a local or mocked dataset."""

    source_name: str = Field(..., min_length=1)
    dataset_id: str | None = None
    table_id: str | None = None
    measure_name: str = Field(..., min_length=1)
    unit: str = Field(..., min_length=1)
    retrieval_timestamp: datetime | None = None


class CalculationTrace(BaseModel):
    """A transparent record of the calculation used in a finding."""

    formula: str = Field(..., min_length=1)
    inputs: dict[str, FiniteFloat] = Field(default_factory=dict)
    output: FiniteFloat


class UnemploymentMetrics(BaseModel):
    """Deterministic metrics included in the briefing response."""

    previous_rate: FiniteFloat
    current_rate: FiniteFloat
    absolute_change: FiniteFloat
    percentage_point_change: FiniteFloat


class PeriodTrace(BaseModel):
    """Explicit period references used in the analysis."""

    previous_period: str = Field(..., min_length=1)
    current_period: str = Field(..., min_length=1)


class EvidenceTraceability(BaseModel):
    """Evidence chain from claim through formula and numeric output."""

    claim: str = Field(..., min_length=1)
    dataset_metadata: EvidenceMetadata
    periods: PeriodTrace
    calculation: CalculationTrace
    numeric_output: UnemploymentMetrics


class BriefingResponse(BaseModel):
    """Structured response for the unemployment-change MVP endpoint."""

    headline: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    metrics: UnemploymentMetrics
    finding: Finding
    traceability: EvidenceTraceability


class UnemploymentChangeRequest(BaseModel):
    """Request payload for deterministic unemployment-change analysis."""

    unemployment: UnemploymentInput
    evidence_metadata: EvidenceMetadata
