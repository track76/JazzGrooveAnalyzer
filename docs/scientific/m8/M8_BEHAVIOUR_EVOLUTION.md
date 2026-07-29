# M8 — Behaviour Evolution

Status: DRAFT

---

# Objective

Behaviour Evolution studies the observable temporal evolution of a
BehaviourTrajectory.

This layer does not generate new Behaviour Points.

It analyses how an existing BehaviourTrajectory evolves through time.

---

# Position inside the JGA architecture

Audio
    ↓
Metric Reconstruction
    ↓
Behaviour Quantification
    ↓
Descriptor System
    ↓
Descriptor Algebra
    ↓
Behaviour Analytics
    ↓
Scientific Behaviour Space
    ↓
Behaviour Evolution

---

# Scientific scope

Behaviour Evolution is the first scientific layer that considers
the BehaviourTrajectory itself as the observation object.

Previous layers describe individual observations.

Behaviour Evolution describes the temporal organisation of those
observations.

---

# Input

BehaviourTrajectory

Definition:

An ordered sequence of Behaviour Points already projected inside the
Scientific Behaviour Space.

The trajectory is immutable.

No geometric information is modified.

---

# Output

BehaviourEvolutionModel

The model represents the observable temporal organisation of one
BehaviourTrajectory.

It contains only observable facts.

No musical interpretation is introduced.

---

# Responsibility

Behaviour Evolution is responsible for identifying:

- Behaviour States
- Behaviour Transitions
- Stable Regions
- Transition Regions
- Evolution Episodes

---

# Out of scope

Behaviour Evolution does NOT:

- classify musicians;
- evaluate artistic quality;
- infer intentions;
- infer emotions;
- modify Behaviour Points;
- modify Scientific Behaviour Space.

---

# Scientific primitives

## Behaviour State

A locally coherent temporal behaviour.

---

## Behaviour Transition

Observable transition between two Behaviour States.

---

## Stable Region

Temporal interval where Behaviour State remains approximately constant.

---

## Transition Region

Temporal interval where Behaviour State changes.

---

## Evolution Episode

A maximal continuous temporal interval composed by
Stable Regions and Transition Regions.

---

# Input contract

Input:
    BehaviourTrajectory

Output:
    BehaviourEvolutionModel

Responsibility:
    Analyse temporal evolution.

Preserved invariants:

- point ordering;
- temporal ordering;
- Behaviour Point identity;
- traceability to MetricCluster;
- traceability to ElementaryMetricEvent.

---

# Architectural rule

Behaviour Evolution consumes BehaviourTrajectory.

It never reconstructs trajectories.

It never projects geometry.

Geometry is completed before Behaviour Evolution begins.

