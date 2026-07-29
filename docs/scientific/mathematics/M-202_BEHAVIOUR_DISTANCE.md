# M-202 — Mathematical Specification of Behaviour Distance

## Status

Official

---

# 1. Purpose

This specification defines the mathematical contract for
scientific distance between Behaviour Spaces.

Behaviour Distance measures the difference between two
validated behavioural representations.

---

# 2. Input

Two comparable Behaviour Spaces.

S1

S2

---

# 3. Output

BehaviourDistance

containing:

- physical distance;
- metric distance;
- normalised distance;
- confidence.

---

# 4. Behaviour Distance Vector

A Behaviour Distance is derived from observable behavioural
dimensions:

D =

(
physical,
metric,
stability,
persistence,
regularity
)

Each component represents one independent scientific
dimension.

---

# 5. Constraints

Behaviour Distance shall:

- operate only on validated representations;
- not access raw audio;
- not introduce musical interpretation;
- preserve descriptor provenance;
- not modify input spaces.

---

# 6. Metric Definition

The numerical formulation of the distance function is deferred.

Future specifications shall define:

- aggregation function;
- weighting model;
- normalization rules.

---

# 7. Relationship with Comparison

Behaviour Space Comparison determines compatibility.

Behaviour Distance quantifies difference only between
compatible spaces.

---

# 8. Future Extensions

Future specifications may define:

- similarity metrics;
- clustering;
- behavioural trajectories comparison.

