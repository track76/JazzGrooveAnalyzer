# M8 Behaviour Distance Properties

Status: DRAFT

==================================================

Objective

Define the mathematical properties required for every
BehaviourDistanceMetric implementation.

==================================================

Identity

The distance between identical observations shall be
zero.

==================================================

Non-Negativity

A behavioural distance shall never be negative.

==================================================

Symmetry

The distance from A to B shall equal the distance from
B to A.

==================================================

Monotonicity

Greater behavioural differences shall never produce
smaller distances.

==================================================

Reproducibility

Repeated evaluation of the same observations shall
always produce the same BehaviourDistance.

==================================================

Architectural Rule

Every BehaviourDistanceMetric implementation shall
satisfy these properties before being integrated into
Boundary Detection.

