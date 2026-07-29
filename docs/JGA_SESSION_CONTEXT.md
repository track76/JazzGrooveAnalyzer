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
Translation Layer contracts, multi-source provenance, Analysis Start
Detection and preparing the transition toward Behaviour Analysis (M5).

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

✓ Analysis Start Detection integrated

✓ Analysis Start Filtering integrated into metric pipeline

✓ Multi-source τ₈ provenance preservation validated

✓ 303/303 tests passing

✓ M4 Metric Reconstruction closed

✓ BehaviourQuantificationContext introduced

✓ D-001 TemporalContinuity Descriptor implemented

✓ D-002 MetricStability Descriptor implemented

✓ 305/305 tests passing

---

# M4 Closure

M4 Metric Reconstruction is completed.

Final M4 achievements:

✓ τ₈ Translation Layer stabilized

✓ Multi-source provenance preservation validated

✓ Analysis Start Detection integrated

✓ Analysis Start Filtering integrated into metric pipeline

✓ Reconstruction pipeline validated on real audio

✓ 303/303 tests passing


# M5 Behaviour Analysis

Initial M5 foundation completed.

Achievements:

✓ Behaviour Quantification Input Contract implemented

✓ BehaviourQuantificationContext created

✓ Behaviour Quantification pipeline integrated

✓ TemporalContinuity descriptor validated

✓ MetricStability descriptor validated

✓ M4 analytical outputs connected to M5

---

# Next Immediate Step

Continue Behaviour Analysis development by extending the
Behaviour Descriptor system and analytical models.
