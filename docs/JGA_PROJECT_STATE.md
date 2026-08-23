# JGA Project State

## Blind Rhythm-Section Event-Correspondence Preregistration

Status: FROZEN — NOT EXECUTED

- `H-VAL001-RHYTHM-CORRESPONDENCE-01` freezes one Ground-Truth-blind candidate
  relation rule over the complete AD-040 Drums, Double Bass and Piano
  populations.
- A candidate requires mutual unique geometric nearest status, an identical
  exact two-sided integer-frame interval signature, independent recurrence of
  that signature at least twice within each source, and no boundary, duplicate
  frame or tie condition.
- Exact frame identity must be recovered by unique bitwise producer
  round-trip. No rounding, tolerance, millisecond threshold, PulseCandidate
  strength, Calibration Zero correspondence evidence or metric information is
  authorized.
- The complete blind population and fingerprint must freeze before any
  symbolic authority is opened. Post-freeze validation may score but never
  retune or modify blind relations.
- The experiment is not executed. Production impact is NONE; raw EME,
  PulseCandidates, AD-038 localizations, AD-040 profiles, calibration artifacts
  and visualizations remain unchanged.
- Preregistration:
  `validation/VAL-001/preregistrations/H-VAL001-RHYTHM-CORRESPONDENCE-01.md`.

## Rhythm Section Timing Profile Authority

Status: IMPLEMENTED

- AD-040 reserves `RhythmSectionTimingProfile` as a provenance-bound,
  read-only downstream projection over existing immutable EME, AD-038 neutral
  Drum-relative geometry and separately referenced Calibration Zero evidence.
- For the current controlled dataset, Drums are assigned
  `TEMPORAL_REFERENCE`; Double Bass and Piano are assigned `ACCOMPANIMENT`;
  Tenor Sax remains outside the core in a melodic/lead analytical role and
  Voice remains `DEFERRED`.
- Analytical role is explicitly bound to source/asset, scope, rule/version,
  execution and scientific authority. Instrument identity does not imply role;
  no automatic role inference is authorized.
- `GEOMETRIC_ONLY`, `AUTHORIZED_EVENT_RELATION`, `UNRESOLVED` and
  `NOT_APPLICABLE` form the minimum correspondence vocabulary. Calibration
  applicability remains separate.
- Raw observation, calibration context and future interpretation are
  non-overwriting levels. Absolute recording time remains authoritative; no
  correction is authorized.
- The minimum immutable implementation stores direct references to authorized
  EME and AD-038 localizations, explicit source/asset role assignments,
  independent correspondence evidence and separate calibration references.
  Deterministic profile identity and scientific fingerprinting depend on
  canonical referenced authority; no timestamp or displacement is copied or
  corrected.
- Controlled integration preserves 63 Drum EME and projects 49 Piano plus 27
  Double Bass relationships. All 16 Tenor Sax EME remain outside the current
  core and Voice remains `DEFERRED`. Focused contracts: 18 passed. Full suite:
  1087 passed, 1 unchanged environment-dependent Demucs external-storage
  failure, 3 warnings.
- Canonical decision:
  `docs/architecture/AD-040_RHYTHM_SECTION_TIMING_PROFILE.md`.

## Pairwise Calibration Zero Measurement Characterization

Status: PASS — MIXED SOURCE-SPECIFIC OUTCOME

- `H-VAL001-CALIBRATION-PAIRWISE-01` executed unchanged after checksum
  verification and independent freeze/verification of exact-equality symbolic
  pair authority.
- Symbolic/valid JGA pair populations are Piano–Drums 36/36, Double
  Bass–Drums 19/18 and Tenor Sax–Drums 9/5. Unmatched symbolic relationships
  are 13, 9 and 3; unresolved JGA pairs are 0, 1 and 4; symbolic ambiguity is
  zero throughout. All evidence remains preserved.
- Piano–Drums and Double Bass–Drums are
  `NO_DETECTABLE_PAIRWISE_BIAS` under the frozen stability rule. Tenor
  Sax–Drums is `INSUFFICIENT_EVIDENCE`; therefore the overall classification
  is `MIXED_SOURCE_SPECIFIC_OUTCOME`.
- All 59 valid errors occur at integer frame offsets to within exact
  stored-timestamp residuals no greater than `6.0771e-12 ms`. This is
  descriptive structure only and establishes no causal mechanism.
- Common absolute candidate behaviour is compatible with cancellation for
  Piano–Drums and Double Bass–Drums; Tenor Sax–Drums remains partial because
  minimum support is absent.
- No correction is authorized. Raw observations are unchanged; Voice remains
  `DEFERRED`. Deterministic replay and independent verification: PASS.
- Scientific fingerprint:
  `38740f74ab22c5c17b4400a6fac3823cbf4ead8650f77d6a5ab81e8ee7921b27`.
- Record: `validation/VAL-001/run_20260823_095617/`.

## Pairwise Calibration Zero Preregistration

Status: FROZEN — NOT EXECUTED

- `H-VAL001-CALIBRATION-PAIRWISE-01` freezes a distinct downstream experiment
  measuring error in Ground-Truth-authorized Piano–Drums, Double Bass–Drums
  and Tenor Sax–Drums temporal relationships.
- Symbolic pairs are constructed by exact equal authoritative symbolic time
  and frozen before JGA pairwise quantities are calculated. Geometrically
  nearest Drum observations, tolerances and result-informed matching are not
  authorized.
- The protocol freezes pairwise quantities, contributor-separated descriptive
  outputs, deterministic bootstrap and stability criteria, frame-resolution
  description, allowed outcomes and reproducibility artifacts.
- The completed absolute Calibration Zero study remains unchanged. No
  correction, production behavior or experiment execution is authorized.
- Voice remains `DEFERRED`; raw Ground Truth, EME, PulseCandidates,
  Drum-relative localizations and existing calibration artifacts are immutable.
- Preregistration:
  `validation/VAL-001/preregistrations/H-VAL001-CALIBRATION-PAIRWISE-01.md`.

## Calibration Zero Measurement Characterization

Status: PASS — SOURCE-INDEPENDENT CANDIDATE BIAS / MIXED MEASUREMENT BEHAVIOUR

- `H-VAL001-CALIBRATION-ZERO-01` executed unchanged from the frozen
  preregistration after sufficient symbolic-event authority was constructed
  without prior access to JGA event-level differences.
- Frozen symbolic/observed/valid populations are Drums 63/63/63, Piano
  49/49/49, Double Bass 28/27/27 and Tenor Sax 12/16/8. One Bass symbolic event
  is unmatched; four Sax cells contain multiple observed EME. All ambiguous
  evidence remains preserved.
- Drums, Piano and Double Bass satisfy the frozen candidate-bias criterion;
  Tenor Sax has insufficient valid support. Qualifying-source pairwise
  intervals include zero and the pooled median interval excludes zero, yielding
  `SOURCE_INDEPENDENT_CANDIDATE_BIAS` under the preregistered rule.
- Frame offsets concentrate at one and two frames, but no valid error is an
  exact frame multiple and residuals span nearly the full nearest-frame range.
  Frame-related evidence is `PARTIAL`; measurement structure is
  `MIXED_MEASUREMENT_BEHAVIOUR`, not quantization-dominated.
- The result characterizes combined controlled rendering/measurement behavior.
  Rendering and detection contributions are not separately identified.
- No correction, tolerance, threshold or production integration is authorized.
  Raw observations are unchanged; Voice remains `DEFERRED`.
- Deterministic replay: PASS. Scientific fingerprint:
  `d9ff1dba90cdb8b96e0412d05dd10c8b972f9dd2c2194187addcff4d6bd2050f`.
- Record: `validation/VAL-001/run_20260823_070702/`.

## Calibration Zero Experiment Preregistration

Status: FROZEN — NOT EXECUTED

- `H-VAL001-CALIBRATION-ZERO-01` freezes the event-authority construction,
  deterministic midpoint-cell correspondence rule, event-level measurement
  quantities, descriptive outputs, frame-offset analysis, candidate-bias
  criteria, source/pairwise analysis and allowed outcomes before access to
  symbolic-vs-JGA timing differences.
- AD-028 does not currently establish event-level Ground Truth. The future
  execution must first construct and freeze provenance-bound symbolic event
  authority without accessing JGA timing differences; insufficient authority
  stops execution before error calculation.
- The experiment is not executed. No calibration result, bias, correction,
  tolerance, threshold or production behavior is authorized.
- Voice remains `DEFERRED`. Raw EME, PulseCandidate, Drum-relative and existing
  validation artifacts remain unchanged.
- Preregistration:
  `validation/VAL-001/preregistrations/H-VAL001-CALIBRATION-ZERO-01.md`.

## Calibration Zero and Measurement Baseline Authority

Status: AUTHORIZED — EXPERIMENT NOT EXECUTED

- AD-039 establishes `CED-VAL-001` and its provenance-bound symbolic authority
  as the JGA Calibration Zero / Controlled Measurement Baseline.
- JGA must characterize controlled rendering and measurement behaviour before
  temporal deviation may be interpreted as human performance behaviour.
- The current 512-sample hop at 44.1 kHz is approximately 11.609977 ms frame
  spacing. It is not established accuracy, measurement error, systematic bias,
  correction or a microtiming threshold.
- Raw observation, calibration baseline and any future baseline-aware evidence
  must remain separate. Raw EME timestamps are immutable.
- Source-specific and pairwise calibration are conceptually reserved, but no
  bias value, correction, tolerance or production behavior is authorized.
- Existing AD-037 EME and AD-038 Drum-relative results remain valid, unchanged
  neutral observations. Their descriptive distributions are motivating
  evidence only.
- Exactly one future experiment is reserved as
  `H-VAL001-CALIBRATION-ZERO-01`; it is not preregistered or executed.
- Production impact: NONE.

## Neutral Drum-Relative EME Localization

Status: PASS

- AD-038 establishes the immediate minimum path as absolute audio timeline →
  authorized EME → neutral Drum-relative localization → later comparison.
- The separate downstream Representation projection preserves all 63 Drum EME
  and produces one immutable localization for every authorized Piano (49),
  Double Bass (27) and Tenor Sax (16) EME: 92 records from 155 preserved EME.
- Losses, merges and creations are zero. Exact timestamps, contributor/source,
  target and selected Drum PulseCandidate lineage, asset, scope, origin, rule
  and execution provenance are retained. Voice remains `DEFERRED`.
- Independent validation reproduced all localization arithmetic. Three targets
  precede the first Drum event, one follows the last, 88 records have an
  observed interval fraction, and two geometric nearest-selection ties are
  explicitly preserved.
- No declared BPM, meter or BeatReference input enters the new projection. The
  existing validated metric path remains unchanged and independently callable.
- Scientific fingerprint:
  `92a6b2e467d0b0b7fe465e9ccb8d9eb6d6e03ed9fb3e7435a2f0fd53bb4c2c62`.
- Focused validation: 17 passed, 2 dependency deprecation warnings.
- Complete automated suite: 1078 passed, 1 environment-dependent Demucs
  external-storage failure, 3 warnings. The configured external root was not
  writable; no heavy write was attempted.
- Record: `validation/VAL-001/run_20260823_060808/`.

## Complete Neutral EME Timing Validation

Status: PASS

- `H-VAL001-EME-NEUTRAL-01` represents all 155 authorized Drums, Piano,
  Double Bass and Tenor Sax EME against the provenance-bound declared quarter
  timeline. Losses, merges and creations are zero; Voice remains `DEFERRED`.
- Every record preserves exact frame-derived timestamp, contributor/source,
  preceding/following BeatReference, elapsed time, normalized phase, neutral
  nearest-reference displacement, PulseCandidate lineage/strength, and full
  declared timeline provenance without musical classification.
- Validation exposed and corrected nondeterministic `MetricContributor` UUID
  creation. Contributor identity is now deterministic from existing source and
  function evidence. Timing and cardinality are unchanged.
- Scientific fingerprint:
  `a8b39d18139fec26c2b3da7bee02942a1bd3a619143208b7d0bafca9129f8500`.
- Record: `validation/VAL-001/run_20260816_200807/`.

## Rhythm-Section Strength Role Discrimination

Status: COMPLETED — HIERARCHICALLY UNRESOLVED

- `H-VAL001-RHYTHM-STRENGTH-01` tested AD-032-preserved onset strength over
  the immutable SHORT/LONG families and complete Drums, Double Bass and Piano
  EME populations. All 139 supporting PulseCandidate identities reproduced.
- Full/early/late centered-strength phase association did not satisfy the
  frozen source or equal-source preference rules. Blind classification is
  `EQUIVALENT_UNRESOLVED`; Ground Truth was accessed only after freeze.
- Strength did not resolve metric role. Autonomous BPM remains `PARTIAL` and
  production integration is not authorized. Scientific fingerprint:
  `24c89394f846c579e46f6c796a181b7ffb35dc3f8cafc948cb5ca687194b43fd`.
- Record: `validation/VAL-001/run_20260816_195601/`.

## Rhythm-Section Metric-Role Discrimination

Status:

COMPLETED — HIERARCHICALLY UNRESOLVED

- `H-VAL001-RHYTHM-ROLE-01` tested only the immutable SHORT and LONG
  common-period families from `H-VAL001-RHYTHM-TEMPO-01`, using the same
  complete AD-037 Drums, Double Bass and Piano EME populations.
- Candidate origin was an exhaustively evaluated nuisance parameter. Neutral
  cycle-occupancy recurrence was selected by a preregistered BIC rule over
  full, early and late scopes, with equal-source consensus.
- Drums preferred SHORT. Double Bass and Piano were unresolved under the
  frozen source rule, so neither family received the required two independent
  source votes.
- Blind classification is `EQUIVALENT_HIERARCHICALLY_UNRESOLVED`. The result
  was frozen before Ground Truth access and does not assign metric role.
- Post-freeze validation confirms that the authoritative reference lies in the
  LONG family; the blind criterion did not select it. Autonomous BPM remains
  `PARTIAL`, and production integration is not authorized.
- Voice remains `DEFERRED`. No production or architectural behavior changed.
- Scientific fingerprint:
  `02912d34d5a5aeafa00b41131863a79b7ece77934e338bb3c923ff174298f5c7`.
- Complete record: `validation/VAL-001/run_20260816_193800/`.

## Rhythm-Section Common-Period Validation

Status:

COMPLETED — AUTONOMOUS BPM PARTIAL

- `H-VAL001-RHYTHM-TEMPO-01` applies the AD-035 exact consecutive-frame
  recurrence rule independently to complete AD-037 Drums, Double Bass and
  Piano EME timestamps. Declared BPM, meter, BeatReferences, normalized phase,
  melodic sources and Ground Truth do not enter blind discovery.
- The frozen blind result contains eight independently cross-supported common
  period tuples and is classified `MULTIPLE_COMMON_PERIODS`.
- Candidate families near 33 and 66 observation frames retain twelve
  measurement-supported 1:2 relationships. No metric role is assigned.
- All common candidates recur in both source-scope halves under the
  preregistered persistence rule. Continuous drift and local tempo remain
  unmeasured.
- Post-freeze Ground Truth validates correspondence of two long-period tuples
  and doubled correspondence of two short-period tuples with the authoritative
  reference. It does not alter the blind population.
- Rhythm-section consensus materially improves source independence and common
  recurrence evidence but does not resolve hierarchical role ambiguity.
  Metric-reference inference remains scientifically unresolved and autonomous
  BPM status is `PARTIAL`.
- Voice remains `DEFERRED`. Production implementation is not authorized.
- Scientific fingerprint:
  `238be4910504e6d2b570a47b6cb1d4ded21a280fddbe300c9f09f88af4b11d38`.
- Complete record: `validation/VAL-001/run_20260816_192519/`.

## Complete EME Phase-Population Analysis

Status:

COMPLETED

- `H-VAL001-EME-PHASE-01` executed its frozen contributor-separated circular
  analysis of the complete AD-037 normalized-phase populations without
  Ground Truth access or musical interpretation.
- The candidate models are a uniform circular null and finite von Mises
  mixtures selected by BIC, with deterministic replay and preregistered
  bootstrap stability and uncertainty criteria.
- No EME may be removed, merged, duplicated or initially pooled across
  contributors. No phase center, component count or musical label is assumed.
- Voice remains `DEFERRED`, not excluded, and shall receive the same contract
  after an authorized Voice EME population exists. Basic Pitch and SOME are
  excluded from this analysis.
- The unchanged preregistration is authoritative at
  `validation/VAL-001/preregistrations/H-VAL001-EME-PHASE-01.md`.
- Double Bass supports two stable phase populations under the preregistered
  95% bootstrap rule. Drums, Piano and Tenor Sax are `INSUFFICIENT_EVIDENCE`
  because their selected component counts do not reach that stability rule.
- No pair of contributors has independently stable structure, so no
  shared-center comparison is authorized. Musical interpretation remains
  prohibited pending a separate PI decision.
- The immutable result is preserved at
  `validation/VAL-001/run_20260816_182736/` with scientific fingerprint
  `75fea68e4e3d6af29241e49a37d9bfd9ec2d0fb1ca822ff02a5466f4a4a1f8c2`.

## EME Materialization and Metric Localization

Status:

COMPLETED

- AD-037 supersedes AD-018's movement-dependent EME existence and
  one-EME-per-contributor/movement cardinality rules while preserving their
  scientific history.
- The production order is now source evidence → EME → metric localization →
  future interpretation. Metric association does not suppress, merge or create
  EME.
- Controlled cardinalities are Drums 63→63, Piano 49→49, Double Bass 27→27
  and Tenor Sax 16→16 from materialized EME through MetricPoint output.
- Multiple same-contributor EME per quarter interval are preserved. Maximum
  interval populations are 2, 3, 2 and 3 respectively.
- Every localizable EME retains preceding/following reference identity,
  elapsed seconds and raw normalized quarter phase in `[0,1)` without musical
  or subdivision interpretation.
- EME and Domain PulseCandidate identities are deterministic and asset-bound;
  observation lineage, metric provenance and Core observations are preserved.
- `H-VAL001-EME-CARDINALITY-01` status is `PASS`. Voice remains deferred.
- Focused Domain, Translation, Representation and controlled-real-audio
  validation: 101 passed, 2 dependency deprecation warnings.
- Complete automated suite excluding the environment-dependent Demucs
  integration test: 1069 passed, 3 warnings. No heavy write was attempted.

## Neutral Signed EME Displacement Validation

Status:

COMPLETED

- `H-VAL001-EME-DISPLACEMENT-01` validates the neutral quantity `EME timestamp
  - associated BeatReference timestamp` in seconds and milliseconds against
  the authorized 55-reference controlled quarter timeline.
- Every authorized EME retains exactly one MetricCluster membership and its
  AD-018 movement identity. No inclusion threshold, deletion, duplication or
  musical interpretation is applied.
- Controlled authorized EME populations are Drums 27, Piano 9, Double Bass 25
  and Tenor Sax 10. All preserve source, contributor, supporting-observation,
  movement and declared-timeline provenance.
- Raw quarter-normalized phase values reveal numerical populations near zero
  and near minus one-half for several sources. No categorical tolerance or
  subdivision meaning is assigned.
- Scientific replay fingerprints are identical across two executions per
  source. Runtime observation and EME UUIDs remain execution-local while
  within-analysis identity and lineage are preserved unchanged.
- The controlled status is `PASS`. The remaining limitation is that a
  quarter-only reference cannot separate temporal displacement from other
  metric phases without independently authorized subdivision evidence.
- Focused Domain, Representation and controlled-real-audio validation: 26
  passed, 2 dependency deprecation warnings.
- Complete automated suite excluding the environment-blocked Demucs
  integration test: 1059 passed, 3 warnings. No heavy write was attempted.

## Controlled BeatReference Timeline Validation

Status:

COMPLETED

- The authoritative controlled asset declares quarter phase `0.0` seconds as
  score time zero = audio sample zero, bound to the controlled WAV checksum.
- The declared path carries exact numeric start/end scope and independent
  provenance for rate, phase and audio-asset scope across Translation into
  Domain reconstruction.
- The quarter period is `10/13` seconds. BeatReferences are generated from
  `origin + index * period`, never recursive floating-point accumulation.
- The 1,865,728-sample, 44.1 kHz controlled WAV scope produces 55 common
  BeatReferences: index 0 at `0/1` seconds through index 54 at `540/13`
  seconds. The next reference lies beyond the scope and is not produced.
- BeatReference identity is deterministic from declared authority, numeric
  scope, exact timestamp and index. Consensus observations are associated
  afterward and do not determine identity, timestamp or cardinality.
- Source-density and EME independence are validated; Core observations remain
  unchanged. The timeline result is `PASS`.
- Focused Domain and controlled-real-audio validation: 21 passed.
- Complete automated suite excluding the environment-blocked Demucs
  integration test: 1057 passed, 3 warnings. The excluded test could not
  write to the configured `JGA_EXTERNAL_ROOT`; no heavy write was attempted.
- Autonomous BPM, meter, measures, downbeat, pickup, sections, Voice AI,
  groove and behaviour interpretation remain outside this validation.

## Total EME Projection

Status:

COMPLETED

- `MetricClusterBuilder` now projects every ElementaryMetricEvent to exactly
  one nearest BeatReference through the existing `BeatProjectionEngine`.
- BeatReferences are ordered by timestamp and index before projection; an exact
  temporal midpoint therefore resolves deterministically to the earlier
  reference.
- The former ±10 ms inclusion window and exclusion behavior are removed. No
  EME is discarded because of temporal distance, and signed offsets remain the
  unchanged event timestamp minus its selected reference timestamp.
- The earlier 71-EME result used the superseded consensus-count BeatReference
  sequence. With the corrected declared quarter timeline, all 77 observations
  remain preserved and are associated only after movement reconstruction;
  EME authorization is a downstream question and is not timeline evidence.
- No offset was interpreted musically. Measure-grid reconstruction, pickup,
  downbeat, sections and timing-behaviour interpretation remain outside this
  milestone.
- Focused Domain, Translation, representation and controlled-audio validation:
  720 passed.
- Complete automated suite: 1058 passed, 1 environment-blocked Demucs test,
  3 warnings. The blocked test could not write to the configured
  `JGA_EXTERNAL_ROOT`; no heavy write was attempted.

## Declared Meter Vertical Slice

Status:

COMPLETED

- Analysis input may supply an immutable meter independently from the declared
  metric reference, with explicit `DECLARED` origin and authority provenance.
- The controlled VAL-001 context supplies 4/4 from `GT-VAL-001-v1`; this is
  authoritative context and is never represented as detected or inferred from
  audio.
- Declared meter crosses the existing Translation boundary and produces the
  Domain `InternalMetricSignature` consumed by reconstructed-measure grouping.
  The existing `pulses_per_beat` reconstruction setting remains separate and
  is not evidence for the declared meter.
- Reconstructed, immutable, analytical and reporting outputs preserve declared
  meter origin and source identity. Without declared meter, time signature is
  `NOT_PRODUCED` and reconstructed measures are absent; no active silent 4/4
  fallback remains.
- Autonomous meter recognition remains `DEFERRED`, not solved. Measure
  boundaries, pickup, measure count, sections and EME correctness were not
  validated by this milestone.
- Focused Domain, Translation, representation, reporting and controlled-audio
  validation: 612 passed.
- Complete automated suite: 1052 passed, 1 environment-blocked Demucs test,
  3 warnings. The blocked test could not write to the configured
  `JGA_EXTERNAL_ROOT`; no heavy write was attempted.

## Declared Metric-Reference Vertical Slice

Status:

COMPLETED

- The analysis input may supply an immutable metric reference with explicit
  `DECLARED` origin, authority identity, source kind, SHA-256 identity and
  temporal scope.
- The controlled VAL-001 context supplies 78 quarter BPM from
  `GT-VAL-001-v1`; this value is contextual validation authority and is never
  represented as detected or inferred from audio.
- The declared reference crosses the existing Translation boundary and drives
  Domain beat-period and reconstructed-measure timing without entering or
  changing Core observation.
- Validation-facing immutable and analytical outputs preserve the declared
  origin and source identity. Without declared context, tempo and reconstructed
  measures are not produced; no silent 120 BPM fallback remains active.
- Autonomous BPM inference remains `DEFERRED`, not solved.
- Meter interpretation remains outside this milestone and is the next separate
  development item.
- Focused Domain, Translation, representation, reporting and controlled-audio
  validation: 593 passed.
- Complete automated suite excluding the environment-blocked Demucs integration
  test: 1043 passed, 3 warnings. The excluded test could not access the
  configured `JGA_EXTERNAL_ROOT`; no heavy write was attempted.

## M93 — Validation Dataset Generalization

Status:

COMPLETED

- AD-036 defines the operational generalization without changing scientific
  validation architecture or schemas.
- `recordings/validation/catalog.json` owns data-defined catalogue registration.
- MusicXML-adjacent `.ground_truth.json` data owns the existing Ground Truth
  identity, provenance and approved normalization values for each source.
- Repository loading verifies registered asset identities and materializes the
  existing immutable Validation Catalog and Ground Truth models.
- Complete validation execution selects a registered item by identity and
  composes the unchanged analysis materializer, Comparator and Scientific
  Validation Record boundaries.
- VAL-001 retains identical identities, checksums, Ground Truth content,
  availability states, Candidate Period population and scientific comparison
  behaviour.
- Focused operational and scientific regression validation: 56 passed.
- Complete automated suite: 1003 passed, 1 known environment-dependent Demucs
  MPS failure, 3 warnings.

## Phase II Validation Block 1

Status:

COMPLETED

- The completed block is summarized by
  `docs/scientific/PHASE_II_VALIDATION_BLOCK_1_COMPLETION_REPORT.md`.
- F-031 and F-032 provide the governing scientific foundations.
- H-VAL001-C1-03 and H-VAL001-C1-04 preserve the controlled experimental
  evidence.
- M91, M91.1 and M92 complete the minimum representation and production
  discovery responsibility supported by that evidence.
- The post-M92 Repository Authority Review found no remaining scientifically
  demonstrated insufficiency requiring implementation.
- No further implementation milestone is currently scientifically justified;
  future implementation requires new reproducible evidence demonstrating an
  actual insufficiency.

## M92 — Candidate Period Discovery

Status:

COMPLETED

- AD-035 defines the first production Candidate Period discovery rule.
- Input is limited to the existing filtered Core PulseCandidate population.
- Discovery preserves every exact consecutive positive frame interval
  occurring at least twice and every supporting adjacent observation pair.
- Frame length is explicit PulseCandidate observation/discovery configuration;
  no library default is recovered silently.
- The immutable CandidatePeriodPopulation is preserved on AnalysisContext
  immediately after filtering and does not feed or alter metric reconstruction.
- No selection, ranking, metric interpretation, phase, non-consecutive lag or
  cross-source candidate abstraction is introduced.
- Focused immutable/discovery validation: 19 passed.
- VAL-001 full mix and all five canonical WAV stems reproduce the complete
  accepted C1-03/C1-04 candidate inventories exactly.

## M91.1 — Candidate Period Representation Responsibility Correction

Status:

COMPLETED

- AD-034 now separates intrinsic Candidate evidence, runtime provenance and
  experimental-validation metadata.
- Experiment ID, validation run ID, validation protocol ID and repeated-run
  fingerprints are no longer mandatory Core representation fields.
- Asset identity and explicit discovery configuration preserve runtime
  traceability; source revision is retained only when available.
- Temporal unit remains population evidence. Frame length is not an intrinsic
  Candidate Period field and may only appear as explicit discovery
  configuration when a discovery procedure requires it.
- H-VAL001-C1-03 and H-VAL001-C1-04 retain their experimental identities and
  reproduction fingerprints in their F-030/SVP-001 records.
- Focused M91 compatibility validation: 12 passed.

## M91 — Scientific Representation of Candidate Periods

Status:

COMPLETED

- AD-034 places already-produced, pre-interpretive Candidate Period evidence
  in the existing Core observational representation location.
- The immutable representation preserves duration, recurrence occurrences,
  observation scope, provenance and reproducibility metadata only.
- It performs no discovery, generation, selection, consumption or metric
  interpretation.
- `H-VAL001-C1-03` is used only as controlled preserved evidence; its
  experiment-local recurrence protocol is not production authority.
- The current `MetricContext`, analysis pipeline, `BeatPeriodEstimator`,
  reconstruction path and validation schemas remain unchanged.
- Focused immutable-representation and preserved-evidence validation:
  10 passed for the VAL-001 full mix and five canonical WAV sources.
- Complete automated suite: 991 passed, 1 known environment-dependent Demucs
  MPS failure, 3 warnings.

## Phase II — Candidate Period Foundation

Status:

CANONICAL

- F-032 defines Recurrence, Candidate Period and Candidate Population.
- Its experimental basis is Campaign 1 experiment `H-VAL001-C1-03`.
- H-VAL001-C1-07 provides the experimental basis for the narrow
  cross-condition correspondence clarification: numerical proximity after a
  controlled transformation is insufficient without an explicitly justified,
  measurement-condition-aware criterion. No such criterion is defined.
- Candidate Periods remain observation-derived and pre-interpretive.
- Blind discovery remains independent from post-blind Ground Truth evaluation.
- No candidate selection, metric interpretation, architecture or implementation
  is introduced.

## Phase II — Hierarchical Metric Periodicity Foundation

Status:

CANONICAL

- F-031 defines observation-derived periodicity, candidate period, metric
  level, metric interpretation, metric reconstruction and hierarchical metric
  periodicity.
- Observation remains free of musical interpretation under AD-006.
- Metric-level interpretation remains owned by the Domain under AD-008.
- Observable Metric Context preserves temporal evidence and organization but
  does not identify meter, tempo, ensemble Pulse or metric level.
- The authoritative `ElementaryMetricEvent → BeatReference → MetricCluster →
  Pulse → InternalMetricTimeline` lineage remains unchanged.
- No production architecture, implementation, validation schema, metric,
  tolerance or algorithm is introduced.

## M89 — PulseCandidate Strength Preservation

Status:

COMPLETED

- AD-032 restores the Translation observation-preservation invariant.
- Core `PulseCandidate.strength` is preserved unchanged in immutable Domain
  PulseCandidate representations.
- No downstream scientific or analytical semantics are introduced.
- Focused and real VAL-001 validation: 20 passed.
- Complete automated suite: 981 passed, 1 known environment-dependent Demucs
  MPS failure, 3 warnings.

## Current Branch

scientific/translation-layer-finalization

## Current Milestone

M42 — Scientific Visualization Evolution

Status:

COMPLETED

## Completed

### M42.1

- Scientific Visualization Semantics
- Multi-Trajectory Visualization
- ScientificVisualizationScene
- VisualizationTrajectoryDescriptor

### M42.2

- TemporalVisualizationWindow
- VisualPoint temporal contract
- TemporalVisualizationProjector
- DefaultTemporalVisualizationProjector
- VisualizationProjectionPipeline

### Consensus Layer Integration

- Ensemble Metric Consensus Layer operational
- DomainPulseCandidateAdapter introduced
- Core PulseCandidate → Domain PulseCandidate translation boundary
- Source identity propagation through:
  AudioStem → MetricSource → MetricContributor → Domain PulseCandidate
- VAL-001 to VAL-004 validation flows completed

## Validation

- 108 tests passed
- No architectural regressions

## Notes

The Visualization Layer now supports immutable,
composable projection stages operating on
ScientificVisualizationScene objects.

Real audio visualization validation is intentionally
deferred until the visualization layer supports
interactive temporal exploration.

------------------------------------------------------------
M33 — COMPLETE OBSERVATION MODEL
------------------------------------------------------------

Status:
IN PROGRESS

Architectural Direction

The project is evaluating the complete removal of the
Analysis Start Filtering mechanism.

Current hypothesis:

The complete observable audio signal shall always be
processed.

Metric Stability is considered an observable property
of the performance rather than a prerequisite for
analysis.

Architectural Decision

AD-021
Status: PROPOSED

Validation

VAL-001


------------------------------------------------------------
M35 — COMPLETE OBSERVATION MODEL
------------------------------------------------------------

Status

COMPLETED

Summary

AD-021 has been accepted.

The analytical pipeline now processes the complete
observable musical signal.

No component of the pipeline discards observations based
on an estimated analysis starting point.

Validation

926 tests passed.

VAL-001 passed.


------------------------------------------------------------
M81 — SCIENTIFIC VALIDATION ARCHITECTURE
------------------------------------------------------------

Status

IN PROGRESS

Completed

- AD-027 Immutable Analysis Representation approved and specified.
- Immutable boundary contract introduced between completed analysis and
  scientific validation.

Pending

- Validation comparator integration.

Validation

- Immutable Analysis Representation contract tests passed.
- VAL-001 scientific validation passed.
- Full suite: 925 passed; one pre-existing Demucs/MPS environment integration
  test could not execute successfully because its configured backend requires
  macOS 14 or later.


------------------------------------------------------------
M83 — GROUND TRUTH LAYER
------------------------------------------------------------

Status

COMPLETED

Completed

- AD-028 M83 Ground Truth Reference approved and specified.
- GT-VAL-001-v1 identity and VAL-001 binding preserved.
- Authoritative MusicXML identity and checksum enforced.
- Immutable time signature, tempo, section, instrumentation and minimum
  metric-position representations implemented.
- Pickup and full-measure identity mapping preserved.
- Original MusicXML and canonical instrument designations preserved.
- Ground Truth loader remains independent from analysis, runtime, Comparator
  and validation outputs.

Pending

- Ground Truth Comparator implementation under a separate approved decision.

Validation

- Ground Truth focused tests: 11 passed.
- Ground Truth plus VAL-001 scientific validation: 19 passed.
- Full suite: 936 passed; one pre-existing Demucs/MPS environment integration
  test could not execute successfully because its configured backend requires
  macOS 14 or later.


------------------------------------------------------------
M84 — SCIENTIFIC VALIDATION CATALOG
------------------------------------------------------------

Status

COMPLETED

Completed

- AD-029 Scientific Validation Catalog approved and specified.
- `JGA-VALIDATION-CATALOG-v1` introduced as an immutable asset catalogue.
- `VAL-001` established as the first Validation Item.
- M83 Ground Truth binding corrected from Validation Dataset identity to
  Validation Item identity.
- GT-VAL-001-v1, authoritative MusicXML and MP3 identities bound without
  duplicating Ground Truth content.
- Asset checksums and definitive repository revisions preserved.
- Licensing status preserved explicitly as `not_specified` for both assets.
- Existing observational `ValidationDataset` retained unchanged and
  scientifically distinct.

Pending

- Comparator and validation metrics under separate approved decisions.

Validation

- Validation Catalog plus Ground Truth focused tests: 21 passed.
- Validation Catalog, Ground Truth and VAL-001 scientific validation:
  29 passed.
- Full suite: 946 passed; one pre-existing Demucs/MPS environment integration
  test could not execute successfully because its configured backend requires
  macOS 14 or later.


------------------------------------------------------------
M85 — SCIENTIFIC COMPARATOR
------------------------------------------------------------

Status

COMPLETED

Completed

- AD-030 Scientific Comparator approved and specified.
- Immutable Analysis Representation schema revision `1` and typed
  validation-facing outputs recorded.
- `JGA-COMPARATOR-001` schema compatibility and mandatory bindings enforced.
- Tempo differences and incompatible beat-unit evidence preserved.
- Exact time-signature evidence preserved without scoring.
- Exact-name section correspondence and signed boundary/length differences
  preserved without inference.
- Instrument categories compared as sets without aggregate accuracy.
- Availability states preserved without value inference.
- Unique execution, result and evidence identities introduced.
- Comparator output remains immutable and suitable for a later Scientific
  Validation Record.

Pending

- Scientific metrics, tolerances, classifications and conclusions under
  separate approved decisions.

Validation

- Comparator and validation-boundary focused tests: 23 passed.
- Comparator through VAL-001 scientific validation: 52 passed.
- Full suite: 967 passed; one pre-existing Demucs/MPS environment integration
  test could not execute successfully because its configured backend requires
  macOS 14 or later.


------------------------------------------------------------
M86 — END-TO-END SCIENTIFIC VALIDATION
------------------------------------------------------------

Status

COMPLETED

Completed

- Completed Analysis to Immutable Analysis Representation materialization
  boundary implemented for schema revision `1`.
- Real VAL-001 audio checksum, execution provenance, configuration,
  completeness, limitations and deterministic content fingerprint preserved.
- Current pipeline defaults excluded from scientific outputs; all four scoped
  quantities are explicitly represented as `NOT_PRODUCED`.
- Runtime state does not escape the deeply immutable representation.

Validation

- Materializer and immutable-boundary focused tests: 12 passed.
- Materializer through VAL-001 comparison validation: 58 passed.
- Full suite: 973 passed; one pre-existing Demucs/MPS environment integration
  test could not execute successfully because its configured backend requires
  macOS 14 or later.


------------------------------------------------------------
M87 — SCIENTIFIC VALIDATION RECORD
------------------------------------------------------------

Status

COMPLETED

Completed

- AD-031 Scientific Validation Record approved and specified.
- Immutable preservation of Comparator evidence, result and input provenance
  implemented.
- Validation Item, Ground Truth, analysis execution, Comparator execution,
  protocol and schema identities preserved.
- Analysis limitations and all Comparator availability states preserved.
- Deterministic record identity and SHA-256 content fingerprint implemented.
- Identity and content binding enforced before record creation.
- Real VAL-001 end-to-end chain completed through the Scientific Validation
  Record without metrics, tolerances, classification or conclusions.

Validation

- Scientific Validation Record focused and real-chain tests: 7 passed.
- M87 boundary through VAL-001 scientific validation: 65 passed.
- Full suite: 980 passed; one pre-existing Demucs/MPS environment integration
  test could not execute successfully because its configured backend requires
  macOS 14 or later.


------------------------------------------------------------
M90 — CONTROLLED DATASET PROVENANCE
------------------------------------------------------------

Status

COMPLETED

Completed

- AD-033 Controlled Dataset Provenance approved and specified.
- `CED-VAL-001`, `DGR-CED-VAL-001-001` and `PR-CED-VAL-001-001`
  established as canonical identities.
- Five authoritative controlled WAV stems preserved by repository-relative
  identity and SHA-256 checksum.
- PCM format, 24-bit depth, 44.1 kHz sample rate, stereo channel configuration,
  sample count and duration preserved as measured Observed Facts.
- Dataset generation and MusicXML-score-time-zero to WAV-sample-zero alignment
  preserved explicitly as Declared Experimental Procedure.
- Unavailable date, software-version and rendering details preserved as
  `not specified` without inference.
- Obsolete MP3 stems excluded from the canonical controlled dataset.
- Ground Truth, Validation Catalog, validation execution and F-030 ownership
  boundaries remain unchanged.

Validation

- Controlled asset identities, checksums and measured format verified against
  all five repository WAV assets.
- M85 focused validation: 23 passed.
- M86 focused validation through the Comparator boundary: 29 passed.
- M87 focused and real VAL-001 chain validation: 7 passed.
- Full suite: 981 passed, one known Demucs/MPS environment integration failure,
  and three warnings. The configured MPS backend requires macOS 14 or later.
