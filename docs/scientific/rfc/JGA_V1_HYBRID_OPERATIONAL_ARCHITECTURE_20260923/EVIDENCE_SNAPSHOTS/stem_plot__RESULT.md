# Exactly Like You — full mix versus separated-stem onset geometry

Study: JGA_FULLMIX_VS_STEMS_GEOMETRY_001_20260923. Bounded PI-authorized representation comparison; no operational adoption, runtime modification, commit or push.

## Decision

**Bass observability: COMPLEMENTARY. Drum observability: COMPLEMENTARY. Timing preservation: MIXED. Dual disambiguation: LIMITED. Overall: HYBRID_DIAGNOSTIC_ONLY.** These are qualified engineering interpretations under the prospectively recorded decision rules, not independently verified instrument-identity or physical-attack accuracy claims. Retain the full mix as operational signal authority; stems provide diagnostic evidence only, subject to PI review.

The separated Bass representation adds substantial observable activity, including in the Piano–Bass exchanges where the frozen full-mix source states contain no Bass support. Conversely, 57 Bass-supported and 168 Drum-supported full-mix events have no compatible event in their corresponding stem under the fixed matching rule. More source-labelled activity does not establish better identity accuracy. Separation and the unchanged detector interact to change observability; this experiment cannot isolate waveform suppression from detector response or prove that a missing match represents physical information loss.

## Exact signal and temporal authority

- Original source: `/Volumes/SSD Track/JGA/downloads/Ray Brown Trio - Exactly Like You.m4a`.
- Source SHA-256: `aec97cfb67096bd6a7c3d432f025523d1269b6b261e2dd6bc01a33c045acac45`.
- Domain: **[0,330) seconds**. Excluded ending: [330,347.8117006802721). Complete files were separated/detected before restricting evaluation; no per-section detector restart.
- Shared temporal ruler: the unchanged 905 full-mix PLP references from the operational parent. `PLP_REFERENCE.csv` SHA-256: `b6ed2a669b4e7d9b9fbcdd43618d0c801f5d4bfd60225b54e81415edee8e1666`.
- Operational parent result freeze: `02b603c6c641b6eb6453bcb39362269710be7f58853a99e18be09ba9915fa6ab`.
- Full-mix source-conditioned parent result freeze: `6482feb0820ddd929b292fb4a0393d4f9eebf30e2fe00bcfeb86023de011231e`.
- Existing independent PI form boundaries: Opening [0,48); Piano / walking Bass [48,141); Piano–Bass exchanges [141,186); Piano–Drum exchanges [186,232); Final theme / turnaround [232,330). Their documented approximate-boundary qualification is retained.

No PLP inference, retuning, stem-derived grid, Ableton integration, proximity filter, source-state reassignment or native timestamp alteration was performed.

## Separation, detector and lineage

No reusable Exactly Like You stems with sufficient lineage were found. Six stems were generated once through the existing `AuthorizedDemucsRunner` / `DemucsSeparator.separate_authorized` backend, following AD-041 and the recovered authorized configuration. Only Bass and Drums were analyzed. This is the existing separator, not a model search.

Demucs 4.1.0, `htdemucs_6s`, Python 3.13.14, torch 2.13.0, torchaudio 2.11.0; existing pinned environment `/Users/StarTrack/Development/JGA-Demucs-env`. CPU, shifts=0, overlap=0.25, jobs=0, split enabled, native segment default 39/5; native mean/std normalization and inverse/output handling retained. Float32 WAV with native rescale clipping policy. The cached checkpoint `5c90dfd2.safetensors` hash is `d2a1745f0744721f6b8ca5bf469b67c651ea5ed1b52998cab033b2158609d411`. No model installation, training or tuning.

All six outputs: 44,100 Hz, stereo, 15,338,496 frames, original coordinate origin and length. Backend decoded PCM was exactly equal to the canonical FFmpeg decode when represented as channel-first float32: maximum absolute difference 0; shared array hash `f564ddbdf46bb062cfe1c1f3c33c7906b65528de08f21b7c6c890c0cc167e465`. This establishes input equivalence, not preservation of all separated transients.

External stem directory: `/Volumes/SSD Track/JGA/experiments/JGA_FULLMIX_VS_STEMS_GEOMETRY_001_20260923/stems/`.

| Asset | SHA-256 |
|---|---|
| bass.wav | `8ca185528ce4c50f7a318fb21e9e49ee68b76c7fbede9e7dace5b61120c46952` |
| drums.wav | `88faa9bd504e4253b9e17da5e8ddd3b5fdc310abb542c2ac493a656752546290` |

`SEPARATION_RESULT.json` preserves all six hashes, derived-asset UUIDs and parent lineage. `SOURCE_AUTHORITY.json` explicitly scopes the new authority binding to this study; it does not replace historical source UUIDs.

Both stems used unchanged `src/jga/dsp/onset_detector.py::BasicOnsetDetector.detect`: `librosa.onset.onset_detect(..., units="samples")`, librosa 0.11.0 defaults, 512-sample hop and 2048-sample FFT. Input preparation follows the frozen full-mix analysis procedure: FFmpeg float64 PCM and arithmetic stereo mean, with no additional peak normalization. The same detector was invoked once per complete stem; no source-specific threshold tuning. The frozen 1,606 full-mix events were reused rather than recomputed.

A NumPy integer caused metadata JSON serialization to stop after both complete event CSVs had been written. `recover_metadata.py` recovered metadata from those CSVs and unchanged stem PCM without rerunning either detector. The partial JSON and disclosure remain preserved. This did not change observations, rules or evaluation populations.

## Prospective controls

`PROSPECTIVE_FREEZE.json` precedes separation; `PREREGISTRATION_FREEZE.json` includes the actual stem hashes and precedes detection. `STEM_EVENT_FREEZE.json` precedes comparison, and `COMPARISON_TABLE_FREEZE.json` precedes summary interpretation.

Event matching uses an inclusive **512-sample / 11.609977 ms** compatibility bound, fixed from native detector resolution before outcomes. All full-mix events are compared with each stem separately. A match requires mutual degree one in the complete bipartite compatibility graph. Zero-degree events remain FULL_MIX_ONLY or STEM_ONLY; multiply compatible events would remain AMBIGUOUS_MATCH. No greedy selection, post-hoc tolerance choice, timestamp correction or quarter-proximity filter. Matching is not restricted by quarter-cell membership. All 1,619 observed edges are mutually unique; there are no ambiguous matches in this particular population.

Quarter assignments reuse exact Decimal midpoint boundaries and tie semantics from the parent: earlier reference owns an exact midpoint, nearest eligible timestamp wins, timestamp/ID resolve ties, no borrowing or reuse across cells. Every non-selected stem event remains gray source-shaped CONTEXT.

Stem pairs are resolved only when both selected observations exist and differ by more than 512 samples. Smaller differences, including exact equality, remain unresolved. The 21 inherited full-mix distinct pairs all exceed this resolution (minimum 34.829932 ms), but their identity evidence and population remain different.

## Populations and event matching

| Quantity | Full mix | Bass stem | Drums stem |
|---|---:|---:|---:|
| In-scope native events | 1,606 | 827 | 1,227 |
| Complete-file stem events | — | 841 | 1,234 |
| Source-supported native events, including Dual | Bass 205; Drum 1,091 | separator hypothesis | separator hypothesis |
| Covered quarter cells | Bass 203; Drum 834 | 672 (74.25%) | 868 (95.91%) |
| Source EMPTY cells | Bass 702; Drum 71 | 233 | 37 |
| Stem CONTEXT events | — | 155 | 359 |
| Matches to corresponding full-mix support | — | 148 | 923 |
| Corresponding supported full-mix events unmatched | — | 57 | 168 |
| Stem matches to ANY full-mix state | — | 548 | 1,071 |
| Stem-only, no full-mix event match | — | 279 | 156 |

The two match counts answer different questions. The 148 Bass-related matches comprise 6 Bass-only and 142 Dual; the other Bass-stem matches are 312 Drum-only and 88 UNKNOWN. The 923 Drum-related matches comprise 756 Drum-only and 167 Dual; the other Drum-stem matches are 2 Bass-only and 146 UNKNOWN. Those are timing compatibilities, not new source-identity assignments. Full-mix-only counts against each stem when ALL source states are included are 1,058 and 535 respectively.

## Common-reference geometry

All values below are milliseconds. SD is sample standard deviation; MAD is median absolute deviation from the median. No ON tolerance is introduced.

| Population | N | Median | Mean | IQR | MAD | SD | Median absolute | Range | Negative / positive / zero |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Bass stem − PLP | 672 | +23.22 | +15.03 | 34.83 | 23.22 | 40.98 | 23.22 | −162.54…+174.15 | 149 / 476 / 47 |
| Drums stem − PLP | 868 | +11.61 | +2.92 | 34.83 | 23.22 | 36.70 | 23.22 | −116.10…+69.66 | 272 / 483 / 113 |
| Resolved stem Drum − Bass | 340 | −23.22 | −23.42 | 104.49 | 58.05 | 73.36 | 58.05 | −255.42…+185.76 | 234 / 106 / 0 |

654 cells contain both stem observations; 340 have resolved selected pairs and 314 remain within one hop. The full-mix parent has 201 both-support cells, of which 180 share a Dual winner and only 21 have distinct selected timestamps. Do not treat the 340 stem pairs as 340 independently verified physical pairs.

The unchanged full-mix PRIMARY non-shared observations are Bass N=23, median −34.83 ms (15 negative / 8 positive), Drum N=654, median +11.61 ms (192 negative / 407 positive / 55 zero), and distinct pairs N=21, median Drum−Bass +46.44 ms (14 Bass-first / 7 Drum-first). The full-mix ALL_SUPPORT population including shared Dual is different: Bass N=203, median +11.61 ms (47/129/27), Drum N=834, median +11.61 ms (224/528/82). Both populations and complete descriptive statistics are preserved in the parent snapshots and `STATISTICS.csv`. A difference between these populations is not a measured shift of the same attacks.

PI expectation: **PARTIALLY_REPRODUCED**. Drum-stem observations are positive in 483/868 (55.65%), negative in 272/868 (31.34%), exact in 113/868 (13.02%). Bass-stem observations are positive in 476/672 (70.83%), negative in 149/672 (22.17%), exact in 47/672 (6.99%). Among resolved stem pairs, Drum precedes Bass in 234/340 (68.82%); Bass precedes Drum in 106/340 (31.18%). The negative-Bass / Bass-first tendency of the smaller non-shared full-mix subset is not reproduced. Identity, selection and matching did not use these signs.

## Conditional timing preservation

| Supported match population; full mix minus stem | N | Median | Mean | IQR | MAD | SD | Median absolute | Range | Negative / positive / zero |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Bass-related | 148 | 0 | −0.08 | 0 | 0 | 7.95 | 0 | −11.61…+11.61 | 35 / 34 / 79 |
| Drum-related | 923 | 0 | +2.77 | 11.61 | 0 | 5.87 | 0 | −11.61…+11.61 | 34 / 254 / 635 |

These are **representation-dependent timing displacements**, conditional on matching. The bound truncates the distribution by construction: it cannot establish global timing accuracy or preservation, and larger shifts can become unmatched. The positive Drum mean indicates that matched full-mix landmarks are later on average than the matched stem landmarks, not that one represents the true attack. Equal sample count and decoded input equivalence do not exclude local separation artifacts.

## Dual audit

| Preregistered category | All 180 shared-Dual cells | 135 without distinct supported full-mix alternative |
|---|---:|---:|
| A Bass only | 3 | 3 |
| B Drums only | 18 | 16 |
| C One candidate each, distinguishable | 29 | 20 |
| D One candidate each, unresolved within one hop | 57 | 56 |
| E Neither | 0 | 0 |
| F Both stems present, multiple candidates in either | 73 | 40 |

Category F takes precedence over selected-pair separation; its selected-pair resolution remains in the audit table. A/B describe stem observability, not absence of the other physical instrument. C supplies two model-derived distinguishable landmarks, not proof of two independently identified physical attacks. No original Dual marker was split, reassigned or replaced.

## Sections

Coverage and pair counts use the same independently defined quarter sections. Pair columns use distinct full-mix pairs versus resolved stem pairs, respectively.

| Section | Cells | Bass cells FM → stem | Drum cells FM → stem | Pairs FM → stem | Stem Bass / Drum EMPTY | Stem Bass / Drum / pair median ms |
|---|---:|---:|---:|---:|---|---|
| Opening | 131 | 44 → 87 | 120 → 117 | 7 → 49 | 44 / 14 | +34.83 / +23.22 / −23.22 |
| Piano / walking Bass | 257 | 82 → 221 | 243 → 255 | 7 → 103 | 36 / 2 | +23.22 / +11.61 / −34.83 |
| Piano–Bass exchanges | 125 | 0 → 111 | 113 → 123 | 0 → 70 | 14 / 2 | +23.22 / +23.22 / −23.22 |
| Piano–Drum exchanges | 127 | 8 → 63 | 113 → 114 | 1 → 29 | 64 / 13 | +23.22 / −11.61 / −81.27 |
| Final theme / turnaround | 265 | 69 → 190 | 245 → 259 | 6 → 89 | 75 / 6 | +11.61 / +11.61 / −23.22 |

`SECTION_COMPARISON.csv` and `STATISTICS.csv` contain all per-section counts, unmatched observations and full-mix/stem distribution statistics. Native event section membership uses event time; quarter statistics use reference time. Boundary differences are therefore retained, not forced to reconcile by moving events.

Piano–Bass exchanges: frozen full-mix Bass support is zero. The Bass stem has **159 native onsets, 111 covered cells**, including 113 matches to existing full-mix non-Bass-supported events and 46 stem-only events. This establishes observable candidate activity in an alternate representation where the full-mix identity layer lacks Bass support. It does not independently verify Bass identity, exclude leakage from piano, or decide that every full-mix identity was wrong.

## Figures and semantics

- [Original full-mix source-conditioned whole track, byte-preserved](FULL_MIX_UNCHANGED.png).
- [Separated-stem whole performance](STEMS_WHOLE.png).
- [Aligned full mix versus stems and unmatched-event lanes](FULLMIX_VS_STEMS.png).
- [Dual-region comparison: prospectively selected Opening](DUAL_OPENING_VIEW.png) and [complete categorical audit](DUAL_CATEGORY_AUDIT.png).
- [Piano–Bass exchange comparison](PIANO_BASS_EXCHANGES.png).
- [Established 122–128.5 s reference zoom](REFERENCE_ZOOM.png).

PDF and SVG versions accompany every figure. Source colors/shapes, light-gray context, reference styling and EMPTY rails follow the existing representation. Stem labels explicitly denote separator hypotheses. Raw full-mix PLP inter-peak BPM is unchanged and explicitly labelled discrete/lattice-affected; no smoothing or performer-tempo inference was added. Whole-track plots retain all 2,054 in-scope stem observations, including 514 context events. Original full-mix graph remains unchanged.

## Limits, validation and preservation

This is one extensively studied development recording, not independent corpus validation. No physical ground reference, independently labelled stem accuracy test or perceptual separation-quality review was introduced. Separator leakage, suppression and landmark alteration remain possible. Default onset detection is applied fairly but is not established as source-optimal. Stem labels are not the same evidence as full-mix source-support states. Higher coverage and cleaner labels alone do not justify replacing the original signal authority.

`FINAL_VALIDATION.json`: source and six stem hashes pass; 117 parent/stage-manifest entries pass; all 637 historical preservation hashes pass; all 1,810 stem-cell winners pass independent exhaustive checks; all 1,619 matching edges pass brute-force verification; no cross-cell reuse; original graph bytes preserved. Repository HEAD and worktree path-status agree with the initial inventory. Scientific parent files, current runtime and canonical project state remain unchanged.

The report and new artifacts are sealed by `RESULT_FREEZE.json`. Large stems remain at the recorded external paths; their hashes and full lineage are included rather than duplicating audio into Git. No commit or push.

**Next action (not executed): PI review the diagnostic-complementarity result while retaining full mix as operational authority.**
