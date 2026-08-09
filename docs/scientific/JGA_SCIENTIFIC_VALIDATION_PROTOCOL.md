# JGA Scientific Validation Protocol

Document ID: SVP-001

Status: LOCKED

---

# 1. Purpose

This document defines the scientific validation methodology of Jazz Groove Analyzer (JGA).

Every significant architectural evolution shall be validated through reproducible experiments using datasets with known ground truth.

This protocol is part of the scientific methodology of JGA.

---

# 2. Scientific Principle

JGA reconstructs musical behaviour exclusively from observable information contained in the audio signal.

No musical metadata may be used during analysis.

Ground truth is used only after execution for validation.

The scientific distinction between observation-derived periodicity and
metric-level interpretation is defined by
`docs/scientific/foundations/F-031_HIERARCHICAL_METRIC_PERIODICITY.md`. This
reference introduces no validation metric, tolerance or comparison rule.

Blind Candidate Discovery and post-blind evaluation are scientifically defined
by `docs/scientific/foundations/F-032_CANDIDATE_PERIODS.md`. F-032 does not
change this protocol's execution or artifact requirements.

---

# 3. Canonical Validation Catalogue and Item

Catalogue ID

JGA-VALIDATION-CATALOG-v1

Validation Item ID

VAL-001

Reference Audio

03 THE COST OF LIVING versione intro + 8 bar.mp3

Ground Truth

- Time Signature: 4/4
- Tempo: 78 BPM
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
- Audio rendered from score
- Blind analysis

VAL-001 is the canonical scientific validation item of JGA.

The scientific catalogue and Validation Item asset binding are defined by:

- `docs/architecture/AD-029_M84_VALIDATION_CATALOG.md`

The canonical Ground Truth reference bound to VAL-001 is defined by:

- `docs/architecture/AD-028_M83_GROUND_TRUTH_REFERENCE.md`

The controlled experimental WAV dataset related to VAL-001 is identified as
`CED-VAL-001`. Its declared generation procedure and temporal origin are
preserved by:

- `docs/scientific/controlled_datasets/CED-VAL-001.md`

Controlled Dataset Provenance does not change the canonical MP3 analysis asset
or the independent Ground Truth binding.

---

# 4. Mandatory Validation

VAL-001 shall be executed after every significant modification involving:

- Observation Layer
- Source Separation
- Source Understanding
- Pulse Extraction
- Metric Reconstruction
- Ensemble Metric Consensus
- Translation Layer
- Domain Reconstruction
- Behaviour Analytics
- Scientific Geometry
- Scientific Report

---

# 5. Validation Workflow

## Phase 1

Repository Validation

- Execute test suite.
- Verify repository consistency.

## Phase 2

Experimental Execution

- Execute JGA on VAL-001.
- Blind analysis only.

## Phase 3

Evidence Collection

Observation

- detected sources
- onset observations
- intro detection

Source Understanding

- observed sources
- source identities
- confidence

Metric Reconstruction

- Pulse Candidates
- Source Pulse Sequences
- Metric Context
- Ensemble Metric Events
- Metric Clusters
- Beat References
- Internal Metric Timeline

Behaviour Analytics

- Behaviour Profile
- Descriptor Set
- Stability

Geometry

- Scientific Geometric Plane
- Scientific Behaviour Space

Scientific Report

- final report

---

# 6. Experimental Artifacts

Each execution produces:

validation/

    VAL-001/

        run_YYYYMMDD_HHMM/

            runtime.log
            baseline.json
            report.json
            diagnostics.json
            figures/
            notes.md

Previous executions shall never be overwritten.

---

# 7. Comparative Validation

The first approved immutable Comparator contract is defined by:

- `docs/architecture/AD-030_M85_COMPARATOR.md`

Each execution shall be compared against:

- previous baseline
- VAL-001 ground truth

Differences shall be classified as:

- Expected Improvement
- Expected Architectural Change
- Regression
- Bug
- Non-significant Difference

---

# 8. Scientific Reproducibility

No scientific result shall be considered publishable unless it is reproducible from:

- Git commit
- Validation dataset
- Validation protocol
- Generated reports
- Execution logs

---

# 9. Scientific Validation Record

Each completed validation and comparative evaluation shall be
preserved as part of the permanent scientific record of JGA.

The Scientific Knowledge Record governs the provenance and
preservation of validation records. This protocol remains the
authority for validation execution, Ground Truth independence and
reproducibility requirements.

See F-030 — Scientific Knowledge Record.

The immutable preservation boundary for one completed validation execution is
defined by:

- `docs/architecture/AD-031_M87_SCIENTIFIC_VALIDATION_RECORD.md`

---

# 10. Future Datasets

Future datasets shall follow the same protocol.

Examples:

- VAL-002
- VAL-003
- ...

---

# 11. Modification Policy

This protocol is LOCKED.

Any modification requires an explicit Architectural Decision.
