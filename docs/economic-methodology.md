# Economic Methodology (Initial)

## Status

This is an **initial methodology document** for PolicyLens AI. It sets expectations for indicator handling and analytical discipline, but it does **not** claim that full production support for every requirement already exists in the codebase.

## Methodological intent

PolicyLens AI should present economic changes in ways that are reproducible, interpretable, and appropriate for public-sector analysis.

The system must distinguish among different kinds of changes instead of treating all deltas as interchangeable.

## Indicator definitions

At a minimum, indicator handling should preserve:
- **indicator name** (for example, unemployment rate or CPI),
- **geography**,
- **time period**,
- **frequency** (monthly, quarterly, annual),
- **unit** (percent, index, currency, persons, etc.),
- **seasonal adjustment status**,
- **revision status**,
- **source metadata**.

## Change definitions

### Month-over-month (MoM)

Month-over-month change compares an observation with the immediately preceding month.

Examples:
- level series: current minus previous,
- index or value series: percentage change where appropriate,
- rates or shares: percentage-point change where appropriate.

The system should not describe a rate change as a percentage change unless that is the intended interpretation.

### Year-over-year (YoY)

Year-over-year change compares an observation with the same period in the prior year.

This is often the more stable lens for seasonal series, but it still requires explicit labeling so users know whether they are reading MoM or YoY movement.

### Percentage change

Percentage change should be used for values where proportional movement is meaningful.

Formula:

```text
((current - previous) / previous) * 100
```

#### Zero-baseline rule

If the baseline (`previous`) is zero, percentage change is **undefined** and must not be fabricated.

PolicyLens AI should surface this explicitly as an undefined case requiring analyst interpretation or alternative framing.

### Percentage-point change

Percentage-point change should be used for rates, shares, and percentages where the correct interpretation is a difference in percentage levels.

Formula:

```text
current - previous
```

Example:
- unemployment rate from 6.3% to 6.5% = **+0.2 percentage points**, not +3.17 percentage points of unemployment rate level movement unless that proportional framing is explicitly intended.

## Confidence labels

Confidence labels should reflect evidence quality and analytical completeness, not rhetorical tone.

An initial working scale may include:
- **high**: evidence is complete, current, internally consistent, and directly supports the finding,
- **moderate**: evidence supports the finding but includes minor caveats, partial coverage, or limited corroboration,
- **low**: evidence is incomplete, highly provisional, or materially uncertain.

Confidence labels should be paired with caveats when uncertainty is non-trivial.

## Revisions

Many official economic series are revised.

Methodological requirements:
- store revision-aware source metadata,
- distinguish initial release values from revised values when possible,
- avoid implying that a revised series is unchanged over time,
- disclose when a conclusion may be sensitive to future revisions.

## Seasonality

Economic series may be seasonally adjusted or unadjusted.

Methodological requirements:
- preserve seasonal adjustment status in source metadata,
- avoid direct comparison of incompatible series without explicit handling,
- label seasonal status in outputs where it affects interpretation,
- prefer the analytically appropriate comparison basis for the series being discussed.

## Source metadata

Every finding should remain traceable to source material.

Required metadata should eventually include:
- source organization,
- dataset or table identifier,
- series name,
- publication or release date,
- observation period,
- access or retrieval timestamp where relevant,
- geography,
- unit,
- seasonal adjustment status,
- revision status,
- citation URL or stable reference.

## Initial implementation note

The current code scaffold implements only a small subset of this methodology through typed models and deterministic change calculations. It does not yet claim complete production support for MoM, YoY, revisions management, seasonal adjustment handling, or source ingestion workflows.
