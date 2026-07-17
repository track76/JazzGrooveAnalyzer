# RFC-001 — Observation Model Review

Version: 0.1 (Draft)

Status:
UNDER DISCUSSION

Author:
Angelo Tracanna

---

# Purpose

This RFC reviews the current observation model adopted by the Jazz Groove
Analyzer (JGA).

Its purpose is to verify whether the current scientific model faithfully
represents the observable reality of a musical performance or whether an
additional observational layer should be introduced.

No implementation shall be modified until this RFC is approved.

---

# Motivation

Recent discussions highlighted a possible ambiguity regarding the nature of
the Elementary Metric Event (EME).

The current model defines the EME as the first temporal entity of the
representation domain.

However, scientific observation suggests that the JGA first receives a
continuous audio signal containing every observable sound event.

The question is therefore:

"When does an observation become an Elementary Metric Event?"

---

# Current Model

Current simplified pipeline:

Audio Signal
    ↓
PulseCandidate
    ↓
Elementary Metric Event
    ↓
Metric Cluster
    ↓
Beat Reference

---

# Question Under Investigation

Does the Elementary Metric Event represent:

A)

the first observable sound event,

or

B)

the first interpreted temporal representation derived from an observation?

---

# Scientific Constraints

The following principles are considered invariant.

- Observation always precedes interpretation.
- The original performance remains the source of truth.
- No observed event is modified.
- Musical meaning must emerge from observable evidence.
- Every higher abstraction level must be traceable to physical observations.

---

# Open Questions

The following questions remain under investigation.

1. Is an EME itself an observation?

2. Does an observation exist before an EME?

3. Should PulseCandidate remain part of the scientific model or only of the DSP pipeline?

4. Is an additional "Observation" entity required?

5. Can the current model already represent the desired behaviour without introducing new entities?

---

# Expected Outcome

The outcome of this RFC shall determine whether the scientific foundations,
Domain Model and implementation require revision.

Until this RFC is approved, the current implementation remains the official
reference model.
