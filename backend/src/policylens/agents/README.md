# Planned agent boundaries

This directory is reserved for future orchestration and agent-facing modules.

PolicyLens AI intends to separate responsibilities so that:
- orchestration controls workflow sequencing,
- data components retrieve and normalize evidence,
- deterministic tools perform calculations,
- validation checks arithmetic and provenance,
- briefing components assemble analyst-facing outputs.

Autonomous LLM behavior is intentionally **not implemented** in this initial scaffold.

Any future agent implementation should preserve the repository's core boundary:

> **LLM explains; code calculates; sources prove.**
