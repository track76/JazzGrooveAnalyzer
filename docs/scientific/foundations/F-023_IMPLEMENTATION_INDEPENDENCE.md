# F-023 — Implementation Independence

## Status

Scientific Foundation

## Purpose

This document establishes the implementation
independence of the Descriptor Algebra.

## Principle

The Descriptor Algebra is a mathematical object.

Its validity is completely independent from
any software implementation.

## Consequences

A Descriptor Operator exists as a mathematical
transformation before any software implementation.

Software implementations merely realize
previously established mathematical operators.

## Scientific Hierarchy

Scientific Theory

↓

Descriptor Algebra

↓

Software Architecture

↓

Implementation

↓

Execution

Correctness shall always be demonstrated at the
mathematical level before implementation.

## Architectural Consequences

No software component defines
Descriptor Algebra.

Software components shall conform to the
Descriptor Algebra.

## Verification

Mathematical correctness and software correctness
are independent verification processes.

Software validation cannot replace
mathematical validation.

Mathematical validation cannot replace
software validation.

Both are mandatory.

## Consequences for Future Research

Every future Descriptor Operator shall first be

- mathematically defined;

- mathematically verified;

- architecturally integrated;

- implemented;

- tested.

This order is mandatory.

