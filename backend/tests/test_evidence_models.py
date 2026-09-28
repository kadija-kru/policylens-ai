from datetime import date

import pytest
from policylens.models.evidence import Observation, SourceMetadata
from pydantic import ValidationError


def _source_metadata() -> SourceMetadata:
    return SourceMetadata(
        publisher="Statistics Agency",
        dataset_name="Labour force survey",
        series_name="Unemployment rate",
        geography="Canada",
        frequency="monthly",
        unit="percent",
        seasonal_adjustment="seasonally_adjusted",
    )


def test_observation_rejects_inverted_period_range() -> None:
    with pytest.raises(ValidationError, match="period_end cannot be earlier than period_start"):
        Observation(
            metric="unemployment_rate",
            period_start=date(2026, 2, 1),
            period_end=date(2026, 1, 31),
            value=6.5,
            source=_source_metadata(),
        )
