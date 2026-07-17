# TAC Domain Mapping

Version: 0.1

Status:
DRAFT

Author:
Angelo Tracanna


# 1. Purpose

This document defines the conceptual mapping between the
Temporal Alignment Context (TAC) and the Jazz Groove Analyzer
(JGA) Domain Model.

The purpose is to describe how observable temporal information
becomes domain-level musical representation.

No implementation change is introduced by this document.


# 2. Scientific Position

TAC belongs to the scientific transition between observation
and musical representation.

TAC does not create musical entities.

TAC provides the temporal relational information required for
the construction of higher-level representations.


# 3. Mapping Overview

The conceptual pipeline is:

Audio Signal

        ↓

Observation Layer

        ↓

Observable Temporal Events

        ↓

Temporal Alignment Context (TAC)

        ↓

Observable Metric Context

        ↓

Domain Entities

        ↓

Elementary Metric Event

        ↓

Metric Cluster

        ↓

Beat Reference


# 4. TAC Observable Layer

TAC receives observable temporal information.

The input is derived from the Observation Layer.

Observable information may include:

- timestamp;
- duration;
- source information;
- confidence;
- temporal relationships.

No musical interpretation is introduced at this stage.


# 5. Relationship with F-003 Observable Metric Context

The Observable Metric Context represents the first contextual
organization of temporal observations.

It may identify:

- metric contributors;
- ensemble pulse;
- local temporal behaviour;
- musical functions.

The Observable Metric Context emerges from observable evidence
and temporal relationships.


# 6. Domain Entity Mapping

Domain entities are created only after observable temporal
relationships have been established.

The Domain Layer may introduce:

- musical contributors;
- metric roles;
- metric events;
- metric structures.

Every domain entity must remain traceable to the original
observable evidence.


# 7. Elementary Metric Event Mapping

The Elementary Metric Event remains the smallest domain-level
metric representation.

EME is not a raw observation.

EME is a metric-relevant representation derived from observable
temporal evidence.

The mapping is:

Observable Event

        ↓

TAC Temporal Relations

        ↓

Observable Metric Context

        ↓

Elementary Metric Event


# 8. Metric Cluster Mapping

Metric Clusters are constructed from Elementary Metric Events.

The Metric Cluster represents collective temporal organization
within the ensemble.

TAC contributes temporal evidence but does not define metric
structure.


# 9. Implementation Constraints

The following constraints apply:

- No implementation change before approval.
- Observation precedes interpretation.
- Domain entities must remain traceable to observations.
- TAC must not become a beat detection mechanism.
- Metric structures must emerge from ensemble behaviour.


# 10. Open Questions

1. Should TAC become an explicit software model?

2. Which existing Domain services consume TAC-derived information?

3. Should PulseCandidate naming be revised?

4. Which mathematical representation best describes TAC relations?

