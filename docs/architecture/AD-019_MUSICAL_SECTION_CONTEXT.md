# AD-019 — Musical Section Context

Status: PROPOSED


## Decision

Jazz Groove Analyzer must support a musical section
context associated with the reconstructed temporal
structure.

A musical section identifies a portion of a performance
according to its formal role inside the composition.


## Context

Jazz performances are not temporally homogeneous.

The same ensemble may change its timing behaviour
depending on:

- introduction
- exposition of the theme
- bridge sections
- improvisation sections
- solos
- final statements


Example:

INTRO

A

B

SOLO SAX

SOLO PIANO

SOLO DOUBLE BASS

OUTRO


These sections provide analytical context for the
interpretation of timing behaviour.


## Problem

Without section context, timing analysis produces a
continuous temporal description but cannot distinguish
different musical situations.


Example:

A bass player's timing during the theme and during a
solo accompaniment may follow different behaviours.


## Decision Rationale

Musical form is an independent analytical dimension.

Therefore:

Temporal Structure:

Audio

    ↓

Metric Reconstruction

    ↓

Bars

    ↓

Beats


Formal Structure:

Composition

    ↓

Musical Sections

    ↓

Bar ranges


The two dimensions intersect at the AnalyticalBar level.


## Relationship

Structure:


AnalyticalScore

        |

        +── MusicalSection

        |

        +── AnalyticalBar

                |

                +── AnalyticalBeat

                        |

                        +── AnalyticalCell


## Definition

A MusicalSection represents a named formal region
of a performance.

Examples:

- INTRO
- A
- B
- C
- BRIDGE
- HEAD
- SOLO SAX
- SOLO PIANO
- SOLO DOUBLE BASS
- OUTRO


## Scope

Included:

- section name
- start bar
- end bar
- association with analytical bars


Excluded:

- automatic form recognition
- harmonic analysis
- melody transcription


## Implementation Strategy

Initial version:

Manual or externally provided section annotations.


Future versions may support:

- structural change detection
- texture analysis
- instrument activity analysis
- automatic form inference


## AD-015 Traceability

INPUT:

Musical form annotation


OUTPUT:

MusicalSection


RESPONSIBLE TRANSFORMATION:

Musical Section Mapping Layer


TRACEABILITY:

MusicalSection

        ↓

AnalyticalBar

        ↓

AnalyticalBeat

        ↓

AnalyticalCell


## Status

Architectural foundation for future form-aware
groove analysis.
