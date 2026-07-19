# Jazz Groove Analyzer (JGA)

# Development Constitution

Version: 1.0

Status: LOCKED

---

## Purpose

This document defines the mandatory development methodology of the Jazz Groove Analyzer.

It governs every architectural, scientific and implementation decision.

Whenever a conflict exists between implementation convenience and this Constitution, the Constitution prevails.

---

# Knowledge Hierarchy

Scientific Theory
        ↓
Observation Model
        ↓
Architecture
        ↓
Domain Model
        ↓
Implementation
        ↓
Validation

This order shall never be inverted.

---

# Development Principles

## DP-001

Theory precedes implementation.

---

## DP-002

Architecture precedes code.

---

## DP-003

The simplest scientifically correct solution is always preferred.

---

## DP-004

Do not introduce new classes, services or abstractions unless the existing architecture is demonstrably insufficient.

---

## DP-005

Prefer extending existing components over creating new ones.

---

## DP-006

A software bug must never be solved by violating the architecture.

---

## DP-007

The Core represents observable facts only.

---

## DP-008

The Domain represents musical interpretation only.

---

## DP-009

The Translation Layer is the only boundary between observation and representation.

---

## DP-010

Every abstraction must have one clear scientific responsibility.

---

## DP-011

Before introducing any architectural change, verify whether the existing model already provides the required capability.

---

## Validation

Every significant pipeline modification shall follow:

Tests
        ↓
Real Audio Validation
        ↓
Commit

(see AD-015)

---

## DP-012

Before proposing any modification, determine whether the
problem is scientific, architectural or implementation-related.

---

## DP-013

Before introducing a new abstraction, demonstrate that the
existing architecture is insufficient.

---

## DP-014

When multiple solutions satisfy the scientific model, the
solution introducing the least architectural complexity
shall be preferred.
