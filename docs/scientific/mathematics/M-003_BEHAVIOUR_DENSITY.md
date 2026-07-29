# M-003 — Mathematical Specification of the Behaviour Density Descriptor

## Status

Official

---

# 1. Purpose

This document defines the mathematical properties of the
Behaviour Density Descriptor.

The descriptor measures the density of validated behavioural
observations inside a temporal interval.

It does not reconstruct behaviour.

It only quantifies an existing BehaviourObservation.

---

# 2. Input

BehaviourObservation

---

# 3. Output

BehaviourDescriptor

Descriptor Name

BehaviourDensity

Descriptor Range

[0.0, 1.0]

---

# 4. Scientific Meaning

BehaviourDensity represents the relative concentration of
validated Pulse events inside a BehaviourObservation.

Higher values indicate a higher number of temporal events
inside the observed interval.

The descriptor does not evaluate musical quality.

---

# 5. Mathematical Definition

Let:

N = number of Pulses contained in the BehaviourObservation

T = temporal duration of the BehaviourObservation

The density is:

BehaviourDensity = N / (N + T)

subject to:

N > 0

T >= 0

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

