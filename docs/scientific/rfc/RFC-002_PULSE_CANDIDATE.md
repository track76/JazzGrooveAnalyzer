# RFC-002 — Scientific Nature of the PulseCandidate

Version: 0.2 (Draft)

Status:
UNDER DISCUSSION

Author:
Angelo Tracanna

---

# Purpose

This RFC investigates the scientific nature of the PulseCandidate within the
Jazz Groove Analyzer (JGA).

Its objective is to determine the exact role of the PulseCandidate in the
transition between physical observation and musical representation.

No implementation shall be modified until this RFC is approved.

---

# Motivation

The PulseCandidate is currently positioned between the observation process
and the construction of Elementary Metric Events (EMEs).

However, its scientific meaning is not yet fully defined.

The current name suggests a possible contribution to pulse estimation, while
the observation model under review raises the question of whether the object
should instead represent a purely observable sound event.

---

# Current Position

Current simplified pipeline:

Audio Signal
    ↓
PulseCandidate
    ↓
Elementary Metric Event
    ↓
Metric Cluster

---

# Repository Analysis

Repository inspection produced the following observations.

The current PulseCandidateBuilder:

- detects audio onsets;
- measures onset strength;
- creates one PulseCandidate for every detected onset;
- assigns an initial confidence value.

No pulse estimation is performed.

No beat estimation is performed.

No metric interpretation is introduced.

The PulseCandidateFilter:

- removes weak candidates;
- removes temporally redundant candidates;
- preserves only the strongest candidate within the configured time window.

No musical semantics are introduced by the filtering stage.

Therefore, the current implementation treats a PulseCandidate as an
onset-derived observation rather than as an already established metric
hypothesis.

---

# Scientific Questions

The following questions remain open.

1. Is a PulseCandidate already a metric hypothesis?

2. Does a PulseCandidate belong to the observation domain or to the
representation domain?

3. Does every observable sound event generate a PulseCandidate?

4. Should PulseCandidates already exclude acoustically irrelevant events?

5. Is the current name scientifically appropriate?

---

# Working Hypothesis

Based on the current implementation, the name PulseCandidate appears to
describe the intended future role of the object rather than its current
behaviour.

This hypothesis requires further scientific validation before any change to
the Domain Model or implementation is considered.

---

# Scientific Constraints

The following principles are considered invariant.

- Observation always precedes interpretation.
- No musical meaning may be introduced without observable evidence.
- Every higher-level representation must remain traceable to physical
  observations.
- The repository remains the source of truth.

---

# Expected Outcome

This RFC shall determine the scientific definition of the PulseCandidate.

Its conclusions may require updates to the observation model, the theoretical
framework and the Domain Model.

Until this RFC is approved, the current implementation remains the official
reference.
