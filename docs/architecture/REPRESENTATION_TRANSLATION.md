# Representation Translation

Status: Stable

---

# Purpose

This document defines the architectural contract between
computational representations produced by the Core and
semantic representations interpreted by the Domain.

Its purpose is to establish a deterministic, traceable and
scientifically interpretable translation layer without
introducing musical interpretation into the computational
pipeline.

This document formally closes the architectural definition
of the Translation Layer.

---

# Architectural Principle

The Translation Layer represents the unique boundary between
computational representations and Domain semantics.

No computational component shall directly instantiate
Domain objects.

Likewise, Domain Services shall never access raw computational
representations.

---

# Responsibilities

The Translation Layer is responsible for:

- receiving computational representations produced by the Core;
- preserving every observable property required by the scientific model;
- transforming computational representations into Domain inputs;
- maintaining complete traceability between observations and Domain objects;
- remaining deterministic and reproducible.

The Translation Layer does not perform musical analysis.

The Translation Layer does not estimate tempo.

The Translation Layer does not infer Beat Reference.

The Translation Layer performs representation translation only.

---

# Translation Boundary

Acquisition
        │
Observation
        │
DSP
        │
────────────────────────────────
 Translation Layer
────────────────────────────────
        │
Domain Services
        │
Analysis

---

# Ownership

Observation owns observable physical phenomena.

DSP owns computational representations.

Translation owns representation mapping.

Domain owns semantic interpretation.

Analysis owns scientific reasoning.

Responsibilities shall never overlap.

---

# Architectural Invariants

The following rules are considered permanent.

1. No DSP algorithm creates Domain objects.

2. Every Domain object originates through the Translation Layer.

3. Translation is deterministic.

4. Translation preserves scientific observability.

5. Translation never introduces musical interpretation.

6. Domain Services remain independent from DSP implementations.

7. Every translation must be reproducible.

---

# Traceability

Every Domain object shall be traceable to the computational
representation from which it originated.

No semantic information may appear without a corresponding
observable origin.

---

# Implementation Strategy

The Translation Layer will be implemented during
Milestone M4 (Metric Reconstruction).

Possible implementation components include dedicated
translation services responsible for converting computational
representations into Domain inputs while preserving complete
architectural separation.

Concrete implementation decisions shall not modify the
architectural contract defined in this document.

---

# Status

The architectural definition of the Translation Layer is
considered complete.

Future work concerns implementation only.

