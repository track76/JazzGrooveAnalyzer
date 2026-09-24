# Native Basic Pitch onset vs human GT — Gallegati 120

**Decision: native BP onset is NOT suitable as a general JGA Bass microtiming landmark on this evidence.**

Target: channel-specific observable onset in Fishman Full Circle; NOT physical string-release Ground Truth. Human annotation interface used 1 ms steps; decimal coordinates do not imply sub-millisecond human accuracy.

## Evidence and procedure

Both supplied GT/freeze hashes and all 12 original source hashes verified. Existing BP evidence covers 36 isolated excerpts, not these complete takes. Official Basic Pitch 0.4.0 bundled ICASSP 2022 CoreML model ran with documented defaults on all 12 complete WAVs. Opaque byte-identical audio copies were the only inference inputs. Filesystem isolation denied repository references and /Volumes; a Python audit hook provided a second guard. Native model arrays, MIDI and all 760 note hypotheses were saved and hashed before GT comparison. Model, defaults, source and output hashes are preserved in PHASE0_AUDIT.json and inference/output/.

The CoreML runtime emitted optional-backend/conversion warnings and a cache-cleanup permission warning. All 12 outputs completed, were finite, and passed saved-hash verification; no fallback model or changed settings were used.

MATCHING_PROTOCOL.json was saved before inference and GT-center inspection. Chronological territories use midpoints between adjacent human events. Candidates must begin in that territory and persist to the human earliest plausible bound. Expected pitch has priority, then octave equivalence, then other pitch. More than one candidate in the highest available tier remains unresolved; no nearest-error, amplitude or duration ranking. This is reference-assisted correspondence, not an autonomous note selector. Persistence filtering excludes pre-attack-ending fragments and can condition the timing distribution; it does not validate those discarded fragments as nonphysical events.

## Recognition and matching

120 GT events; 107 unique correct-pitch matches; 0 octave-equivalent; 0 wrong-pitch; 13 multiple-candidate events; 0 missed under this association rule. Expected pitch appears in all 120 association sets.

760 native hypotheses = 107 selected + 26 highest-tier hypotheses in 13 ambiguous events + 347 other associated hypotheses + 280 unassociated additional hypotheses. Additional hypotheses are not automatically false physical notes. No raw prediction was deleted. Timing statistics exclude the 13 ambiguous events and therefore are conditional on defensible matching, not 120-event accuracy.

## Raw timing, N=107

- N: 107
- median_signed_ms: -3.9217687074852847
- mean_signed_ms: -1.243878610634649
- median_absolute_ms: 13.221995464846259
- IQR_signed_ms: 25.597392290228616
- P95_absolute_ms: 56.87746031746016
- maximum_absolute_ms: 68.07210884355186
- minimum_ms: -68.07210884355186
- maximum_ms: 64.33265306122405
- within_5_ms_pct: 24.299065420560748
- within_10_ms_pct: 43.925233644859816
- within_20_ms_pct: 63.55140186915887
- within_30_ms_pct: 80.37383177570094
- within_50_ms_pct: 94.39252336448598
- interval_counts: {'BEFORE': 60, 'INSIDE': 5, 'AFTER': 42}

## Stratified timing

| Group | N | Signed median ms | Mean ms | Absolute median ms | Signed IQR ms | Absolute P95 ms | Max absolute ms | ≤10 ms % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| E | 27 | 26.209 | 4.178 | 32.794 | 60.384 | 64.083 | 68.072 | 7.41 |
| A | 21 | 8.812 | 1.520 | 20.024 | 35.455 | 33.988 | 39.965 | 19.05 |
| D | 29 | -6.250 | -4.387 | 8.676 | 13.189 | 36.970 | 64.333 | 58.62 |
| G | 30 | -4.959 | -5.020 | 5.679 | 9.767 | 13.950 | 15.148 | 80.00 |
| mf | 36 | 0.977 | 4.057 | 13.466 | 27.615 | 46.960 | 62.577 | 38.89 |
| comfortable-natural | 36 | -8.475 | -8.427 | 16.068 | 22.195 | 63.521 | 64.441 | 38.89 |
| forte | 35 | -2.991 | 0.692 | 9.800 | 23.238 | 39.220 | 68.072 | 54.29 |
| 20260914_0028 | 9 | 31.688 | 16.635 | 32.702 | 23.338 | 56.840 | 62.577 | 11.11 |
| 20260914_0029 | 8 | 14.209 | 17.815 | 14.209 | 14.196 | 28.365 | 28.865 | 12.50 |
| 20260914_0030 | 9 | -8.676 | -8.021 | 8.676 | 17.124 | 21.498 | 22.667 | 66.67 |
| 20260914_0031 | 10 | -7.933 | -7.400 | 7.933 | 10.835 | 13.950 | 14.143 | 60.00 |
| 20260914_0033 | 8 | -9.836 | -13.214 | 36.831 | 90.464 | 64.024 | 64.441 | 12.50 |
| 20260914_0034 | 8 | -21.677 | -21.989 | 21.677 | 8.882 | 37.873 | 39.965 | 12.50 |
| 20260914_0035 | 10 | -5.086 | 3.510 | 14.010 | 15.730 | 56.069 | 64.333 | 40.00 |
| 20260914_0036 | 10 | -6.180 | -5.685 | 6.405 | 4.926 | 13.155 | 15.148 | 80.00 |
| 20260914_0037 | 10 | 26.291 | 6.880 | 35.263 | 55.359 | 56.040 | 68.072 | 0.00 |
| 20260914_0038 | 5 | 14.629 | 13.063 | 14.629 | 15.776 | 26.669 | 28.330 | 40.00 |
| 20260914_0039 | 10 | -6.494 | -9.014 | 6.494 | 6.621 | 20.848 | 23.472 | 70.00 |
| 20260914_0040 | 10 | -3.263 | -1.974 | 3.734 | 5.833 | 8.076 | 9.942 | 100.00 |

All threshold percentages, interval counts and ranges for every group/take are in RESULTS.json.

## Interpretation — inference, not a causal claim

TIMING BIAS: CONDITION-DEPENDENT, with substantial within-condition instability. E-string median absolute error is 32.79 ms versus G-string 5.68 ms. A-string take medians switch from late in mf/forte to early in comfortable-natural; this is inconsistent with one constant global delay. One take per string/condition confounds take effects with condition, so it cannot establish a causal dynamic effect. E comfortable-natural alone has a 90.46 ms signed IQR.

The pooled signed median −3.92 ms masks large event errors. MAE 13.22 ms, P95 56.88 ms, max 68.07 ms, and 13 unresolved correspondences are material relative to JGA’s 10–30 ms effects. No arbitrary pass threshold or bias correction was introduced. Strong pitch recognition does not establish onset correctness. Recognition is PARTIAL for an unambiguous timing test, sufficient for this conditional 107-event comparison.

No PLP, spectral-flux selection, historical audio, model tuning, timestamp correction, or alternative detector was used. GT and previous artifacts remain unchanged.

## Deliverables

- GALLEGATI_NATIVE_BP_VS_GT_120.csv: exactly 120 rows.
- GALLEGATI_NATIVE_BP_ONSET_VS_GT_120.pdf
- GALLEGATI_NATIVE_BP_ERROR_BY_STRING_CONDITION.pdf
- GALLEGATI_NATIVE_BP_TIMING_EXAMPLES.pdf
- ALL_HYPOTHESES_ASSOCIATION_AUDIT.json and ADDITIONAL_UNASSOCIATED_BP_NOTES.json
- RAW_RESULTS_FREEZE.json and inference/output/TRANSCRIPTION_COMPLETE.json

NATIVE BASIC PITCH TIMING TEST COMPLETED: YES
BP NOTE RECOGNITION SUFFICIENT FOR TIMING TEST: PARTIAL
NATIVE BP ONSET SUITABLE AS JGA BASS MICROTIMING LANDMARK: NO

COMMIT: NONE · PUSH: NONE. Stop for PI review.
