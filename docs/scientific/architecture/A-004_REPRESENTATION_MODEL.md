# A-004 — Representation Model

Status
    PROPOSED

Version
    1.0

Author
    Angelo Tracanna

------------------------------------------------------------
Purpose
------------------------------------------------------------

This document defines the Representation Model of the Jazz
Groove Analyzer.

The Representation Model transforms validated Domain
objects into geometrical representations suitable for
scientific visualization.

Representation objects never replace Domain objects.

They expose the same scientific information in a
representation-oriented form.

------------------------------------------------------------
Architectural Position
------------------------------------------------------------

Observation

↓

Domain

↓

Representation

↓

Visualization

↓

Scientific Report

------------------------------------------------------------
Scientific Principle
------------------------------------------------------------

The Representation Layer never introduces scientific
information.

Every Representation Object shall preserve complete
traceability to the originating Domain objects.

------------------------------------------------------------
Representation Objects
------------------------------------------------------------

The initial Representation Model is composed of:

- MetricClusterPortrait

- MetricLandscape

Future representation objects may be introduced only if they
do not duplicate Domain entities.

------------------------------------------------------------
Representation Responsibilities
------------------------------------------------------------

Representation Objects:

- organize geometric information

- preserve scientific identity

- expose visualization-ready structures

They never:

- modify Domain objects

- infer musical knowledge

- perform statistical analysis

------------------------------------------------------------
Architectural Independence
------------------------------------------------------------

Representation Objects are independent from graphical
frameworks.

They contain no rendering logic.

They contain no user interface logic.

------------------------------------------------------------
Scientific Traceability
------------------------------------------------------------

Every Representation Object shall remain completely
traceable to:

- Metric Cluster

- Beat Reference

- Elementary Metric Events

This traceability is mandatory for every future
implementation.
