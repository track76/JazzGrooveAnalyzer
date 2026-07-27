# Behaviour Space Domain Model

## Status

Draft

---

# Purpose

This document defines the Domain Model associated with the Scientific
Behaviour Space introduced in Foundation F-007.

The Behaviour Space is a scientific representation of observable rhythmic
behaviours.

The Domain Model introduces the entities required to represent such space
without introducing interpretation.

---

# Domain Entities

## ScientificBehaviourSpace

Represents the complete scientific space generated for one analysis.

Contains:

- BehaviourTrajectory
- BehaviourRegion (future)
- BehaviourDistance (future)

---

## BehaviourTrajectory

Represents the chronological evolution of one observable behaviour.

Properties:

- ordered
- immutable
- reproducible

A trajectory is composed of BehaviourPoints.

---

## BehaviourPoint

Represents one observable behaviour projected inside the Behaviour Space.

A BehaviourPoint is not an audio event.

It is a scientific projection of an observable metric behaviour.

---

## BehaviourDistance

Represents the scientific distance between two BehaviourPoints.

Its mathematical definition is intentionally left open until future
scientific validation.

---

## BehaviourRegion

Represents a region containing behaviours with similar observable
properties.

Regions shall emerge from scientific analysis rather than predefined
categories.

---

# Constraints

The Domain Model satisfies:

- deterministic construction
- immutability
- observational traceability
- temporal consistency

---

# Relationships

ScientificBehaviourSpace

        contains

BehaviourTrajectory

        contains

BehaviourPoint

Future milestones will introduce BehaviourDistance and BehaviourRegion.

