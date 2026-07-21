# M-001 — Mathematical Specification of the Temporal Continuity Descriptor

## Status

Official

---

# 1. Purpose

This document formally defines the mathematical properties of the
Temporal Continuity Descriptor.

The descriptor measures the continuity of a reconstructed
BehaviourObservation.

It never reconstructs temporal information.

It only quantifies an already validated Behaviour representation.

---

# 2. Input

BehaviourObservation

---

# 3. Output

BehaviourDescriptor

Descriptor Name

TemporalContinuity

Descriptor Range

[0.0, 1.0]

where

0.0 = complete temporal discontinuity

1.0 = perfect temporal continuity

---

# 4. Mathematical Properties

The descriptor shall satisfy:

- Determinism
- Reproducibility
- Traceability
- Locality
- Monotonicity

---

# 5. Mathematical Constraints

The descriptor shall always satisfy

0.0 ≤ TemporalContinuity ≤ 1.0

The descriptor shall never produce NaN.

The descriptor shall never produce infinite values.

---

# 6. Scientific Interpretation

Higher values indicate greater temporal continuity.

Lower values indicate greater temporal fragmentation.

The descriptor never evaluates musical quality.

It measures only observable temporal behaviour.

---

# 7. Implementation Constraints

Implementation shall preserve every mathematical property defined in
this document.


---

# 8. Mathematical Definition

Let

N = number of Pulses contained in the BehaviourObservation.

Let

C = number of temporally connected Pulses.

The Temporal Continuity Descriptor is defined as

TemporalContinuity = C / N

subject to

N > 0

The descriptor therefore satisfies

0.0 ≤ TemporalContinuity ≤ 1.0

Perfect temporal continuity

TemporalContinuity = 1.0

occurs when every Pulse of the BehaviourObservation belongs to one
continuous temporal sequence.

Lower values indicate increasing temporal fragmentation.

