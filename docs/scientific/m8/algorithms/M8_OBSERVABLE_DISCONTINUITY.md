# M8 Observable Discontinuity

Status: DRAFT

==================================================

Objective

Define the scientific meaning of an observable
behavioural discontinuity.

==================================================

Definition

An observable discontinuity is a measurable change in
one or more behavioural observables that interrupts
the local coherence of a BehaviourTrajectory.

==================================================

Scientific Properties

An observable discontinuity shall be

- measurable

- reproducible

- explainable

- derived exclusively from observable quantities

==================================================

Non-Discontinuities

The following do not constitute observable
discontinuities.

- isolated numerical noise

- missing observations

- computational artefacts

- single outliers

==================================================

Detection Requirements

Every detected discontinuity shall

- have observable evidence

- preserve temporal ordering

- be traceable to the originating observables

==================================================

Architectural Role

Observable Discontinuity

        ↓

BoundaryEvidence

        ↓

BehaviourState

==================================================

Architectural Rule

BoundaryEvidence formalises an observable
discontinuity.

It never introduces additional interpretation.

