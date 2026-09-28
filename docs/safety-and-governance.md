# Safety and Governance

## Status

This document defines the initial safety and governance baseline for PolicyLens AI. It is meant to guide implementation and review, not to imply that all controls are already production-complete.

## Analyst-in-the-loop operation

PolicyLens AI is a decision-support system.

Requirements:
- outputs are prepared for analyst review,
- human analysts remain accountable for interpretation and downstream use,
- the system must not present itself as the final authority on public policy questions,
- analyst approval is required before any briefing is treated as actionable.

## No automatic policy decisions

PolicyLens AI must not:
- automatically determine public policy,
- issue binding decisions,
- rank policy choices as definitive recommendations without human review,
- conceal normative judgments as if they were objective facts.

The system may help compare evidence, quantify changes, and summarize trade-offs, but final policy judgment belongs to authorized humans.

## Uncertainty disclosure

Outputs should disclose uncertainty explicitly.

Requirements:
- confidence labels should be attached to findings,
- caveats should be shown when evidence is incomplete, provisional, or revision-sensitive,
- undefined or weakly supported calculations should not be expressed as precise conclusions,
- summary language should not overstate certainty.

## Provenance and auditability

PolicyLens AI should preserve a traceable chain from output to source.

Requirements:
- findings should cite evidence references,
- calculations should be reproducible from stored inputs,
- versions of logic and source metadata should be reviewable,
- audit logs or equivalent trace artifacts should make it possible to understand why a result was produced.

## Privacy and data handling

Although the initial scaffold does not yet implement ingestion pipelines, the project should assume privacy-conscious operation.

Requirements:
- minimize collection of unnecessary personal or sensitive data,
- document permitted data classes before ingestion features are added,
- restrict access to uploaded materials and analysis artifacts,
- avoid retaining sensitive documents longer than needed for approved workflows.

## Prompt-injection defenses for documents

Future document-processing features must assume that uploaded documents may contain adversarial instructions.

Requirements:
- treat document text as untrusted content, not system instruction,
- isolate extraction and analysis from execution-capable tool paths,
- require explicit allowlists for any action that could affect external systems,
- validate citations and structured facts independently of document narrative,
- ensure that embedded instructions in source material cannot override system governance.

## Evaluation requirements

Before higher-risk capabilities are added, the project should include evaluations for:
- arithmetic correctness,
- citation completeness,
- provenance preservation,
- confidence-label consistency,
- prompt-injection resilience for document workflows,
- regression coverage for known failure modes.

## Governance posture for this repository stage

At this stage, the repository should remain:
- small,
- testable,
- deterministic where numbers are involved,
- explicit about what is not yet implemented,
- and conservative about unsupported claims.
