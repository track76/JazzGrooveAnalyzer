# C-015 — Projection Input Contract

Status: APPROVED

Layer: Representation

Depends on:

- C-014 Geometric Projection Contract

---

# Purpose

This document defines the unique scientific input accepted by the
Scientific Projection Engine.

The Projection Engine shall never consume Domain objects directly.

---

# Input Object

ProjectionInput is the unique entry point of the projection process.

It encapsulates a fully validated Representation object.

ProjectionInput owns no scientific interpretation.

ProjectionInput owns no visualization semantics.

---

# Responsibilities

ProjectionInput shall:

- preserve provenance;
- preserve determinism;
- preserve immutability;
- preserve representation integrity.

---

# Forbidden Operations

ProjectionInput shall never:

- modify Representation objects;
- generate coordinates;
- perform analysis;
- perform aggregation;
- infer musical behaviour.

---

# Architectural Position

Representation
        ↓
ProjectionInput
        ↓
ScientificProjectionEngine
        ↓
MetricPoint

---

# E0F-005

- [x] Domain untouched.
- [x] Translation untouched.
- [x] Representation preserved.
- [x] Visualization independent.

Result: PASS.

