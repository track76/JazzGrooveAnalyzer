# M8 Continuity Detection

Status: DRAFT

==================================================

Objective

Determine whether adjacent observations belong to the
same BehaviourState.

==================================================

Scientific Hypothesis

Local behavioural continuity implies persistence of
the current BehaviourState.

BehaviourState transitions occur only when continuity
is observably interrupted.

==================================================

Input

BehaviourTrajectory

==================================================

Output

BoundaryEvidence*

==================================================

First Algorithm

For the initial implementation,

all consecutive observations are assumed to belong to
the same BehaviourState.

Therefore,

no BoundaryEvidence is generated.

==================================================

Rationale

This establishes the reference implementation.

Subsequent versions will progressively replace this
assumption with measurable continuity criteria.

