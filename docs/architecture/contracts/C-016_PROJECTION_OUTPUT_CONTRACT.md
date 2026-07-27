# C-016 — Projection Output Contract

Status: APPROVED

Layer: Representation

Depends on:

- C-014 Geometric Projection Contract
- C-015 Projection Input Contract
- G-015 Projection Mathematics

---

# 1. Purpose

This document defines the unique output produced by the Scientific
Projection Engine.

The output of every scientific projection shall be a MetricPoint.

No alternative output type is permitted.

---

# 2. Output Identity

Projection shall produce exactly one MetricPoint for every successful
scientific projection.

The MetricPoint represents the geometric encoding of a validated
Representation object.

It does not replace the Representation object.

It complements it.

---

# 3. Ownership

Representation owns MetricPoint.

Projection generates MetricPoint.

Visualization consumes MetricPoint.

Ownership shall never overlap.

---

# 4. Scientific Properties

The produced MetricPoint shall preserve:

- scientific identity;
- provenance;
- temporal consistency;
- deterministic reconstruction;
- representation integrity.

Projection shall never introduce additional scientific meaning.

---

# 5. Immutability

Once generated, a MetricPoint shall be immutable.

Any transformation requiring different coordinates shall generate a new
MetricPoint.

---

# 6. Compatibility

MetricPoint shall remain compatible with:

- MetricTrajectory
- MetricClusterPortrait
- MetricLandscape

without modification of its scientific semantics.

---

# 7. Forbidden Operations

Projection shall never:

- modify an existing MetricPoint;
- reuse MetricPoint instances with different semantics;
- generate visualization-dependent points;
- alter provenance.

---

# 8. Architectural Rule

ProjectionInput
        ↓
ScientificProjectionEngine
        ↓
MetricPoint

MetricPoint is the terminal product of the scientific projection.

No intermediate geometric object shall become part of the public API.

---

# E0F-006

- [x] Compatible with C-014.
- [x] Compatible with C-015.
- [x] Compatible with G-015.
- [x] MetricPoint remains the unique geometric output.
- [x] Domain untouched.
- [x] Visualization untouched.

Result: PASS.

