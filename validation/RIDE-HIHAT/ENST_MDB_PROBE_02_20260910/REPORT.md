# Ride-vs-HiHat probe02: ENST acoustic development → frozen MDB validation

2026-09-10. **EXECUTED — ENST_CONTROLLED_DISCRIMINATION_WORKS_MDB_TRANSFER_FAILS. STOP FOR PI REVIEW.**

## Finding and limits

The new model passed the prospectively modest ENST diagnostic gate, but **did not establish useful selective Ride admission** even on held-out ENST. Its single frozen MDB validation failed: at p>=0.5 every eligible Ride/Hi-Hat event was called Ride; the selective rule abstained on all of them. This is **NOT_IMPROVED cross-domain discrimination** relative to preserved GMD development. Higher recall alone is not improved discrimination when all negatives are called positive. No model, feature, threshold or input change followed the result.

The accepted GMD report remains unchanged at `validation/RIDE-HIHAT/GMD_MDB_PROBE_20260910/REPORT.md`, SHA-256 `a748d39b63a9807e7c5a4408ac4bef6cadacd27e1689c38cf8afe14b9db20ec0`. Its execution was not rerun. Prior MDB aggregate results were already known to the project. MDB was unused by this NEW model until its freeze: independence is model-relative, not a claim of globally never-seen validation or unexposed research decisions.

## Admission

PI-supplied archive: `/Volumes/SSD Track/JGA/downloads/ENST-drums-audio.tar.bz2`. SHA-256 `3b4bb5c73db9d365c3ad54d12b9c3a2b9ce3295ab2a31f181f94dee88f413884`. Readable full tar inventory: 3,658 members; full bzip stream integrity checked through EOF. This is a **local integrity/custody binding**, not a match to an unavailable publisher checksum for the legacy archive. The later Zenodo archive checksum/license was not substituted. PI declares authorized legacy-provider access; research-use terms remain applicable and no commercial permission is inferred. Existing external dataset audit documents provider annotation/legacy licensing authority; source: https://perso.telecom-paristech.fr/grichard/ENST-drums/ . No external dataset or video was downloaded.

Extracted only 47 isolated stick/pedal hit recordings from original overhead_L and their 47 matching annotations: **88,497,315 bytes**, across three player–kit groups. Archive retained; no other audio channels or mixes duplicated. Data root: `/Volumes/SSD Track/JGA/datasets/RIDE-HIHAT-EXTERNAL/ENST-legacy-audio-20260910/`. Every selected member was reread for SHA-256/length, and all47 WAV/annotation pairs passed timestamp order/support checks. These are provider annotated audio onsets, not independently measured physical contacts. No listening labels or audio alignment repair.

Before training, generic `c` annotations were resolved as missing identity authority: group1 c1 in a crash-named recording and group3 c4 in Ride-named recordings. Fifteen such events were preserved as UNRESOLVED_PROVIDER_SOURCE_CLASS and excluded, rather than forced positive or negative from a generic code. This prospective coverage rule is in [PROTOCOL.md](PROTOCOL.md); no performance result existed when it was bound. The explicit rc source and HH labels remained usable.

## Development population and frozen method

Player2 training (74 examples); player1 calibration (53); player3 held-out evaluation (96). Split chosen prospectively from documentary subtype coverage: player2 provides stick open/closed HH and multiple Rides; player1 selected HH uses pedal. No group swapping or random event split. **223 usable examples: 26 Ride, 60 HH, 137 controls.** Of245 provider annotations, seven failed the unchanged full-crop boundary rule and15 had unresolved generic cymbal identity. No extra zero/incomplete feature crops; resource cap inactive.

| Subtype | Train | Calibration | Held-out | Total |
|---|---:|---:|---:|---:|
| HH_CLOSED | 5 | 0 | 5 | 10 |
| HH_HALF_OPEN | 5 | 0 | 5 | 10 |
| HH_OPEN | 5 | 0 | 5 | 10 |
| HH_PEDAL_CLOSED | 0 | 5 | 10 | 15 |
| HH_PEDAL_OPEN | 0 | 5 | 5 | 10 |
| HH_WIDE_OPEN | 0 | 0 | 5 | 5 |
| RIDE_DOME | 0 | 0 | 5 | 5 |
| RIDE_UNSPECIFIED | 11 | 5 | 5 | 21 |

Ride is unspecified unless a descriptor is explicit; five held-out `dome` events retain that provider subtype (not an invented bow label). No generic Ride→bow conversion; no undocumented bell labels. HH pedal/half-open/wide-open descriptors and native state codes are retained. Native Chinese cymbals remain contrasts. All native negative/control counts and exclusions are in inventory JSON.

Representation/model reused from probe01: 250 ms complete onset-centred crop, no other annotated onset within the crop; mono mean,44.1kHz analysis, RMS normalization, Hann2048/hop441,32 Slaney mel bands20–20,000Hz, log1p magnitude,26frames/832coordinates. Train-only scaling; balanced logistic regression C1/lbfgs/max_iter2000/tol1e-6. Converged in49 iterations. No timing/rhythm/tempo/meter/filename/source-ID features. Previous tails may remain; overlap exclusions do not establish complete source isolation.

The predeclared viability gate was balanced accuracy>0.5 and AP>prevalence on both all-controls and Ride-vs-HH subsets. ENST passed this modest diagnostic check; it did not establish reliable event admission. The unchanged calibration rule yielded low0.5 and high1.0000000000000002 because a negative calibration score saturated at1.0. Thus **no probability can reach the Ride-admission threshold**. This is an unresolvable operating point under the fixed rule, preserved rather than repaired. Undefined admitted-Ride precision is not100% precision. No statistical significance or high-confidence sufficiency claim follows.

## Results

| Population | N / Ride | Precision | Recall | AP | Ride prevalence | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|
| ENST held-out/all controls | 96 / 10 | 0.400000 | 1.000000 | 0.343084 | 0.104167 | 0.912791 |
| ENST held-out/Ride–HH | 45 / 10 | 0.416667 | 1.000000 | 0.363619 | 0.222222 | 0.800000 |
| MDB/all controls | 2507 / 219 | 0.087425 | 1.000000 | 0.089169 | 0.087355 | 0.500437 |
| MDB/Ride–HH | 1262 / 219 | 0.173534 | 1.000000 | 0.173810 | 0.173534 | 0.500000 |

| Selective population | Ride admitted | Correct NOT_RIDE | False NOT_RIDE | Abstain | Decision coverage | Ride recall |
|---|---:|---:|---:|---:|---:|---:|
| ENST held-out/all | 0 | 71 | 0 | 25 | 0.739583 | 0.000000 |
| ENST held-out/Ride–HH | 0 | 21 | 0 | 24 | 0.466667 | 0.000000 |
| MDB/all | 0 | 2 | 0 | 2505 | 0.000798 | 0.000000 |
| MDB/Ride–HH | 0 | 0 | 0 | 1262 | 0.000000 | 0.000000 |

### Subtype errors at p>=0.5

TP/FN concern positive Ride; FP/TN concern negative HH. Full control/group confusion and PR curves are retained externally.

| Dataset | Subtype | N | TP | FP | FN | TN |
|---|---|---:|---:|---:|---:|---:|
| ENST held-out | HH_CLOSED | 5 | 0 | 0 | 0 | 5 |
| ENST held-out | HH_HALF_OPEN | 5 | 0 | 0 | 0 | 5 |
| ENST held-out | HH_OPEN | 5 | 0 | 0 | 0 | 5 |
| ENST held-out | HH_PEDAL_CLOSED | 10 | 0 | 9 | 0 | 1 |
| ENST held-out | HH_PEDAL_OPEN | 5 | 0 | 0 | 0 | 5 |
| ENST held-out | HH_WIDE_OPEN | 5 | 0 | 5 | 0 | 0 |
| ENST held-out | RIDE_DOME | 5 | 5 | 0 | 0 | 0 |
| ENST held-out | RIDE_UNSPECIFIED | 5 | 5 | 0 | 0 | 0 |
| MDB | HH_CLOSED | 788 | 0 | 788 | 0 | 0 |
| MDB | HH_OPEN | 99 | 0 | 99 | 0 | 0 |
| MDB | HH_PEDAL | 156 | 0 | 156 | 0 | 0 |
| MDB | RIDE_BELL | 6 | 6 | 0 | 0 | 0 |
| MDB | RIDE_UNSPECIFIED | 213 | 213 | 0 | 0 | 0 |

## Independent validation and descriptive comparison

Model/scaler/calibration, protocol, implementation, input and environment were frozen before opening MDB in this run. The entry point verified freeze bindings; no refitting. One validation on all23 original admitted MDB recordings, with the identical prospective eligibility rule as probe01:2,507 eligible events; 28 boundary and5,459 other-onset exclusions. Ride219, HH1,043; no favorable track selection or changed MDB population. Source authority and original files unchanged.

Preserved GMD→MDB Ride–HH precision11.76%, recall8.22%, AP23.62%, balanced accuracy47.64%. ENST→MDB precision17.35%, recall100%, AP17.38%, balanced accuracy50%. The apparent precision/recall increase comes with predicting **all1,262 eligible Ride/HH opportunities positive**, yielding precision equal to Ride prevalence. Ranking discrimination did not improve: AP fell and ROC AUC is approximately0.501. All-control predictions similarly called2,505/2,507 events Ride. The selective rule admits none. This is not useful transfer or a successful high-confidence timing-admission stage.

The domain-mismatch hypothesis is not causally settled: ENST training here contains just11 Ride examples and74 total, with different subtype/capture coverage from GMD. Development group, acoustic specimen, microphone and recording conditions are confounded. Do not conclude that acoustic training cannot work, or that domain mismatch was ruled out. Only this frozen bounded substitution failed. No post-hoc diagnosis or additional experiment was executed.

## Preservation and next action

External result root: `/Volumes/SSD Track/JGA/experiments/RIDE-HIHAT-ENST-MDB-02/`. Inventories, missingness, source lineage, features, model, predictions, PR curves, result JSON, freeze/environment and logs preserved. One ENST fit; one MDB application. Eleven synthetic label/eligibility/patch tests passed. Feature, eligibility, score and evaluation calculations were compared with probe01; no new representation introduced. Single Codex implementer/analyst; no independent human reviewer or fresh-run replay claimed.

| Record | SHA-256 |
|---|---|
| Protocol | `7bf87111fe674b8a2cf25cb1ca85318f50f4b04c574ac93a04f01a98e4b539ab` |
| Implementation | `de97bc598dd16818c2cf78f64a94aa78530135314dace81d78ab3a4a96763603` |
| ENST admission | `5cef8c2ed9c863921e13563c820c44da333d13af4adc380d1c7ab732901a62c5` |
| Pre-execution binding | `08548c37272d66326be18de6dbcd3d2207d243ba692e86adecc0ce1227a38784` |
| Freeze | `2305892a0ba1a396fa7654bd1b3e8c4887b59dec50f2e33eeeaf6c7209fc7616` |
| ENST result | `b08caa10aed12ab698c41f9934ba4641001f9aee417adbde8b15aaea99c10bcf` |
| MDB result | `7bc4b7f29056dd3598ebd6af4081cd1078d5c35d6ca276e5f3a562aa73d3d5a2` |

Python3.13.14, numpy2.4.6, scipy1.18.0, scikit-learn1.9.0, soundfile0.14.0, librosa0.11.0; exact platform/runtime and thread policy in freeze. Historical authorities and Double-Bass/timing work unchanged. No commit/push.

**Next minimal step:** PI authorization for one bounded diagnosis of cross-domain score saturation under the frozen preprocessing, without retraining or threshold repair. No such diagnostic begins here. Autonomous Ride recognition, BeatReference and BPM remain unauthorized.
