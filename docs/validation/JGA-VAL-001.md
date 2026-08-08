# JGA-VAL-001

Copyright © 2026 Angelo Tracanna

---

## Dataset

File:

03 THE COST OF LIVING versione intro + 8 bar.mp3

Location:

recordings/validation/

---

## Experimental Setup

Analysis mode:

BLIND

The software receives only the audio file.

Configuration:

- Separator:
  DummyMultiStemSeparator

- Instrument classifier:
  DummyInstrumentClassifier 0.1.0

---

## Observed Results

### Audio Acquisition

Status:

PASS

Observed:

- duration: 42.24 seconds
- sample rate: 44100 Hz
- channels: 2

---

### Source Understanding

Status:

NOT VALIDATED

Reason:

Current experiment uses DummyInstrumentClassifier.

Observed:

- 7 observed stems
- classification confidence: 0.0

---

### Metric Reconstruction

Status:

BASELINE

Observed:

- Beat References: 42
- Metric Clusters: 42
- Reconstructed Measures: 2

---

## Scientific Notes

This experiment represents the first blind baseline.

No musical metadata has been provided to the software.

The observed output is stored as a reference point
for future experiments.

---

