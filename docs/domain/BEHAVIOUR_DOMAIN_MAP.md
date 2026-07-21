# Behaviour Domain Map

## Purpose

Behaviour Analysis describes the temporal evolution of the reconstructed metric
structure produced by M4.

Its purpose is not to reconstruct metric entities but to represent their dynamic
behaviour.

---

# Domain Input

InternalMetricTimeline

---

# Domain Output

BehaviourProfile

---

# Domain Entities

## BehaviourObservation

Represents a local temporal observation extracted from an InternalMetricTimeline.

It is the smallest observable behavioural unit.

---

## BehaviourProfile

Represents the complete behavioural description of an analysed performance.

It is the canonical output of Behaviour Analysis.

---

# Entity Relationships

InternalMetricTimeline

↓

BehaviourObservation*

↓

BehaviourProfile

---

# Builder Responsibilities

BehaviourObservationBuilder

Creates BehaviourObservation objects from an InternalMetricTimeline.

BehaviourProfileBuilder

Aggregates BehaviourObservation objects into one BehaviourProfile.

---

# Architectural Constraints

Behaviour Analysis never modifies:

- Pulse
- MetricCluster
- ElementaryMetricEvent
- InternalMetricTimeline

Behaviour Analysis only creates new behavioural representations.

---

# Scientific Constraints

Behaviour has no musical meaning.

Behaviour has no stylistic meaning.

Behaviour is a descriptive representation of reconstructed temporal behaviour.

---

# Canonical Pipeline

InternalMetricTimeline

↓

BehaviourObservationBuilder

↓

BehaviourProfileBuilder

↓

BehaviourProfile
