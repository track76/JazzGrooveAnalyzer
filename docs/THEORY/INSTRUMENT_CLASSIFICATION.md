# Instrument Classification

## Purpose

The Instrument Classification module assigns each observed source to an instrument family using only measurable audio features.

The classification is deterministic, interpretable and independent from machine learning.

---

# Input

The classifier receives a FeatureSet.

The classifier never accesses AudioStem.

---

# Output

The classifier produces an InstrumentClassification.

---

# Instrument Families

- Bass
- Chordal
- Percussion
- Wind
- Voice
- Unknown

---

# Available Features

- Duration
- RMS
- Zero Crossing Rate
- Spectral Centroid
- Spectral Bandwidth
- Spectral Rolloff

Only these observable features may be used.

---

# Scientific Principles

- observable signal only
- deterministic rules
- interpretable decisions
- no hidden state
- no machine learning
- architecture independent from DSP

---

# Decision Strategy

Classification is rule-based.

Each rule is justified by measurable acoustic properties.

Confidence is derived from rule consistency.

---

# Extensibility

New features may be added without modifying the classifier interface.

New instrument families may be introduced without changing the FeatureSet contract.
