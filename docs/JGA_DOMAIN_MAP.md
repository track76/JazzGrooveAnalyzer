# =========================================================
# Jazz Groove Analyzer (JGA)
#
# File:
#     JGA_DOMAIN_MAP.md
#
# Description:
#     Canonical map of the JGA Domain Model.
#
# Author:
#     Angelo Tracanna
#
# Copyright © 2026 Angelo Tracanna
# All Rights Reserved.
# =========================================================

# JGA Domain Map

## Purpose

This document is the canonical map of the Jazz Groove Analyzer Domain Model.

Its purpose is to preserve architectural consistency during the evolution
of the project.

Before introducing any new Domain entity, service or relationship,
this document must be consulted and, if necessary, updated.

The Domain Map represents the conceptual organization of the JGA.
It is **not** the execution pipeline.

---

# Domain Principles

The Domain Model is independent from:

- DSP implementations
- Machine Learning
- Audio acquisition
- External libraries

The Domain describes only musical concepts and observable rhythmic behaviour.

---

# Domain Graph

AudioRecording
    │
    ▼
AudioStem
    │
    ▼
SoundSource
    │
    ▼
PulseCandidate
    │
    ▼
Pulse
    │
    ▼
ElementaryMetricEvent (EME)
    │
    ├────────► MetricCluster
    │                 │
    │                 ▼
    │       InternalMetricTimeline
    │                 │
    │                 ▼
    │          BeatReference
    │
    └────────► EnsembleProfile

---

# Core Rule

ElementaryMetricEvent (EME) is the first musical entity generated from observable events.

Every higher-level rhythmic representation originates from EME.

---

# Architectural Rules

1. Domain entities never depend on DSP.

2. Domain entities never depend on Audio acquisition.

3. MetricCluster is built from ElementaryMetricEvents.

4. BeatReference emerges from the InternalMetricTimeline.

5. Every new Domain entity must appear in this document before implementation.

6. New relationships must preserve the consistency of this map.

---

# Evolution Policy

When introducing a new concept:

1. Verify whether it already exists in the Domain.
2. Verify whether an existing entity already models it.
3. Place the concept inside this map.
4. Only then update the Domain Model.
5. Only then implement the code.

No implementation should precede the Domain Map.
