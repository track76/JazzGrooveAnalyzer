# Jazz Groove Analyzer (JGA)

# Software Architecture

Version 1.0 (Draft)

Author

Angelo Tracanna

---

# Purpose

This document describes the software architecture of the Jazz Groove Analyzer.

Unlike the Method Specification, this document focuses exclusively on the software structure, package organisation and data flow.

The scientific meaning of hierarchical metric periodicity is governed by
`docs/scientific/foundations/F-031_HIERARCHICAL_METRIC_PERIODICITY.md`. The
Foundation introduces no new software component or architectural boundary.

---

# High-Level Pipeline

Audio File

↓

Audio Loader

↓

Audio Normalization

↓

Source Separation

↓

AudioStem Generation

↓

Rhythmic Behaviour Analysis

↓

Behaviour Change Detection

↓

Behaviour Profile

↓

Metric Evidence Index

↓

Metric State Machine

↓

Ensemble Metric Event (EME)

↓

Metric Cluster

↓

Ensemble Metric Reference

↓

Groove Analysis

↓

Reporting

---

# Main Packages

src/jga/

analysis/

audio/

metric/

pipeline/

runtime/

separation/

tests/

utils/

---

# Core Data Objects

AudioStem

↓

RhythmicBehaviourSegment

↓

BehaviourProfile

↓

MetricEvidence

↓

MetricState

↓

EnsembleMetricEvent

↓

MetricCluster

↓

EnsembleMetricReference

---

# Design Philosophy

The JGA analyses musical behaviours rather than musical instruments.

Every analytical stage increases the semantic interpretation of the musical signal.

No stage directly estimates the beat.

The Ensemble Metric Reference is progressively reconstructed from the observed behaviours of the ensemble.

---

# Future Modules

Behaviour Change Detector

Metric State Machine

Groove Descriptor

Interaction Analyzer

Swing Analyzer

Expressive Timing Analyzer

Automatic Report Generator

---

# Core Execution Model

Audio Source
      │
      ▼
Acquisition
      │
      ▼
Observation
      │
      ▼
DSP
      │
      ▼
Core Representation
      │
      ▼
Representation Translation
      │
      ▼
Domain Services
      │
      ▼
Ensemble Analysis Result

## Architectural Principles

The Core is responsible for computational processing.

The Domain is responsible for musical interpretation.

The integration between the two shall occur through an explicit architectural boundary.

---

# M7 — Behaviour Quantification / Analytics Boundary

The Behaviour pipeline is formally divided into
three independent architectural layers.

Representation

↓

Quantification

↓

Analytics

Each layer has independent responsibilities.

No layer may perform responsibilities belonging
to another layer.


---

# M8 — Mathematical Layer

Behaviour Analytics is governed by the Mathematical Principles
defined in F-000.

Every analytical operator must satisfy:

- determinism;
- immutability;
- explicit Input/Output contracts;
- provenance preservation.


---

# M8.1 Descriptor Relations

DescriptorSet
        ↓
DescriptorRelation*
        ↓
AnalyticalStructure
        ↓
BehaviourAnalyticsResult

Descriptor Relations constitute the first mathematical layer
inside Behaviour Analytics.


---

# M8.2 Descriptor Operators

Descriptor Operators form the mathematical engine of
Behaviour Analytics.

DescriptorSet
        ↓
DescriptorRelation*
        ↓
DescriptorOperator*
        ↓
AnalyticalStructure


- architecture/SCIENTIFIC_GEOMETRY.md


- architecture/SCIENTIFIC_GEOMETRIC_PLANE.md


---

# Scientific Validation Boundary

Completed analysis is exposed to the Scientific Validation Layer through the
Immutable Analysis Representation defined by:

- architecture/AD-027_IMMUTABLE_ANALYSIS_REPRESENTATION.md

The Validation Layer does not consume mutable runtime state.

The independent Ground Truth reference boundary is defined by:

- architecture/AD-028_M83_GROUND_TRUTH_REFERENCE.md

The immutable scientific validation catalogue is defined by:

- architecture/AD-029_M84_VALIDATION_CATALOG.md

The operational data-only registration and item-selected execution of
schema-compatible validation items is defined by:

- architecture/AD-036_M93_VALIDATION_DATASET_GENERALIZATION.md

M93 changes no scientific validation schema or boundary responsibility.

The scientific Comparator boundary is defined by:

- architecture/AD-030_M85_COMPARATOR.md

The approved completed-analysis materialization boundary is defined by AD-027
and implemented in `src/jga/analysis_representation/`.

The permanent Scientific Validation Record boundary is defined by:

- architecture/AD-031_M87_SCIENTIFIC_VALIDATION_RECORD.md

Controlled experimental dataset generation provenance is defined by:

- architecture/AD-033_M90_CONTROLLED_DATASET_PROVENANCE.md

The immutable observational representation for already-produced Candidate
Period evidence is defined by:

- architecture/AD-034_M91_CANDIDATE_PERIOD_REPRESENTATION.md

This standalone Core representation does not add Candidate Period discovery
or alter Metric Context, Translation, Domain reconstruction or validation
schemas.

M91.1 keeps experimental execution identities and repeated-run proof in
F-030/SVP-001 scientific records. The general Core representation preserves
only Candidate evidence, observation scope, temporal unit and minimum runtime
provenance. Discovery measurement conditions must be explicit configuration,
not recovered from implementation defaults.

The minimum production discovery boundary is defined by:

- architecture/AD-035_M92_CANDIDATE_PERIOD_DISCOVERY.md

It consumes only filtered Core PulseCandidates immediately after filtering and
preserves the resulting immutable Candidate Period population alongside the
unchanged reconstruction pipeline.
