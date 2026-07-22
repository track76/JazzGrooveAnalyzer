# F-011 — Descriptor Operators

## Status

Draft

## Purpose

Descriptor Algebra is the mathematical framework formed by the
set of Descriptor Operators.

Descriptor Algebra is NOT represented by a software class.

Every Descriptor Operator performs exactly one deterministic
mathematical transformation.

---

# Scientific Definition

A Descriptor Operator transforms one or more DescriptorRelation
objects into an AnalyticalStructure.

---

# Input

DescriptorRelation*

---

# Output

AnalyticalStructure

---

# Mathematical Principles

Every Descriptor Operator:

- is deterministic;
- is immutable;
- preserves provenance;
- never modifies DescriptorRelation objects;
- never creates BehaviourDescriptors;
- never introduces musical interpretation.

---

# Allowed Operators (M8)

- Identity
- Grouping
- Ordering
- Selection

---

# Reserved Operators

- Aggregation
- Correlation
- Similarity
- Distance
- Projection
- Composition
- Reduction

These operators require their own mathematical specification.

---

# Forbidden Operations

A Descriptor Operator shall never:

- modify descriptors;
- infer musical semantics;
- classify performances;
- predict behaviour;
- alter provenance.

