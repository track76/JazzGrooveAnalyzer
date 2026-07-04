# Jazz Groove Analyzer (JGA)

# DOMAIN_MODEL_MAP

## Official Domain Model Architecture

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Purpose

The purpose of this document is to define the official Domain Model of the Jazz Groove Analyzer (JGA).

It establishes the conceptual organisation of the scientific model and provides the reference architecture from which every software component shall be derived.

This document is normative.

Every concept belonging to the JGA Domain Model shall be declared here before being formally specified and subsequently implemented.

---

# 2. Scope

This document defines:

- the conceptual architecture of the Domain Model;
- the domain layers;
- the categories of domain objects;
- the dependency rules between layers;
- the official inventory of domain concepts.

This document intentionally excludes:

- mathematical algorithms;
- software implementation;
- programming languages;
- infrastructure;
- persistence mechanisms.

---

# 3. Fundamental Principle

The Jazz Groove Analyzer is developed according to a model-driven methodology.

The development process follows the sequence:

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

The Domain Model represents the bridge between the scientific theory and the software implementation.

No implementation shall introduce concepts that are absent from the Domain Model.

---

# 4. Domain Architecture

The Domain Model is organised into four conceptual layers.

```
Physical Domain

↓

Cognitive Domain

↓

Metric Domain

↓

Analytical Domain
```

Each layer represents a progressively higher level of abstraction.

Information always flows from the upper layers towards the lower ones.

---

# 5. Domain Categories

Every object belonging to the Domain Model shall belong to exactly one category.

## Aggregate Root

Represents the root of a coherent domain structure.

---

## Entity

Represents a domain concept possessing persistent identity.

Entities remain distinguishable throughout their lifecycle.

---

## Value Object

Represents a domain concept defined exclusively by its value.

Value Objects possess no identity.

---

## Domain Service

Represents a domain behaviour.

A Domain Service performs operations but never owns domain state.

---

## Domain Event

Represents a significant domain transition.

Domain Events describe facts rather than behaviours.

---

## Repository

Represents a persistence abstraction.

Repositories belong to the infrastructure layer and are therefore outside the scientific Domain Model.

---

# 6. Physical Domain

The Physical Domain represents the observable reality.

## Aggregate Root

- AudioRecording

## Entities

- AudioStem
- MusicalSource
- SourceElement

These concepts describe the physical origin of the information analysed by the JGA.

---

# 7. Cognitive Domain

The Cognitive Domain represents the musical understanding produced by the Ensemble Understanding process.

## Entities

- Meter
- MusicalRole
- MetricContributor
- EnsembleState
- MusicalSection
- TempoContext

These concepts describe the musical context inferred from the observable audio signal.

---

# 8. Metric Domain

The Metric Domain represents the temporal model of the ensemble.

## Entities

- ElementaryMetricEvent (EME)
- MetricCluster (CM)
- Pulse
- InternalMetricTimeline (TMI)

## Value Objects

- LocalTempo
- BeatIndex
- ClusterIndex

The Metric Domain constitutes the theoretical core of the Jazz Groove Analyzer.

---

# 9. Analytical Domain

The Analytical Domain represents the knowledge produced after the temporal reference has been established.

## Entities

- InstrumentProfile
- PerformanceProfile
- AnalysisReport

## Value Objects

- TemporalDeviation
- MetricStability
- TimingDistribution

The Analytical Domain never contributes to the construction of the temporal reference.

Its responsibility is exclusively analytical.

---

# 10. Shared Value Objects

The following Value Objects are shared across multiple domains.

- Identifier
- TimePoint
- TimeInterval
- Duration
- BPM
- ConfidenceScore

Shared Value Objects are immutable.

They are defined exclusively by their value.

---

# 11. Domain Services

The following Domain Services are currently identified.

- AudioLoader
- StemSeparator
- SourceIdentifier
- RoleClassifier
- MetricContributorDetector
- EMEExtractor
- MetricClusterBuilder
- TMIEstimator
- LocalTempoEstimator
- TemporalAnalyzer
- StatisticalAnalyzer

Domain Services implement behaviour.

They never define domain concepts.

---

# 12. Domain Events

The current version of the Domain Model does not formally define Domain Events.

This category is reserved for future extensions.

---

# 13. Dependency Rules

The following dependency hierarchy is mandatory.

```
Physical Domain

↓

Cognitive Domain

↓

Metric Domain

↓

Analytical Domain
```

Dependencies shall always follow this direction.

Reverse dependencies are forbidden.

Circular dependencies are forbidden.

---

# 14. Domain Evolution Rules

Every new concept introduced into the Jazz Groove Analyzer shall follow the sequence below.

1. Scientific definition

2. Inclusion in the Domain Model Map

3. Individual specification

4. Documentation

5. Tests

6. Implementation

7. Validation

No software component shall become part of the official project before completing this process.

---

# 15. Official Domain Inventory

## Aggregate Roots

- AudioRecording

---

## Entities

### Physical Domain

- AudioStem
- MusicalSource
- SourceElement

### Cognitive Domain

- Meter
- MusicalRole
- MetricContributor
- EnsembleState
- MusicalSection
- TempoContext

### Metric Domain

- ElementaryMetricEvent
- MetricCluster
- Pulse
- InternalMetricTimeline

### Analytical Domain

- InstrumentProfile
- PerformanceProfile
- AnalysisReport

---

## Value Objects

- Identifier
- TimePoint
- TimeInterval
- Duration
- BPM
- BeatIndex
- ClusterIndex
- LocalTempo
- ConfidenceScore
- TemporalDeviation
- MetricStability
- TimingDistribution

---

## Domain Services

- AudioLoader
- StemSeparator
- SourceIdentifier
- RoleClassifier
- MetricContributorDetector
- EMEExtractor
- MetricClusterBuilder
- TMIEstimator
- LocalTempoEstimator
- TemporalAnalyzer
- StatisticalAnalyzer

---

## Domain Events

Reserved for future versions.

---

# 16. Relationship with the Theoretical Framework

Every object declared in this document shall correspond to exactly one concept defined by the JGA Theoretical Framework.

The Domain Model shall never introduce independent theoretical concepts.

The software implementation shall derive exclusively from the Domain Model.

---

# 17. Conclusion

The Domain Model Map constitutes the official conceptual architecture of the Jazz Groove Analyzer.

It defines the complete organisation of the Domain Model independently from implementation technology.

Every future specification, software component and validation activity shall remain fully consistent with this document and with the JGA Theoretical Framework.