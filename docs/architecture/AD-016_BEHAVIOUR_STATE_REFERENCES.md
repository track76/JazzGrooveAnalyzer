# AD-016 — BehaviourState References BehaviourTrajectory

Status: LOCKED

## Context

Behaviour Evolution analyses one BehaviourTrajectory.

BehaviourState is not an independent geometric object.

## Decision

BehaviourState SHALL reference one BehaviourTrajectory.

BehaviourState SHALL identify an observable interval inside that
trajectory.

BehaviourState SHALL NOT own GeometricPoint objects.

BehaviourTrajectory remains the single source of truth.

## Consequences

- no duplication of geometry
- immutable architecture
- complete traceability
- lower memory footprint
- future descriptors remain attachable to BehaviourState

## Architectural Rule

Geometry owns geometry.

Behaviour Evolution owns interpretation.

