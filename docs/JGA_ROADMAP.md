# Jazz Groove Analyzer (JGA)

# Official Roadmap

## Current scientific priority — 2026-09-10 consolidated checkpoint

Canonical [checkpoint and workflow](scientific/JGA_TIMING_CHECKPOINT_20260910.md) and [prospective Hi-Hat 2&4 rule](scientific/JGA_HIHAT_2_4_TIMING_RULE_20260910.md).

**Real/full mix → approved source separation → relevant stem → instrument/event recognition → timing evidence → domain interpretation → internal BPM/behaviour.** Direct-full-mix recognition is an explicit control only. This applies to future Double-Bass full-mix analysis as well.

Where qualified: jazz Drums → Hi-Hat identity → recurrent/local timekeeping qualification → 2&4 reference → T_BEAT=T_HH/2 → internal BPM → freeze → later external comparison. Abstain when qualification is unavailable. Generic BeatReference remains fallback; Ride remains separate articulation/swing/microtiming evidence. Do not pool sources or quantize Bass events onto the reference.

CED-VAL-005 motivates the rule retrospectively; it does not prospectively validate it. Chet full-pipeline recognition yielded zero HH candidates, so the 2&4 mapping was not tested. Neither custom training nor a new model search follows automatically.

**Next minimal experiment, only after separate PI authorization:** Ray Brown Trio - Easy Does It.m4a through this full pipeline, with external/PI tempo hidden until internal result freeze. File availability is not execution authorization. No new experiment occurs in this consolidation.

Global Drum periodicity/recurrence and DEFERRED_PARALLEL null work remain preserved. Double-Bass capture/identity work remains independent and unexecuted. Historical milestones below do not override this current checkpoint.

---

## Vision

The Jazz Groove Analyzer (JGA) is developed as a scientific framework for reconstructing and analysing the internal temporal behaviour of jazz ensembles.

Each milestone extends the framework while preserving scientific interpretability, architectural consistency and reproducibility.

---

# Milestone M0

## Infrastructure Stabilization

**Status:** ✅ Completed

### Deliverables

- Repository initialization
- Python project structure
- Testing framework
- CI-ready repository
- Stable development workflow

---

# Milestone M1

## Core Architecture

**Status:** ✅ Completed

### Deliverables

- Core architecture
- Domain model
- Runtime infrastructure
- Pipeline abstraction
- Interfaces

---

# Milestone M2

## Observation Layer

**Status:** ✅ Completed

### Deliverables

- SignalRepresentation
- Transient
- Onset
- Feature extraction
- Observation infrastructure

---

# Milestone M3

## Core Integration

**Status:** ✅ Completed

### Goal

Integrate the Observation Layer into the Core architecture without breaking architectural independence.

### Current Sprint

M3.1 — AudioStemCollection

### Deliverables

- AudioStemCollection
- Core entry point redesign
- Acquisition/Core separation
- Pipeline integration

---

# Milestone M4

## Metric Reconstruction

**Status:** ✅ Completed

### Completed

- PulseCandidate generation pipeline foundation
- ElementaryMetricEvent construction
- MetricCluster reconstruction foundation
- Beat Reference emergence path validation
- τ₈ Translation Layer implementation
- Multi-source metric translation with provenance preservation
- Domain Input construction
- Analysis Start Detection integration
- Real audio validation
- Reconstruction pipeline validation

### Architectural Extensions

M4 established the foundation for future musical structure analysis.

The current Analysis Start Detection layer represents the first step toward a future Musical Structure Timeline capable of identifying:

- Intro sections
- Head / thematic sections
- AABA form
- Solo sections
- Trading sections
- Outro / Coda sections

---

# Milestone M5

## Behaviour Analysis

**Status:** ⬜ Planned

### Objectives

- Behaviour Profile
- Behaviour descriptors
- Behaviour comparison
- Temporal behaviour modelling
- Analysis of metric behaviour evolution inside musical sections

---

# Milestone M6

## Scientific Validation

**Status:** ⬜ Planned

### Objectives

- Mathematical validation
- Benchmark recordings
- Experimental evaluation
- Performance analysis

---

# Milestone M7

## Visualization

**Status:** ⬜ Planned

### Objectives

- Analysis reports
- Interactive visualizations
- Scientific plots
- Export facilities

---

# Milestone M8

## Research Platform

**Status:** ⬜ Planned

### Objectives

- Public API
- Plugin architecture
- External datasets
- Research workflows

---

# Milestone M9

## Version 1.0

**Status:** ⬜ Planned

### Objectives

- Stable scientific framework
- Complete documentation
- Reproducible research platform
- Public release