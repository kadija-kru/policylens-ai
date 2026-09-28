"""Typed briefing output models for analyst-facing summaries."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from policylens.models.evidence import EvidenceReference


class ConfidenceLabel(StrEnum):
    """Initial confidence labels for evidence-backed findings."""

    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"


class Caveat(BaseModel):
    """A limitation or uncertainty that should accompany a finding."""

    message: str = Field(..., min_length=1)


class Finding(BaseModel):
    """A briefing finding with evidence and uncertainty metadata."""

    statement: str = Field(..., min_length=1)
    confidence: ConfidenceLabel
    caveats: list[Caveat] = Field(default_factory=list)
    evidence: list[EvidenceReference] = Field(default_factory=list)


class BriefingOutput(BaseModel):
    """Structured analyst-facing briefing content."""

    title: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    findings: list[Finding] = Field(default_factory=list)
