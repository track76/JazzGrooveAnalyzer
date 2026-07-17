# F-001 — Scientific Observation

Version: 1.1 (Draft)

Status:
UNDER REVIEW

Author:
Angelo Tracanna

---

# Purpose

This document defines the scientific observation model
adopted by the Jazz Groove Analyzer.

It is a Foundation Document.

No implementation may contradict the principles
defined here.

---

# Principle

The Jazz Groove Analyzer is not a beat correction
system.

It is not a quantization system.

It is not a performance enhancement system.

The JGA is a scientific observation framework.

Its purpose is to observe, document and describe
musical events without altering them.

---

# Observation Layer

The physical observation of a musical performance is
performed by the Observation Layer.

The Observation Layer transforms the audio signal into
observable events (such as Onsets) without introducing
musical interpretation.

These observations preserve the temporal reality of the
recorded performance.

---

# Observable Musical Event

Every Elementary Metric Event (EME) represents
an observable musical fact.

An EME preserves its original occurrence in time.

The JGA never moves, corrects or quantizes
an observed event.

The EME belongs to the Domain representation and
remains traceable to the physical observations from
which it originates.

---

# Observation Domains

The JGA separates two domains.

Physical Time

Observed directly from the audio signal.

Examples:

- samples
- milliseconds

Metric Time

Built after the Observable Metric Context
has been identified.

Every EME is projected into the Internal
Metric Timeline without changing its original
timestamp.

---

# Scientific Principle

Observation always precedes interpretation.

The JGA first observes.

The JGA then contextualizes.

Only afterwards may musical interpretation
take place.

---

# Consequences

The original musical performance always
remains the source of truth.

The JGA documents musical behaviour.

It never reconstructs an ideal performance.
