# Core–Domain Boundary

Status: Draft

## Purpose

This document defines the architectural contract between the
computational Core and the semantic Domain.

The objective is to preserve the independence of both layers while
allowing the scientific model to be constructed from computational
representations.

No implementation details are defined in this document.

---

## Responsibilities

### Core

The Core performs computational analysis.

Its responsibilities include:

- audio preprocessing;
- observation;
- DSP;
- temporal analysis;
- intermediate computational representations.

The Core never assigns musical meaning.

---

### Domain

The Domain represents the scientific model of the Jazz Groove Analyzer.

Its responsibilities include:

- musical interpretation;
- metric inference;
- semantic representations;
- construction of the canonical analytical model.

The Domain never depends on DSP implementation details.

---

## Boundary Contract

The Core exposes computational representations.

The Domain consumes semantic representations.

The conversion between the two layers shall occur through a dedicated
translation mechanism.

Neither layer may directly instantiate objects belonging to the other.

---

## Design Principles

Single Responsibility

Each layer owns its own model.

Explicit Translation

Every transition across the boundary must be explicit.

Dependency Direction

Core → Translation → Domain

No reverse dependency is allowed.
