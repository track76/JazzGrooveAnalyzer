# M8 Domain Design

Status: DRAFT

==================================================

Aggregate Root

BehaviourEvolutionModel

Input

BehaviourTrajectory

Output

Complete observable temporal evolution.

Responsibilities

- own all evolution entities
- preserve ordering
- preserve traceability

Invariant

BehaviourTrajectory is immutable.

==================================================

Entity

BehaviourState

Input

BehaviourTrajectory interval.

Output

Locally coherent behavioural state.

Responsibilities

- represent one stable behavioural condition
- expose temporal boundaries

Invariants

- contiguous interval
- non-empty interval

==================================================

Entity

BehaviourTransition

Input

Two consecutive BehaviourStates.

Output

Observable transition.

Responsibilities

- connect states
- describe observable change

Invariants

- one origin
- one destination
- positive duration

==================================================

Entity

StableRegion

Input

BehaviourState.

Output

Stable temporal interval.

Responsibilities

Represent behavioural stability.

Invariant

Contains exactly one BehaviourState.

==================================================

Entity

TransitionRegion

Input

BehaviourTransition.

Output

Transition interval.

Responsibilities

Represent behavioural change.

Invariant

Contains exactly one BehaviourTransition.

==================================================

Entity

EvolutionEpisode

Input

StableRegions
TransitionRegions

Output

Complete contiguous behavioural episode.

Responsibilities

Group one complete evolution episode.

Invariant

Temporal continuity is preserved.

==================================================

Architectural rule

Behaviour Evolution never modifies

- BehaviourTrajectory
- GeometricPoint
- MetricCluster
- ScientificBehaviourSpace

It only produces higher-level observable objects.

