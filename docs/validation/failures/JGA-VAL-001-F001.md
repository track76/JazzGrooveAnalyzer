# JGA-VAL-001-F001

Copyright © 2026 Angelo Tracanna

---

## Title

Beat period estimation failure caused by simultaneous metric events.

---

## Experiment

JGA-VAL-001

Blind validation.

---

## Observation

The validation pipeline produced:

Estimated period:

0.06300294861972092 seconds

Estimated BPM:

952.3363797169812

---

## Analysis

Pulse candidates preserve a plausible temporal distribution.

ElementaryMetricEvents preserve source timestamps.

The error appears during beat period estimation.

---

## Root Cause

BeatPeriodEstimator computes the average distance between consecutive ElementaryMetricEvents.

Multiple contributors producing events at the same musical instant generate zero-distance intervals.

These intervals incorrectly reduce the estimated period.

---

## Affected Component

src/jga/domain/services/beat_period_estimator.py

---

## Status

CONFIRMED

---

