# JGA Project State

## CED-VAL-004 Physical-to-JGA Comparison Result

Status: **FROZEN — PI REVIEW REQUIRED**

- `H-CEDVAL004-PHYSICAL-TO-JGA-COMPARISON-01` executed unchanged against
  `PR-CED-VAL-004-PHYSICAL-ONSET-001`; dataset and frozen physical-onset
  authority verification passed.
- Untuned AD-037 observation produced 10 PulseCandidates / 10 EME per source.
  All 10 Drums and all 10 Double Bass physical events had exactly one EME in
  their frozen marker-midpoint cell; there were no missing, ambiguous,
  boundary, or unmatched observations.
- Every signed physical-to-JGA displacement was positive. Drums had median
  399 samples (9.047619047619048 ms); Double Bass had median 461.5 samples
  (10.464852607709751 ms). These are descriptive measurements, not
  corrections or tolerances.
- Producer-frame round-trip, exact marker decomposition, full cardinality,
  lineage, firewalls, and two complete deterministic executions passed.
- Scientific fingerprint:
  `cebccb70224dce4e519197e84178e11afdc1e98b8148914a7512ac6df06ef22e`.
- Strength and confidence were not used or emitted. H02, historical results,
  raw assets, architecture, production semantics, and production code remain
  unchanged. No correction is authorized.
- Frozen evidence is in
  `validation/CED-VAL-004-PHYSICAL-ONSET/run_20260824_112730/`.

## CED-VAL-004 Physical-to-JGA Comparison Preregistration

Status: FROZEN RULE — NOT EXECUTED

- `H-CEDVAL004-PHYSICAL-TO-JGA-COMPARISON-01` freezes AD-037
  `ElementaryMetricEvent.timestamp` as `t_JGA`, with exact 512-sample frame
  round-trip and explicit frame-resolution authority.
- Contributor-separated marker midpoint cells transfer the established
  Calibration Zero correspondence framework. Zero, single, multiple,
  boundary, tied and unconsumed observations remain explicit; strength and
  error minimization cannot select an EME.
- Primary signed error is `n_JGA - n_physical`; absolute error and exact marker
  decomposition remain separate. Source-specific reporting precedes pooled
  description.
- JGA has not been run on CED-VAL-004 for this study. Strength remains
  unopened, H02/H03 and historical results are unchanged, and production
  impact is none.

## CED-VAL-004 Physical-Onset Authority

Status: PASS — FROZEN PHYSICAL GROUND TRUTH — PI REVIEW REQUIRED

- The unchanged `H-CEDVAL004-PHYSICAL-ONSET-MEASUREMENT-01` first-nonzero
  rule produced 20/20 valid physical onsets with 20/20 exact-zero pre-marker
  baselines, no missing responses and no authority conflicts.
- Drums latency is one sample (`10/441 ms`) for all 10 events. Double Bass
  latency ranges from 176 to 236 samples, with median 202 samples.
- Left/right first-response samples agree for all 20 events. Two complete
  executions reproduce identities, signed values, onsets, latency quantities,
  statuses and fingerprint exactly.
- Scientific fingerprint: `7b2ec48f…`; complete record:
  `validation/CED-VAL-004-PHYSICAL-ONSET/run_20260824_110800/`.
- This authority establishes physical onset only. JGA, strength and H02 remain
  unopened pending separate PI review and authorization.

## CED-VAL-004 Physical-Onset Measurement Preregistration

Status: FROZEN RULE — EXECUTED UNCHANGED

- `H-CEDVAL004-PHYSICAL-ONSET-MEASUREMENT-01` defines `t_physical` as the
  first signed 24-bit source sample differing from exact digital-zero control
  at or after each marker within the fixed eight-second causal window.
- The event onset is the earlier channel response; channel-specific frames,
  values and disagreement remain preserved. Exact two-second pre-marker zero
  verification is mandatory, and any conflict remains unresolved rather than
  introducing a threshold.
- The rule is specific to the frozen no-dither, no-normalization,
  byte-reproducible common-clock authority. It does not generalize to nonzero
  baselines.
- Physical onset is frozen downstream. JGA, strength and H02 remain unopened.

## CED-VAL-004 Marker and Raw Waveform Authority

Status: FROZEN INPUT AUTHORITY — PASS — PHYSICAL ONSET NOT MEASURED

- `PR-CED-VAL-004-PHYSICAL-ONSET-001` freezes the PI-created Ableton Live
  11.3.43 common-clock session, 20-event exact marker schedule, canonical
  Marker/Drums/Double Bass assets and source-specific digital-silence controls.
- Every WAV is stereo 44.1 kHz signed 24-bit PCM with exactly 8,820,000 frames.
  The marker contains exactly the 20 authorized samples at amplitude
  `+4,194,304` in both channels; canonical and second-render assets are
  byte-identical.
- Dataset fingerprint: `704ce592…`. Complete authority:
  `validation/CED-VAL-004-PHYSICAL-ONSET/input_authority_manifest.json`.
- This freeze ends at scheduled excitation → marker → raw waveform.
  `t_physical`, JGA, strength and H02 remain unopened.

## CED-VAL-004 Physical-Onset Generation Preregistration

Status: FROZEN PROTOCOL — EXECUTED BY PI-CREATED ASSET AUTHORITY

- `PR-CED-VAL-004-PHYSICAL-ONSET-GENERATION-01` defines a prospective
  common-clock marker-referenced dataset for Drums and Double Bass.
- A single offline render must preserve one exact marker channel, separate
  unmodified source waveforms, equal-scope no-event controls and a canonical
  event/sample manifest.
- Twenty fixed 10-second isolated slots contain 10 excitations per source,
  balanced 5/5 across temporal halves, and place each marker two seconds after
  slot start. Generation is fixed at 44.1 kHz/24-bit PCM with a one-sample
  marker amplitude of 4,194,304.
  Marker authority remains distinct from a later separately preregistered
  non-JGA first-causal-response authority.
- The first technically valid render is frozen as canonical. Source rerender
  byte identity is not mandatory; any nondeterminism is retained and measured
  separately. Marker rerender identity and all common-clock checks remain
  mandatory.
- No physical-onset measurement, JGA execution, H02/H03 change or production
  impact is authorized.
- Protocol:
  `validation/CED-VAL-004-PHYSICAL-ONSET/preregistrations/PR-CED-VAL-004-PHYSICAL-ONSET-GENERATION-01.md`.

## CED-VAL-003 Strength-Max Correspondence Validation

Status: PASS EXECUTION — INSUFFICIENT SCORABLE EVIDENCE

- All 56 unique-strength predictors were frozen before Ground Truth and joined
  deterministically to frozen Calibration Zero authority.
- Drums 0/54 and Double Bass 0/2 were scorable; all 56 remain
  `AMBIGUOUS_MULTIPLE_OBSERVED`, so correct/incorrect and accuracy are
  undefined rather than zero-performance evidence.
- The study neither supports nor contradicts strength as a correspondence
  predictor. Unique physical discrimination is not independent scoring
  authority.
- Historical H02 results, the three-dataset conclusion, Calibration Zero, raw
  observations and production authority remain unchanged.
- Scientific fingerprint `f9dd0c08…`; complete record:
  `validation/CED-VAL-003-SWING-3-4/run_20260823_212608/`.

## CED-VAL-003 Strength-Max Correspondence Validation Preregistration

Status: FROZEN — NOT YET SCORED

- The 56 already-frozen unique-strength maximum identities are preserved in a
  Ground-Truth-free predictor manifest before scoring.
- Frozen Calibration Zero may score only where its existing authority uniquely
  adjudicates a contained EME; unresolved authority remains `UNSCORABLE`.
- No predictor recomputation, threshold, rematching, H02 rescoring or
  production effect is authorized.

## CED-VAL-003 Within-Cell Strength Discriminability

Status: PASS — FROZEN PHYSICAL DISCRIMINABILITY

- Exact binary64 strength produced `UNIQUE_STRENGTH_MAXIMUM` in 56/56 cells:
  Drums 54/54 and Double Bass 2/2; ties and unresolved cases are zero.
- The result demonstrates deterministic physical distinction only. It does not
  identify correct correspondence, resolve historical ambiguity or authorize
  H02 rescoring/production use.
- Ground Truth, thresholds, tolerances and cross-source comparisons were not
  used. H02, H03, Calibration Zero and raw observations remain unchanged.
- Scientific fingerprint `902c9a7d…`; complete record:
  `validation/CED-VAL-003-SWING-3-4/run_20260823_212023/`.

## CED-VAL-003 Within-Cell Strength Discriminability Preregistration

Status: FROZEN — NOT YET EXECUTED

- `H-CEDVAL003-WITHIN-CELL-STRENGTH-DISCRIMINABILITY-01` freezes exact
  binary64 within-cell ordering over the accepted 56-cell strength artifact.
- Unique maximum, exact tie and unresolved classifications are physical
  discriminability only; they cannot select correspondence or change H02.
- Ground Truth, thresholds, tolerances and cross-source comparisons are
  prohibited.

## CED-VAL-003 PulseCandidate Strength Measurement Authority

Status: PASS — FROZEN MEASUREMENT AUTHORITY

- Exact lineage-bound strength was recovered for all 112 observations in all
  56 frozen ambiguous cells: Drums 108/108, Double Bass 4/4, Piano 0/0.
- Two executions and a second complete run reproduced identities, frames,
  indices, binary64 values, memberships and fingerprint exactly; lineage
  failures are zero.
- Strength is now authoritative only as a provenance-bound within-source
  physical measurement for this population. Cross-source comparability and
  discrimination/selection authority remain unauthorized.
- Ground Truth and H02 scoring were not accessed. No rank, selection or
  threshold was produced; historical H02/Calibration Zero evidence remains
  unchanged.
- Scientific fingerprint `6903decb…`; complete record:
  `validation/CED-VAL-003-SWING-3-4/run_20260823_211259/`.

## CED-VAL-003 PulseCandidate Strength Authority Preregistration

Status: FROZEN — NOT YET EXECUTED

- `H-CEDVAL003-PULSECANDIDATE-STRENGTH-AUTHORITY-01` freezes exact recovery of
  lineage-bound strength for 112 observations in 56 ambiguous cells.
- Recovery is WAV → unchanged observation pipeline → exact PulseCandidate/EME
  identity join. Two exact replays are mandatory.
- The study establishes within-source measurement authority only. It cannot
  rank/select observations, access Ground Truth, rescore H02 or establish
  cross-source comparability.
- Preregistration:
  `validation/CED-VAL-003-SWING-3-4/preregistrations/H-CEDVAL003-PULSECANDIDATE-STRENGTH-AUTHORITY-01.md`.

## CED-VAL-003 Ambiguous-Cell Physical-Authority Evidence Gap

Status: FROZEN EVIDENCE GAP — NO EXPERIMENT PREREGISTERED

- The complete population is 56 `AMBIGUOUS_MULTIPLE_OBSERVED` cells containing
  112 observations: Drums 54/108, Double Bass 2/4 and Piano 0/0.
- Frozen authority preserves exact identities, timestamps, lineage,
  source/asset provenance and temporal-sequence context, but none currently
  authorizes a Ground-Truth-independent preference among observations inside a
  cell.
- Numeric PulseCandidate strength/confidence and EME confidence are not
  retained in the frozen CED-VAL-003 artifacts; strength also lacks validated
  within-cell discrimination semantics. No transient, spectral, envelope or
  Drum-component descriptor is authoritative.
- No experiment is forced. The minimum next evidence is lineage-bound numeric
  PulseCandidate strength plus independent deterministic within-source
  repeatability/measurement validation; this does not itself authorize a
  selection rule.
- Symbolic proximity is excluded. H02, H03, Calibration Zero, frozen scores,
  raw observations, AD-040 and production code remain unchanged;
  `GEOMETRIC_ONLY` remains authoritative.
- Frozen record:
  `validation/CED-VAL-003-SWING-3-4/preregistrations/EG-CEDVAL003-AMBIGUOUS-PHYSICAL-AUTHORITY-01.md`.

## CED-VAL-003 H02 Scorability Authority Audit

Status: FROZEN READ-ONLY AUDIT — PASS

- Complete deterministic audit explains all 56 unscorable candidates: 54 are
  blocked by Drum `AMBIGUOUS_MULTIPLE_OBSERVED` authority and 2 by Double Bass
  `AMBIGUOUS_MULTIPLE_OBSERVED` authority.
- Candidate-discovery limitations, mixed limitations, indeterminate cases and
  identity/provenance join failures are all zero. Blind candidate evidence
  exists; the limitation primarily affects validation.
- All 55 unscorable symbolic relations remain individually preserved. Frozen
  precision/recall/F1 remain unchanged and apply only to 33 scorable candidates.
- Audit fingerprint `34dafe33…`; complete record:
  `validation/CED-VAL-003-SWING-3-4/run_20260823_205731/`.

- `AUD-CEDVAL003-H02-SCORABILITY-01` freezes a read-only, deterministic audit
  of all 89 candidates, including 56 unscorable candidates and 55 unscorable
  symbolic relations.
- Exact identity joins trace frozen blind/scoring evidence through Calibration
  Zero event and pair authority without rematching or rescoring.
- H02, Calibration Zero, raw observations, frozen metrics, AD-040 and
  production code remain immutable.
- Preregistration:
  `validation/CED-VAL-003-SWING-3-4/preregistrations/AUD-CEDVAL003-H02-SCORABILITY-01.md`.

## H02 Three-Dataset Scientific Conclusion

Status: FROZEN — PI-AUTHORIZED EVIDENCE SYNTHESIS

- H02 is `EXPERIMENTALLY_SUPPORTED`, `SOURCE_SENSITIVE`,
  `REPLICATED_FOR_DOUBLE_BASS_DRUMS_UNDER_TESTED_CONTROLLED_CONDITIONS`,
  `NOT_GENERALIZED_FOR_PIANO_DRUMS` and `NOT_PRODUCTION_AUTHORIZED`.
- Strong Double Bass–Drums behavior replicated on CED-VAL-002 and CED-VAL-003
  within tested controlled conditions. Piano–Drums did not show stable
  conservative behavior across datasets.
- CED-VAL-003's 56 ambiguous/unscorable candidates and 55 unscorable symbolic
  relations remain preserved and materially limit its generalization evidence.
- Aggregate performance cannot replace source-specific evidence. No causal
  claim about 3/4, swing, density or analytical role is authorized.
- Calibration remains separate context; no correction is authorized. H02 and
  AD-040 are unchanged, no H03 exists, and `GEOMETRIC_ONLY` remains production
  authority.
- Frozen conclusion:
  `validation/H02_THREE_DATASET_SCIENTIFIC_CONCLUSION.md`.

## CED-VAL-003-SWING-3-4 H02 Independent Replication

Status: FROZEN RESULT — PARTIAL CORRESPONDENCE EVIDENCE

- The unchanged `H-VAL001-RHYTHM-CORRESPONDENCE-02` rule executed blind on
  `PR-CED-VAL-003-SWING-3-4-001`, without symbolic, calibration, meter or tempo
  input. Two complete blind executions replayed byte-identically.
- Blind result: 89 candidates (Piano 14; Double Bass 75), 61 unresolved;
  fingerprint `a76e37ed…`.
- Post-freeze scoring: Piano 3 TP / 2 FP / 9 FN from 5 scorable candidates;
  Double Bass 26 TP / 2 FP / 6 FN from 28 scorable candidates; overall 29 TP /
  4 FP / 15 FN, precision 0.878788, recall 0.659091 and F1 0.753247.
- Fifty-six blind candidates remain ambiguous/unscorable under frozen
  Ground-Truth correspondence authority and are preserved.
- Frozen classification: `PARTIAL_CORRESPONDENCE_EVIDENCE`; three-dataset
  generalization is `MIXED`. Double Bass supplies supporting replication,
  while Piano behavior and scorable coverage remain source/dataset-sensitive.
- H02 remains experimental and is not promoted. `GEOMETRIC_ONLY` remains
  production authority; raw observations and production code are unchanged.
- Scientific fingerprint: `374ab02a…`; complete record:
  `validation/CED-VAL-003-SWING-3-4/run_20260823_204545/`.

## CED-VAL-003-SWING-3-4 Controlled Dataset

Status: CALIBRATION ZERO FROZEN RESULT — PI REVIEW REQUIRED

- `H-CEDVAL003-CALIBRATION-ZERO-01` executed exactly against
  `PR-CED-VAL-003-SWING-3-4-001`; all checksum authority passed.
- Observed EME populations are Drums 155, Double Bass 100 and Piano 50. The
  frozen midpoint rule produced 193 valid absolute correspondences.
- Absolute outcome is `SOURCE_SPECIFIC_CANDIDATE_BIAS`; measurement structure
  is `MIXED_MEASUREMENT_BEHAVIOUR`. Drums are `INSUFFICIENT_EVIDENCE` after
  mandatory ambiguity sensitivity; Double Bass and Piano retain stable
  candidate systematic bias.
- Exact symbolic authority produced 12 valid Piano–Drums and 32 valid Double
  Bass–Drums JGA pairs. Both are `INSUFFICIENT_EVIDENCE` after the frozen
  ambiguity-sensitivity support gate.
- Two complete executions replayed deterministically; independent arithmetic,
  cardinality and lineage verification passed. Raw observations remain
  immutable, no correction is authorized, and H02 was neither executed nor
  inspected.
- Scientific fingerprint: `589ee3c1…`; complete record:
  `validation/CED-VAL-003-SWING-3-4/run_20260823_203324/`.

- `H-CEDVAL003-CALIBRATION-ZERO-01` binds exclusively to frozen authority
  `PR-CED-VAL-003-SWING-3-4-001` and fingerprint `9345f592…`.
- Exact-rational symbolic authority, contributor-separated midpoint cells,
  exact-equality symbolic pair authority, absolute/pairwise quantities,
  512/44100 frame description, fixed WAV-scope halves `512/21`, minimum
  support 10/5, deterministic 10,000-resample bootstrap, sensitivity and
  classification criteria are frozen before result access.
- No prior numerical calibration result transfers. Dataset assets, raw
  observations and H02 remain immutable; no correction or execution is
  authorized.
- Preregistration:
  `validation/CED-VAL-003-SWING-3-4/preregistrations/H-CEDVAL003-CALIBRATION-ZERO-01.md`.

- The initial failed discovery remains preserved. Following PI correction,
  assets were discovered under actual external root
  `datasets/CED-VAL-003-SWING/`, with scientific filenames retaining
  `CED-VAL-003-SWING-3-4` and audio directory `steams/`.
- Three equal stereo 24-bit PCM 44.1 kHz stems each contain 2,150,400 frames
  (`1024/21` seconds) with PI-declared common export-from-beginning origin.
- Explicit checksum-bound MusicXML Ground Truth declares 3/4 and quarter =
  140/minute and yields Drums 155, Double Bass 100 and Piano 57 exact-rational
  symbolic onset groups. No declaration entered JGA or H02.
- Complete symbolic scope `306/7` seconds is contained within the WAV scope;
  the untrimmed rendered tail is `106/21` seconds.
- A new independent Calibration Zero is mandatory before separately authorized
  unchanged blind H02 execution. No production behavior changed.
- Authority:
  `docs/scientific/controlled_datasets/CED-VAL-003-SWING-3-4.md` and
  `validation/CED-VAL-003-SWING-3-4/input_authority_manifest.json`.
- Dataset fingerprint: `9345f592…`.

## H02 Independent Out-of-Sample Validation

Status: MIXED GENERALIZATION — SCIENTIFIC CONCLUSION FROZEN

- The unchanged `H-VAL001-RHYTHM-CORRESPONDENCE-02` rule executed blind on
  corrected `PR-CED-VAL-002-SWING-002`, separately from Calibration Zero.
- Blind result: 125 candidates (Piano 11; Double Bass 114), fingerprint
  `c053888a…`, with deterministic replay before Ground Truth access.
- Post-freeze: Piano 4 TP / 7 FP / 20 FN; Double Bass 109 TP / 3 FP / 9 FN;
  overall 113 TP / 10 FP / 29 FN, precision 0.918699, recall 0.795775 and F1
  0.852830.
- Frozen classification: `PARTIAL_CORRESPONDENCE_EVIDENCE`; out-of-sample
  generalization evidence is `MIXED` because source-specific performance differs
  materially.
- No correction or production promotion is authorized. `GEOMETRIC_ONLY`
  remains production authority. Complete record:
  `validation/CED-VAL-002-SWING/run_20260823_192726/`.
- PI acceptance freezes H02 as experimentally supported, source-sensitive,
  conservative in some conditions and not production-authorized. At least one
  further genuinely independent controlled replication is mandatory before
  production promotion may be reconsidered.
- Frozen conclusion:
  `validation/CED-VAL-002-SWING/H02_OUT_OF_SAMPLE_SCIENTIFIC_CONCLUSION.md`.

## CED-VAL-002-SWING Calibration Zero Execution

Status: FROZEN RESULT — PI REVIEW REQUIRED

- `H-CEDVAL002-CALIBRATION-ZERO-01` executed exactly against corrected
  `PR-CED-VAL-002-SWING-002`; all checksum authority passed.
- Observed EME populations are Drums 192, Double Bass 127 and Piano 63. The
  frozen midpoint rule produced 378 valid absolute correspondences.
- Absolute outcome: `SOURCE_SPECIFIC_CANDIDATE_BIAS`; measurement structure:
  `MIXED_MEASUREMENT_BEHAVIOUR`.
- Exact symbolic authority produced 24 valid Piano–Drums and 118 valid Double
  Bass–Drums JGA pairs. Both are `CANDIDATE_PAIRWISE_BIAS` under the frozen
  criterion.
- Raw observations remain immutable. No correction is authorized. H02 remains
  frozen and was neither executed nor inspected.
- Scientific fingerprint: `d4b0b187…`; complete record:
  `validation/CED-VAL-002-SWING/run_20260823_170857/`.

## CED-VAL-002-SWING Calibration Zero Preregistration

Status: FROZEN — NOT EXECUTED

- `H-CEDVAL002-CALIBRATION-ZERO-01` binds exclusively to corrected provenance
  `PR-CED-VAL-002-SWING-002` and dataset fingerprint `631eaf01…`; the
  superseded pre-correction authority remains historical evidence only.
- Before EME comparison, execution must freeze exact-rational symbolic-event
  and exact-equality symbolic-pair authorities from corrected MusicXML.
- Contributor-separated midpoint-cell correspondence, absolute and pairwise
  quantities, 512/44100 frame description, exact WAV-scope halves, minimum
  support 10/5, deterministic 10,000-resample median bootstrap, ambiguity
  sensitivity, bias/stability criteria and outcome vocabularies are frozen
  before result access.
- CED-VAL-001 numerical calibration evidence does not transfer. No correction,
  production behavior or H02 execution is authorized.
- Preregistration:
  `validation/CED-VAL-002-SWING/preregistrations/H-CEDVAL002-CALIBRATION-ZERO-01.md`.

## CED-VAL-002-SWING Corrected Controlled Dataset

Status: CORRECTED INPUT AUTHORITY FROZEN — CALIBRATION PENDING

- PI correction after commit `64c8c93` changed the MusicXML and Sibelius
  assets; the three WAV assets remain byte-identical. The prior manifest and
  documentation remain preserved as superseded/pre-correction evidence.
- Corrected MusicXML remains well formed with Piano 64, Double Bass 127 and
  Drums 192 exact-rational symbolic onset groups. Symbolic scope is exactly
  128 quarter units / `256/5` seconds, first onset 0 and last onset 48 seconds.
- All three WAVs remain equal stereo 24-bit PCM, 44.1 kHz, 2,478,080 frames
  and `123904/2205` seconds. Their `11008/2205`-second tail beyond symbolic
  scope is neutral, preserved and temporally coherent with the PI-declared
  common export-from-beginning origin.
- Corrected authority supersedes revision 1 for all future Calibration Zero
  and H02 work. A new Calibration Zero remains mandatory; H02 was not executed
  and can later be applied unchanged after separate approval.
- Corrected records:
  `docs/scientific/controlled_datasets/CED-VAL-002-SWING_CORRECTED.md` and
  `validation/CED-VAL-002-SWING/input_authority_manifest_v2_corrected.json`.
- Corrected dataset/manifest fingerprint:
  `631eaf017cfaf335ee2945bfbe0df19221a0a0d069fee3602880eda7a851ade1`.

## CED-VAL-002-SWING Independent Controlled Dataset

Status: SUPERSEDED PRE-CORRECTION INPUT AUTHORITY

- The new external controlled dataset is checksum-bound at
  `$JGA_EXTERNAL_ROOT/datasets/CED-VAL-002-SWING/` without copying or altering
  its three WAV stems or symbolic sources.
- Drums, Double Bass and Piano WAV assets independently verify as stereo
  24-bit little-endian PCM at 44.1 kHz with identical 2,478,080-frame counts
  and exact duration `123904/2205` seconds. Sibelius `Export from beginning`
  is preserved as declared common-origin procedure; no onset alignment or
  trimming occurred.
- Well-formed MusicXML contains Piano, Bass and Drums and supports a later
  deterministic exact-rational event-authority build. Input-only
  characterization found 64, 127 and 192 symbolic onset groups respectively;
  no JGA observation or H02 outcome entered that characterization.
- Dataset identity and all asset checksums differ from `CED-VAL-001`. PI
  provenance establishes non-use in H01/H02 development; no statistical
  independence claim is made.
- A new Calibration Zero and pairwise applicability characterization is
  required before H02 execution. The frozen H02 rule can later be applied
  unchanged; it was not executed.
- Canonical records:
  `docs/scientific/controlled_datasets/CED-VAL-002-SWING.md` and
  `validation/CED-VAL-002-SWING/input_authority_manifest.json`.
- Dataset/manifest fingerprint:
  `8a32b9296056d465312ede6cb7de5a8ccf2decc323aa289dbc7b4200ec73afd4`.

## Blind Rhythm-Section Event-Correspondence Hypothesis 02

Status: LOW_RECALL — SCIENTIFIC CONCLUSION FROZEN

- `H-VAL001-RHYTHM-CORRESPONDENCE-02` preserves Hypothesis 01 as a frozen
  negative result and removed exactly its scientifically unjustified
  cross-source signature-equality requirement.
- A candidate still requires mutual unique nearest geometry, valid exact
  two-sided frame signatures independently recurrent at least twice within
  each event's own source, and complete boundary, tie, frame-authority,
  provenance and replay integrity.
- Blind execution froze 13 candidates before Ground Truth access: 12
  Piano–Drums and 1 Double Bass–Drums. Deterministic replay was byte-identical;
  63 relationships remain unresolved.
- Post-freeze scoring reports Piano TP/FP/FN 11/1/25 and Double Bass 1/0/17;
  overall precision is 0.9230769231, recall 0.2222222222 and F1
  0.3582089552. No blind candidate is ambiguous/unscorable.
- Frozen classification: `LOW_RECALL`. The evidence is conservative and
  potentially useful, but production promotion remains unauthorized. No raw
  observation or production behavior changed.
- PI acceptance freezes Hypothesis 02 as a conservative candidate-discovery
  rule, not a complete correspondence model. It demonstrates limited blind
  temporal-comparison discovery but no generalization beyond the controlled
  render.
- Before production promotion may be considered, the unchanged rule requires
  one separately preregistered, checksum-bound, out-of-sample controlled
  validation with blind freeze before Ground Truth reveal, deterministic
  replay, complete provenance, contributor-specific evidence and applicable
  Calibration Zero characterization. A controlled swing/walking-bass render
  is preferred for representative out-of-sample evaluation without assuming
  improved performance.
- No numerical precision threshold is authorized. AD-040 `GEOMETRIC_ONLY`
  remains production authority; candidates remain experimental evidence.
- Blind/result fingerprints:
  `259246226fee627934708eeb9aafc8bd8eb8e3ebbe7340b76935f2a4c0d8b674` /
  `2bf5ddb3c40620c3ddf5ebf8cbf7aad6d6ed74d770481d8eb921b579ad96c082`.
- Preregistration and record:
  `validation/VAL-001/preregistrations/H-VAL001-RHYTHM-CORRESPONDENCE-02.md`,
  `validation/VAL-001/run_20260823_115555/`.
- Frozen conclusion:
  `validation/VAL-001/H-VAL001-RHYTHM-CORRESPONDENCE-02_SCIENTIFIC_CONCLUSION.md`.

## Blind Rhythm-Section Event-Correspondence Experiment

Status: INSUFFICIENT_CANDIDATES

- `H-VAL001-RHYTHM-CORRESPONDENCE-01` executed unchanged against the frozen
  populations of 63 Drums, 27 Double Bass and 49 Piano EME.
- Exact producer round-trip established unique frame authority for every EME.
  The complete blind result and checksum manifest froze before any symbolic
  authority was opened; deterministic replay was byte-identical.
- The frozen rule produced zero blind candidates. All 76 accompaniment
  relationships remain `UNRESOLVED / GEOMETRIC_ONLY`: 27 Double Bass and 49
  Piano. No relation was promoted to `AUTHORIZED_EVENT_RELATION`.
- Post-freeze scoring reports Piano–Drums TP=0, FP=0, FN=36 and Double
  Bass–Drums TP=0, FP=0, FN=18. Overall precision and F1 are undefined and
  recall is 0.0. One Double Bass symbolic relation is unscorable; no blind
  candidate is ambiguous/unscorable.
- Frozen classification: `INSUFFICIENT_CANDIDATES`. Raw observations and all
  AD-038, AD-040 and Calibration Zero authority remain unchanged. Production
  impact is NONE.
- Blind/result fingerprints:
  `7a11a950a60d79f1a75099bdf9e083b7fc35a3f3845d5041304f8ec637c2f3d6` /
  `471664e57ace2a21ffbf6e1a54940bfe773d99f5baa3023eefc3fc1e1a67d045`.
- Record: `validation/VAL-001/run_20260823_111348/`.

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
