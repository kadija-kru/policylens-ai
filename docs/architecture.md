# PolicyLens AI Architecture

## Status

This document describes the **planned** architecture for PolicyLens AI. It is an initial design artifact for repository setup, not a claim that all components are implemented today.

## Design objective

PolicyLens AI is intended to support evidence-based public-sector analysis with clear boundaries between orchestration, data handling, deterministic analysis, validation, and briefing generation.

The governing design rule is:

> **LLM explains; code calculates; sources prove.**

## Planned components

### 1. Orchestrator

The orchestrator manages the workflow for a single analytical task.

Responsibilities:
- accept a user or analyst request,
- select the relevant economic workflow,
- sequence data retrieval, calculation, validation, and briefing steps,
- enforce that deterministic numeric outputs come from code tools rather than free-form language generation,
- require validation before a briefing is finalized.

The orchestrator is a control layer, not a calculation layer.

### 2. Data component

The data component will be responsible for:
- registering official sources,
- normalizing observations into a consistent schema,
- storing source metadata such as publication date, table identifier, geography, frequency, units, and revision state,
- preserving provenance so every downstream conclusion can cite its origin.

In the current scaffold, evidence and observation models define the shape this layer is expected to produce.

### 3. Analysis component

The analysis component performs deterministic calculations and transformations.

Examples:
- absolute change,
- percentage change,
- percentage-point change,
- period alignment,
- contributor ranking,
- anomaly flag preparation.

#### Deterministic calculation boundary

This boundary is central to PolicyLens AI:
- language models may summarize or explain a result,
- but the underlying numeric result must come from versioned, tested code,
- and the code path must be reproducible from the cited source observations.

This repository currently implements only a small subset of that analysis boundary through basic calculation tools.

### 4. Validation component

The validation component is expected to verify:
- that cited observations exist,
- that calculations can be reproduced from source values,
- that required metadata fields are present,
- that caveats and confidence labels are attached where needed,
- that missing or undefined cases are surfaced explicitly rather than glossed over.

This validation step should prevent unsupported claims from reaching analyst-facing outputs.

### 5. Briefing component

The briefing component will assemble analyst-facing outputs such as:
- structured findings,
- confidence labels,
- caveats,
- evidence references,
- and optionally narrative summaries or chart-ready annotations.

A briefing should remain an accountable summary of validated evidence, not an autonomous policy recommendation.

## Evidence traceability flow

The intended evidence flow is:

1. **Source registration**  
   Official publication and dataset metadata are captured.
2. **Observation normalization**  
   Raw values are normalized into typed observations with period, geography, and unit fields.
3. **Deterministic calculation**  
   Code computes derived metrics from normalized observations.
4. **Validation**  
   Arithmetic, metadata completeness, and reference integrity are checked.
5. **Briefing assembly**  
   Findings and caveats are generated with references back to sources and calculations.
6. **Analyst review**  
   A human reviewer decides whether the output is fit for use.

## Initial implementation boundary

This repository foundation currently includes:
- a minimal FastAPI service,
- typed evidence and briefing models,
- deterministic calculation helpers,
- tests for core calculation behavior.

It does not yet include:
- dataset connectors,
- orchestrated workflows,
- validation engines,
- storage systems,
- or LLM-backed briefing generation.
