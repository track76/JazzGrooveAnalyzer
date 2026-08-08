# VAL-001 Reference Validation Item

Status: LOCKED

---

# Purpose

VAL-001 is the canonical scientific validation item of Jazz Groove Analyzer.

It belongs to `JGA-VALIDATION-CATALOG-v1`, defined by:

- `docs/architecture/AD-029_M84_VALIDATION_CATALOG.md`

Its purpose is exclusively the experimental validation of the JGA pipeline.

It is **NOT** used by JGA during analysis.

---

# Blind Analysis Principle

JGA receives only the audio signal.

The software has no access to:

- score
- tempo
- time signature
- measure count
- musical form
- instrumentation
- ground truth

These data are reserved exclusively for post-analysis scientific validation.

Providing any of this information to the analysis pipeline would invalidate the experiment.

---

# Ground Truth (Validation Only)

Canonical Ground Truth

GT-VAL-001-v1

The Ground Truth identity, approved MusicXML source and
normalization rules are defined by:

- `docs/architecture/AD-028_M83_GROUND_TRUTH_REFERENCE.md`

Time Signature

4/4

Tempo

78 BPM

Structure

- Intro: 4 measures
- Section A: 8 measures

Instrumentation

- Voice
- Saxophone
- Piano
- Double Bass
- Drum Set

Origin

- Score written in Sibelius
- Digital rendering
- Reference dataset

---

# Scientific Objective

The objective is to verify how accurately JGA reconstructs the musical behaviour from the audio signal alone.

The comparison with the ground truth is performed only after the execution has completed.

---

# Validation Outputs

Typical outputs include:

- observed sources
- pulse candidates
- source pulse sequences
- metric context
- ensemble metric events
- beat references
- behaviour profile
- scientific report

These outputs are compared with the reference ground truth to evaluate the scientific correctness of the reconstruction.
