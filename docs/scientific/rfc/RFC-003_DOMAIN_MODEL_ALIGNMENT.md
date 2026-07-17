# RFC-003 — Domain Model Alignment after TAC Introduction

Version: 0.2 (Draft)

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

# Scientific Context

The introduction of TAC clarified the transition between:

- physical observation;
- temporal contextualization;
- musical representation.

The review focused on the role of PulseCandidate and the relationship
between observation-level candidates and Domain-level entities.

---

# PulseCandidate Classification

Repository analysis identified two concepts sharing the same name.

## Core PulseCandidate

The Core PulseCandidate represents an observable temporal candidate
derived from audio analysis.

It contains observable information such as:

- timestamp;
- strength;
- confidence.

It does not perform:

- pulse estimation;
- beat estimation;
- musical interpretation.

---

## Domain PulseCandidate

The Domain PulseCandidate represents a temporal candidate inside the
musical representation layer.

It contains:

- identity;
- sound source reference;
- timestamp;
- confidence.

Its role is to preserve a domain-level temporal representation before
metric structures are constructed.

---

# Domain Alignment Result

The current Domain Model remains structurally compatible with the TAC
scientific model.

Existing entities:

- MetricContributor;
- ElementaryMetricEvent;
- MetricCluster;
- Pulse;
- InternalMetricTimeline;
- BeatReference;

remain consistent with the emergent metric architecture.

No Domain entity removal or addition is required at this stage.

---

# PulseCandidate Naming

The shared name between Core PulseCandidate and Domain PulseCandidate
creates semantic ambiguity.

A future naming refinement may be considered.

No rename is introduced by this RFC.

---

# PulseCandidateExtractor

The current repository contains an abstract PulseCandidateExtractor
interface without active runtime implementation.

Its architectural responsibility remains unresolved.

No layer migration is introduced at this stage.

---

# Final Scientific Position

The current architecture is considered valid.

The required action is conceptual clarification, not implementation
refactoring.

Future evolution shall proceed only after approval of the scientific
classification of existing entities.

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

This RFC establishes the current scientific alignment between TAC
and the Domain Model.

Further implementation evolution shall follow only after this review
is approved.

