# Jazz Groove Analyzer (JGA)

**A Scientific Framework for the Reconstruction and Quantification of Collective Metric Behaviour in Jazz Ensembles**

---

## Author

**Angelo Tracanna**

Copyright © 2026 Angelo Tracanna. All Rights Reserved.

---

## Overview

The Jazz Groove Analyzer (JGA) is an original scientific framework for the
analysis of collective metric behaviour in jazz ensembles.

Unlike conventional beat-tracking systems, JGA does not estimate beats or
tempo directly from audio. Instead, it reconstructs the ensemble metric
reference through a hierarchy of deterministic and scientifically traceable
representations.

The framework is theory-driven: scientific definitions always precede
software implementation.

---

## Scientific Principles

- Theory precedes implementation.
- Every transformation has explicit Input/Output contracts.
- No implicit transformations are allowed.
- The Core never assigns musical meaning.
- The Domain interprets only validated representations.
- Every software component is traceable to a scientific definition.

---

## Current Development Status

**Version**

v0.5.0-alpha

**Current Milestone**

M5 — Behaviour Quantification

**Completed Milestones**

- ✅ M1 — Scientific Foundations
- ✅ M2 — Domain Modelling
- ✅ M3 — Translation Layer
- ✅ M4 — Metric Reconstruction
- ✅ M5 Phase 1 — Behaviour Quantification Foundations

---

## Current Processing Pipeline

```text
Audio Recording
        ↓
Observation Layer
        ↓
Metric Context
        ↓
τ₈ Translation
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
Behaviour Observation
        ↓
Behaviour Profile
        ↓
Behaviour Quantification

E0F
```

## Canonical Rhythm Section Timing Report

The first normal-use scientific reporting workflow composes unchanged JGA
observations with AD-037 EME materialization, AD-038 neutral Drum-relative
geometry, and the AD-040 Rhythm Section Timing Profile. Analytical roles are
always supplied explicitly and bound to source checksums; instrument names do
not assign roles.

```bash
PYTHONPATH=src .venv/bin/python tools/run_rhythm_section_timing_report.py \
  --source "TEMPORAL_REFERENCE=Drums=/path/to/drums.wav" \
  --source "ACCOMPANIMENT=Double Bass=/path/to/bass.wav" \
  --expected-sha256 "Drums=<sha256>" \
  --expected-sha256 "Double Bass=<sha256>" \
  --execution-id <stable-execution-id> \
  --provenance-id <input-authority-id> \
  --role-authority-id <role-authority-id> \
  --role-authority-fingerprint <role-authority-fingerprint> \
  --calibration-applicability <APPLICABLE|NOT_APPLICABLE|UNESTABLISHED> \
  --calibration-authority-id <calibration-authority-id> \
  --calibration-authority-fingerprint <calibration-authority-fingerprint> \
  --jga-revision <git-commit> \
  --output rhythm-section-timing-report.json
```

The output schema is `JGA_RHYTHM_SECTION_TIMING_REPORT_V1`. JSON is serialized
with sorted keys, ASCII encoding, no NaN values, and compact separators. Its
scientific fingerprint is SHA-256 over the canonical scientific content before
the fingerprint field is added. Existing output files are not overwritten.

The report establishes only provenance-bound frame-resolved observations,
neutral temporal geometry, and an AD-040 profile. Its default correspondence
status is `GEOMETRIC_ONLY`; no calibration or timestamp correction is applied.
Calibration applicability is supplied through a separate provenance-bound
authority and is never inferred from the fixed `NOT_APPLIED` application and
`NONE` correction statuses.
It does not establish beat identity, musical correspondence, tempo, BPM,
meter, downbeat, swing, groove, rushing/dragging, intention, human microtiming,
physical-onset Ground Truth, or acquisition-clock synchrony.
