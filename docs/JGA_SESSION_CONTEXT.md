# Jazz Groove Analyzer (JGA)

**Version:** v0.2.0-alpha

**Current Milestone:** M4 — Metric Reconstruction

**Repository Status:** Active Development

---

# Project Vision

The Jazz Groove Analyzer (JGA) is a scientific software framework for analysing the temporal behaviour of jazz ensembles.

Its objective is to reconstruct the internal metric organisation emerging from the interaction among musicians rather than detecting externally imposed beats.

The framework is designed to support scientific research through a layered, interpretable and extensible architecture.

---

# Current Architecture

```
Acquisition Layer
        │
        ▼
AudioStemCollection
        │
        ▼
Observation
        │
        ▼
DSP
        │
        ▼
Domain
        │
        ▼
Analysis
```

---

# Locked Architectural Principles

1. JGA is a scientific framework.
2. The repository is the source of truth.
3. The Core is independent from data acquisition.
4. AudioStemCollection is the logical input of the Core.
5. Observation describes physical phenomena.
6. DSP processes signals without musical interpretation.
7. Domain interprets observations.
8. Beat Reference is an emergent property.
9. The pipeline orchestrates layers without containing musical logic.
10. Architecture precedes implementation.

---

## Current Objective

Complete M4 Metric Reconstruction consolidation by validating the
Translation Layer contracts and preparing the transition toward
Behaviour Analysis (M5).

---

# Development Workflow

1. Verify the repository.
2. Design.
3. Implement one change.
4. `git diff`
5. `pytest`
6. Commit
7. Push

---

# Current Status

- Repository active development
- Tests passing
- Observation Layer completed
- M3.1 AudioStemCollection integration completed

✓ AudioStemCollection introduced

✓ AudioStemCollection integrated into AnalysisContext

✓ NullSeparator updated

✓ M4 Translation Layer implemented

✓ τ₈ Domain Translation completed

✓ ElementaryMetricEvent generation validated

✓ MetricSource → SoundSource contract validated

✓ Real audio validation completed

✓ 145/145 tests passing

---

# Next Immediate Step

Complete M4 consolidation and begin the preparation of
Behaviour Analysis (M5).
