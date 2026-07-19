# F-005 — Ensemble Behaviour

## Purpose

The purpose of Ensemble Behaviour is to describe the collective temporal
behaviour emerging from the Internal Metric Timeline.

Unlike observable musical events, Ensemble Behaviour represents the
dynamic evolution of the reconstructed temporal model throughout the
performance.

---

## Ensemble Metric Continuity

The Internal Metric Timeline is a continuous temporal representation.

Temporal continuity does not imply the uninterrupted presence of
observable musical events.

Instead, continuity describes the persistence of the reconstructed
metric reference despite local variations in the observable signal.

Consequently, temporary silences, missing attacks or sparse metric
activity do not necessarily interrupt the Internal Metric Timeline.

---

## Scientific Definition

Temporal continuity is the property that allows consecutive Pulse
entities to be interpreted as belonging to the same reconstructed
Internal Metric Timeline.

The continuity of the Internal Metric Timeline is inferred exclusively
from the reconstructed Pulse sequence.

No external musical information shall be introduced.

---

## Scientific Invariants

### Invariant 1

Temporal continuity is reconstructed exclusively from the Pulse
sequence.

### Invariant 2

Temporal continuity never modifies Pulse entities.

### Invariant 3

Temporal continuity never creates additional Pulse entities.

### Invariant 4

Temporal continuity never alters physical timestamps.

### Invariant 5

Temporal continuity is deterministic.

The same Pulse sequence always produces the same continuity
representation.

---

## Architectural Consequences

Temporal continuity is a property of the Pulse sequence as a whole.

It is never a property of an individual Pulse.

Therefore every algorithm operating on temporal continuity shall analyse
the complete Pulse sequence rather than isolated Pulse entities.
