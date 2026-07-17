# JGA Metric Stability Model

Version: 1.0 (Draft)

Status:
UNDER DISCUSSION

Author:
Angelo Tracanna

---

# Purpose

This document formally defines the mathematical
meaning of Metric Stability inside the
Jazz Groove Analyzer.

This document is normative.

Algorithms must follow this specification.

---

# Principle

The JGA never measures "groove".

The JGA measures observable rhythmic behaviour.

Every metric must derive only from observable
audio events.

No musical interpretation is performed.

---

# Regularity

Definition

Regularity measures the temporal consistency
between consecutive Pulse Intervals.

Input

Pulse Intervals

Output

Regularity Score

Range

0.0 – 1.0

Meaning

High values indicate low temporal dispersion.

Regularity does NOT measure duration.

---

# Metric Hierarchy

The JGA distinguishes two kinds of metrics.

## Observed Metrics

Observed Metrics are computed directly from
observable audio events.

They do not depend on any higher-level
musical interpretation.

Current Observed Metrics:

- Pulse Intervals
- Regularity
- Persistence

## Derived Metrics

Derived Metrics are computed from one or
more Observed Metrics.

Current Derived Metrics:

- Metric Stability

# Persistence

Definition

Persistence measures how long a rhythmic
behaviour remains observable.

Input

Observed Pulse Intervals

Output

Persistence Score

Range

0.0 – 1.0

Meaning

A longer stable behaviour has higher persistence.

Persistence does NOT measure precision.

---

# Metric Stability

Definition

Metric Stability is an emergent property.

It is not measured directly.

Metric Stability derives from:

- Regularity
- Persistence

Metric Stability therefore represents the
degree to which a rhythmic behaviour is both:

- temporally regular
- temporally persistent

---

# Determinism

Metric Stability is deterministic.

Given the same Pulse Intervals,
the JGA must always produce the same
Metric Stability Score.

No stochastic or heuristic component
is allowed.

This guarantees:

- reproducibility

- scientific validation

- deterministic testing


# Responsibilities

RegularityScorer

Computes temporal regularity.

PersistenceScorer

Computes temporal persistence.

StabilityScorer

Combines Regularity and Persistence.

It must not recompute them.

---

# Architectural Rule

The Engine never computes Metric Stability.

The Engine delegates mathematical evaluation
to the Math Layer.

---

# Future Extensions

Future versions may include:

- confidence estimation

- local stability

- adaptive windows

- multiple periodic regions

without changing the meaning of
Metric Stability defined here.

