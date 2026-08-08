# M33 — Persistent Stable Region Model

Status

PROPOSED

---

## Objective

Replace the current point-based intro detection with a region-based model.

The beginning of the musical analysis shall correspond to the first persistent
stable region rather than to the first stable observation.

---

## Current Model

Stability Curve

↓

First Stability Point above threshold

↓

Analysis Start

This model assumes that a single stable observation is sufficient.

Experimental validation (VAL-001) has shown that this assumption is not always
valid.

---

## New Model

Stability Curve

↓

Persistent Stable Region Detection

↓

Analysis Start

The beginning of the analysis corresponds to the first Stable Region.

---

## Stable Region

A Stable Region is a contiguous sequence of Stability Points satisfying
persistence constraints.

The exact persistence parameters are implementation details and shall remain
configurable.

Examples include:

- minimum number of consecutive Stability Points;
- minimum temporal duration;
- maximum interruption tolerance.

---

## Scientific Motivation

Musical stability is not an instantaneous phenomenon.

It emerges over time through the persistence of rhythmic organization.

Therefore the detector shall identify stable regions rather than isolated
stable observations.

---

## Validation

Validation shall be performed using VAL-001.

The detector shall identify the beginning of the metrically stable musical
section.

No information contained in the ground truth shall be used during analysis.

