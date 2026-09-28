"""Typed evidence models for observations, calculations, and source traceability."""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field, FiniteFloat, HttpUrl, model_validator


class SourceMetadata(BaseModel):
    """Metadata describing the authoritative origin of an observation."""

    publisher: str = Field(..., min_length=1)
    dataset_name: str = Field(..., min_length=1)
    table_id: str | None = None
    series_name: str = Field(..., min_length=1)
    release_date: date | None = None
    citation_url: HttpUrl | None = None
    geography: str = Field(..., min_length=1)
    frequency: Literal["daily", "weekly", "monthly", "quarterly", "annual", "other"]
    unit: str = Field(..., min_length=1)
    seasonal_adjustment: Literal["seasonally_adjusted", "not_seasonally_adjusted", "unknown"]
    revision_status: Literal["initial", "revised", "unknown"] = "unknown"
    retrieved_at: datetime | None = None


class Observation(BaseModel):
    """A normalized economic observation tied to source metadata."""

    metric: str = Field(..., min_length=1)
    period_start: date
    period_end: date
    value: FiniteFloat
    source: SourceMetadata

    @model_validator(mode="after")
    def validate_period_range(self) -> "Observation":
        if self.period_end < self.period_start:
            msg = "period_end cannot be earlier than period_start"
            raise ValueError(msg)
        return self


class CalculationResult(BaseModel):
    """A deterministic result derived from one or more observations."""

    calculation_type: Literal[
        "absolute_change",
        "percentage_change",
        "percentage_point_change",
    ]
    value: FiniteFloat
    formula: str = Field(..., min_length=1)
    input_metrics: list[str] = Field(default_factory=list)


class EvidenceReference(BaseModel):
    """Reference linking a finding to observations and calculations."""

    claim_id: str = Field(..., min_length=1)
    observations: list[Observation] = Field(default_factory=list)
    calculations: list[CalculationResult] = Field(default_factory=list)
    note: str | None = None

    @model_validator(mode="after")
    def validate_supporting_evidence(self) -> "EvidenceReference":
        if not self.observations and not self.calculations:
            msg = "at least one observation or calculation is required"
            raise ValueError(msg)
        return self
