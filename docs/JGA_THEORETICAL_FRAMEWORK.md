# JGA Theoretical Framework

**Version:** 3.0

**Status:** Active

**Project:** Jazz Groove Analyzer (JGA)

**Author:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna**

---

# 1. Introduction

The Jazz Groove Analyzer (JGA) is a scientific framework for the mathematical
representation of collective metric behaviour in musical ensembles.

Unlike conventional beat tracking systems, the JGA does not aim to estimate
tempo or identify beats directly from audio.

Its primary objective is to construct an interpretable mathematical model
capable of describing the observable rhythmic behaviour of an ensemble
through a hierarchy of progressively higher-level Domain representations.

The software is therefore the implementation of a scientific theory rather
than the theory itself.

---

# 2. Scientific Problem

The central scientific problem addressed by the JGA is not beat detection,
tempo estimation or onset localisation.

Instead, the project investigates how a collective metric reference emerges
from the interaction of multiple rhythmic sources.

The object of study is therefore the observable metric behaviour of an
ensemble.

---

# 3. Observed Phenomenon

The phenomenon investigated by the JGA is defined as:

> Collective Metric Behaviour

Collective metric behaviour is the observable temporal organisation generated
by the interaction among the rhythmic contributors of a musical ensemble.

The JGA does not attempt to infer performer intentions, expressive meaning,
or aesthetic qualities.

Only observable properties extracted from the audio signal belong to the
scientific domain of the framework.

---

# 4. Fundamental Principles

The following principles are considered invariant.

1. Theory always precedes implementation.

2. Every mathematical object corresponds to a Domain object.

3. Every Domain object must have an explicit mathematical definition.

4. Every algorithm must remain interpretable.

5. Only observable properties belong to the scientific model.

6. Behaviour is represented rather than inferred.

7. The framework must remain independent of the specific source-separation
technology.

8. Local analysis precedes global reconstruction.

9. Higher abstraction levels may only depend on the immediately preceding
representation.

10. Scientific reproducibility has priority over implementation convenience.

11. Domain invariants must always preserve scientific consistency.

---

# 5. Hierarchy of Musical Representation

The JGA represents rhythmic behaviour through a hierarchy of Domain objects.

Before Domain representation, the Observation Layer provides the physical
observations extracted from the audio signal.

The Observation Layer does not introduce musical interpretation.
It preserves observable temporal information that becomes the foundation
for subsequent Domain representations.


Audio Recording

↓

Audio Stem

↓

Elementary Metric Event

↓

Beat Reference

↓

Metric Cluster

↓

Pulse

↓

Internal Metric Timeline

↓

Musical Analysis

Each representation is constructed exclusively from the immediately
preceding level.

No Domain object may bypass the hierarchy.

This hierarchy defines the current theoretical representation adopted
by the JGA.

---

# 6. Elementary Metric Event

The Elementary Metric Event (EME) is the smallest temporal
entity represented within the JGA Domain Model.

Each EME corresponds to one temporal event derived from the observation
process and represents a domain-level representation rather than a musical
interpretation.

---

# 7. Beat Reference

A Beat Reference represents the theoretical metric reference inferred
from the collective rhythmic behaviour of the ensemble.

It is not detected directly from the audio signal but is constructed
from observable rhythmic evidence.

---

# 8. Metric Cluster

A Metric Cluster groups the Elementary Metric Events that belong to the
same Beat Reference.

It represents the collective rhythmic evidence supporting one theoretical
beat.

---

# 9. Pulse

A Pulse represents one theoretical pulsation of the ensemble.

Each Pulse is derived from exactly one Metric Cluster and preserves the
temporal position established by the corresponding Beat Reference.

---

# 10. Internal Metric Timeline

The Internal Metric Timeline represents the ordered sequence of Pulses
describing the theoretical metric evolution of the ensemble.

It constitutes the highest-level Domain object currently implemented in
the JGA.

---

# 11. Domain Representation

The current Domain Layer implements the complete theoretical chain:

Audio Recording

↓

Audio Stem

↓

Elementary Metric Event

↓

Beat Reference

↓

Metric Cluster

↓

Pulse

↓

Internal Metric Timeline

This hierarchy constitutes the current scientific representation adopted
by the JGA.

---

# 12. Scientific Consequences

The proposed framework implies that:

• Beat References emerge from collective rhythmic behaviour.

• Metric Clusters represent observable rhythmic evidence.

• Pulses are theoretical objects rather than detected events.

• Internal Metric Timelines provide the basis for higher-level musical
analysis.

• The scientific model remains independent of DSP implementation details.

---

# 13. Future Developments

The next stage of the theoretical framework will focus on the analysis
of the Internal Metric Timeline.

Planned developments include:

• Metric Stability

• Pulse Interval Analysis

• Tempo Estimation

• Groove Metrics

• Collective Metric Behaviour

# 14. Canonical Project Documentation

The Jazz Groove Analyzer is supported by a set of canonical documents that
must evolve together with the source code.

These documents constitute the architectural and scientific memory of the
project.

- JGA_THEORETICAL_FRAMEWORK.md
- JGA_DOMAIN_MAP.md
- JGA_DECISIONS.md
- JGA_PROJECT_STATE.md

Every modification affecting the scientific model, the Domain Model or the
project architecture must preserve the consistency of these documents.