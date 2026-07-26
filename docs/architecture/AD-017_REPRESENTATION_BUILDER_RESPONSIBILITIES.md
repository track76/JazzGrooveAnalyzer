# AD-017 — Representation Builder Responsibilities

Status
    ACCEPTED

------------------------------------------------------------
Decision
------------------------------------------------------------

Representation builders shall have a single responsibility.

MetricPointBuilder is responsible for creating MetricPoint
objects from validated Domain entities.

MetricClusterPortraitBuilder is responsible only for
assembling MetricClusterPortrait objects from existing
MetricPoint instances.

Future projection services shall compute geometric
measurements independently from representation builders.

------------------------------------------------------------
Rationale
------------------------------------------------------------

Representation construction and geometric measurement are
distinct architectural responsibilities.

Keeping them separated preserves modularity, testability and
scientific traceability.

------------------------------------------------------------
Consequences
------------------------------------------------------------

MetricClusterPortraitBuilder shall not compute geometric
measurements.

MetricProjectionService (or equivalent future component)
shall remain solely responsible for geometric projection.

