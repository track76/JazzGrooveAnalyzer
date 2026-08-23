# AD-039 — Calibration Zero and Measurement Baseline Authority

Status: LOCKED

## Decision and Governing Principle

`CED-VAL-001`, together with its provenance-bound authoritative symbolic
source, is the **JGA Calibration Zero / Controlled Measurement Baseline**.
Its calibration purpose is to characterize the relationship:

```text
authoritative symbolic event time
→ controlled audio rendering
→ physical audio observation
→ JGA detection
→ ElementaryMetricEvent timestamp
```

The controlled dataset is not a model of human performance timing.

Before JGA interprets temporal deviation as performance behaviour, it shall
first characterize the temporal deviation produced by its own controlled
rendering and measurement pipeline. Measurement precedes interpretation. A
non-zero measured temporal difference alone is not evidence of human
microtiming.

This decision authorizes calibration authority and future experimental scope
only. It authorizes no correction, tolerance, threshold, production change or
calibration result.

## Mission Alignment

Scientific Question:
: What temporal differences, bias, resolution effects and residual uncertainty
  arise between authoritative symbolic event time and JGA-observed EME time
  under a controlled, provenance-bound rendering and observation process?

Direct Contribution to JGA Mission:
: It separates measurement-system behaviour from later claims about human
  musical timing.

Missing Scientific Evidence:
: Event-level, source-specific signed measurement differences and their
  repeatability under Calibration Zero conditions.

Why Existing Evidence Is Insufficient:
: Existing EME and Drum-relative results validate preservation and neutral
  timestamp geometry, not correspondence to authoritative symbolic event time
  or decomposition of rendering and measurement effects.

Smallest Experiment Capable of Obtaining the Missing Evidence:
: The single future experiment reserved below.

Architectural Impact:
: None now.

Complexity Introduced:
: Documentation authority and a future evidence distinction only.

## Epistemic Quantities

For an event whose event-level correspondence has been independently
authorized and preserved:

```text
e_i = t_JGA,i - t_GT,i
```

`e_i` is **Observed Measurement Error**: an empirical signed measurement
difference. It is not automatically detector error because it may contain
controlled rendering, virtual-instrument envelope, transient morphology,
framewise observation, onset-localization, configuration and other measurable
pipeline effects.

A conceptual measurement model is:

```text
t_observed = t_reference + b + epsilon
```

- **Systematic bias (`b`)** is a stable and reproducible component demonstrated
  empirically across controlled observations.
- **Quantization / temporal resolution** is discretization or loss of sub-frame
  temporal information. It is not necessarily a systematic offset.
- **Residual uncertainty (`epsilon`)** is variation not demonstrated to be a
  stable systematic bias and shall remain explicit uncertainty.

The current observation hop is 512 samples at 44.1 kHz:

```text
512 / 44100 seconds ≈ 11.609977 milliseconds
```

This is frame spacing, or the nominal temporal sampling interval of the current
observation process. It is not JGA accuracy, measurement error, maximum error,
a correction value or a microtiming threshold. It shall not be subtracted from
timestamps merely because observed values occur at or near its multiples.

The descriptive absolute nearest-Drum-distance population from AD-038 is
motivating evidence only. Its values, including the concentration observed at
approximately 330–410 ms, remain neutral geometric nearest-neighbour distances
and are not validated musical microtiming displacement.

## Correctable and Non-Correctable Components

A measurement component may become eligible for mathematical correction only
after controlled calibration demonstrates that it is systematic,
reproducible, stable, provenance-bound, sufficiently characterized and
independently validated. PI authorization remains required after that evidence.

Unresolved quantization, residual variability, unstable rendering behaviour,
uncertain event correspondence and insufficiently characterized detector
behaviour are not correctable calibration bias. They shall remain explicit
measurement uncertainty and shall not be mathematically removed.

For a future demonstrated simple bias, the following relationship is reserved
conceptually:

```text
t_corrected = t_observed - b
```

No value of `b` is authorized. In particular, `b` is not assumed to equal
11.609977 ms. No timestamp correction is authorized by this decision.

## Source-Specific and Pairwise Calibration

Calibration authority shall permit source-specific measurement behaviour.
Conceptually, for sources A and B:

```text
t_A,observed = t_A,true + b_A + epsilon_A
t_B,observed = t_B,true + b_B + epsilon_B

Delta_observed = Delta_true + (b_A - b_B) + residual uncertainty
```

Only if `b_A` and `b_B` are independently demonstrated and validated may a
future PI decision authorize:

```text
Delta_corrected = Delta_observed - (b_A - b_B)
```

These equations are conceptual only. No source-specific or pairwise correction
is currently authorized.

## Required Future Representation Distinction

Any future calibration-aware work shall distinguish:

1. **Raw / Observed** — the immutable timestamp or temporal difference
   physically measured by JGA.
2. **Calibration Baseline** — empirically established measurement behaviour for
   the applicable source, rendering condition, detector configuration and
   provenance.
3. **Baseline-Aware Timing Evidence** — a separately represented future result
   that may contain an authorized corrected estimate, residual uncertainty and
   calibration provenance.

Raw observations shall never be overwritten. If correction is later
authorized, raw observation, calibration model, corrected estimate,
uncertainty and provenance shall remain separate and recoverable.

## Calibration Reference Dataset Authority

Calibration Zero is provenance-bound by `CED-VAL-001`, AD-028 and AD-033. Its
auditable calibration record shall preserve, where available:

- symbolic source identity and authoritative symbolic event time;
- MusicXML, MIDI or authority-equivalent symbolic evidence;
- exact audio-stem identity and SHA-256;
- sample rate, sample count and sample-zero relationship;
- rendering provenance and source/instrument identity;
- observation configuration, frame/hop configuration and detector/version;
- PulseCandidate and EME lineage;
- temporal scope and execution identity.

The scientific record shall preserve the distinction between symbolic event,
rendered acoustic event, detected physical observation and EME representation.
The existing M83 Ground Truth schema does not yet establish GroundTruthEvent;
event-level correspondence is therefore missing evidence for the future
experiment, not a current Observed Fact.

## Single Reserved Future Calibration Experiment

Exactly one next controlled experiment is reserved:

`H-VAL001-CALIBRATION-ZERO-01`

It shall preserve event-level correspondence with authoritative symbolic time
and measure, per source: signed error, absolute error, mean, median, complete
error distribution, frame-offset distribution, possible source-specific
systematic bias, residual dispersion, repeatability and rendering/detection
uncertainty where distinguishable. It shall determine whether the evidence is
best described by stable offset, frame quantization, source-dependent bias,
residual variability or a combination.

The experiment is not preregistered or executed by this decision. Its future
preregistration shall define correspondence authority, falsifiable acceptance
rules and Ground Truth access discipline before execution. No microtiming
threshold is authorized.

## Separate Scientific Paths

Controlled Calibration Path:

```text
Symbolic Ground Truth
→ controlled rendering
→ physical observation
→ EME
→ measurement-error characterization
→ bias/uncertainty decomposition
→ JGA Calibration Baseline
→ optional future validated correction model
```

Human Performance Path:

```text
real audio
→ physical observation
→ EME
→ neutral inter-instrument temporal relationships
→ calibration-baseline awareness
→ only later scientifically authorized musical interpretation
```

Controlled Ground Truth shall never manufacture or alter observations in the
human-performance path.

## Ground Truth Firewall

Ground Truth is authorized for controlled calibration, validation and
measurement characterization. It is not authorized to create or move EME in
real performances, force event correspondence, manufacture tempo or meter, or
manufacture musical interpretation. Existing SVP-001 independence and AD-028
ownership remain authoritative.

## Scientific History and Publication

Under F-030, the complete path from raw observation to any future timing claim
shall remain auditable. Records shall preserve why calibration became
necessary, motivating descriptive observations, preregistrations, negative
results, decisions, experiments, correction criteria, validation outcomes and
PI gates. Historical evidence shall not be rewritten to make scientific
development appear linear or predetermined.

## Relationship to Existing Authority

- The Scientific Manifesto and Scientific Research Constitution continue to
  govern observation before interpretation and research minimalism.
- The Knowledge Model governs evidence classification and prevents frame
  spacing or motivating observations from being promoted to demonstrated bias.
- F-030 governs preservation of calibration history and reproducibility.
- AD-028 continues to own Ground Truth identity and independence.
- AD-033 continues to own controlled dataset generation provenance.
- AD-037 continues to preserve EME existence and cardinality independently of
  later localization or calibration.
- AD-038 continues to govern neutral Drum-relative geometry. Its validated
  results remain valid observations and are not calibration-corrected.

## Architectural and Production Consequence

No new architectural layer, runtime component or dependency is introduced.
The architecture reserves a future distinction among raw observation,
calibration baseline and baseline-aware evidence without implementing it.
Production impact is **NONE**.
