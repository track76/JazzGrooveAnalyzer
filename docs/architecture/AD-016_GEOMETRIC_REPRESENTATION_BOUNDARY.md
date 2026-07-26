# AD-016 — Geometric Representation Boundary

Status
    ACCEPTED

------------------------------------------------------------
Decision
------------------------------------------------------------

Metric Geometry does not introduce new Domain entities.

The Domain Model remains the single scientific
representation of observable musical phenomena.

Geometry constitutes a Representation Layer built on top of
existing Domain entities.

------------------------------------------------------------
Rationale
------------------------------------------------------------

The following Domain entities already contain the complete
scientific information required by Metric Geometry:

- ElementaryMetricEvent

- BeatReference

- MetricCluster

Introducing geometric equivalents of these entities would
duplicate scientific information and violate the
architectural separation between Domain and Representation.

------------------------------------------------------------
Consequences
------------------------------------------------------------

The Geometry layer operates exclusively through
representational transformations.

It does not duplicate Domain objects.

It does not modify Domain objects.

It does not introduce alternative scientific identities.

Future geometric builders shall consume existing Domain
entities and generate Representation objects only.

