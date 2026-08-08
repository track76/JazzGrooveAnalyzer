# JGA Validation Dataset

## Terminology Boundary

This document describes the existing analysis-produced observational
`ValidationDataset` artifact.

It is not the immutable scientific validation catalogue introduced by M84. The
scientific catalogue and its Validation Items are defined by:

- `docs/architecture/AD-029_M84_VALIDATION_CATALOG.md`

## Purpose

The Validation Dataset is the scientific observational artifact produced by JGA for experimental validation.

## Pipeline

Audio
    ↓
Metric Reconstruction
    ↓
Behaviour Analytics
    ↓
Semantic Observation
    ↓
Validation Dataset
    ↓
Scientific Export

## Inputs

- MetricEventObservation
- TimingBehaviour
- BehaviourObservation
- BehaviourProfile
- RepresentationResult

## Outputs

A neutral observational dataset.

Supported export formats:

- CSV
- JSON
- TXT
- PNG

## Scientific Principles

- Observation precedes interpretation.
- No semantic inference.
- Full traceability.
- Reproducible scientific validation.

## Architecture Contract

Observed Data
        ↓
ValidationDatasetBuilder
        ↓
ValidationDataset
        ↓
Scientific Exporters
