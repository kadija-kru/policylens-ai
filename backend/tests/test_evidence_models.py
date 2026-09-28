import math

import pytest
from policylens.models.evidence import (
    CalculationResult,
    EvidenceReference,
    Observation,
    SourceMetadata,
)
from pydantic import ValidationError


def _source_metadata(**overrides: object) -> SourceMetadata:
    payload = {
        "publisher": "Statistics Agency",
        "dataset_name": "Labour force survey",
        "series_name": "Unemployment rate",
        "geography": "Canada",
        "frequency": "monthly",
        "unit": "percent",
        "seasonal_adjustment": "seasonally_adjusted",
        "citation_url": "https://example.com/table",
    }
    payload.update(overrides)
    return SourceMetadata(**payload)


def test_evidence_models_accept_valid_nested_payloads() -> None:
    observation = Observation(
        metric="unemployment_rate",
        period_start="2026-01-01",
        period_end="2026-01-31",
        value=6.5,
        source=_source_metadata(),
    )
    calculation = CalculationResult(
        calculation_type="percentage_point_change",
        value=0.2,
        formula="current - previous",
        input_metrics=["unemployment_rate"],
    )
    reference = EvidenceReference(
        claim_id="claim-1",
        observations=[observation],
        calculations=[calculation],
        note="Validated against monthly release.",
    )

    assert reference.model_dump(mode="json") == {
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
        "note": "Validated against monthly release.",
    }


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("frequency", "biweekly"),
        ("seasonal_adjustment", "adjusted"),
        ("citation_url", "not-a-url"),
    ],
)
def test_source_metadata_rejects_invalid_literal_and_url_values(
    field_name: str, value: str
) -> None:
    with pytest.raises(ValidationError):
        _source_metadata(**{field_name: value})


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_observation_rejects_non_finite_values(value: float) -> None:
    with pytest.raises(ValidationError):
        Observation(
            metric="unemployment_rate",
            period_start="2026-01-01",
            period_end="2026-01-31",
            value=value,
            source=_source_metadata(),
        )


def test_observation_rejects_inverted_period_range() -> None:
    with pytest.raises(ValidationError, match="period_end cannot be earlier than period_start"):
        Observation(
            metric="unemployment_rate",
            period_start="2026-02-01",
            period_end="2026-01-31",
            value=6.5,
            source=_source_metadata(),
        )


def test_evidence_reference_requires_supporting_observation_or_calculation() -> None:
    with pytest.raises(
        ValidationError, match="at least one observation or calculation is required"
    ):
        EvidenceReference(claim_id="claim-1")
