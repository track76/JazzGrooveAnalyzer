# M8 Boundary Detection

Status: DRAFT

==================================================

Objective

Detect observable BehaviourState boundaries.

Boundary detection precedes state segmentation.

==================================================

Input

BehaviourTrajectory

BehaviourDescriptors

==================================================

Output

Ordered Boundary sequence.

==================================================

Responsibilities

- analyse observables

- detect discontinuities

- reject local fluctuations

- preserve temporal ordering

==================================================

Non Responsibilities

- build BehaviourState

- merge regions

- classify behaviour

==================================================

Architectural Pipeline

BehaviourTrajectory
        ↓
BoundaryDetector
        ↓
Boundary*
        ↓
BehaviourStateSegmenter
        ↓
BehaviourState*

==================================================

Architectural Rule

Boundary detection identifies evidence.

Segmentation builds domain objects.

