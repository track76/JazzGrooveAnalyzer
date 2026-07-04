# Jazz Groove Analyzer (JGA)

# JGA_DOMAIN_MODEL

## Domain Model Specification

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Purpose

This document defines the official Domain Model of the Jazz Groove Analyzer (JGA).

Its purpose is to establish the software entities that represent the theoretical concepts introduced in the JGA Theoretical Framework.

The Domain Model constitutes the bridge between the scientific theory and the software implementation.

No implementation decisions are defined here.

This document specifies only:

- domain entities;
- responsibilities;
- relationships;
- invariants;
- conceptual hierarchy.

Every future implementation of the JGA must preserve the one-to-one correspondence between this Domain Model and the theoretical framework.

---

# 2. Guiding Principle

The software shall not invent the model.

The software shall implement an already defined scientific model.

Consequently:

Theory

↓

Domain Model

↓

Documentation

↓

Tests

↓

Implementation

↓

Validation

---

# 3. Domain Layers

The JGA Domain Model is organised into four conceptual layers.

## Layer 1 — Physical Domain

Represents observable entities extracted from the audio recording.

Entities include:

- AudioRecording
- AudioStem
- MusicalSource
- SourceElement

These entities describe the physical origin of musical events.

---

## Layer 2 — Cognitive Domain

Represents the musical understanding produced by Level A0.

Entities include:

- MusicalRole
- MetricContributor
- Meter
- TempoContext
- Section
- EnsembleState

These entities describe the musical interpretation of the observed sources.

---

## Layer 3 — Metric Domain

Represents the temporal structure of the ensemble.

Entities include:

- ElementaryMetricEvent (EME)
- MetricCluster (CM)
- Pulse
- Internal Metric Timeline (TMI)
- LocalTempo

This layer constitutes the theoretical core of the JGA.

---

## Layer 4 — Analytical Domain

Represents the measurements produced after the temporal reference has been established.

Entities include:

- TemporalDeviation
- MetricStability
- ClusterStatistics
- InstrumentProfile
- PerformanceProfile
- TimingDistribution
- AnalysisReport

These entities never participate in the construction of the temporal reference.

They describe the behaviour of the performance.

---

# 4. Conceptual Hierarchy

The complete hierarchy of the model is

Audio Recording

↓

Audio Stem

↓

Musical Source

↓

Source Element

↓

Musical Role

↓

Metric Contributor

↓

Elementary Metric Event (EME)

↓

Metric Cluster (CM)

↓

Pulse

↓

Internal Metric Timeline (TMI)

↓

Local Tempo

↓

Temporal Analysis

↓

Statistics

↓

Reports

---

# 5. Entity Responsibilities

Every domain entity shall satisfy the following principles.

## Single Responsibility

Each entity has exactly one responsibility.

No entity shall represent multiple independent concepts.

## Scientific Correspondence

Each entity corresponds to exactly one theoretical object defined in the JGA Theoretical Framework.

## Traceability

Every implementation class shall be traceable to one and only one domain entity.

---

# 6. Entity Specification Template

Each entity described in this document shall contain the following sections.

Purpose

Scientific Definition

Responsibilities

Inputs

Outputs

Relationships

Constraints

Future Software Representation

This template guarantees consistency between theory and implementation.

---

# 7. Relationships

Relationships between entities shall be explicit.

They include:

- composition;
- aggregation;
- association;
- dependency;
- temporal dependency.

Implicit relationships are not permitted.

---

# 8. Domain Invariants

The following principles shall always remain true.

## Invariant 1

No software entity may contradict the theoretical framework.

## Invariant 2

No domain entity may simultaneously represent multiple theoretical concepts.

## Invariant 3

Every observable event remains preserved throughout the analysis.

## Invariant 4

The Internal Metric Timeline is never directly observed.

It is always estimated from Metric Clusters.

## Invariant 5

The Domain Model is independent of implementation technology.

Python is not part of the Domain Model.

---

# 9. Development Rule

Any new software component introduced into the JGA must satisfy the following sequence.

1. Theoretical definition

2. Domain entity

3. Documentation

4. Tests

5. Implementation

6. Validation

Components that do not satisfy this sequence shall not become part of the official project.

---

# 10. Next Step

The following sections of this document will formally define every entity of the Domain Model.

Each entity will be derived directly from the JGA Theoretical Framework while preserving full conceptual consistency.

The Domain Model therefore represents the definitive bridge between scientific theory and software implementation.