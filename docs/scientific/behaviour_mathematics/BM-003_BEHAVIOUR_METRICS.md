# BM-003 — Behaviour Metrics

## Status

Scientific Foundation

## Purpose

This document introduces Behaviour Metrics.

Behaviour Metrics define mathematical distances
between observable behaviours.

They provide the quantitative basis for
comparison without altering Behaviour Space.

## Scientific Principle

A Behaviour Metric quantifies the degree of
difference between two behaviours.

It does not explain the difference.

It measures it.

## Definition

Let

B

be the Behaviour Space.

A Behaviour Metric is a mapping

d : B × B → ℝ≥0

assigning a non-negative real value to every
pair of behaviours.

## Input

Behaviour

×

Behaviour

## Transformation

Metric Evaluation

## Output

Non-negative Real Number

## Metric Properties

A Behaviour Metric shall satisfy

- non-negativity;

- identity of indiscernibles;

- symmetry;

- triangle inequality.

## Interpretation

A smaller value indicates greater behavioural
similarity.

A larger value indicates greater behavioural
difference.

The numerical value has no musical meaning
outside the analytical context in which the
metric is defined.

## Candidate Metrics

Future Behaviour Metrics may evaluate

- rhythmic similarity;

- temporal dispersion;

- metric divergence;

- behavioural persistence;

- structural coherence.

## Architectural Consistency

Behaviour Metrics belong exclusively to the
Behaviour Mathematics layer.

They consume Behaviour representations.

They never modify

- BehaviourDescriptors;

- DescriptorRelations;

- AnalyticalStructures.

## Scientific Consequences

Behaviour Metrics provide the mathematical
foundation for comparison, clustering,
classification and statistical analysis of
observable musical behaviour.

