from fastapi.testclient import TestClient
from policylens.api.main import app

client = TestClient(app)


def test_unemployment_change_endpoint_returns_deterministic_briefing() -> None:
    response = client.post(
        "/api/v1/analysis/unemployment-change",
        json={
            "unemployment": {
                "previous_rate": 6.3,
                "current_rate": 6.5,
                "previous_period": "2026-01",
                "current_period": "2026-02",
                "geography": "Canada",
            },
            "evidence_metadata": {
                "source_name": "Statistics Canada",
                "dataset_id": "labour-force-survey",
                "table_id": "14-10-0287-01",
                "measure_name": "Unemployment rate",
                "unit": "percent",
                "retrieval_timestamp": "2026-02-15T12:00:00Z",
            },
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "headline": "Canada unemployment change",
        "summary": (
            "Canada unemployment increased from 6.3% in 2026-01 to 6.5% in 2026-02, "
            "a 0.2 percentage-point rise."
        ),
        "metrics": {
            "previous_rate": 6.3,
            "current_rate": 6.5,
            "absolute_change": 0.2,
            "percentage_point_change": 0.2,
        },
        "finding": {
            "statement": (
                "Canada unemployment increased from 6.3% in 2026-01 to 6.5% in 2026-02, "
                "a 0.2 percentage-point rise."
            ),
            "confidence": "moderate",
            "caveats": [
                {
                    "message": "Single-period change; interpret with broader trend context.",
                }
            ],
            "evidence": [
                {
                    "claim_id": "unemployment-change",
                    "observations": [],
                    "calculations": [
                        {
                            "calculation_type": "percentage_point_change",
                            "value": 0.2,
                            "formula": "current_rate - previous_rate",
                            "input_metrics": ["previous_rate", "current_rate"],
                        },
                    ],
                    "note": "Source Statistics Canada; periods 2026-01 and 2026-02.",
                }
            ],
        },
        "traceability": {
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
                "output": 0.2,
            },
            "numeric_output": {
                "previous_rate": 6.3,
                "current_rate": 6.5,
                "absolute_change": 0.2,
                "percentage_point_change": 0.2,
            },
        },
    }


def test_unemployment_change_endpoint_rejects_invalid_rate_range() -> None:
    response = client.post(
        "/api/v1/analysis/unemployment-change",
        json={
            "unemployment": {
                "previous_rate": 6.3,
                "current_rate": 101.0,
                "previous_period": "2026-01",
                "current_period": "2026-02",
                "geography": "Canada",
            },
            "evidence_metadata": {
                "source_name": "Statistics Canada",
                "measure_name": "Unemployment rate",
                "unit": "percent",
            },
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "unemployment", "current_rate"]


def test_unemployment_change_endpoint_returns_low_confidence_for_missing_metadata() -> None:
    response = client.post(
        "/api/v1/analysis/unemployment-change",
        json={
            "unemployment": {
                "previous_rate": 6.3,
                "current_rate": 6.5,
                "previous_period": "2026-01",
                "current_period": "2026-02",
                "geography": "Canada",
            },
            "evidence_metadata": {
                "source_name": "Statistics Canada",
                "measure_name": "Unemployment rate",
                "unit": "percent",
                "dataset_id": None,
                "table_id": None,
                "retrieval_timestamp": None,
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["finding"]["confidence"] == "low"
