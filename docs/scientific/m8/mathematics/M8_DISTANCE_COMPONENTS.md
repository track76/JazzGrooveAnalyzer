# M8 Behaviour Distance Components

Status: DRAFT

==================================================

Objective

Define which observable components contribute to the
BehaviourDistance.

==================================================

Scientific Principle

BehaviourDistance is computed exclusively from
observable quantities contained in
BehaviourObservation.

==================================================

Component Selection

Each observable component may contribute to the final
distance.

The contribution of each component shall be explicitly
defined and scientifically justified.

==================================================

Requirements

- observable

- deterministic

- reproducible

- independently measurable

==================================================

Architectural Rule

No BehaviourDistanceMetric implementation may use
quantities that are not represented by
BehaviourObservation.

