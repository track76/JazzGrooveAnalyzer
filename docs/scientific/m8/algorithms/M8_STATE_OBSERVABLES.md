# M8 State Observables

Status: DRAFT

==================================================

Objective

Define which observable quantities may justify the
beginning of a new BehaviourState.

==================================================

Scientific Principle

Only observable quantities produced by previous
JGA layers may participate in BehaviourState
segmentation.

No hidden variables are permitted.

==================================================

Candidate Observables

- trajectory direction

- trajectory curvature

- behavioural density

- behavioural continuity

- behavioural persistence

- descriptor stability

- descriptor variation

==================================================

Forbidden Inputs

- musical style

- performer identity

- harmonic analysis

- genre

- historical information

- metadata

==================================================

Decision Rule

A BehaviourState boundary may be generated only by
observable changes supported by BehaviourTrajectory
and BehaviourDescriptors.

==================================================

Architectural Dependencies

Metric Reconstruction
        ↓

Behaviour Quantification
        ↓

Behaviour Analytics
        ↓

Scientific Behaviour Space
        ↓

Behaviour Evolution

==================================================

Architectural Rule

Behaviour Evolution consumes previous scientific
results.

It never recreates them.

