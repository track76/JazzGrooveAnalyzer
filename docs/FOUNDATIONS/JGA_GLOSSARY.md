# JGA Glossary

Version: 1.0

Author and Creator:
Angelo Tracanna

Copyright © 2026 Angelo Tracanna.
All rights reserved.

---

# Introduction

This glossary defines the official terminology adopted by the Jazz Groove Analyzer (JGA).

Each concept is defined exactly once and shall be used consistently throughout the entire project.

The definitions contained in this document constitute the authoritative reference for every theoretical, mathematical, algorithmic, and software component of the JGA.

---

# Audio Signal

## Definition

The continuous physical manifestation of the acoustic energy generated during a musical performance.

## Domain

Observation

## Role

Serves as the primary source of information for the entire Jazz Groove Analyzer.

## Relationships

Produces Transients.

## Introduced In

Foundations of JGA – Chapter 5

---

# Transient

## Definition

A rapid local variation of the acoustic signal associated with an abrupt change in its physical properties.

## Domain

Observation

## Role

Represents the earliest observable acoustic variation.

## Relationships

Derived from the Audio Signal.

May contribute to the identification of an Onset.

## Introduced In

Foundations of JGA – Chapter 6

---

# Onset

## Definition

The perceptual beginning of a musical sound or acoustic event.

## Domain

Observation

## Role

Represents the earliest perceptually meaningful temporal reference associated with a sound.

## Relationships

May originate from one or more Transients.

May generate one or more PulseCandidates.

## Introduced In

Foundations of JGA – Chapter 7

---

# PulseCandidate

## Definition

An observed temporal event that may contribute to the temporal organization of a musical performance.

## Domain

Observation

## Role

Represents the highest level of temporal observation before the representation domain begins.

## Relationships

Derived from one or more Onsets.

May generate an Elementary Metric Event.

## Introduced In

Foundations of JGA – Chapter 8

---

# Elementary Metric Event (EME)

## Definition

The formal metric representation of a PulseCandidate interpreted within the temporal model of the Jazz Groove Analyzer.

## Domain

Representation

## Role

Represents the elementary building block of the temporal model.

## Relationships

Originates from a PulseCandidate.

Forms Metric Clusters.

## Introduced In

Foundations of JGA – Chapter 9

---

# Metric Cluster (MC)

## Definition

An organized set of Elementary Metric Events that collectively describe a common temporal reference within a musical performance.

## Domain

Representation

## Role

Represents the first collective organization of metric events.

## Relationships

Composed of Elementary Metric Events.

Contributes to the reconstruction of one or more Pulses.

## Introduced In

Foundations of JGA – Chapter 10

---

# Pulse

## Definition

A coherent temporal reference reconstructed from one or more Metric Clusters.

## Domain

Representation

## Role

Represents the fundamental temporal reference used to model musical time.

## Relationships

Emerges from Metric Clusters.

Contributes to the reconstruction of the Internal Metric Timeline.

## Introduced In

Foundations of JGA – Chapter 11

---

# Internal Metric Timeline (IMT)

## Definition

The continuous temporal model reconstructed from the sequence of Pulses throughout a musical performance.

## Domain

Representation

## Role

Represents the complete temporal organization of the ensemble.

## Relationships

Constructed from Pulses.

Provides the temporal reference for all subsequent analyses.

## Introduced In

Foundations of JGA – Chapter 12

---

# Observation Domain

## Definition

The conceptual domain containing entities directly derived from the acoustic signal without assigning musical meaning.

## Includes

- Audio Signal
- Transient
- Onset
- PulseCandidate

## Introduced In

Foundations of JGA – Chapter 4

---

# Representation Domain

## Definition

The conceptual domain containing the theoretical entities used to reconstruct musical time.

## Includes

- Elementary Metric Event (EME)
- Metric Cluster (MC)
- Pulse
- Internal Metric Timeline (IMT)

## Introduced In

Foundations of JGA – Chapter 4

---

# Official Abbreviations

The following abbreviations constitute the official terminology adopted throughout the Jazz Groove Analyzer.

These abbreviations shall be used consistently in all theoretical documents, mathematical formulations, software architecture, source code, and scientific publications.

| Abbreviation | Term |
|--------------|------|
| AS | Audio Signal |
| TR | Transient |
| ON | Onset |
| PC | PulseCandidate |
| EME | Elementary Metric Event |
| MC | Metric Cluster |
| P | Pulse |
| IMT | Internal Metric Timeline |

---

# Terminology Policy

The terminology defined in this glossary is normative.

Every theoretical document, mathematical formulation, software component, source code module, and scientific publication belonging to the Jazz Groove Analyzer shall adopt these definitions consistently.

Any modification to this glossary shall require a corresponding revision of the theoretical framework.