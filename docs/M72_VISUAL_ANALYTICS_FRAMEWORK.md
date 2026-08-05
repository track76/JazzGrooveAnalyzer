# M72 — Visual Analytics Framework

## Status

LOCKED

---

# Purpose

The Visual Analytics Layer of the Jazz Groove Analyzer is not intended to
produce generic statistical charts.

Its purpose is to provide musicologists and musicians with a visual
representation of the metric behaviour of a jazz ensemble while preserving
the musical context of the performance.

The visualization is conceived as an analytical musical score.

---

# Architectural Principle

The musical context always has priority over numerical representation.

Every visualization shall preserve:

- musical form;
- metric structure;
- instrumentation;
- temporal evolution;
- significant metric phenomena.

Pure statistical information is secondary.

---

# Musicological Reading Principle

The visualization must be readable by a musicologist exactly as an
orchestral score is read.

The representation replaces traditional musical notation with the
representation of metric behaviour.

The graphical language shall therefore remain consistent with the reading
habits of trained musicians.

---

# Permanent Structure

Every analytical score SHALL contain the following elements.

## 1. Recording Information

Always visible.

- Title
- Artist
- Ensemble
- Duration
- Time Signature
- Average BPM

---

## 2. Musical Form

Always visible.

Examples:

- Cold Intro
- Intro
- A1
- A2
- B
- A3
- Solo Trumpet
- Solo Piano
- Trading
- Head Out
- Ending

The musical form is the highest-level temporal reference.

---

## 3. Metric Grid

Always visible.

For every measure the visualization shall show:

- measure number;
- time signature;
- beat subdivision;
- internal beat reference;
- local BPM whenever available.

Measures are represented with stronger vertical separators.

Internal beats are represented with thinner vertical separators.

The metric grid represents the reconstructed internal metric reference.

---

## 4. Instrument Lanes

The left side of the score contains one horizontal lane for every instrument.

Example:

Trumpet

Piano

Bass

Drums

Future versions may distinguish individual drum components:

- Ride
- Hi-Hat
- Snare
- Bass Drum

---

## 5. Metric Behaviour

Metric events are represented on the reconstructed beat grid.

Normal behaviour shall be visually unobtrusive.

Only significant deviations should immediately attract the observer's
attention.

---

# Graphical Hierarchy

## Measure separators

Strong visual weight.

## Beat separators

Thin visual weight.

Clearly visible but visually unobtrusive.

## Normal events

Small filled dots.

The eye should naturally ignore stable behaviour.

## Significant events

Slightly larger and visually emphasized.

The emphasis shall derive primarily from shape and line weight rather than
from colour.

---

# Offset Annotation

Every represented event may contain its metric offset expressed in
milliseconds.

Example:

+8 ms

-5 ms

Normal values should remain visually discreet.

Significant values may use heavier typography.

---

# Colour Policy

The analytical score shall initially be developed in monochrome.

Colour is considered optional.

If colour becomes necessary it should support interpretation rather than
replace graphical hierarchy.

Blue may be preferred over red in order to avoid the visual semantics of
error correction.

---

# Visual Economy Principle

The analytical score shall use the minimum graphical complexity necessary
to communicate metric behaviour.

Stable regions should not generate unnecessary visual noise.

The observer's attention must naturally focus on musical events rather than
on graphical decoration.

---

# Incremental Validation Rule

Every new graphical element follows the same workflow.

Implementation

↓

Observation on real recordings

↓

Musicological evaluation

↓

Confirmation, modification or removal

No visualization element becomes permanent before being validated on
real musical material.

---

# Long-Term Vision

The M72 framework is the foundation of the future Analytical Score of the
Jazz Groove Analyzer.

Future milestones may introduce additional visual layers including:

- metric trajectories;
- groove envelopes;
- interaction graphs;
- leadership transitions;
- ensemble synchronization indicators.

These additions shall never compromise the readability of the analytical
score defined in this document.

---

# Metric Reference Alignment Principle

## Status

**LOCKED**

---

## Beat Position Representation

The Analytical Score represents metric time as a sequence of discrete reference points.

A beat is not represented as a temporal interval between two lines.

A beat is represented by the exact position of the reconstructed internal metric reference.

Therefore:

- the vertical line represents the beat position;
- the beat number is aligned with that vertical line;
- the internal BPM value is aligned with that same vertical line;
- all Metric Events are measured relative to this reference.

Example:

        1          2          3          4
      124.4      125.1      123.8      124.7

        |          |          |          |

        |     ●    |          |          |
             -8 ms

The space between two beat reference lines represents the temporal distance between consecutive metric references.

It does not represent the beat location.


---

# Visual Layout Reference v1

## Status

**LOCKED**

---

## Analytical Score Rendering Model

The Analytical Score visualization follows a metric reference based layout.

The renderer does not represent continuous elapsed time.

It represents discrete reconstructed metric reference points.

---

## Layout Rules

The visualization follows these rules:

- Measure numbers are aligned with the beginning of the measure boundary.
- Beat numbers are aligned with their vertical metric reference line.
- Internal BPM values are aligned with the same beat reference position.
- Measure boundaries are represented by stronger vertical lines.
- Internal beats are represented by lighter reference lines.
- Instrument lanes are horizontal and aligned with Metric Events.
- Metric Events are positioned according to their temporal deviation from the metric reference.

---

## Rendering Separation Principle

The visualization layer must not contain musical interpretation logic.

The responsibility separation is:


---

# Visual Layout Reference v1

## Status

**LOCKED**

---

## Analytical Score Rendering Model

The Analytical Score visualization follows a metric reference based layout.

The renderer does not represent continuous elapsed time.

It represents discrete reconstructed metric reference points.

---

## Layout Rules

The visualization follows these rules:

- Measure numbers are aligned with the beginning of the measure boundary.
- Beat numbers are aligned with their vertical metric reference line.
- Internal BPM values are aligned with the same beat reference position.
- Measure boundaries are represented by stronger vertical lines.
- Internal beats are represented by lighter reference lines.
- Instrument lanes are horizontal and aligned with Metric Events.
- Metric Events are positioned according to their temporal deviation from the metric reference.

---

## Rendering Separation Principle

The visualization layer must not contain musical interpretation logic.

The responsibility separation is:

Domain Model

↓

Analytical Score

↓

Visualization Renderer

↓

Graphic Output

The renderer receives already interpreted analytical entities and only translates them into visual representation.

---

## Visual Validation Reference

Current validated visual prototype:

- four beats per measure;
- beat reference aligned to vertical positions;
- internal BPM shown for every beat;
- instrument lanes aligned horizontally;
- significant metric deviations highlighted.


---

# Absolute Time Display Principle

## Status

**LOCKED**

---

## Measure Absolute Time Representation

The Analytical Score displays absolute musical time at measure level.

Absolute time belongs to the measure boundary, not to the individual beat.

The displayed format is:

M:SS

Milliseconds are not displayed in the main analytical score.

---

## Visual Position

The absolute time label is positioned below the measure boundary line.

The measure number remains above the measure boundary.

Example:

        1              2              3              4

     124.4          125.1          124.8          125.0

        |              |              |              |

0:00   |              |              |              |

---

## Information Hierarchy

The Analytical Score separates three different concepts:

Measure number:
musical structural position.

Absolute time:
position inside the recording timeline.

Beat and internal BPM:
local reconstructed metric behaviour.

---

## Domain Model Extension

Measure:

- measure_number
- start_time_seconds
- start_time_display (M:SS)

MetricReferencePoint:

- measure_number
- beat_number
- internal_bpm
- metric_position

Absolute time is a property of the measure boundary and not of the individual beat.


---

# Temporal Reference Layer Principle

## Status

**LOCKED**

---

## Temporal Information Separation

The Analytical Score separates musical structure, metric reference and absolute time.

Three independent layers are represented:

### Measure Layer

Represents musical form boundaries.

Contains:

- measure number
- measure starting absolute time

Visual position:

- measure number above the measure boundary;
- measure time aligned below the measure boundary.

Example:


---

# Temporal Reference Layer Principle

## Status

**LOCKED**

---

## Temporal Information Separation

The Analytical Score separates musical structure, metric reference and absolute time.

Three independent layers are represented.

---

## Measure Layer

Represents musical form boundaries.

Contains:

- measure number
- measure starting absolute time

Visual position:

- measure number above the measure boundary;
- measure time aligned below the measure boundary.

Example:

        1

        |

       0:00

---

## Metric Layer

Represents reconstructed internal pulse.

Contains:

- beat number
- internal BPM
- metric reference position

The measure boundary is not considered a beat.

Example:

|      |      |      |      |

       1      2      3      4

    124.4  125.1  124.8  125.0

The number of metric references depends on the reconstructed metric pulse structure.

Examples:

4/4:
- 4 metric pulses

3/4:
- 3 metric pulses

5/4:
- 5 metric pulses

Compound meters must be represented according to the reconstructed pulse structure and not only by the written time signature.

---

## Event Layer

Represents observed musical events.

Contains:

- instrument/source
- absolute position
- deviation from metric reference

Example:

Bass

        ●
       -8 ms

---

## Absolute Beat Time

Each metric reference point can contain its absolute position in the recording.

Display format:

M:SS.mmm

Milliseconds are used because microtiming analysis requires sub-second precision.

Example:

Beat:

1          2          3          4

BPM:

124.4      125.1      124.8      125.0

Time:

0:00.000  0:00.482  0:00.963  0:01.445

---

## Rendering Principle

The renderer must not infer temporal position from visual spacing.

All positions must originate from analytical data:

- Measure boundary
- Metric reference point
- Event timestamp

The visualization is a representation of the reconstructed musical structure.

