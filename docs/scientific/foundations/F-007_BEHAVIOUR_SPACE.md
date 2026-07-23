# F-007 — Behaviour Space

## Status

Draft

## Purpose

This document introduces the mathematical space in which BehaviourDescriptors
exist. It establishes the theoretical foundation for Behaviour Analytics.

## Motivation

Representation produces observable behavioural facts.

Quantification transforms observations into BehaviourDescriptors.

Behaviour Analytics operates exclusively on BehaviourDescriptors.

Therefore every BehaviourDescriptor shall belong to a formally defined
mathematical space called Behaviour Space.

## Definition

Let

B

be the Behaviour Space.

A BehaviourDescriptor is an element

d ∈ B

Behaviour Space contains only quantified behavioural entities.

Raw observations never belong to Behaviour Space.

## Principles

1. Representation never creates Behaviour Space.

2. Quantification maps observations into Behaviour Space.

3. Analytics operates only inside Behaviour Space.

4. Operators never modify observations.

5. Operators transform BehaviourDescriptors.

## Mapping

BehaviourObservation

↓

BehaviourDescriptor

↓

Behaviour Space

↓

Descriptor Relation

↓

Descriptor Operator

↓

Analytical Structure

## Consequences

All Descriptor Operators shall explicitly declare

- Domain

- Codomain

- Preconditions

- Postconditions

No operator may accept objects outside Behaviour Space.

