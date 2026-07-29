# M8 — Behaviour Evolution Model

Status: DRAFT

---

# Scientific object

BehaviourEvolutionModel

The BehaviourEvolutionModel is the complete observable description of
the temporal evolution of one BehaviourTrajectory.

---

# Composition

BehaviourEvolutionModel

├── Behaviour States
├── Behaviour Transitions
├── Stable Regions
├── Transition Regions
└── Evolution Episodes

---

# Behaviour State

Definition

A Behaviour State is a maximal interval during which the observable
behaviour remains internally coherent according to explicitly defined
scientific criteria.

Properties

- temporal interval
- representative behaviour
- local stability
- traceability

---

# Behaviour Transition

Definition

A Behaviour Transition is the observable change connecting two
Behaviour States.

Properties

- origin state
- destination state
- transition interval
- transition magnitude

---

# Stable Region

Definition

A Stable Region is a temporal interval where Behaviour State remains
approximately invariant.

---

# Transition Region

Definition

A Transition Region is a temporal interval where Behaviour State
changes continuously or discontinuously.

---

# Evolution Episode

Definition

An Evolution Episode is the maximal contiguous interval composed by
Stable Regions and Transition Regions.

Episodes partition the BehaviourTrajectory.

---

# Scientific constraints

The BehaviourEvolutionModel

- preserves temporal ordering;
- preserves Behaviour Point identity;
- preserves traceability to MetricCluster;
- preserves traceability to ElementaryMetricEvent;
- introduces no musical interpretation.

---

# Architectural contracts

Input

BehaviourTrajectory

Output

BehaviourEvolutionModel

Responsibility

Describe observable temporal evolution.

Invariant

BehaviourTrajectory is never modified.
