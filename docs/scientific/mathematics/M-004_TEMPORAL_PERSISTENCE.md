# M-004 — Mathematical Specification of the Temporal Persistence Descriptor

## Status

Official

---

# 1. Purpose

This document defines the mathematical properties of the
Temporal Persistence Descriptor.

The descriptor measures how long a validated behavioural
observation persists inside a temporal interval.

It does not reconstruct behaviour.

It only quantifies an existing BehaviourObservation.

---

# 2. Input

BehaviourObservation

---

# 3. Output

BehaviourDescriptor

Descriptor Name

TemporalPersistence

Descriptor Range

[0.0, 1.0]

---

# 4. Scientific Meaning

TemporalPersistence represents the relative duration of a
validated behavioural state.

Higher values indicate that a behaviour remains observable
for a longer temporal interval.

The descriptor does not evaluate musical quality.

---

# 5. Mathematical Definition

Let:

D = duration of the BehaviourObservation

T = total duration of the analysed InternalMetricTimeline

The descriptor is:

TemporalPersistence = D / T

subject to:

T > 0

---

# 6. Mathematical Properties

The descriptor shall satisfy:

- Determinism
- Reproducibility
- Traceability
- Locality

---

# 7. Implementation Constraints

The descriptor shall:

- use only validated Domain information;
- never access raw audio;
- never reconstruct metric information;
- never introduce new observable variables.

