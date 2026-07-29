# M8 Domain Model

Status: DRAFT

--------------------------------------------------

ScientificBehaviourSpace
        │
        ▼
BehaviourTrajectory
        │
        ▼
BehaviourEvolutionModel
        │
        ├──────────────┐
        ▼              ▼
BehaviourState   BehaviourTransition
        │              │
        ├──────┐       │
        ▼      ▼       ▼
 StableRegion  TransitionRegion
        │
        ▼
EvolutionEpisode

--------------------------------------------------

ScientificBehaviourSpace

Geometry output.
Contains one or more BehaviourTrajectory objects.

--------------------------------------------------

BehaviourTrajectory

Input object of Behaviour Evolution.

Immutable.

Produced by Geometry.

--------------------------------------------------

BehaviourEvolutionModel

Root aggregate describing the temporal evolution of one
BehaviourTrajectory.

--------------------------------------------------

BehaviourState

Locally coherent behavioural state.

--------------------------------------------------

BehaviourTransition

Observable transition between Behaviour States.

--------------------------------------------------

StableRegion

Temporal interval where BehaviourState remains coherent.

--------------------------------------------------

TransitionRegion

Temporal interval where BehaviourState changes.

--------------------------------------------------

EvolutionEpisode

Maximal contiguous interval composed by StableRegions
and TransitionRegions.

--------------------------------------------------

Traceability

ScientificBehaviourSpace
↓

BehaviourTrajectory
↓

GeometricPoint
↓

MetricCluster
↓

BeatReference
↓

ElementaryMetricEvent

No information loss is permitted.

