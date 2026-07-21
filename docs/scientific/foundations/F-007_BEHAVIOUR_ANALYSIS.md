# F-007 — Behaviour Analysis

## Status

Draft

---

# Purpose

Behaviour Analysis is the first scientific level that studies the temporal evolution
of the reconstructed metric structure.

It does not reconstruct musical events.

It does not identify beats.

It does not infer musical meaning.

Its objective is to describe how the reconstructed metric organization evolves
through time.

---

# Input

Behaviour Analysis receives a validated InternalMetricTimeline.

The InternalMetricTimeline represents the complete reconstructed metric
reference produced by M4.

No direct information from the audio signal is used.

---

# Output

Behaviour Analysis produces a BehaviourProfile.

The BehaviourProfile is the canonical representation of the temporal behaviour
of the reconstructed metric structure.

It becomes the formal input of the following analysis stages.

---

# Observable Object

The observable object is not a Pulse.

The observable object is the temporal evolution of the InternalMetricTimeline.

Behaviour therefore represents an emergent property of the reconstructed metric
organization.

---

# Behaviour Definition

Behaviour is defined as:

"The observable temporal evolution of a reconstructed metric structure."

Behaviour is not:

- a beat;
- a pulse;
- an onset;
- a musical interpretation;
- a stylistic classification.

---

# Scientific Principles

## Principle 1

Behaviour emerges from reconstructed metric structures.

It is never directly observable in the audio signal.

---

## Principle 2

Behaviour is evaluated only after metric reconstruction has been completed.

---

## Principle 3

Behaviour never modifies the reconstructed metric representation.

It only describes it.

---

## Principle 4

Behaviour descriptors are measurements.

Behaviour itself is the represented phenomenon.

---

# Domain Contract

Input:

InternalMetricTimeline

Output:

BehaviourProfile

No implicit transformations are allowed.

---

# Architectural Position

Audio

↓

Observation Layer

↓

Metric Reconstruction (M4)

↓

InternalMetricTimeline

↓

Behaviour Analysis (M5)

↓

BehaviourProfile

↓

Historical Comparison (M6)

---

# Consequences

Behaviour Analysis introduces no new musical semantics.

Its purpose is exclusively to describe the dynamic properties of reconstructed
metric behaviour.

