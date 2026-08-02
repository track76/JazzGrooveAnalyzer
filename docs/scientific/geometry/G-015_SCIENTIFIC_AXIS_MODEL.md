# G-015 — Scientific Axis Model


Status

PROPOSED


Version

1.0


Author

Angelo Tracanna


------------------------------------------------------------
Purpose
------------------------------------------------------------

This document defines the semantic model of scientific axes
inside the Representation Layer of the Jazz Groove Analyzer.


Scientific axes provide the mathematical dimensions required
to represent observable musical phenomena.

They do not introduce new information.

They organize and preserve information already produced by
the Domain Layer.


------------------------------------------------------------
Fundamental Principle
------------------------------------------------------------

A scientific axis represents exactly one measurable
scientific dimension.

An axis must have:

- explicit semantic meaning;
- explicit scientific unit;
- deterministic calculation;
- complete provenance.


An axis never represents:

- graphical position;
- screen coordinates;
- rendering information;
- user interface concepts;
- musical judgement;
- aesthetic interpretation.


------------------------------------------------------------
Architectural Position
------------------------------------------------------------

Scientific axes belong exclusively to the Representation Layer.


Audio

↓

Domain

↓

Representation

↓

Visualization


The Domain Layer does not define axes.

The Visualization Layer consumes axes but never defines
their scientific meaning.


------------------------------------------------------------
Axis Definition
------------------------------------------------------------

Every scientific axis shall define:


Identifier

A stable unique identifier.


Semantic Meaning

The scientific property represented by the axis.


Unit

The measurement unit associated with the represented quantity.


Provenance

The Domain information from which the axis value is derived.


Mathematical Domain

The valid numerical range and constraints.


------------------------------------------------------------
Current Axis Model
------------------------------------------------------------


AXIS-001

Identifier:

metric_temporal_displacement


Name:

Metric Temporal Displacement


Meaning:

Temporal displacement between one
ElementaryMetricEvent and its BeatReference.


Unit:

milliseconds


Source:

ElementaryMetricEvent timestamp

and

BeatReference timestamp


Calculation:

event.timestamp - beat_reference.timestamp


Status:

DEFINED


------------------------------------------------------------
Axis Independence
------------------------------------------------------------

Each axis must represent one independent scientific dimension.

An axis must not encode multiple unrelated properties.


Correlation between axes belongs to later analytical
processing and never to axis definition.


------------------------------------------------------------
Axis Invariants
------------------------------------------------------------

Every scientific axis shall preserve:

- determinism;
- reproducibility;
- scientific traceability;
- renderer independence;
- visualization independence.


------------------------------------------------------------
Forbidden Operations
------------------------------------------------------------

The following operations are forbidden:

- introducing graphical semantics into an axis;
- modifying axis meaning during visualization;
- deriving axes from rendering requirements;
- combining unrelated scientific dimensions.


------------------------------------------------------------
Future Extensions
------------------------------------------------------------

Additional axes may be introduced only when:

- the represented property is observable;
- the mathematical definition is explicit;
- provenance is preserved;
- compatibility with existing coordinates is maintained.


------------------------------------------------------------
Architectural Consequence
------------------------------------------------------------

Scientific axes establish the semantic foundation for:

- ScientificCoordinate;
- CoordinateSystem;
- Metric Geometry;
- future Visualization Layer.


A visualization is therefore a projection of scientific
axes and never the origin of their meaning.
