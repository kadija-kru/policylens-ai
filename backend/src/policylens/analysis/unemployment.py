"""Deterministic unemployment-change analysis workflow."""

from __future__ import annotations

from policylens.models.briefing import Caveat, ConfidenceLabel, Finding
from policylens.models.evidence import CalculationResult, EvidenceReference
from policylens.models.unemployment import (
    BriefingResponse,
    CalculationTrace,
    EvidenceMetadata,
    EvidenceTraceability,
    PeriodTrace,
    UnemploymentInput,
    UnemploymentMetrics,
)
from policylens.tools.calculations import absolute_change, percentage_point_change


def analyze_unemployment_change(
    unemployment: UnemploymentInput, evidence_metadata: EvidenceMetadata
) -> BriefingResponse:
    """Return a deterministic briefing response for unemployment-rate changes."""

    absolute_delta = _normalize_delta(
        absolute_change(unemployment.previous_rate, unemployment.current_rate)
    )
    percentage_point_delta = _normalize_delta(
        percentage_point_change(unemployment.previous_rate, unemployment.current_rate)
    )
    finding_statement = _build_finding_statement(unemployment, percentage_point_delta)
    confidence = _determine_confidence(unemployment, evidence_metadata)
    caveat = Caveat(message="Single-period change; interpret with broader trend context.")
    metrics = UnemploymentMetrics(
        previous_rate=unemployment.previous_rate,
        current_rate=unemployment.current_rate,
        absolute_change=absolute_delta,
        percentage_point_change=percentage_point_delta,
    )
    calculation_trace = CalculationTrace(
        formula="current_rate - previous_rate",
        inputs={
            "current_rate": unemployment.current_rate,
            "previous_rate": unemployment.previous_rate,
        },
        output=percentage_point_delta,
    )

    return BriefingResponse(
        headline=f"{unemployment.geography} unemployment change",
        summary=finding_statement,
        metrics=metrics,
        finding=Finding(
            statement=finding_statement,
            confidence=confidence,
            caveats=[caveat],
            evidence=[
                EvidenceReference(
                    claim_id="unemployment-change",
                    calculations=[
                        CalculationResult(
                            calculation_type="absolute_change",
                            value=absolute_delta,
                            formula="current_rate - previous_rate",
                            input_metrics=["previous_rate", "current_rate"],
                        ),
                        CalculationResult(
                            calculation_type="percentage_point_change",
                            value=percentage_point_delta,
                            formula="current_rate - previous_rate",
                            input_metrics=["previous_rate", "current_rate"],
                        ),
                    ],
                    note=(
                        f"Source {evidence_metadata.source_name}; "
                        f"periods {unemployment.previous_period} and "
                        f"{unemployment.current_period}."
                    ),
                )
            ],
        ),
        traceability=EvidenceTraceability(
            claim=finding_statement,
            dataset_metadata=evidence_metadata,
            periods=PeriodTrace(
                previous_period=unemployment.previous_period,
                current_period=unemployment.current_period,
            ),
            calculation=calculation_trace,
            numeric_output=metrics,
        ),
    )


def _build_finding_statement(
    unemployment: UnemploymentInput, percentage_point_delta: float
) -> str:
    if percentage_point_delta > 0:
        direction = "increased"
        move = "rise"
    elif percentage_point_delta < 0:
        direction = "decreased"
        move = "decline"
    else:
        direction = "was unchanged"
        move = "change"

    if percentage_point_delta == 0:
        return (
            f"{unemployment.geography} unemployment {direction} at "
            f"{unemployment.current_rate:.1f}% between {unemployment.previous_period} "
            f"and {unemployment.current_period}."
        )

    return (
        f"{unemployment.geography} unemployment {direction} from "
        f"{unemployment.previous_rate:.1f}% in {unemployment.previous_period} to "
        f"{unemployment.current_rate:.1f}% in {unemployment.current_period}, "
        f"a {abs(percentage_point_delta):.1f} percentage-point {move}."
    )


def _determine_confidence(
    unemployment: UnemploymentInput, evidence_metadata: EvidenceMetadata
) -> ConfidenceLabel:
    edge_case_rate = (
        unemployment.previous_rate <= 0.0
        or unemployment.previous_rate >= 100.0
        or unemployment.current_rate <= 0.0
        or unemployment.current_rate >= 100.0
    )
    missing_metadata = (
        evidence_metadata.retrieval_timestamp is None
        or (evidence_metadata.dataset_id is None and evidence_metadata.table_id is None)
    )

    if edge_case_rate or missing_metadata:
        return ConfidenceLabel.LOW

    return ConfidenceLabel.MODERATE


def _normalize_delta(value: float) -> float:
    return round(value, 4)
