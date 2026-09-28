import pytest
from policylens.models.briefing import BriefingOutput, ConfidenceLabel, Finding
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

    assert briefing.model_dump() == {
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


@pytest.mark.parametrize("field_name", ["title", "summary"])
def test_briefing_output_rejects_empty_required_text(field_name: str) -> None:
    payload = {
        "title": "Labour market update",
        "summary": "Unemployment increased modestly month over month.",
        "findings": [],
    }
    payload[field_name] = ""

    with pytest.raises(ValidationError):
        BriefingOutput(**payload)


def test_finding_rejects_invalid_confidence_value() -> None:
    with pytest.raises(ValidationError, match="high|moderate|low"):
        Finding(
            statement="National unemployment rate increased.",
            confidence="certain",
        )
