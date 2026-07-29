# M8 Observable Evaluation

Status: DRAFT

==================================================

Objective

Define how observable quantities are evaluated before
BoundaryEvidence is produced.

==================================================

Scientific Principle

Evaluation transforms observable measurements into
scientific evidence.

It does not create BehaviourStates.

==================================================

Input

BehaviourTrajectory

BehaviourDescriptors

==================================================

Output

ObservableEvaluation

==================================================

Responsibilities

- evaluate observable quantities

- identify significant variations

- reject insignificant fluctuations

- preserve temporal ordering

==================================================

Architectural Pipeline

BehaviourTrajectory
        ↓
ObservableEvaluation
        ↓
BoundaryEvidence
        ↓
BehaviourState

==================================================

Architectural Rule

Evaluation precedes evidence generation.

Evidence precedes state construction.

