# F-008 — Descriptor Relations

## Status

Draft

## Purpose

This document formally defines the mathematical relations between
BehaviourDescriptors.

## Motivation

Behaviour Analytics does not operate on isolated descriptors.

It operates on relationships between descriptors.

Therefore DescriptorRelation is a mathematical object.

## Behaviour Space

Let

B

be the Behaviour Space defined in F-007.

A Descriptor Relation is defined as

R ⊆ B × B

Every DescriptorRelation represents an explicitly observable relationship
between two BehaviourDescriptors.

## Principles

DescriptorRelation never modifies descriptors.

DescriptorRelation never creates descriptors.

DescriptorRelation only establishes formal relationships.

## Relation Categories

The framework may define:

- Identity
- Ordering
- Grouping
- Selection

Future extensions may introduce:

- Similarity
- Distance
- Dominance
- Dependency
- Equivalence

without changing the architecture.

## Consequences

Descriptor Operators shall receive DescriptorRelation objects.

Operators never consume raw BehaviourDescriptors directly.

