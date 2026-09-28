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
    """A briefing finding with evidence and uncertainty metadata.

    `confidence` expresses how strongly the available evidence supports the statement.
    `evidence` may be empty only for provisional narrative findings that still require
    evidence assembly before analyst use.
    """

    statement: str = Field(..., min_length=1)
    confidence: ConfidenceLabel = Field(
        ..., description="Analyst-facing confidence label for the supporting evidence."
    )
    caveats: list[Caveat] = Field(default_factory=list)
    evidence: list[EvidenceReference] = Field(
        default_factory=list,
        description=(
            "Traceable evidence references backing the finding; may be empty only "
            "while a finding remains provisional."
        ),
    )


class BriefingOutput(BaseModel):
    """Structured analyst-facing briefing content."""

    title: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    findings: list[Finding] = Field(..., min_length=1)
