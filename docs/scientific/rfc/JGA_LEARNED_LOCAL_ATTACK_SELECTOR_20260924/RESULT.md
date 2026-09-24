# JGA learned local attack selector — controlled Fishman study

**Result: successful conditional local selection on 35/40 holdout GT events; not a validated autonomous BP note-identity pipeline or historical transfer.**

## Authority, scope and isolation

Target: channel-specific observable Fishman Full Circle pizzicato onset; NOT physical string release. Both supplied GT/freeze hashes and frozen native BP output hashes verified. All source audio copies match their original hashes. Basic Pitch was not rerun. Native candidate timestamps were retained without correction.

This is process-isolated validation after prior investigator exposure to all 12 takes and GT/native BP results. It is not investigator-blind and not a pristine corpus-level holdout. The existing deterministic take split was reused without searching for a favorable allocation. Development takes: 0028,0029,0030,0033,0034,0036,0039,0040. Holdout: 0031(G mf),0035(D comfortable-natural),0037(E forte),0038(A forte). Split hashed before development.

A preparation coordinator routed only the 80 development references. macOS filesystem sandboxes denied each compute process access to the parent repository, original GT, prior matched-result tables, and external volumes. Explicit negative-read checks passed and are recorded. Holdout process received only opaque WAVs, native BP hypotheses, fixed implementation and frozen model. All 288 per-hypothesis holdout predictions and features were saved/hashed before the separate GT evaluation. No holdout retuning.

## Inputs and matching limitation

Every native BP hypothesis was queried, not just the previously GT-resolved cohort. Search windows were NOT selected using holdout GT. Evaluation subsequently reused the previously fixed pitch/chronology/persistence association rule (JGA_NATIVE_BP_GT_120_20260924/MATCHING_PROTOCOL.json). This is reference-assisted evaluation correspondence, not a deployable note-identity filter. Five holdout notes remain BP-correspondence ambiguous. No nearest-GT hypothesis choice was made.

## Fixed preprocessing and labels

One global window: native BP onset ±150 ms, clipped only by file extent. Chosen prospectively as a local context scale, tested on development only; no individual GT window adjustment. Local candidates: every positive-flux local maximum above numerical floor 1e−12, 30≤f<250 Hz, Hann1024, hop44, 44.1kHz. Crop starts align to the original 44-sample grid; original STFT frame centers are retained. Waveform and spectral features use fixed surrounding context. No unrestricted full-take attack search or suppression/re-arm.

Hann support 23.22ms; hop 0.998ms. The finer hop does not imply 1ms physical timing accuracy. Centered spectral features can precede the human observable onset; the approximately −5ms tendency remains uncorrected.

Candidates inside human plausible bounds are interval-compatible positives. Candidates outside but within 5ms of the bounds are separately labelled near-interval proxies (half training weight); others are negative landmark examples. All qualifying proxies are retained, not only the nearest candidate. These labels learn a signal landmark near GT; they do not prove all other local peaks are nonphysical attacks. Human marker precision was 1ms, not sub-ms.

Development: 80 GT,72 uniquely recognized notes; all72 GT centers fall inside the global window. Candidate coverage:38/72 within5ms,72/72 within10ms,72/72 within20ms. Average40.24 candidates/window, range25–49; median41. Eight BP-ambiguous events are outside the supervised cohort, not silently solved.

## Selector and development results

19 preserved morphology features plus signed/absolute BP distance and relative BP-activity position. Logistic C=0.1/C=1 and depth3 leaf5 tree compared with thresholds0.5/0.75 using leave-one-development-take-out CV. Balanced class weights, training-fold-only scaling, proxy sample weights0.5. Selection objective fixed before training: largest within10ms useful yield, then lowest P95, then simpler model.

Selected logistic C=0.1, score threshold0.5. Select highest score when unique; tied top score or below threshold abstains; empty window returns NO_CANDIDATE. No averaging or correction. CV72/72 selected and within10ms; median absolute5.143ms, P955.665ms, max6.222ms. Exact coefficients/scaler/code hashes in development/output/SELECTOR_FREEZE.json.

Largest standardized weights: low_energy_pre_log, peak_local_mean_ratio, rise_slope_norm, low_spectral_concentration_change, spectral_slope_change, centroid_change, peak_local_max_ratio, log_flux_peak. See feature figure for signs; correlated weights are not causal attribution.

## Holdout population and metrics

40 GT;35 uniquely associated recognized BP notes;5 BP-correspondence ambiguities. All35 have local candidates within10ms. Conditional decisions:35 ATTACK_SELECTED,0 ABSTAIN_AMBIGUOUS,0 NO_CANDIDATE. The5 unmatched correspondences are NOT relabelled as selector abstentions. Correct association within prospective100ms scoring tolerance35; wrong selections beyond100ms0; errors>20ms0.

Selection coverage:35/40=87.5% overall;35/35=100% of recognized cohort. Overall useful-event yield within10ms:87.5%. Conditional timing within10/20/30ms:100%; within5ms40%. Signed median−5.213ms; mean−5.083ms; median absolute5.213ms; signed IQR0.520ms; P955.621ms; maximum absolute5.915ms. All35 predictions precede the human plausible interval (before35/inside0/after0). Thus these are close landmarks, not exact recovery of the annotated center.

Raw holdout query population:288 BP hypotheses →95 selections and193 abstentions. Beyond the35 resolved selected targets,60 selected per-hypothesis outputs remain unverified as separate physical attacks. This experiment does not establish their precision, deduplicate them, or solve note identity. Full predictions remain preserved.

## Same-population baselines

| Method | N | Median absolute ms | P95 absolute ms | Maximum absolute ms | Within10 | Useful yield /40 |
|---|---:|---:|---:|---:|---:|---:|
| Native BP | 35 | 14.629 | 51.478 | 68.072 | 34.29% | 30.00% |
| Nearest to BP | 35 | 19.217 | 53.096 | 74.342 | 40.00% | 35.00% |
| Earliest | 35 | 148.039 | 179.044 | 215.023 | 0.00% | 0.00% |
| Largest flux | 35 | 5.227 | 36.775 | 37.560 | 88.57% | 77.50% |
| JGA selector | 35 | 5.213 | 5.621 | 5.915 | 100.00% | 87.50% |

Baseline definitions: native onset; local candidate minimizing absolute BP distance (earlier on exact tie); earliest local candidate; largest local flux (earlier on exact tie). Same35 resolved notes, same windows/candidates for every acoustic method. No GT ranking.

## Stratification (ms)

| Group | Resolved / GT | Signed median | Abs median | Abs P95 | Max abs | Within10 |
|---|---:|---:|---:|---:|---:|---:|
| A | 5/10 | -5.238 | 5.238 | 5.481 | 5.531 | 100.0% |
| D | 10/10 | -4.744 | 4.744 | 5.508 | 5.724 | 100.0% |
| E | 10/10 | -5.266 | 5.266 | 5.430 | 5.499 | 100.0% |
| G | 10/10 | -5.235 | 5.235 | 5.762 | 5.915 | 100.0% |

| Group | Resolved / GT | Signed median | Abs median | Abs P95 | Max abs | Within10 |
|---|---:|---:|---:|---:|---:|---:|
| COMFORTABLE_NATURAL | 10/10 | -4.744 | 4.744 | 5.508 | 5.724 | 100.0% |
| f | 15/20 | -5.238 | 5.238 | 5.508 | 5.531 | 100.0% |
| mf | 10/10 | -5.235 | 5.235 | 5.762 | 5.915 | 100.0% |

| Group | Resolved / GT | Signed median | Abs median | Abs P95 | Max abs | Within10 |
|---|---:|---:|---:|---:|---:|---:|
| 20260914_0031 | 10/10 | -5.235 | 5.235 | 5.762 | 5.915 | 100.0% |
| 20260914_0035 | 10/10 | -4.744 | 4.744 | 5.508 | 5.724 | 100.0% |
| 20260914_0037 | 10/10 | -5.266 | 5.266 | 5.430 | 5.499 | 100.0% |
| 20260914_0038 | 5/10 | -5.238 | 5.238 | 5.481 | 5.531 | 100.0% |

The four low-E forte largest-flux late errors (>30ms) were avoided by the learned selector without a condition-specific rule. Each of the10 low-E forte recognized events is within10ms. No wrong (>20ms) selections exist in the resolved holdout cohort; all5 unresolved cases arise at BP correspondence, not lack of local candidates. Because each string is represented by one holdout take, string/condition/take effects cannot be causally separated.

## Decision and limits

LOCAL CANDIDATE COVERAGE SUFFICIENT: YES (recognized cohort)
JGA SELECTOR LEARNED: YES
HOLDOUT SELECTION COVERAGE:87.5%
HOLDOUT MEDIAN ABSOLUTE ERROR:5.213ms
HOLDOUT P95 ABSOLUTE ERROR:5.621ms
HOLDOUT WITHIN ±10ms:100% of35selected
IMPROVEMENT OVER NATIVE BP: YES
IMPROVEMENT OVER NEAREST-BP CANDIDATE: YES
IMPROVEMENT OVER EARLIEST-CANDIDATE: YES
IMPROVEMENT OVER LARGEST-FLUX CANDIDATE: YES
GENERALIZES ACROSS HOLDOUT TAKES: YES (resolved cohort on all4takes)
JGA LOCAL ATTACK SELECTOR VALIDATED ON CONTROLLED CORPUS: YES — bounded conditional local-selector validation; prior investigator exposure and unresolved identity population limit the claim.

Errors of roughly5ms with tight tails improve substantially over native BP on this controlled cohort at the10–30ms study scale, but a systematic early coordinate remains. No universal accuracy or historical/physical-onset validity is claimed. Independent fresh-corpus confirmation and deployable BP identity handling remain needed before broader claims. No Ray Brown transfer executed.

## Files

Requested three PDFs, DEVELOPMENT_CANDIDATES.csv, HOLDOUT_ATTACK_SELECTIONS.csv, EVALUATION.json with complete pooled/stratified metrics; original candidate/features and all-query predictions under development/output and holdout/output. Freeze records preserve split,model,predictions,evaluation.

GT, native BP, previous freezes, canonical JGA and historical reports unchanged. COMMIT:NONE. PUSH:NONE. Stop for PI review.
