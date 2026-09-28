# PolicyLens AI

**PolicyLens AI** is an agentic economic intelligence platform for evidence-based public-sector analysis.

Its first principle is simple:

> **LLM explains; code calculates; sources prove.**

This repository establishes the initial backend and governance foundation for a system that helps analysts monitor economic conditions, investigate changes, and prepare evidence-backed briefing outputs without delegating policy decisions to an automated model.

## Purpose

PolicyLens AI is designed to support public-sector analysts by:
- structuring evidence from authoritative sources,
- calculating indicator changes deterministically,
- producing traceable findings and caveats, and
- preserving human accountability for interpretation and decisions.

## Non-goals

This initial repository foundation does **not** include:
- external data ingestion APIs,
- LLM or agent runtime integrations,
- databases or background jobs,
- forecasting or simulation engines,
- automated policy recommendations, or
- frontend dashboards.

## Core principles

- **LLM explains; code calculates; sources prove.**
- **Analyst in the loop.** Human reviewers remain responsible for judgment and approval.
- **Deterministic computations.** Numerical results must come from tested code paths.
- **Evidence traceability.** Findings must map back to source metadata, periods, and calculations.
- **Explicit uncertainty.** Confidence labels and caveats must be surfaced clearly.
- **Reviewable scope.** The first implementation stays intentionally small and auditable.

## MVP scope

The initial MVP foundation in this repository covers:
- a documented architecture for orchestrated economic analysis,
- typed data models for evidence and briefing outputs,
- deterministic calculation utilities for basic indicator deltas,
- a FastAPI backend with a health endpoint, and
- local tooling, tests, and CI for a clean development baseline.

The current MVP slice now answers a focused question such as: **“Why did unemployment change this month?”** using deterministic local input, sourced metadata, and validated calculations.

## Architecture overview

The planned system separates orchestration, data handling, deterministic analysis, validation, and briefing generation.

- **Orchestrator** coordinates workflow stages and enforces boundaries.
- **Data layer** normalizes source metadata and observations.
- **Analysis tools** perform deterministic calculations in code.
- **Validation layer** checks arithmetic, provenance, and completeness.
- **Briefing layer** assembles findings, confidence labels, and caveats for analysts.

See [/docs/architecture.md](docs/architecture.md) for the planned component model and evidence flow.

## Repository layout

```text
.
├── .github/workflows/ci.yml
├── backend/
│   ├── src/policylens/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── models/
│   │   └── tools/
│   └── tests/
├── docs/
│   ├── architecture.md
│   ├── economic-methodology.md
│   └── safety-and-governance.md
├── .env.example
├── Makefile
├── pyproject.toml
└── README.md
```

## Local development

### Requirements

- Python 3.11+
- `pip`

### Install

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### Run the API

```bash
make run
```

By default, the API is available at `http://127.0.0.1:8000`. If you want a different host or port, copy the placeholder values from `.env.example` and **export them in your shell manually** before running `make run`; the Makefile does not auto-load env files. The health endpoint is:

```text
GET /health
```

## MVP Slice 1

PolicyLens AI now includes a local, deterministic unemployment-change workflow. It does **not** call external APIs yet; the request payload supplies mock/local data and source metadata so the evidence chain stays reviewable.

Endpoint:

```text
POST /api/v1/analysis/unemployment-change
```

Example request:

```json
{
  "unemployment": {
    "previous_rate": 6.3,
    "current_rate": 6.5,
    "previous_period": "2026-01",
    "current_period": "2026-02",
    "geography": "Canada"
  },
  "evidence_metadata": {
    "source_name": "Statistics Canada",
    "dataset_id": "labour-force-survey",
    "table_id": "14-10-0287-01",
    "measure_name": "Unemployment rate",
    "unit": "percent",
    "retrieval_timestamp": "2026-02-15T12:00:00Z"
  }
}
```

Example response:

```json
{
  "headline": "Canada unemployment change",
  "summary": "Canada unemployment increased from 6.3% in 2026-01 to 6.5% in 2026-02, a 0.2 percentage-point rise.",
  "metrics": {
    "previous_rate": 6.3,
    "current_rate": 6.5,
    "absolute_change": 0.2,
    "percentage_point_change": 0.2
  },
  "finding": {
    "statement": "Canada unemployment increased from 6.3% in 2026-01 to 6.5% in 2026-02, a 0.2 percentage-point rise.",
    "confidence": "moderate",
    "caveats": [
      {
        "message": "Single-period change; interpret with broader trend context."
      }
    ],
    "evidence": [
      {
        "claim_id": "unemployment-change",
        "calculations": [
          {
            "calculation_type": "percentage_point_change",
            "formula": "current_rate - previous_rate",
            "value": 0.2
          }
        ],
        "note": "Source Statistics Canada; periods 2026-01 and 2026-02."
      }
    ]
  },
  "traceability": {
    "claim": "Canada unemployment increased from 6.3% in 2026-01 to 6.5% in 2026-02, a 0.2 percentage-point rise.",
    "dataset_metadata": {
      "source_name": "Statistics Canada",
      "dataset_id": "labour-force-survey",
      "table_id": "14-10-0287-01",
      "measure_name": "Unemployment rate",
      "unit": "percent",
      "retrieval_timestamp": "2026-02-15T12:00:00Z"
    },
    "periods": {
      "previous_period": "2026-01",
      "current_period": "2026-02"
    },
    "calculation": {
      "formula": "current_rate - previous_rate",
      "output": 0.2
    }
  }
}
```

## Testing

Run the checks from the repository root:

```bash
make lint
make test
```

Equivalent direct commands:

```bash
ruff check .
pytest
```

For this MVP slice, the key commands run from the repository root are:

```bash
ruff check .
pytest
```

## Roadmap

### Near term
- Add the first end-to-end economic question workflow.
- Introduce normalized source adapters for official datasets.
- Expand deterministic indicator calculations and validation coverage.
- Add evidence-to-briefing trace tests.

### Later
- Add analyst-facing briefing templates.
- Add evaluation suites for arithmetic consistency and citation quality.
- Add controlled document analysis for budget and policy materials.
- Add scenario and early-warning modules with explicit methodology constraints.

## Safety and governance

PolicyLens AI is intended for **decision support**, not automated decision-making.

- No automatic policy decisions or recommendations are produced.
- Uncertainty and caveats must be disclosed.
- Evidence provenance and auditability are first-class requirements.
- Uploaded documents and retrieved data must be handled with prompt-injection defenses and privacy safeguards.

See [/docs/safety-and-governance.md](docs/safety-and-governance.md) for the detailed governance baseline.

## Project status

This repository is an **initial foundation**. It demonstrates architecture direction, typed models, deterministic calculations, and testable backend scaffolding. It does **not** claim production readiness or complete methodology support.
