# M-200 — Behaviour Space Projection

## Status

Official

---

# 1. Purpose

This specification defines the transformation from validated
BehaviourDescriptor objects into geometric representations.

The projection preserves the quantitative information contained
in Behaviour Descriptors.

---

# 2. Input

DescriptorSet

---

# 3. Output

ScientificProjectionInput

containing ScientificCoordinate objects.

---

# 4. Definition

Given:

D = {d1, d2, ..., dn}

each descriptor generates one scientific coordinate:

Ci = projection(di)

where:

- coordinate name preserves descriptor identity;
- coordinate value preserves descriptor value;
- unit defines the measurement domain.

---

# 5. Constraints

Projection shall:

- not modify descriptors;
- not generate new measurements;
- not access audio;
- preserve provenance.

---

# 6. Future Extensions

Future specifications may define:

- geometric distance;
- trajectory evolution;
- behaviour comparison.

