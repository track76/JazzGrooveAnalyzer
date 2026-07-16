# Jazz Groove Analyzer (JGA)

**Version:** v0.2.0-alpha

**Current Milestone:** M3.1

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

Consolidate the JGA Core architecture by validating Core responsibilities and continuing the integration of the AudioStemCollection workflow.

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

- Repository synchronized with GitHub
- Tests passing
- Observation Layer completed
- M3.1 started
✓ AudioStemCollection introduced

✓ AudioStemCollection integrated into AnalysisContext

✓ NullSeparator updated

✓ 102/102 tests passing

---

# Next Immediate Step

Design the `AudioStemCollection` domain object before modifying the pipeline.