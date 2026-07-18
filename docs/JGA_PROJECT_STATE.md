# Jazz Groove Analyzer (JGA)

# Project State

---

## General Information

**Project Name**

Jazz Groove Analyzer (JGA)

**Version**

v0.2.0-alpha

**Current Milestone**

M4 — Metric Reconstruction

**Status**

Active Development

**Last Update**

July 2026

**Main Branch**

main

**Programming Language**

Python 3.13

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

✓ Infrastructure Stabilization

✓ Core Architecture

✓ Observation Layer

✓ DSP Layer

✓ Domain Layer

✓ Runtime Infrastructure

✓ Analysis Pipeline

✓ Documentation Governance

The project completed the first phase of Core integration.

Completed

✓ AudioStemCollection introduced

✓ AudioStemCollection integrated into AnalysisContext

✓ NullSeparator updated

✓ 105 / 105 tests passing

Current objective:

Complete the scientific alignment review between TAC, PulseCandidate
classification and the Domain Model before any Domain evolution.

Current focus:

✓ RFC-001 Observation Model Review incorporated

✓ TAC Observation Model v0.2 introduced

✓ RFC-002 PulseCandidate scientific classification revised (v0.4)

✓ Core and Domain PulseCandidate distinction identified

✓ TAC Domain Mapping specification introduced

✓ RFC-003 Domain Model alignment review documented

✓ Domain Model compatibility with TAC confirmed

✓ BeatReference emergence path confirmed through InternalMetricTimeline

Open issue:

Future PulseCandidate naming refinement and Domain Map evolution
remain under consideration.

No Domain Model modification introduced at this stage.

---

# Repository Structure

```

JazzGrooveAnalyzer/

docs/

src/

tests/

recordings/

experiments/

math/

output/

README.md

pyproject.toml

requirements.txt

```

---

# Current Software Architecture

Current packages

```

jga.audio

jga.core

jga.domain

jga.dsp

jga.engines

jga.interfaces

jga.io

jga.math

jga.observation

jga.pipeline

jga.runtime

jga.separation

jga.utils

jga.visualization

```

Current layered architecture

```

Acquisition Layer

↓

AudioStemCollection

↓

Observation

↓

DSP

↓

Domain

↓

Analysis

```

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

105 / 105 tests passing

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

CHANGELOG.md

CONTRIBUTING.md

MASTER_CONVERSATIONS.md

JGA_RESEARCH_JOURNAL.md

JGA_PROJECT_STATE.md

Future documentation

JGA_DEVELOPMENT_RULES.md

JGA_VALIDATION_PROTOCOL.md

JGA_DECISIONS.md

JGA_SESSION_CONTEXT.md

JGA_ROADMAP.md

docs/core/AUDIO_STEM_COLLECTION.md

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

M4

Metric Reconstruction

Status

In Progress

---

# Immediate Objectives

1.

Design AudioStemCollection

2.

Implement AudioStemCollection

3.

Integrate Acquisition Layer with Core

4.

Preserve Core independence

5.

Update Analysis Pipeline

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

Repository synchronized.

Working tree clean.

105 / 105 tests passing.

Observation Layer completed.

DSP Layer completed.

Current development focuses on Core Integration (M3.1).

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

