# RFC-003 — Domain Model Alignment after TAC Introduction

Version: 0.1 (Draft)

Status:
UNDER REVIEW

Author:
Angelo Tracanna

---

# Purpose

This RFC evaluates the alignment of the current JGA Domain Model
after the introduction of the Temporal Alignment Context (TAC).

Its objective is to verify whether existing Domain entities and
relationships remain consistent with the scientific architecture
defined by RFC-001, RFC-002 and the TAC Observation Model.

No implementation shall be modified until this RFC is approved.

---

# Motivation

The introduction of TAC clarified the transition between:

- physical observation;
- temporal contextualization;
- musical representation.

Repository analysis revealed that some existing concepts require
architectural clarification, especially the role of PulseCandidate.

The current repository contains two concepts sharing the same name:

- Core PulseCandidate;
- Domain PulseCandidate.

This RFC investigates whether the current Domain Model correctly
represents this distinction.

---

# Current Scientific Model

The current conceptual flow is:

Audio Signal

    ↓

Observation Layer

    ↓

Core PulseCandidate

    ↓

TAC Temporal Alignment Context

    ↓

Observable Metric Context

    ↓

Domain Representation

    ↓

Elementary Metric Event

    ↓

Metric Cluster

    ↓

Internal Metric Timeline

    ↓

Beat Reference

---

# Repository Analysis

## Core PulseCandidate

The Core implementation represents an observable temporal candidate
derived from audio analysis.

Characteristics:

- timestamp;
- onset strength;
- confidence.

It does not perform:

- pulse estimation;
- beat estimation;
- musical interpretation.

---

## Domain PulseCandidate

The Domain implementation represents a source-associated temporal
candidate.

Characteristics:

- identity;
- sound source;
- timestamp;
- confidence;
- creation metadata.

Its relationship with Elementary Metric Event requires scientific
clarification.

---

# Domain Model Observations

The current Domain Model contains:

- ElementaryMetricEvent;
- MetricCluster;
- Pulse;
- InternalMetricTimeline;
- BeatReference.

These entities are consistent with the emergent metric model.

The current open question concerns the position and naming of
PulseCandidate.

---

# PulseCandidateExtractor

The repository contains:

PulseCandidateExtractor

inside:

jga.domain.services

The abstraction currently has no implementation and is not used
by the runtime.

Its architectural location requires review because extraction
from audio observation may belong outside the Domain Layer.

---

# Scientific Questions

1. Should Core PulseCandidate and Domain PulseCandidate receive
different names?

2. Should Domain PulseCandidate remain an explicit Domain entity?

3. Should PulseCandidateExtractor belong to the Observation or Engine
Layer instead of Domain?

4. Should the Domain Map be updated after this review?

5. Does TAC require additional Domain representations?

---

# Scientific Constraints

The following principles remain invariant:

- Observation precedes interpretation.
- Domain entities must not depend on acquisition mechanisms.
- Beat Reference emerges from ensemble behaviour.
- Every abstraction must remain traceable to observable evidence.
- No implementation change precedes architectural approval.

---

# Expected Outcome

This RFC will determine whether the current Domain Model requires
conceptual clarification, naming changes or architectural updates.

Until approval, the current implementation remains the official
reference.

