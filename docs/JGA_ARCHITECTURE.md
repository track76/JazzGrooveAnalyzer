# Jazz Groove Analyzer (JGA)

# Software Architecture

Version 1.0 (Draft)

Author

Angelo Tracanna

---

# Purpose

This document describes the software architecture of the Jazz Groove Analyzer.

Unlike the Method Specification, this document focuses exclusively on the software structure, package organisation and data flow.

---

# High-Level Pipeline

Audio File

↓

Audio Loader

↓

Audio Normalization

↓

Source Separation

↓

AudioStem Generation

↓

Rhythmic Behaviour Analysis

↓

Behaviour Change Detection

↓

Behaviour Profile

↓

Metric Evidence Index

↓

Metric State Machine

↓

Ensemble Metric Event (EME)

↓

Metric Cluster

↓

Ensemble Metric Reference

↓

Groove Analysis

↓

Reporting

---

# Main Packages

src/jga/

analysis/

audio/

metric/

pipeline/

runtime/

separation/

tests/

utils/

---

# Core Data Objects

AudioStem

↓

RhythmicBehaviourSegment

↓

BehaviourProfile

↓

MetricEvidence

↓

MetricState

↓

EnsembleMetricEvent

↓

MetricCluster

↓

EnsembleMetricReference

---

# Design Philosophy

The JGA analyses musical behaviours rather than musical instruments.

Every analytical stage increases the semantic interpretation of the musical signal.

No stage directly estimates the beat.

The Ensemble Metric Reference is progressively reconstructed from the observed behaviours of the ensemble.

---

# Future Modules

Behaviour Change Detector

Metric State Machine

Groove Descriptor

Interaction Analyzer

Swing Analyzer

Expressive Timing Analyzer

Automatic Report Generator

---

# Core Execution Model

Audio Source
      │
      ▼
Acquisition
      │
      ▼
Observation
      │
      ▼
DSP
      │
      ▼
Core Representation
      │
      ▼
Representation Translation
      │
      ▼
Domain Services
      │
      ▼
Ensemble Analysis Result

## Architectural Principles

The Core is responsible for computational processing.

The Domain is responsible for musical interpretation.

The integration between the two shall occur through an explicit architectural boundary.
