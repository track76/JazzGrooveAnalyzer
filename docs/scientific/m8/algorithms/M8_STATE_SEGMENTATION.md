# M8 State Segmentation

Status: DRAFT

==================================================

Objective

Segment one BehaviourTrajectory into a sequence of
BehaviourStates.

==================================================

Input

BehaviourTrajectory

==================================================

Output

Ordered BehaviourState sequence.

==================================================

Principles

- purely observational
- deterministic
- reproducible
- no musical interpretation
- no statistical assumptions

==================================================

Scientific Question

Given one BehaviourTrajectory,

where does one BehaviourState end and another begin?

==================================================

Output Constraints

- complete coverage

- no overlaps

- no gaps

- temporal ordering preserved

==================================================

Architectural Rule

Segmentation never modifies
BehaviourTrajectory.

It only produces BehaviourState objects.

