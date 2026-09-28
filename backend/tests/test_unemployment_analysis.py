from datetime import datetime

import pytest
from policylens.analysis.unemployment import analyze_unemployment_change
from policylens.models.briefing import ConfidenceLabel
from policylens.models.unemployment import EvidenceMetadata, UnemploymentInput
from pydantic import ValidationError


def _input(**overrides: object) -> UnemploymentInput:
    payload = {
        "previous_rate": 6.3,
        "current_rate": 6.5,
        "previous_period": "2026-01",
        "current_period": "2026-02",
        "geography": "Canada",
    }
    payload.update(overrides)
    return UnemploymentInput(**payload)


def _metadata(**overrides: object) -> EvidenceMetadata:
    payload = {
        "source_name": "Statistics Canada",
        "dataset_id": "labour-force-survey",
        "table_id": "14-10-0287-01",
        "measure_name": "Unemployment rate",
        "unit": "percent",
        "retrieval_timestamp": "2026-02-15T12:00:00Z",
    }
    payload.update(overrides)
    return EvidenceMetadata(**payload)


def test_analyze_unemployment_change_for_increase() -> None:
    response = analyze_unemployment_change(_input(), _metadata())

    assert response.headline == "Canada unemployment change"
    assert response.summary == (
        "Canada unemployment increased from 6.3% in 2026-01 to 6.5% in 2026-02, "
        "a 0.2 percentage-point rise."
    )
    assert response.metrics.model_dump() == {
        "previous_rate": 6.3,
        "current_rate": 6.5,
        "absolute_change": pytest.approx(0.2),
        "percentage_point_change": pytest.approx(0.2),
    }
    assert response.finding.confidence is ConfidenceLabel.MODERATE
    assert response.finding.caveats[0].message == (
        "Single-period change; interpret with broader trend context."
    )
    assert response.traceability.model_dump(mode="json") == {
        "claim": (
            "Canada unemployment increased from 6.3% in 2026-01 to 6.5% in 2026-02, "
            "a 0.2 percentage-point rise."
        ),
        "dataset_metadata": {
            "source_name": "Statistics Canada",
            "dataset_id": "labour-force-survey",
            "table_id": "14-10-0287-01",
            "measure_name": "Unemployment rate",
            "unit": "percent",
            "retrieval_timestamp": "2026-02-15T12:00:00Z",
        },
        "periods": {
            "previous_period": "2026-01",
            "current_period": "2026-02",
        },
        "calculation": {
            "formula": "current_rate - previous_rate",
            "inputs": {
                "current_rate": 6.5,
                "previous_rate": 6.3,
            },
            "output": pytest.approx(0.2),
        },
        "numeric_output": {
            "previous_rate": 6.3,
            "current_rate": 6.5,
            "absolute_change": pytest.approx(0.2),
            "percentage_point_change": pytest.approx(0.2),
        },
    }


def test_analyze_unemployment_change_for_decrease() -> None:
    response = analyze_unemployment_change(
        _input(previous_rate=6.5, current_rate=6.1),
        _metadata(),
    )

    assert response.summary == (
        "Canada unemployment decreased from 6.5% in 2026-01 to 6.1% in 2026-02, "
        "a 0.4 percentage-point decline."
    )
    assert response.metrics.absolute_change == pytest.approx(-0.4)
    assert response.metrics.percentage_point_change == pytest.approx(-0.4)


def test_analyze_unemployment_change_for_no_change() -> None:
    response = analyze_unemployment_change(
        _input(previous_rate=6.4, current_rate=6.4),
        _metadata(),
    )

    assert response.summary == (
        "Canada unemployment was unchanged at 6.4% between 2026-01 and 2026-02."
    )
    assert response.metrics.absolute_change == pytest.approx(0.0)


def test_analyze_unemployment_change_lowers_confidence_for_missing_metadata() -> None:
    response = analyze_unemployment_change(
        _input(),
        _metadata(dataset_id=None, table_id=None, retrieval_timestamp=None),
    )

    assert response.finding.confidence is ConfidenceLabel.LOW


def test_analyze_unemployment_change_lowers_confidence_for_boundary_rate() -> None:
    response = analyze_unemployment_change(
        _input(previous_rate=0.0, current_rate=0.3),
        _metadata(),
    )

    assert response.finding.confidence is ConfidenceLabel.LOW


def test_analyze_unemployment_change_lowers_confidence_for_upper_boundary_rate() -> None:
    response = analyze_unemployment_change(
        _input(previous_rate=99.7, current_rate=100.0),
        _metadata(),
    )

    assert response.finding.confidence is ConfidenceLabel.LOW


def test_unemployment_input_rejects_invalid_range() -> None:
    with pytest.raises(ValidationError, match="less than or equal to 100"):
        _input(current_rate=101.0)


def test_evidence_metadata_accepts_optional_dataset_or_table_ids() -> None:
    metadata = _metadata(dataset_id=None, table_id="14-10-0287-01")

    assert metadata.retrieval_timestamp == datetime.fromisoformat("2026-02-15T12:00:00+00:00")
