# JGA Scientific Evidence Index

Index ID: `JGA-SCIENTIFIC-EVIDENCE-INDEX-001`

Version: `1.0`

Status: **FROZEN CANONICAL PUBLICATION-TRACEABILITY INDEX**

## 1. Purpose, authority, and use

This is the canonical publication-oriented index for the scientific evidence
currently preserved by Jazz Groove Analyzer. It was authorized from the
read-only audit `AUD-JGA-PUBLICATION-EVIDENCE-01`. It creates no scientific
authority, changes no historical classification, and does not replace any
dataset authority, preregistration, execution record, result, fingerprint,
scientific conclusion, or architectural decision.

Use this index to navigate from a bounded claim to immutable evidence. If this
index conflicts with a cited repository artifact, the cited artifact and the
repository knowledge hierarchy prevail; report an Evidence Conflict rather
than repairing history. Descriptive summaries are not promoted to authority.

The governing scientific framework is:

- [Scientific Research Constitution](scientific/JGA_SCIENTIFIC_RESEARCH_CONSTITUTION.md)
- [Development Constitution](JGA_DEVELOPMENT_CONSTITUTION.md)
- [Knowledge Model](scientific/foundations/JGA_KNOWLEDGE_MODEL.md)
- [Scientific Knowledge Record](scientific/foundations/F-030_SCIENTIFIC_KNOWLEDGE_RECORD.md)
- [Scientific Validation Protocol](scientific/JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md)
- [Observation Model](scientific/JGA_OBSERVATION_MODEL.md)
- [Project State](JGA_PROJECT_STATE.md)

### Evidence object types

| Type | Meaning |
|---|---|
| Descriptive documentation | Human-facing account; not sufficient authority by itself. |
| Scientific authority | Prospectively frozen dataset, protocol, Ground Truth, decision, or governing record. |
| Executable/replayable evidence | Preserved method or verifier capable of reconstructing or checking scientific content. |
| Raw experimental evidence | Frozen system output or measurement before scoring/interpretation. |
| Derived result | Deterministic scoring, measurement, comparison, or summary derived from frozen evidence. |
| Scientific interpretation | Bounded conclusion authorized by evidence; never retroactively changes raw evidence. |

### Reproducibility classifications

- `A — PUBLICATION_READY_REPRODUCIBLE`: complete reconstructable authority and evidence chain.
- `B — REPRODUCIBLE_WITH_DOCUMENTATION_GAP`: underlying evidence is reproducible; publication-facing traceability is incomplete.
- `C — PARTIALLY_REPRODUCIBLE`: one or more material reconstruction elements are missing.
- `D — HISTORICAL_EVIDENCE_ONLY`: informative but not completely reproducible from preserved authority/assets.
- `E — INVALIDATED_OR_SUPERSEDED`: not current scientific authority.

Frozen inventory totals: **40 processes: A=14, B=20, C=4, D=1, E=1**.

## 2. Current publication claims

Every claim below is limited by its cited scope and firewall.

| Claim ID | Authorized claim | Class | Primary evidence | Scope and limitations |
|---|---|---:|---|---|
| `CL-JGA-001` | JGA can produce deterministic provenance-bearing temporal observations under the frozen tested inputs. | A/B | [AD-021](architecture/AD-021_COMPLETE_OBSERVATION_MODEL.md), [AD-037](architecture/AD-037_EME_MATERIALIZATION_METRIC_LOCALIZATION.md), modern VAL/CED execution records below | Tested assets/configurations only; not universal detector accuracy. |
| `CL-JGA-002` | AD-037 preserves EME cardinality, identity, source/contributor lineage, and neutral localization from authorized observations. | B/C | [AD-037](architecture/AD-037_EME_MATERIALIZATION_METRIC_LOCALIZATION.md), VAL-001 EME chains below | EME is observable evidence, not symbolic note/beat identity. |
| `CL-JGA-003` | Multiple exact recurrent Candidate Periods coexist in frozen VAL-001/CED-VAL-001 observations before metric interpretation. | B | [`H-VAL001-C1-03`](../validation/VAL-001/run_20260809_100843/), [F-032](scientific/foundations/F-032_CANDIDATE_PERIODS.md) | Does not identify beat, tempo, tactus, meter, or hierarchy. |
| `CL-JGA-004` | Candidate Period discovery is deterministic under the preserved controlled inputs and exact recurrence rule. | B | `C1-03`, `C1-04`, [AD-034](architecture/AD-034_M91_CANDIDATE_PERIOD_REPRESENTATION.md), [AD-035](architecture/AD-035_M92_CANDIDATE_PERIOD_DISCOVERY.md) | Early environment/verification packaging is heterogeneous. |
| `CL-JGA-005` | H02 event-correspondence evidence is experimentally supported and source-sensitive across three controlled datasets. | A | [VAL-001 conclusion](../validation/VAL-001/H-VAL001-RHYTHM-CORRESPONDENCE-02_SCIENTIFIC_CONCLUSION.md), [CED-VAL-002 conclusion](../validation/CED-VAL-002-SWING/H02_OUT_OF_SAMPLE_SCIENTIFIC_CONCLUSION.md), CED-VAL-003 replication below | Controlled datasets only; no production selection/correction authority. |
| `CL-JGA-006` | CED-VAL-004 supports reproducible controlled physical-response measurement and descriptive physical-to-JGA displacement. | A | CED-VAL-004 chains below | Dataset/source-specific; no transferable latency correction. |
| `CL-JGA-007` | JGA supplied the strongest temporal-localization evidence among JGA, librosa, and Essentia in CED-VAL-007 and CED-VAL-008. | A | CED-VAL-007/008 benchmark chains below | Controlled DS-Kick, 44.1 kHz conditions only; no universal superiority. |
| `CL-JGA-008` | CED-VAL-007 preserves reproducible uniform-120-BPM symbolic recovery evidence for all three systems. | A | CED-VAL-007 chain below | One controlled 4/4 uniform-tempo render. |
| `CL-JGA-009` | CED-VAL-008 preserves reproducible four-segment variable-tempo symbolic recovery evidence for all three systems. | A | CED-VAL-008 chain below | One prospectively authored 120/100/140/110-BPM render. |
| `CL-JGA-010` | JGA recovered the CED-VAL-008 nonuniform consecutive-interval structure with the lowest global interval-error RMSE of the three systems. | A | [CED-VAL-008 result](../validation/CED-VAL-008-VARIABLE-TEMPO-BENCHMARK/run_20260825_102058/result.json) | Controlled timeline only; no general tempo-tracking claim. |
| `CL-JGA-011` | JGA had the lowest timing RMSE in all three frozen CED-VAL-008 transition neighborhoods. | A | CED-VAL-008 result/report | T1–T3 only; continuity was recovered by all three systems. |
| `CL-JGA-012` | librosa was the stronger external metric performer in CED-VAL-008, but is not scientifically independent of JGA's librosa-based observation frontend. | A | CED-VAL-008 result; production dependency paths cited below | Metric evidence does not authorize integration or independent validation. |
| `CL-JGA-013` | Essentia supplies a more algorithmically independent comparator, with weaker CED-VAL-008 timing/interval/transition evidence. | A | CED-VAL-007/008 Essentia raw/result records | Independence alone does not establish scientific utility or adapter necessity. |
| `CL-JGA-014` | JGA produces reproducible source-labelled real-audio observations and neutral geometry on frozen distributed-file coordinates. | B | CED-VAL-005/006 profiles below | Acquisition clock/session origin, physical onset, and human microtiming remain unestablished. |
| `CL-JGA-015` | Frozen external-tracker populations can be related reproducibly to JGA Drum observations through neutral geometry. | B | CED-VAL-005/006 geometry chains below | No musical correspondence, correctness, or tracker accuracy follows. |
| `CL-JGA-016` | Calibration experiments characterize bounded measurement behavior without authorizing correction of immutable observations. | A | VAL-001/CED-VAL-002/003/004 calibration chains | Descriptive calibration evidence only; transfer is prohibited. |

### First scientifically usable release traceability addendum

Release `v0.3.0-alpha` packages, without expanding, the evidence-bearing
workflow supporting `CL-JGA-001`, `CL-JGA-002`, and `CL-JGA-014`. Its Python
package version is the PEP 440 equivalent `0.3.0a0`. The release authority and
deterministic verifier are in
[`validation/releases/JGA-v0.3.0-alpha`](../validation/releases/JGA-v0.3.0-alpha/).

The real-audio integration gate is
[`ACC-CEDVAL006-CANONICAL-RHYTHM-SECTION-REPORT-02`](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/acceptance_20260825_113950/),
fingerprint
`ea1490dc0171631381186b6728ee1b49ce5549041c38410b06132d021ee7e100`.
Its predecessor
[`ACC-CEDVAL006-CANONICAL-RHYTHM-SECTION-REPORT-01`](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/acceptance_20260825_112627/)
remains immutable negative evidence of the calibration-provenance and
acquisition-clock-firewall defects; the successful repeat does not erase it.

Release scope remains provenance-bound observation, AD-037 materialization,
AD-038 `GEOMETRIC_ONLY` geometry, AD-040 projection, and deterministic
`JGA_RHYTHM_SECTION_TIMING_REPORT_V1` serialization. The unsupported claims in
Section 10 remain unchanged and bind the release.

Post-release derived-input authority
[`PR-CEDVAL006-CONTROLLED-MIXDOWN-001`](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/controlled_mixdown_authority/)
binds a byte-reproducible controlled mix of all 15 frozen CED-VAL-006 musical
WAV sources. It is a `DETERMINISTIC_CONTROLLED_DERIVED_MIX`, not a provider
mix or Ground Truth. The preceding `MIX_INPUT_AUTHORITY_MISSING` stop remains
valid procedural chronology; no separation or JGA result is created by the
mix authority.

Post-release robustness execution
[`EXEC-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01`](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/separation_robustness_20260825_01/)
characterizes the effect of inserting the frozen Demucs 4.1.0 `htdemucs`
separation path before unchanged JGA `v0.3.0-alpha`. Result fingerprint
`02e2522497ae7ec822b9c176cc45c1c2daeda53872f73a0529039ea174922bba`.
The two separation populations were scientifically nonidentical; both are
preserved and scored without selection, averaging, alignment, or correction.
This is bounded robustness evidence for the derived CED-VAL-006 condition,
not general separator quality, universal JGA robustness, physical-onset
accuracy, or musical correspondence.

## 3. Complete scientific-process inventory

The inventory consolidates repeated executions under their scientific process.
`NOT FOUND` means the audit found no canonical artifact of that kind; it is not
permission to infer one.

| # | Scientific process | Prospective authority / method | Execution / raw / result / replay | Class | Current use or status |
|---:|---|---|---|---:|---|
| 1 | `H-VAL001-C1-03` Candidate Period discovery | Experiment-local protocol in [`run_20260809_100843`](../validation/VAL-001/run_20260809_100843/) | `blind_candidate_discovery.json`, `post_blind_analysis.json`, `manifest.json`, `report.md`; repeated fingerprints | B | Supports `CL-JGA-003/004`. |
| 2 | `H-VAL001-C1-04` relationship audit | [`run_20260809_1344/relationship_audit.py`](../validation/VAL-001/run_20260809_1344/relationship_audit.py) | `blind_relationship_audit.json`, `post_blind_comparison.json`, `manifest.json`, `report.md` | B | No additional dimension shown indispensable. |
| 3 | `H-VAL001-C1-07` cross-condition clarification | Project State/F-032 reference; canonical preregistration `NOT FOUND` | Canonical execution/result path `NOT FOUND`; `HISTORICAL ONLY` | D | Numerical proximity across measurement conditions is insufficient by itself. |
| 4 | `H-VAL001-BEATREF-01` | Historical method `NOT FOUND` | [`run_20260816_171303/result.json`](../validation/VAL-001/run_20260816_171303/result.json), status `FAIL` | E | Failed/superseded; not current BeatReference authority. |
| 5 | Declared-meter vertical slice | Architecture/project-state authority | VAL-001 historical run set; complete modern chain `NOT FOUND` | C | Pipeline validation only. |
| 6 | Declared metric-reference vertical slice | Architecture/project-state authority | VAL-001 historical run set; complete modern chain `NOT FOUND` | C | Pipeline validation only. |
| 7 | Neutral signed EME displacement | Project State; exact preregistration `NOT FOUND` | Historical VAL-001 record; modern verifier `NOT FOUND` | C | Neutral displacement only. |
| 8 | EME cardinality/localization | [AD-037](architecture/AD-037_EME_MATERIALIZATION_METRIC_LOCALIZATION.md) | Historical VAL-001 integration evidence; unified raw/replay bundle `NOT FOUND` | C | Supports part of `CL-JGA-002`. |
| 9 | `H-VAL001-EME-NEUTRAL-01` | Experiment method in run | [`run_20260816_200807`](../validation/VAL-001/run_20260816_200807/) | B | Complete neutral EME timing; no modern verifier. |
| 10 | `H-VAL001-EME-PHASE-01` | [Preregistration](../validation/VAL-001/preregistrations/H-VAL001-EME-PHASE-01.md) | VAL-001 2026-08-16 execution records; canonical mapping via Project State | B | Contributor-separated phase populations only. |
| 11 | `H-VAL001-RHYTHM-TEMPO-01` | [Preregistration](../validation/VAL-001/preregistrations/H-VAL001-RHYTHM-TEMPO-01.md) | VAL-001 2026-08-16 records | B | Recurrent common-period evidence; not tempo authority. |
| 12 | `H-VAL001-RHYTHM-ROLE-01` | [Preregistration](../validation/VAL-001/preregistrations/H-VAL001-RHYTHM-ROLE-01.md) | VAL-001 2026-08-16 records | B | Bounded role discrimination. |
| 13 | `H-VAL001-RHYTHM-STRENGTH-01` | [Preregistration](../validation/VAL-001/preregistrations/H-VAL001-RHYTHM-STRENGTH-01.md) | VAL-001 2026-08-16 records | B | Source-sensitive strength evidence. |
| 14 | `H-VAL001-DRUM-RELATIVE-EME-01` | [Preregistration](../validation/VAL-001/preregistrations/H-VAL001-DRUM-RELATIVE-EME-01.md) | [`run_20260823_060808`](../validation/VAL-001/run_20260823_060808/) | B | Neutral drum-relative geometry. |
| 15 | `H-VAL001-CALIBRATION-ZERO-01` | [Preregistration](../validation/VAL-001/preregistrations/H-VAL001-CALIBRATION-ZERO-01.md) | [`run_20260823_070702`](../validation/VAL-001/run_20260823_070702/) with manifest/verifier/result | A | Mixed measurement behavior; no correction. |
| 16 | `H-VAL001-CALIBRATION-PAIRWISE-01` | [Preregistration](../validation/VAL-001/preregistrations/H-VAL001-CALIBRATION-PAIRWISE-01.md) | [`run_20260823_095617`](../validation/VAL-001/run_20260823_095617/) | A | Pairwise characterization; Voice deferred. |
| 17 | `H-VAL001-RHYTHM-CORRESPONDENCE-01` | [Preregistration](../validation/VAL-001/preregistrations/H-VAL001-RHYTHM-CORRESPONDENCE-01.md) | [`run_20260823_111348`](../validation/VAL-001/run_20260823_111348/) | A | Negative/insufficient candidate evidence preserved. |
| 18 | `H-VAL001-RHYTHM-CORRESPONDENCE-02` | [Preregistration](../validation/VAL-001/preregistrations/H-VAL001-RHYTHM-CORRESPONDENCE-02.md) | [`run_20260823_115555`](../validation/VAL-001/run_20260823_115555/), [conclusion](../validation/VAL-001/H-VAL001-RHYTHM-CORRESPONDENCE-02_SCIENTIFIC_CONCLUSION.md) | A | H02 support remains controlled and source-sensitive. |
| 19 | CED-VAL-002 Calibration Zero | [Preregistration](../validation/CED-VAL-002-SWING/preregistrations/H-CEDVAL002-CALIBRATION-ZERO-01.md), corrected dataset authority | [`run_20260823_170857`](../validation/CED-VAL-002-SWING/run_20260823_170857/) | A | Corrected authority supersedes pre-correction identity. |
| 20 | CED-VAL-002 H02 replication | H02 preregistration above | [`run_20260823_192726`](../validation/CED-VAL-002-SWING/run_20260823_192726/), [conclusion](../validation/CED-VAL-002-SWING/H02_OUT_OF_SAMPLE_SCIENTIFIC_CONCLUSION.md) | A | Independent controlled replication. |
| 21 | CED-VAL-003 Calibration Zero | [Preregistration](../validation/CED-VAL-003-SWING-3-4/preregistrations/H-CEDVAL003-CALIBRATION-ZERO-01.md) | [`run_20260823_203324`](../validation/CED-VAL-003-SWING-3-4/run_20260823_203324/) | A | 3/4 mixed behavior; no correction. |
| 22 | CED-VAL-003 H02 replication | H02 frozen rule | [`run_20260823_204545`](../validation/CED-VAL-003-SWING-3-4/run_20260823_204545/) | A | Third controlled dataset. |
| 23 | CED-VAL-003 strength authority | [Preregistration](../validation/CED-VAL-003-SWING-3-4/preregistrations/H-CEDVAL003-PULSECANDIDATE-STRENGTH-AUTHORITY-01.md) | Later CED-VAL-003 run/Project State; one canonical result link `NOT FOUND` | B | Measurement authority only. |
| 24 | CED-VAL-003 within-cell discriminability | [Preregistration](../validation/CED-VAL-003-SWING-3-4/preregistrations/H-CEDVAL003-WITHIN-CELL-STRENGTH-DISCRIMINABILITY-01.md) | Later CED-VAL-003 run/Project State | B | Cannot establish correspondence. |
| 25 | CED-VAL-003 strength-max validation | [Preregistration](../validation/CED-VAL-003-SWING-3-4/preregistrations/H-CEDVAL003-STRENGTH-MAX-CORRESPONDENCE-VALIDATION-01.md) | Later CED-VAL-003 record/Project State | B | Bounded predictor evidence only. |
| 26 | CED-VAL-003 H02 scorability audit | [Audit protocol](../validation/CED-VAL-003-SWING-3-4/preregistrations/AUD-CEDVAL003-H02-SCORABILITY-01.md) | Later CED-VAL-003 audit record/Project State | B | Cause/limitation audit; does not rescore H02. |
| 27 | CED-VAL-004 physical onset | [Preregistration](../validation/CED-VAL-004-PHYSICAL-ONSET/preregistrations/H-CEDVAL004-PHYSICAL-ONSET-MEASUREMENT-01.md), [input authority](../validation/CED-VAL-004-PHYSICAL-ONSET/input_authority_manifest.json) | [`run_20260824_110800`](../validation/CED-VAL-004-PHYSICAL-ONSET/run_20260824_110800/) | A | Controlled physical authority only. |
| 28 | CED-VAL-004 physical-to-JGA | [Preregistration](../validation/CED-VAL-004-PHYSICAL-ONSET/preregistrations/H-CEDVAL004-PHYSICAL-TO-JGA-COMPARISON-01.md) | [`run_20260824_112730`](../validation/CED-VAL-004-PHYSICAL-ONSET/run_20260824_112730/) | A | Descriptive displacement; no correction. |
| 29 | CED-VAL-004 strength prediction | [Preregistration](../validation/CED-VAL-004-PHYSICAL-ONSET/preregistrations/H-CEDVAL004-PULSECANDIDATE-STRENGTH-PHYSICAL-PREDICTION-01.md) | [`run_20260824_115749`](../validation/CED-VAL-004-PHYSICAL-ONSET/run_20260824_115749/) | A | `INSUFFICIENT_NONVACUOUS_CANDIDATES`. |
| 30 | CED-VAL-005 real-audio profile | [Input authority](../validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/INPUT_AUTHORITY.md), [preregistration](../validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/preregistrations/H-CEDVAL005-REAL-AUDIO-RHYTHM-SECTION-TIMING-PROFILE-01.md) | [`run_20260824_112305`](../validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/run_20260824_112305/) | B | Distributed-file geometry only. |
| 31 | CED-VAL-005 external trackers | [Preregistration](../validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/preregistrations/H-CEDVAL005-EXTERNAL-BEAT-POSITION-FEASIBILITY-01.md) | [`external_beat_benchmark_20260824_164758`](../validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/external_beat_benchmark_20260824_164758/) | B | No Ground Truth/tracker accuracy claim. |
| 32 | CED-VAL-005 external/JGA geometry | [Preregistration](../validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/preregistrations/H-CEDVAL005-EXTERNAL-BEAT-TO-JGA-DRUMS-GEOMETRY-01.md) | [`external_beat_jga_geometry_20260824_170946`](../validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/external_beat_jga_geometry_20260824_170946/) | B | Neutral geometry, not correspondence. |
| 33 | CED-VAL-005 visualization | [Preregistration](../validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/preregistrations/H-CEDVAL005-FIVE-WINDOW-LOCAL-NEUTRAL-VISUALIZATION-01.md) | [`local_visualizations_20260824_160657`](../validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/local_visualizations_20260824_160657/) | B | Presentation evidence only. |
| 34 | CED-VAL-006 real-live profile | [Input authority](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/INPUT_AUTHORITY.md), [preregistration](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/preregistrations/H-CEDVAL006-REAL-LIVE-AUDIO-RHYTHM-SECTION-TIMING-PROFILE-01.md) | [`run_20260824_183919`](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/run_20260824_183919/) | B | Acquisition clock/origin partial. |
| 35 | CED-VAL-006 external trackers | [Preregistration](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/preregistrations/H-CEDVAL006-EXTERNAL-BEAT-POSITION-FEASIBILITY-01.md) | [`external_beat_benchmark_20260824_191341`](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/external_beat_benchmark_20260824_191341/) | B | No Ground Truth/tracker accuracy claim. |
| 36 | CED-VAL-006 external/JGA geometry | [Preregistration](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/preregistrations/H-CEDVAL006-EXTERNAL-BEAT-TO-JGA-DRUMS-GEOMETRY-01.md) | [`external_beat_jga_geometry_20260824_193151`](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/external_beat_jga_geometry_20260824_193151/) | B | Neutral geometry only. |
| 37 | CED-VAL-006 visualization | [Preregistration](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/preregistrations/H-CEDVAL006-FIVE-WINDOW-LOCAL-NEUTRAL-VISUALIZATION-01.md) | [`local_visualizations_20260824_185658`](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/local_visualizations_20260824_185658/) | B | Presentation evidence only. |
| 38 | CED-VAL-007 rendered response | [Preregistration](../validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/preregistrations/H-CEDVAL007-RENDERED-RESPONSE-MEASUREMENT-01.md) | [`run_20260824_210717`](../validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/run_20260824_210717/) | A | Dataset-specific rendered response. |
| 39 | CED-VAL-007 three-system benchmark | [Preregistration](../validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/preregistrations/H-CEDVAL007-THREE-SYSTEM-SYMBOLIC-BEAT-RECOVERY-01.md) | [`run_20260824_212203`](../validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/run_20260824_212203/) | A | Uniform controlled benchmark. |
| 40 | CED-VAL-008 three-system benchmark | [Preregistration](../validation/CED-VAL-008-VARIABLE-TEMPO-BENCHMARK/preregistrations/H-CEDVAL008-THREE-SYSTEM-VARIABLE-TEMPO-SYMBOLIC-BEAT-RECOVERY-01.md) | [`run_20260825_102058`](../validation/CED-VAL-008-VARIABLE-TEMPO-BENCHMARK/run_20260825_102058/) | A | Variable-tempo controlled benchmark. |

## 4. Candidate Period evidence chain

### Scientific authority

- Theory: [F-031](scientific/foundations/F-031_HIERARCHICAL_METRIC_PERIODICITY.md) and [F-032](scientific/foundations/F-032_CANDIDATE_PERIODS.md).
- Representation: [AD-034](architecture/AD-034_M91_CANDIDATE_PERIOD_REPRESENTATION.md).
- Production discovery rule: [AD-035](architecture/AD-035_M92_CANDIDATE_PERIOD_DISCOVERY.md).
- Completion review: [Phase II Validation Block 1](scientific/PHASE_II_VALIDATION_BLOCK_1_COMPLETION_REPORT.md).

### Experiment chains

- `H-VAL001-C1-03`: blind Candidate Population and fingerprint were frozen
  before GT access. The run preserves method, raw blind JSON, post-blind
  comparison, report and manifest. Classification B.
- `H-VAL001-C1-04`: consumes the frozen C1-03 record, preserves its own blind
  relationship audit, repeated fingerprints and post-blind comparison.
  Classification B.
- `H-VAL001-C1-07`: referenced by F-032/Project State for the narrow
  cross-condition non-equivalence clarification. Canonical protocol/execution
  linkage is `NOT FOUND`; classification `D — HISTORICAL_EVIDENCE_ONLY`.
- `H-VAL001-RHYTHM-TEMPO-01`, `RHYTHM-ROLE-01`, and
  `RHYTHM-STRENGTH-01`: prospective protocols and deterministic evidence are
  preserved, but publication cross-links and early environment authority are
  incomplete; classification B.

Authorized claims are limited to reproducible pre-interpretive recurrence,
coexisting Candidate Periods, complete occurrence/provenance preservation,
and bounded role/strength evidence. Candidate identity does not establish
beat, BPM, tempo, meter, tactus, subdivision, hierarchy, or musical function.

## 5. EME evidence chain

The canonical order is:

```text
source observation
→ authorized AD-037 materialization
→ immutable EME identity/cardinality/lineage
→ neutral metric or drum-relative geometry
→ separately authorized correspondence
→ future interpretation
```

The stages must not be collapsed. [AD-037](architecture/AD-037_EME_MATERIALIZATION_METRIC_LOCALIZATION.md)
preserves EME existence independently of localization. [AD-038](architecture/AD-038_DRUM_RELATIVE_EME_LOCALIZATION.md)
defines neutral drum-relative localization. [AD-040](architecture/AD-040_RHYTHM_SECTION_TIMING_PROFILE.md)
defines a downstream read-only profile. H01/H02 are separate correspondence
experiments and do not retroactively redefine observation or materialization.

Primary records are processes 7–18 in the inventory. The strongest modern
chains are the calibration and correspondence runs from 2026-08-23. Older
cardinality/displacement and phase records remain valid within their frozen
scope but carry C/B documentation classifications. No EME result authorizes
symbolic note identity, beat identity, groove quality, intention, or removal
of observations.

## 6. Controlled validation evidence

### CED-VAL-007 — uniform-tempo benchmark

- Dataset authority: `PR-CED-VAL-007-CONTROLLED-BEAT-BENCHMARK-001` in
  [INPUT_AUTHORITY.md](../validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/INPUT_AUTHORITY.md)
  and [manifest](../validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/input_authority_manifest.json).
- Dataset fingerprint: `cd93455778d1484067f9a3caa3037b6467d27c7e8d5a8c0df694658bad2484e9`.
- Symbolic GT: [symbolic_beat_reference.json](../validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/symbolic_beat_reference.json), 64 events at 120 BPM; frozen independently of systems.
- Rendered response: preregistration and [`run_20260824_210717`](../validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/run_20260824_210717/); this authority is separate and not a general latency correction.
- Three-system preregistration: [`H-CEDVAL007-THREE-SYSTEM-SYMBOLIC-BEAT-RECOVERY-01`](../validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/preregistrations/H-CEDVAL007-THREE-SYSTEM-SYMBOLIC-BEAT-RECOVERY-01.md).
- Blind raw authority: [`raw_system_output_authority.json`](../validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/run_20260824_212203/raw_system_output_authority.json).
- JGA/librosa/Essentia raw evidence: the three `*_raw_output.json` files in
  [`run_20260824_212203`](../validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/run_20260824_212203/).
- Execution/scoring/replay: `execute.py`, three runner scripts, `score.py`,
  `verify.py`, artifact/completion manifests and scientific content in that run.
- Result: [result.json](../validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/run_20260824_212203/result.json).
- Combined fingerprint: `637c3898f9607f60cabbb43aeabd26383aacf216e475007e79ce07da5848d2a0`.
- Result commit: `75bc1c5b0a27bb04d958f4f68957e1e538fb83ce`.

Authorized result: JGA 63/64, librosa 62/64, Essentia 63/64; JGA had the
lowest median absolute timing error and RMSE. Scope is one controlled DS-Kick,
4/4, 120-BPM, 44.1-kHz render. No universal tracker, jazz, physical-onset, or
adapter claim follows.

### CED-VAL-008 — variable-tempo benchmark

- Dataset authority: `PR-CED-VAL-008-VARIABLE-TEMPO-BENCHMARK-001` in
  [INPUT_AUTHORITY.md](../validation/CED-VAL-008-VARIABLE-TEMPO-BENCHMARK/INPUT_AUTHORITY.md)
  and [manifest](../validation/CED-VAL-008-VARIABLE-TEMPO-BENCHMARK/input_authority_manifest.json).
- Authority commit: `241f4909b265fdf3ca81e9c6c305dfae567c0047`.
- Filename provenance: the earlier one-space transcription is
  `SUPERSEDED_DESCRIPTIVE_FILENAME_DECLARATION`; exact checksum-bound names
  contain two spaces after `v0.1` and are `AUTHORITATIVE_RAW_ASSET_IDENTITIES`.
  The manifest preserves both the superseded names and PI adjudication.
- DRUM SHA-256: `cfeb385ab00320f654453a1ff64c6dce9d1d0e80c2008dade847df671a744848`.
- Canonical Live Set SHA-256:
  `c15a80ac9fa04d52d49f09bd91f905d25012b50f36e904da1c047aabfa9c8288`.
- Dataset fingerprint: `9aab028fb1ac6740f1e257d0254afea485225879be888d0e4b60c20ba46ee86d`.
- Exact rational GT: [symbolic_beat_reference.json](../validation/CED-VAL-008-VARIABLE-TEMPO-BENCHMARK/symbolic_beat_reference.json), 64 events across 120/100/140/110 BPM; rational non-integer sample coordinates remain unrounded.
- Preregistration: [`H-CEDVAL008-THREE-SYSTEM-VARIABLE-TEMPO-SYMBOLIC-BEAT-RECOVERY-01`](../validation/CED-VAL-008-VARIABLE-TEMPO-BENCHMARK/preregistrations/H-CEDVAL008-THREE-SYSTEM-VARIABLE-TEMPO-SYMBOLIC-BEAT-RECOVERY-01.md), commit `e5ecfa8676f62b773b2fde07c9d69cf9d4dcc777`.
- Shared mono authority: `shared_mono.npy` and `shared_mono_manifest.json` in
  [`run_20260825_102058`](../validation/CED-VAL-008-VARIABLE-TEMPO-BENCHMARK/run_20260825_102058/), raw-byte SHA-256
  `d7fd7083fdbb81642675499f83510582d5ee57438a812501abab4edd167e3660`.
- Blind freeze: `blind_raw_freeze_manifest.json`, fingerprint
  `8faeac955645a2345ef9c67c21725931605c6d22b40adba5b8302eccaccfe176`.
- Raw evidence: two fresh-process outputs and one frozen raw output per system.
- Scoring: `score.py`, two score records, `scoring_replay.json`, and
  [result.json](../validation/CED-VAL-008-VARIABLE-TEMPO-BENCHMARK/run_20260825_102058/result.json).
- Analyses: global recovery/timing, S1–S4, T1–T3, complete consecutive
  intervals, and four frozen post-change intervals per transition.
- Verification: run `verify.py`, artifact manifest, completion protocol;
  exact raw and scoring replay passed.
- Combined fingerprint: `0118157aceb2effcd8655f3ab29e314c01f92fd80152b3fead7c882acb13880b`.
- Result commit: `054d2b6734ec3c01a3bc3882ed740dc52daafa59`.

Authorized result: all systems matched 63/64; JGA/librosa had no extras and
Essentia had one. JGA led global localization, global interval RMSE, all four
segment timing RMSE values, and all three transition RMSE values. librosa led
the external metrics but shares algorithmic/frontend lineage with JGA.
Essentia is more independent but less reliable in this controlled result.

The subsequent read-only review concluded `DO_NOT_IMPLEMENT` for an External
Temporal Reference Adapter because no external system demonstrated necessary
information unavailable from existing JGA evidence. Repository artifact for
that review: `NOT FOUND`; it is PI review evidence, not historical experiment
authority, and must not be cited as a frozen repository decision without a
separately authorized addendum.

## 7. Real-audio evidence and external assets

### CED-VAL-005

- Dataset: Cambridge Music Technology / Mixing Secrets full multitrack,
  Maurizio Pagnutti Sextet, “All The Gin Is Gone.”
- Authority: [`PR-CED-VAL-005-REAL-JAZZ-MULTITRACK-001`](../validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/INPUT_AUTHORITY.md).
- Manifest/fingerprint: [input_authority_manifest.json](../validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/input_authority_manifest.json),
  `d9d6341f837bc5f56054ffd6c91f6be65a7bdbb8043526a9ac70d924a81335af`.
- Assets: 16 checksum-bound 24-bit/44.1-kHz WAVs with technical scope and
  source labels. Analytical inputs are separately frozen.
- Rights: educational-use restrictions; commercial use requires permission.
- Provider/source reference and supplied Readme are recorded by the authority.
- Authorized coordinate: immutable distributed-file sample coordinate only.
- Unestablished: common acquisition system/clock, simultaneous capture,
  editing history, physical onset, exact common session/export origin.
- Evidence: processes 30–33; all preserve scripts, outputs, manifests,
  fingerprints, replay, reports and firewalls.

### CED-VAL-006

- Dataset: LEWITT COSMIX real live multitrack.
- Authority: [`PR-CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK-001`](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/INPUT_AUTHORITY.md).
- Manifest/fingerprint: [input_authority_manifest.json](../validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/input_authority_manifest.json),
  `9d837f710fbf3292c80490d499bc96df0a8fe1140bc9139b65de8a553c4c2eca`.
- Assets: 15 checksum-bound 24-bit/48-kHz WAVs, checksum-bound video and rights
  PDF; provider page and technical roles are recorded.
- Rights: supplied exploitation-rights PDF restricts commercial use and
  requires attribution for publication/public release.
- Authority classification: `ACQUISITION_AUTHORITY_PARTIAL`.
- Authorized coordinate: immutable per-file/distributed coordinate; Drum and
  Bass selected assets share distributed scope.
- Unestablished: recorder/routing authority, hardware clock, exact common
  session/file origin, exhaustive timing-process history and physical onset.
- Evidence: processes 34–37 with deterministic manifests/replay.

Machine-specific `/Volumes/...` paths are operational locations, not
publication identities. Publication identity is dataset ID + exact asset name
+ checksum + technical role + manifest fingerprint + provider/rights record.
Do not copy or redistribute externally licensed assets through this index.

## 8. Comparative external-system evidence and environment

JGA production uses librosa for audio loading, onset detection/onset strength,
and frame/time conversion, including:

- [`file_audio_source.py`](../src/jga/audio/file_audio_source.py)
- [`pulse_candidate_builder.py`](../src/jga/engines/pulse_candidate_builder.py)
- [`source_pulse_candidate_builder.py`](../src/jga/engines/source_pulse_candidate_builder.py)

JGA does not call `librosa.beat_track`, but shared implementation lineage means
librosa beat tracking cannot independently validate JGA. Essentia remains the
more independent comparator. This dependency caveat never changes scoring.

Material modern environment authority includes:

- `librosa==0.11.0` for CED-VAL-007/008 external baselines;
- `essentia==2.1b6.dev1389`;
- Essentia wheel SHA-256
  `84e5167b95d9e74b2ddd928555d5a1e11997a458dae25e653544a953bc3068b9`;
- Python, platform/architecture and NumPy versions in raw-output records;
- CPU and declared single-thread limits for Essentia where preregistered;
- exact runner call/configuration and package/callable provenance;
- JGA/result commits cited by the modern records.

Early VAL-001 records do not consistently preserve a complete environment
lock, JGA commit, or standalone verifier. Those omissions are documentation
gaps and must not be silently filled from a later environment.

## 9. Negative, falsification, and supersession record

| Record | Preserved consequence |
|---|---|
| `H-VAL001-BEATREF-01` failure | Failed result remains E-class evidence; it is not current BeatReference authority. |
| H01 insufficient candidates | Negative outcome constrained H02 methodology; candidates were not manufactured. |
| Source-sensitive H02 | H02 is not universal; source and dataset scope remain mandatory. |
| Mixed Calibration Zero behavior | No correction, normalization, or universal bias was authorized. |
| CED-VAL-002 pre-correction authority | Superseded by checksum-bound corrected authority; historical identity remains visible. |
| CED-VAL-003 ambiguous physical authority | Evidence gap was frozen; symbolic proximity and strength cannot manufacture physical authority. |
| CED-VAL-003 scorability/strength limitations | Strength evidence cannot select correspondence or rescore historical H02. |
| CED-VAL-004 strength prediction | `INSUFFICIENT_NONVACUOUS_CANDIDATES`; singleton cells are not predictor successes. |
| CED-VAL-005/006 acquisition limitations | Common distributed scope does not establish acquisition clock, origin, or human microtiming. |
| CED-VAL-008 filename conflict | One-space transcription superseded; exact two-space identities accepted prospectively without changing assets/checksums. |
| Calibration transfer rejection | No CED-VAL-004/007 response or latency constant transfers to another dataset. |
| External adapter rejection | Read-only review evidence found no demonstrated implementation necessity; repository authority addendum `NOT FOUND`. |

Negative evidence is part of the scientific record and must be cited when it
constrains a claim. New addenda may reference it; historical records must not
be rewritten.

## 10. Unsupported and forbidden claims

| Unsupported claim | Evidence preventing or limiting it |
|---|---|
| Universal JGA/librosa/Essentia superiority | CED-VAL-007/008 are two controlled DS-Kick configurations only. |
| Real-jazz beat-tracking accuracy | CED-VAL-005/006 have no symbolic or physical beat Ground Truth. |
| Human microtiming | Real-audio acquisition clock/session origin and physical onset are unestablished. |
| Swing or groove interpretation | Controlled/real-audio results preserve neutral timing evidence only. |
| Rushing or dragging | No authorized musical correspondence or performance-intention model. |
| Intention | Audio observation cannot establish performer intent. |
| Universal physical-onset accuracy | CED-VAL-004 onset authority is source/dataset/protocol-specific. |
| Transferable latency correction | Calibration/response results explicitly prohibit numerical transfer. |
| Acquisition-clock correspondence for CED-VAL-005/006 | Equal distributed-file scope is insufficient; required acquisition authority is partial/unestablished. |
| Universal sample-rate invariance | Evidence preserves explicit frame/rate conditions; no universal invariance protocol/result exists. |
| Universal tempo, meter, or downbeat recovery | Benchmarks test bounded quarter-note schedules and do not validate universal metric interpretation. |
| Strength as a general correspondence selector | CED-VAL-003/004 negative and insufficient evidence prevents promotion. |
| Production necessity of an External Temporal Reference Adapter | External systems supplied no demonstrated indispensable mission capability; the review is not a frozen experiment authority. |

## 11. Supersession and authority notes

- Historical artifact status is determined by the cited record, Project State,
  and governing decisions—not by this index.
- AD-037 supersedes the movement-dependent portions of historical AD-018 while
  preserving its observation/interpretation distinction.
- CED-VAL-002 corrected input authority supersedes the pre-correction dataset
  identity for current evidence.
- CED-VAL-008's PI adjudication supersedes only the descriptive one-space
  filename transcription, not any physical asset or checksum.
- `H-VAL001-C1-07` remains `HISTORICAL ONLY` until a new provenance-bearing
  addendum identifies its immutable chain; this index does not repair it.
- Missing values remain `NOT FOUND` or `UNKNOWN`; later assumptions must not be
  backfilled into historical authority.

## 12. Publication reproduction-bundle status

### Preserved unresolved documentation gaps

The index makes these gaps visible but does not repair or reinterpret their
historical evidence:

1. `H-VAL001-C1-07` has no located canonical preregistration/execution chain.
2. The early declared-meter and declared-reference vertical slices lack a
   complete modern raw/replay package.
3. Early neutral EME displacement/cardinality evidence lacks one unified
   raw-output and replay bundle.
4. Early VAL-001 processes do not consistently preserve complete environment
   locks, JGA commits, or standalone verifiers.
5. Several later CED-VAL-003 strength/audit processes are recoverable through
   Project State and run ordering but lack direct canonical result cross-links.
6. External assets have checksum-bearing identities, but durable archival or
   reacquisition references are not yet centralized for publication.
7. The CED-VAL-007/008 adapter review is preserved in PI review history, while
   a frozen repository review artifact is `NOT FOUND`.

These are **seven** documentation gaps. None authorizes a stronger claim or
requires alteration of historical authority.

Status: **RECOMMENDED FOR FUTURE PUBLICATION PREPARATION — NOT YET BUILT**.

The minimum future bundle should contain:

1. this canonical evidence index;
2. cited preregistrations and authority manifests;
3. cited execution, scoring and verifier scripts;
4. immutable raw/scientific-content records;
5. result, artifact and fingerprint manifests;
6. exact cited repository commits;
7. minimal material environment locks;
8. external dataset checksums and obtain/verification instructions; and
9. this claim firewall, negative-evidence and supersession record.

Repository-publishable materials include documentation, manifests, checksums,
scripts, numerical records and results subject to repository rights. Large or
licensed raw assets require durable external archival storage or authoritative
reacquisition instructions; CED-VAL-005/006 assets must not be redistributed
without their applicable permissions.

## 13. Index verification policy

A separate index verifier is intentionally not introduced. The index is one
additive Markdown navigation artifact; a dedicated parser would create a
second representation requiring synchronized maintenance. Before freezing a
revision, use read-only repository checks to require:

- all Markdown-linked repository paths exist;
- the inventory has exactly 40 unique numbered processes;
- classifications total A=14, B=20, C=4, D=1, E=1;
- the claim matrix contains exactly 16 current claims;
- the forbidden-claim table contains exactly 13 entries;
- cited commits resolve;
- CED-VAL-007 result fingerprint equals
  `637c3898f9607f60cabbb43aeabd26383aacf216e475007e79ce07da5848d2a0`;
- CED-VAL-008 result fingerprint equals
  `0118157aceb2effcd8655f3ab29e314c01f92fd80152b3fead7c882acb13880b`;
- staged changes contain only this index; and
- no historical artifact, production file, manifest, result, fingerprint, or
  raw asset changed.

Publication traceability is sufficient to resume the Candidate Period/main
JGA completion path once these checks and the isolated index commit pass.
