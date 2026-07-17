# RFC-002 — Scientific Nature of the PulseCandidate

Version: 0.4 (Draft)

Status:
UNDER REVIEW

Author:
Angelo Tracanna

---

# Purpose

This RFC investigates the scientific nature and architectural role
of the PulseCandidate within the Jazz Groove Analyzer (JGA).

Its objective is to clarify the transition between physical
observation, temporal contextualization and musical representation.

No implementation shall be modified until this RFC is approved.

---

# Motivation

The PulseCandidate was originally positioned between the observation
process and the construction of Elementary Metric Events (EMEs).

However, repository analysis revealed that the current architecture
contains two different concepts sharing the same name:

- Core PulseCandidate
- Domain PulseCandidate

The ambiguity is therefore not caused by the algorithmic behaviour,
but by the overlap of terminology between architectural layers.

---

# Current Position

The simplified historical pipeline was:

Audio Signal
    ↓
PulseCandidate
    ↓
Elementary Metric Event
    ↓
Metric Cluster


The current scientific model introduces the missing temporal
contextualization layer:

Audio Signal
    ↓
Observation Layer
    ↓
Observable Temporal Events
    ↓
TAC Temporal Alignment Context
    ↓
Observable Metric Context
    ↓
Domain Representation
    ↓
Elementary Metric Event

---

# Repository Analysis

Repository inspection produced the following observations.

## Core PulseCandidate

The current Core implementation:

- detects temporal events derived from audio analysis;
- stores timestamp information;
- stores onset strength;
- stores confidence.

No pulse estimation is performed.

No beat estimation is performed.

No musical interpretation is introduced.

The Core PulseCandidate therefore represents an
observation-layer temporal candidate.


## Domain PulseCandidate

The Domain implementation contains:

- identity;
- sound source reference;
- timestamp;
- confidence;
- creation metadata.

The Domain PulseCandidate represents a temporal contribution
associated with a musical source.

It belongs to the representation layer.

---

# Scientific Clarification

The term PulseCandidate currently refers to two different
architectural concepts.

## Core PulseCandidate

Scientific interpretation:

Observable temporal candidate.

Role:

To represent an event extracted from the physical audio signal
before musical interpretation.


## Domain PulseCandidate

Scientific interpretation:

Candidate temporal contribution within a musical representation.

Role:

To represent a source-associated event that may contribute to
metric analysis.


The two concepts are related but not identical.

The ambiguity originates from the shared naming.

---

# Relationship with TAC Observation Model

The TAC Observation Model introduces the conceptual boundary
between observable events and metric representation.

TAC does not replace PulseCandidate.

TAC provides the temporal relational context required before
metric interpretation.

The scientific transition becomes:

Observable Temporal Event

        ↓

TAC Temporal Relations

        ↓

Observable Metric Context

        ↓

Domain Representation

        ↓

Elementary Metric Event

---

# Scientific Questions

The following questions remain open.

1. Should Core PulseCandidate receive a different name?

2. Should Domain PulseCandidate remain part of the Domain Model?

3. Should TAC become an explicit software representation?

4. Which temporal relations are necessary for metric emergence?

5. Is the term "PulseCandidate" scientifically appropriate?

---

# Resolution Proposal

Repository analysis indicates that PulseCandidate is not a single
scientific entity but two related concepts located at different
architectural layers.

The current implementation remains valid.

No algorithmic change is required.

Future architectural work may introduce clearer naming to separate:

- observable temporal candidates;
- domain-level metric candidates.

---

# Scientific Constraints

The following principles remain invariant:

- Observation always precedes interpretation.
- No musical meaning may be introduced without observable evidence.
- Every higher-level representation must remain traceable to physical
  observations.
- The repository remains the source of truth.

---

# Expected Outcome

This RFC shall define the final scientific classification of
PulseCandidate and determine whether naming changes or Domain Model
adjustments are required.

Until this RFC is approved, the current implementation remains the
official reference.

