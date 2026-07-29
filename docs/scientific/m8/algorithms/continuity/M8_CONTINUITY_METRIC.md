# M8 Continuity Metric

Status: DRAFT

==================================================

Objective

Define the quantitative notion of behavioural
continuity.

==================================================

Scientific Question

Given two consecutive observations,

how is behavioural continuity measured?

==================================================

Requirements

A continuity metric shall be

- observable

- deterministic

- reproducible

- explainable

==================================================

Metric Properties

The metric shall

- compare consecutive observations

- quantify behavioural similarity

- quantify behavioural variation

- support boundary detection

==================================================

Architectural Rule

Boundary detection depends on the continuity metric.

The continuity metric is independent from
BehaviourState construction.

