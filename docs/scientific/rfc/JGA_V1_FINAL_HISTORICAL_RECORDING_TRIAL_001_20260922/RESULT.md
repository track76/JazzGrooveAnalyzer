# JGA v1 final historical-recording trial

**Target: Ray Brown Trio — Exactly Like You. Engineering assessment: PARTIALLY_USABLE.**

This completed trial assembles frozen research evidence; it does not deploy a new production runtime. It is scientifically useful for reproducible exploratory source-associated marker geometry and limited exposed-Drum acoustic timing. It does not yet establish general Bass–Drum performer microtiming.

## Authority and scope

Source SHA-256 `aec97cfb67096bd6a7c3d432f025523d1269b6b261e2dd6bc01a33c045acac45`. Original full mix remains signal authority; no new decode, inference, source separation, PLP retuning or attack detector. Analyze [0,330) s; exclude [330,347.8117006802721) s using existing PI M7 stop/phrase/ending annotation. Boundaries are approximate whole seconds, not inferred from offsets.

PLP B3 output freeze `4384911f6086ba8a1a6f9deaa8370ae9ba22f6339ae42b3b0b4a015204efa7ac` is reused unchanged. Its inter-maximum interval supplies BPM context. Nearest stored maximum is an operational reference coordinate, not independently verified intended beat for every event. No reference extrapolation. Historical independent PLP FAIL remains unchanged; development 5/5 is not independent corpus evidence. The rejected proximity prior is not used.

## Population and uncertainty

Native frozen 1627; included 1606; excluded 21. Disjoint source states: {'BASS_AND_DRUM_SUPPORTED': 196, 'DRUM_SUPPORTED': 895, 'UNKNOWN': 506, 'BASS_SUPPORTED': 9}. Bass-inclusive 205, Drum-inclusive 1091; both include shared dual markers and must not be summed as independent attacks.

Qualified acoustic estimates: 9 Drum; one abstention among ten historical attempts. Bass: zero qualified full-mix attack estimates. Other markers are not counted as failed estimator trials: refinement was never applied to them. Numerical uncertainty is unquantified for native attacks and PLP phase; no ±hop or fabricated HIGH-confidence bounds. Original Drum visual intervals are shown as qualified acoustic bounds, not calibrated physical confidence intervals.

PLP maxima in scope 905; inter-peak coverage 329.930340 s; leading unbracketed 0.069660 s. Duration-weighted BPM median 161.50, Q1 161.50, Q3 172.27; unsmoothed interval range 152.00–172.27. Extremes are algorithmic inter-peak observations, not automatically genuine performance accelerations.

## Section readout

| Section | Native | Bass incl. | Drum incl. | Dual | Unknown | Weighted BPM |
|---|---:|---:|---:|---:|---:|---:|
| M1: Opening / solo-launch transition | 252 | 44 | 162 | 40 | 86 | 161.50 |
| M2: Piano solo / walking Bass | 435 | 83 | 313 | 81 | 120 | 161.50 |
| M3: Piano-Bass exchanges | 251 | 0 | 149 | 0 | 102 | 161.50 |
| M4: Piano-Drum exchanges | 207 | 8 | 164 | 8 | 43 | 161.50 |
| M56: Final theme / turnaround / crescendo | 461 | 70 | 303 | 67 | 155 | 161.50 |

## Timing distributions

Full N/coverage/median/mean/IQR/MAD/sample SD/median absolute/range are in TIMING_STATISTICS.csv, separately by marker state, overlapping source group, section and refined acoustic estimates. Values below are descriptive offsets, not signed physical performer judgments.

| Category | N | Median ms | Mean ms | IQR ms | MAD ms | SD ms | Median abs ms | Range ms |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| BASS_INCLUSIVE | 205 | 11.61 | 9.34 | 34.83 | 23.22 | 33.50 | 23.22 | -116.10 to 69.66 |
| DRUM_INCLUSIVE | 1091 | 11.61 | 0.84 | 69.66 | 23.22 | 50.60 | 34.83 | -174.15 to 197.37 |
| REFINED_DRUM | 9 | -54.33 | -34.11 | 41.27 | 28.57 | 74.31 | 65.85 | -111.38 to 141.77 |

## Ahead/on/behind and pairwise boundary

Qualified Drum interval signs relative to a fixed numerical PLP coordinate: {'AHEAD_OF_FIXED_PLP_COORDINATE': 7, 'BEHIND_FIXED_PLP_COORDINATE': 2}. This does not establish intended-beat assignment or physical performer ahead/behind. Native markers cannot receive a defensible performer sign from unquantified attack uncertainty. Zero line denotes a reference coordinate, not a target to attract events to.

Independent Bass–Drum attack pairs: 0. Distinct single-source-support co-covered reference cells: 7; these do not justify an arbitrary one-to-one attack pairing. Dual support is one marker, never evidence for zero Bass–Drum delay. No Ride/Hi-Hat relationships or kit-component accuracy inferred from generic Drum.

## What the graphs mean

[Whole performance](WHOLE_PERFORMANCE.png) and [03:36–03:40 zoom](ZOOM_REFERENCE.png) are also provided as PDF/SVG. Colored observations are source-associated markers with categorical, provisional source support. Shared dual markers are crosses. Black diamonds and vertical bounds show the separately preserved Drum acoustic estimates and reviewed intervals. No artificial attack-error bars on native markers; missing confidence remains missing. Large offsets in fills can denote subdivisions or nearest-reference assignment, not performer lateness.

## Scientific usefulness and single blocker

Reliable computational measurements: frozen event coordinates, source-evidence provenance, pulse coordinates, their arithmetic relations, coverage and section assignment under the supplied form map. Qualified estimates: provisional Bass/Drum-associated geometry and the nine exposed sharp-Drum acoustic landmarks. These permit auditable musical hypotheses about changing texture and temporal organization, not a causal or physical groove verdict.

The single material blocker is **transferable source-associated full-mix attack-timing qualification, most decisively Double Bass**. This does not require fictional sample-perfect truth: sufficiently justified categorical or bounded timing evidence would suffice. Current markers lack that qualification. Thus an operational freeze claiming completed historical Bass–Drum microtiming is not justified by this trial. No new detector or model search follows automatically.

Exactly Like You is heavily exposed development material. Native detection, source associations, acoustic reference reviews and PLP listening all have recorded reuse limitations. Native sampling lattices, model neighborhood support, sparse Bass coverage, review anchoring, unquantified reference phase and nearest-peak assignment limit interpretation. Descriptive means/quantiles are not significance tests, listener validation or corpus generalization.

Next action: PI review of the completed trial and its single attack-timing qualification blocker. No further experiment executed.

## Section interpretation and execution validation

The Piano–Bass exchange section (141–186 s) contains **zero Bass-supported markers despite its independent form label**. This is a source-evidence coverage gap, not evidence that Bass is absent. Of 205 Bass-inclusive markers, 196 are dual-support; only nine are Bass-only. Drum support covers 1,091/1,606 native events (67.93%); Bass support 205/1,606 (12.76%); UNKNOWN 506/1,606 (31.51%). These denominators are native observables, not all musical attacks, so they are not musical recall. The nine qualified acoustic estimates all lie in the Piano–Drum section. No section supports a general physical Bass–Drum lag verdict.

All five section duration-weighted inter-peak BPM medians are about 161.50. This does not imply constant tempo: the unchanged 512/22050-second PLP timestamp lattice yields discrete neighboring interval rates near 152.00, 161.50 and 172.27 BPM. Alternation between them must not be interpreted as instantaneous performer accelerations. Marker displacement also retains detector/reference sampling structure.

Independent validation checks original timestamps/states, byte-identical snapshots, 637 historical preservation entries, nearest-peak assignments using a separate bisect implementation, original acoustic estimates, and summary statistics. Both PNG figures were visually inspected: labels, zero coordinates, marker/refined distinction and review bounds are visible. No synthetic numerical uncertainty is added.

The initial readout failed only on JSON serialization of a NumPy scalar. FAILED_SERIALIZATION_RUN preserves its incomplete summary and completed tables. The frozen trial.py remains unchanged; run_readout.py adds scalar serialization only. All six completed CSV tables match the recovered run byte-for-byte. No parameter or scientific rule changed. Reproduction should use a fresh copy of the input/configuration package and the serialization adapter; scripts intentionally refuse to overwrite existing results.
