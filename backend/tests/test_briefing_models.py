import pytest
from policylens.models.briefing import BriefingOutput, Caveat, ConfidenceLabel, Finding
from policylens.models.evidence import (
    CalculationResult,
    EvidenceReference,
    Observation,
    SourceMetadata,
)
from pydantic import ValidationError


def test_briefing_output_serializes_with_valid_fields() -> None:
    briefing = BriefingOutput(
        title="Labour market update",
        summary="Unemployment increased modestly month over month.",
        findings=[
            Finding(
                statement="National unemployment rate increased.",
                confidence=ConfidenceLabel.MODERATE,
            )
        ],
    )

    assert briefing.model_dump(mode="json") == {
        "title": "Labour market update",
        "summary": "Unemployment increased modestly month over month.",
        "findings": [
            {
                "statement": "National unemployment rate increased.",
                "confidence": "moderate",
                "caveats": [],
                "evidence": [],
            }
        ],
    }


def test_finding_round_trips_nested_caveats_and_evidence() -> None:
    finding = Finding(
        statement="National unemployment rate increased.",
        confidence=ConfidenceLabel.MODERATE,
        caveats=[Caveat(message="Provincial revisions may affect the estimate.")],
        evidence=[
            EvidenceReference(
                claim_id="claim-1",
                observations=[
                    Observation(
                        metric="unemployment_rate",
                        period_start="2026-01-01",
                        period_end="2026-01-31",
                        value=6.5,
                        source=SourceMetadata(
                            publisher="Statistics Agency",
                            dataset_name="Labour force survey",
                            series_name="Unemployment rate",
                            citation_url="https://example.com/table",
                            geography="Canada",
                            frequency="monthly",
                            unit="percent",
                            seasonal_adjustment="seasonally_adjusted",
                        ),
                    )
                ],
                calculations=[
                    CalculationResult(
                        calculation_type="percentage_point_change",
                        value=0.2,
                        formula="current - previous",
                        input_metrics=["unemployment_rate"],
                    )
                ],
            )
        ],
    )

    assert finding.model_dump(mode="json") == {
        "statement": "National unemployment rate increased.",
        "confidence": "moderate",
        "caveats": [{"message": "Provincial revisions may affect the estimate."}],
        "evidence": [
            {
                "claim_id": "claim-1",
                "observations": [
                    {
                        "metric": "unemployment_rate",
                        "period_start": "2026-01-01",
                        "period_end": "2026-01-31",
                        "value": 6.5,
                        "source": {
                            "publisher": "Statistics Agency",
                            "dataset_name": "Labour force survey",
                            "table_id": None,
                            "series_name": "Unemployment rate",
                            "release_date": None,
                            "citation_url": "https://example.com/table",
                            "geography": "Canada",
                            "frequency": "monthly",
                            "unit": "percent",
                            "seasonal_adjustment": "seasonally_adjusted",
                            "revision_status": "unknown",
                            "retrieved_at": None,
                        },
                    }
                ],
                "calculations": [
                    {
                        "calculation_type": "percentage_point_change",
                        "value": 0.2,
                        "formula": "current - previous",
                        "input_metrics": ["unemployment_rate"],
                    }
                ],
                "note": None,
            }
        ],
    }


@pytest.mark.parametrize("field_name", ["title", "summary"])
def test_briefing_output_rejects_empty_required_text(field_name: str) -> None:
    payload = {
        "title": "Labour market update",
        "summary": "Unemployment increased modestly month over month.",
        "findings": [
            {
                "statement": "National unemployment rate increased.",
                "confidence": "moderate",
            }
        ],
    }
    payload[field_name] = ""

    with pytest.raises(ValidationError):
        BriefingOutput(**payload)


def test_briefing_output_requires_at_least_one_finding() -> None:
    with pytest.raises(ValidationError):
        BriefingOutput(
            title="Labour market update",
            summary="Unemployment increased modestly month over month.",
            findings=[],
        )


def test_finding_rejects_invalid_confidence_value() -> None:
    with pytest.raises(ValidationError, match="high|moderate|low"):
        Finding(
            statement="National unemployment rate increased.",
            confidence="certain",
        )
