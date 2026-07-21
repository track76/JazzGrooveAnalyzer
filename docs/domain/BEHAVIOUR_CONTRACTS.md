# Behaviour Contracts

## Purpose

This document defines the formal contracts governing Behaviour Analysis.

Behaviour Analysis starts after Metric Reconstruction has been completed.

Its responsibility is to transform reconstructed metric representations into
behavioural representations without altering any previously validated entity.

---

# Contract BA-001

## Name

BehaviourObservationBuilder

### Input

InternalMetricTimeline

### Output

BehaviourObservation*

### Preconditions

- InternalMetricTimeline exists
- Timeline is valid
- Timeline contains at least two consecutive Pulse objects

### Postconditions

- One or more BehaviourObservation objects are created
- No modification is performed on the input timeline

---

# Contract BA-002

## Name

BehaviourProfileBuilder

### Input

BehaviourObservation*

### Output

BehaviourProfile

### Preconditions

- At least one BehaviourObservation exists
- Observations belong to the same InternalMetricTimeline

### Postconditions

- One BehaviourProfile is produced
- BehaviourProfile completely represents the analysed behaviour
- BehaviourProfile becomes the canonical output of M5

---

# Architectural Invariants

Behaviour Analysis never modifies:

- ElementaryMetricEvent
- MetricCluster
- Pulse
- InternalMetricTimeline

Behaviour Analysis only creates new behavioural representations.

---

# Representation Flow

InternalMetricTimeline

↓

BehaviourObservation

↓

BehaviourProfile

No implicit transformations are allowed.

Each transformation has one declared input and one declared output.

---

# Validation

Every Behaviour Analysis stage must be validated through:

1. Unit Tests
2. Integration Tests
3. Real Audio Validation
4. Architectural Contract Verification

Implementation is allowed only after successful validation of every previous step.
