# Instrument Classification Rules

## Goal

Transform measurable audio features into deterministic classification rules.

No empirical threshold is introduced until experimentally validated.

---

# Rule Structure

Each rule has:

- identifier
- rationale
- input features
- expected behaviour
- validation status

---

## Rule R1

Name:
Low Spectral Centroid

Rationale:
Low-frequency instruments tend to concentrate spectral energy at lower frequencies.

Feature:
Spectral Centroid

Validation:
Pending

---

## Rule R2

Name:
Low Spectral Rolloff

Rationale:
Low-frequency instruments exhibit lower spectral rolloff.

Feature:
Spectral Rolloff

Validation:
Pending

---

## Rule R3

Name:
Low Zero Crossing Rate

Rationale:
Periodic low-frequency waveforms usually generate fewer zero crossings.

Feature:
Zero Crossing Rate

Validation:
Pending

---

## Rule R4

Name:
High Spectral Bandwidth

Rationale:
Percussive sounds generally occupy a wider frequency range.

Feature:
Spectral Bandwidth

Validation:
Pending

---

## Rule R5

Name:
Short Duration

Rationale:
Percussive events are typically shorter than sustained sources.

Feature:
Duration

Validation:
Pending

---

# Validation

All thresholds will be derived from real audio measurements.

No threshold shall be hard-coded before experimental validation.
