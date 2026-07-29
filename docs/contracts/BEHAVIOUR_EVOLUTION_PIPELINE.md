# Behaviour Evolution Pipeline Contract

Status: DRAFT

==================================================

Pipeline

BehaviourTrajectory
        ↓
BoundaryDetector
        ↓
BoundaryEvidence*
        ↓
BehaviourStateSegmenter
        ↓
BehaviourState*
        ↓
BehaviourEvolutionBuilder
        ↓
BehaviourEvolutionModel

==================================================

Component Contracts

BoundaryDetector

Input
BehaviourTrajectory

Output
BoundaryEvidence*

--------------------------------------------------

BehaviourStateSegmenter

Input
BoundaryEvidence*

Output
BehaviourState*

--------------------------------------------------

BehaviourEvolutionBuilder

Input
BehaviourState*

Output
BehaviourEvolutionModel

==================================================

Architectural Rule

Each component consumes exactly the output produced
by the previous component.

No component bypasses another.

