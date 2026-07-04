# Jazz Groove Analyzer (JGA)
# Project State

---

## Project Information

**Project Name**

Jazz Groove Analyzer (JGA)

**Version**

0.1.0-alpha

**Current Milestone**

T4 — Musical Analysis Services

**Status**

Domain Layer Stable

**Last Update**

2 July 2026

**Main Branch**

main

**Programming Language**

Python 3.13.14

**Repository Layout**

src-layout

**Testing Framework**

pytest

---

# Project Vision

The Jazz Groove Analyzer (JGA) is a scientific software framework for
the analysis of rhythmic behaviour in jazz ensembles.

Unlike conventional beat tracking systems, the JGA does not attempt
to estimate tempo directly from onset sequences.

Instead, it reconstructs the underlying metric reference through the
collective rhythmic behaviour of all performers.

The primary objective of the project is not beat detection, but the
construction of an interpretable mathematical model capable of
describing rhythmic interaction inside an ensemble.

The software is therefore the implementation of a scientific theory,
not simply an audio analysis tool.

---

# Scientific Scope

The JGA studies rhythmic behaviour rather than isolated events.

Its purpose is to explain how metric stability emerges from the
interaction among multiple rhythmic sources.

The project focuses on:

• ensemble interaction

• metric behaviour

• rhythmic stability

• metric persistence

• temporal perception

• collective metric reconstruction

The project explicitly avoids treating expressive timing or intentional
subdivisions as timing errors.

---

# Scientific Principles

The following principles are considered invariant.

1.
JGA is NOT a beat detector.

2.
Metric reference emerges from collective rhythmic behaviour.

3.
Intentional rhythmic subdivisions
(triplets, quintuplets, septuplets, etc.)
are never considered timing errors.

4.
Every algorithm must be mathematically explainable.

5.
Theory always precedes implementation.

6.
Software implements the scientific model,
never the opposite.

7.
Every architectural decision must preserve
scientific interpretability.

---

# Current Development Phase

Completed

✓ Repository stabilized

✓ Domain Model completed

✓ Core Domain Services completed

✓ Builder chain completed

✓ Complete unit test suite

✓ Scientific architecture consolidated

The project has completed the construction of the Domain Layer.

The next development phase focuses on Musical Analysis Services.

---

# Repository Structure

```
JazzGrooveAnalyzer/

docs/
    Scientific documentation

src/
    JGA source code

tests/
    Automated tests

recordings/
    Audio recordings

experiments/
    Experimental scripts

output/
    Generated analysis

README.md

pyproject.toml
```

---

# Current Software Architecture

Current packages

```
jga.audio

jga.core

jga.engines

jga.math

jga.metric

jga.pipeline

jga.runtime

jga.separation

jga.visualization
```

The infrastructure is considered stable.

Future scientific modules will be introduced without redesigning the
existing architecture unless explicitly required.

---

# Current Domain Model

Implemented Domain Objects

✓ AudioRecording

✓ AudioStem

✓ SoundSource

✓ MusicalFunction

✓ MetricContributor

✓ ElementaryMetricEvent

✓ BeatReference

✓ MetricCluster

✓ Pulse

✓ InternalMetricTimeline

---

# Domain Services

Implemented

✓ ElementaryMetricEventBuilder

✓ MetricContributorResolver

✓ MetricClusterBuilder

✓ PulseBuilder

✓ InternalMetricTimelineBuilder

---

# Mathematical Model

Implemented

✓ Elementary Metric Event

✓ Beat Reference

✓ Metric Cluster

✓ Pulse

✓ Internal Metric Timeline

Under Development

• Metric Stability

• Pulse Interval Analysis

• Tempo Estimation

• Groove Metrics

---

# Test Status

Framework

pytest

Current Result

67 / 67 tests passing

Coverage

✓ Domain Entities

✓ Domain Services

✓ Smoke Tests

Status

Entire test suite passing.

---

# Documentation

Current documents

README.md

JGA_METHOD.md

JGA_GLOSSARY.md

JGA_ARCHITECTURE.md

JGA_THEORETICAL_FRAMEWORK.md

JGA_PRINCIPLES.md

DESIGN_DECISIONS.md

ROADMAP.md

CHANGELOG.md

CONTRIBUTING.md

MASTER_CONVERSATIONS.md

JGA_RESEARCH_JOURNAL.md

JGA_PROJECT_STATE.md

Future documentation

JGA_DOMAIN_MODEL.md

JGA_DEVELOPMENT_RULES.md

JGA_VALIDATION_PROTOCOL.md

---

# Development Workflow

Every new component follows exactly this workflow.

1.

Mathematical definition

↓

2.

Domain Model

↓

3.

Documentation

↓

4.

Unit Tests

↓

5.

Implementation

↓

6.

Scientific Validation

↓

7.

Commit

Implementation never precedes formal definition.

---

# Permanent Architectural Decisions

The following decisions are considered stable.

• Repository uses src-layout.

• Tests are outside the source package.

• Infrastructure is considered stable.

• Theory always precedes implementation.

• Every mathematical object corresponds to a Domain object.

• Every Domain object must have dedicated tests.

• Every algorithm must remain mathematically interpretable.

• Architectural redesigns require explicit justification.

---

# Current Milestone

T4

Musical Analysis Services

Status

Ready to start.

---

# Immediate Objectives

1.

Metric Stability Analyzer

2.

Pulse Interval Analysis

3.

Tempo Estimation

4.

Groove Metrics

5.

Scientific Validation

---

# Long-Term Roadmap

T4

Musical Analysis Services

T5

Groove Behaviour Analysis

T6

Scientific Validation

T7

Visualization Layer

T8

Research Publication

T9

Open-source Framework

---

# Long-Term Vision

The Jazz Groove Analyzer aims to become a scientific reference framework
for rhythmic behaviour analysis in jazz ensembles.

The project prioritizes scientific rigor, mathematical transparency,
software quality and reproducible research.

The software is intended to support future scientific publications,
validation studies and collaborative research.

---

# Repository Status

Current repository status

Stable

Domain Layer completed.

67 / 67 tests passing.

Ready for Musical Analysis Services.

---

# Conversation Bootstrap

When starting a new conversation:

1.
Read this document completely.

2.
Assume every architectural decision described here has already been approved.

3.
Do not redesign the infrastructure unless explicitly requested.

4.
Continue development from the current milestone.

5.
Preserve theoretical consistency.

6.
Clearly distinguish verified theory from working hypotheses.

7.
Treat the JGA as a scientific research project rather than a conventional software application.

8.
Always prioritize the mathematical model over implementation details.

9.
Maintain coherence with the existing Domain Model.

10.
Assume that this document represents the current official state of the project.

11.

Assume that the Domain Layer described in this document is complete and validated.

12.

Do not redesign the Domain Model or its architectural decisions unless explicitly requested.