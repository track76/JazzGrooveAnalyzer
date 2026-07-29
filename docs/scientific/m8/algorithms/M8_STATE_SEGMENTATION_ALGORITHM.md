# M8 State Segmentation Algorithm

Status: DRAFT

==================================================

Purpose

Identify BehaviourState boundaries along one
BehaviourTrajectory.

==================================================

Input

BehaviourTrajectory

==================================================

Output

Ordered BehaviourState sequence.

==================================================

Observational Principle

A BehaviourState exists while the observable behaviour
remains locally coherent.

A new BehaviourState begins when a measurable behavioural
discontinuity is detected.

==================================================

Algorithm Responsibilities

- analyse the complete trajectory

- preserve temporal ordering

- detect state boundaries

- produce complete coverage

==================================================

Algorithm Constraints

- deterministic

- reproducible

- no random decisions

- no heuristic thresholds without scientific justification

- no musical interpretation

==================================================

Boundary Detection

Boundary detection SHALL depend only on observable
changes measured along the BehaviourTrajectory.

No external metadata shall be used.

==================================================

Architectural Rule

BehaviourTrajectory

↓

BehaviourStateSegmenter

↓

BehaviourState*

The segmenter never modifies the trajectory.

