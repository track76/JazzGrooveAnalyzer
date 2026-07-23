# F-024 — Operator Compatibility

## Status

Scientific Foundation

## Purpose

This document defines compatibility between
Descriptor Operators.

Compatibility determines whether two Descriptor
Operators may be composed while preserving the
Descriptor Algebra.

## Definition

Let

O₁ : R(B) → R(B)

and

O₂ : R(B) → R(B)

be Descriptor Operators.

O₁ and O₂ are compatible if

Codomain(O₁) = Domain(O₂).

## Compatibility Principle

Every valid operator composition requires
compatibility between adjacent operators.

No implicit conversion is permitted.

## Input

DescriptorRelation

↓

Compatible Descriptor Operator

↓

DescriptorRelation

↓

Compatible Descriptor Operator

↓

DescriptorRelation

## Properties

Operator compatibility

- preserves Behaviour Space;

- preserves Descriptor Relations;

- preserves Input/Output contracts;

- guarantees valid composition.

## Consequences

Every analytical pipeline is a sequence of
pairwise compatible Descriptor Operators.

Compatibility is a necessary condition for
Descriptor Algebra composition.

## Architectural Consistency

Compatibility is evaluated exclusively through
declared Domain and Codomain.

Implementation details are irrelevant.

