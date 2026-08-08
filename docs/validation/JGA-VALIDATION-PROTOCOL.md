# JGA Validation Protocol

Copyright © 2026 Angelo Tracanna

---

## Terminology Boundary

The immutable scientific Validation Catalog and its Validation Items are defined
by `docs/architecture/AD-029_M84_VALIDATION_CATALOG.md`.

References below to experiment datasets describe historical validation
experiment material, not the M84 catalogue model.

---

## Purpose

This document defines the scientific validation methodology
for Jazz Groove Analyzer (JGA).

The objective is to evaluate the capability of JGA to reconstruct
musical structure and rhythmic behaviour from audio observation.

---

## Validation Principle

Validation is performed using controlled audio datasets.

The software receives only the audio signal.

Musical metadata used for comparison is kept separate
and is never provided as input during blind analysis.

---

## Validation Workflow

Each validation experiment contains:

1. Blind Analysis

Input:
- audio file only

Produced by JGA:
- detected sources
- ensemble profile
- metric reconstruction
- beat references
- measures
- analytical representation

---

2. Ground Truth Comparison

After analysis, results are compared with an independent reference.

Reference information may include:

- tempo
- meter
- musical sections
- instrument inventory
- expected structure

---

## Validation Dataset Structure

Each dataset contains:

- input audio
- blind analysis result
- ground truth reference
- scientific report

---

## Result Classification

Each observation is classified as:

PASS
- expected behaviour achieved

PARTIAL
- behaviour partially reconstructed

FAIL
- result differs from expected behaviour

NOT VALIDATED
- component not yet available or tested

---

## Experimental Record

Every validation run must record:

- software version
- input file
- date
- configuration
- observed output
- deviations
- conclusions

---
