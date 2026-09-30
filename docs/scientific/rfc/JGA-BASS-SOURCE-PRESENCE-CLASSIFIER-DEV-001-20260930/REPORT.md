# BASS Source-Presence Classifier — Development

Task `JGA-BASS-SOURCE-PRESENCE-CLASSIFIER-DEV-001-20260930`, PI authorization
`PI-BASS-SOURCE-PRESENCE-CLASSIFIER-DEV-20260930`.

**Status: DEVELOPMENT ONLY. NOT scientifically validated.** One pipeline is frozen. No held-out
prediction was made and no held-out human label was opened.

## Headline

A source-neutral FullMix descriptor separates stable human Bass-present from stable human
Bass-absent at balanced accuracy **0.7908** against a **0.5000** majority baseline, using **one
feature** and **no** PLP, stems, quarter/measure, or timing information.

The most important number in this report is not the accuracy. It is that **32 supervised-eligible
rows cannot support 16 predictors**, and the data says so plainly: the 16-feature logistic scored
0.6883, *worse* than the single descriptor's 0.7908.

## Development data

| | |
|---|---|
| Development total | 40 |
| Stable present | 12 |
| Stable absent | 20 |
| Human unstable, **excluded** | 8 |
| **Supervised-eligible used** | **32** |

The PI's caution not to assume all 40 development landmarks are eligible was correct. Eight are
human-unstable and are excluded, never relabelled. The 10 unstable item numbers are public, so
publishing *which* 8 fall in development would let a later step derive the identities of the 2
inside the held-out set. **Those identities are deliberately withheld; only counts appear here.**

## Held-out firewall

No held-out human answer was read, inferred, or reconstructed. Never opened:
`SEALED_BASS_HELD_OUT_LABELS.json`, `BASS_CONSENSUS_ALL60_SEALED.json`, `PRE_SEAL_RECORDS/`, or any HD
plaintext of held-out answers. Backups were not inspected to recover them. Held-out *membership* was
used for exactly one purpose: asserting every trained row is a development member.

`REPRODUCTION/predict_bass.py` is **label-blind by construction** — it reads the frozen record and
the Phase A feature table, never a label file. A named test asserts its source contains no
human-label read, so the next task cannot use it to open held-out answers.

## Two methodology errors I made and corrected

I report these because both inflated my own numbers before I caught them.

1. **Threshold selected using the validation fold's own labels.** This leaked each evaluation
   observation into its own prediction and reported 0.8842 for the single feature and 0.8625 for
   the 16-feature model. **Both withdrawn.** Every number here uses the corrected protocol, where
   the threshold comes from inner CV on the training fold only.
2. **No scaling inside the folds.** L2 shrinkage was applied per-unit across features spanning 0.01
   to 224549, so it was not regularizing on a common footing. The PI required in-fold scaling. Adding
   it **changed the ranking** — it is precisely why the single-feature model now wins.

## Validation design

Repeated stratified k-fold with a nested inner loop. Outer: stratified 5-fold × 10 repeats = 50
evaluations. Inner: stratified 4-fold on the training portion only, choosing the decision threshold.
Imputation, scaling, zero-variance filtering, hyperparameter choice, and threshold selection all occur
**inside every training fold**. No statistic from a validation fold ever enters its training fold.

## Baselines

| baseline | balanced accuracy |
|---|---|
| majority class (always ABSENT) | 0.5000 |
| balanced chance, 200 draws | 0.5042 |
| **frozen single descriptor** | **0.7908** |

Single-feature reference sweep across all 16 source-neutral descriptors: `peak_prominence` 0.8063,
`subband_energy_share_3` 0.7312, `subband_energy_share_1` 0.6312, `spectral_flux` 0.6271, then a long
tail near 0.45–0.55.

**Caveat I cannot remove:** the frozen feature topped that sweep, so its figure carries a selection
advantage. A nested estimate that re-picked the best descriptor *inside* each fold gave 0.7558 under
the pre-scaling protocol — slightly *below* the 16-feature model. On 32 rows the single descriptor
and the multivariate model are not cleanly separable.

## Model candidates

| candidate | features | BA | sens | spec | prec | F1 |
|---|---|---|---|---|---|---|
| **logreg on `peak_prominence`** | **1** | **0.7908** | 0.9167 | 0.6650 | 0.6215 | 0.7407 |
| tree depth 3 | 16 | 0.7600 | 0.7000 | 0.8200 | 0.7000 | 0.7000 |
| logreg C=1 | 16 | 0.6883 | 0.8167 | 0.5600 | 0.5269 | 0.6405 |
| tree depth 2 | 16 | 0.6783 | 0.5417 | 0.8150 | 0.6373 | 0.5856 |
| logreg C=0.5 | 16 | 0.6725 | 0.7250 | 0.6200 | 0.5337 | 0.6148 |
| logreg C=0.05 | 16 | 0.6500 | 0.7250 | 0.5750 | 0.5058 | 0.5959 |
| svc RBF C=0.5 | 16 | 0.6242 | 0.3583 | 0.8900 | 0.6615 | 0.4649 |
| svc RBF C=1 | 16 | 0.5842 | 0.3083 | 0.8600 | 0.5692 | 0.4000 |

A small preregistered family, 6 regularization values for the linear model, two tree depths, one
nonlinear comparator. No deep learning, no large search, no sweep.

## Frozen pipeline

- **Feature:** `peak_prominence` — scipy `find_peaks` prominence at the candidate frame, FullMix.
- **Model:** L2 logistic regression, balanced class weights, C=1.0.
- **Threshold:** 0.50, from inner CV on the 32 development rows.
- **Preprocessing:** median imputation declared as fallback; StandardScaler frozen from the 32 rows;
  no run-time feature selection.
- **Seed:** 20260930. **Software:** python 3.13.14, numpy 2.4.6, scipy 1.18.0, scikit-learn 1.9.0.
- **Outputs:** BASS-present probability and binary predicted class.
- **Uncertainty:** **not provided.** With n=32 these are uncalibrated margins and must not be read
  as confidence.

### Which threshold is operative — read this before using the package

The package contains **two different threshold numbers**. They are not in conflict; they answer
different questions. Confusing them is the specific error this section exists to prevent.

| value | what it is | operative? |
|---|---|---|
| **`0.50`** | The preregistered inner-threshold procedure (stratified 4-fold CV on the training rows, out-of-fold scores, grid 0.05–0.95 maximising balanced accuracy) applied to **all 32 supervised-eligible development rows**. | **YES — this is `model.decision_threshold`** |
| `0.55` | The **mode across the 50 outer-fold training fits** (each on ~25–26 rows). It describes the cross-validation *procedure*. | **NO — non-operative** |

Observed outer-fold threshold distribution: **`{0.45: 1, 0.50: 18, 0.55: 20, 0.60: 11}`**, range
0.45–0.60. So `0.55` is a 20/50 plurality over `0.50`'s 18/50 — a narrow plurality, not a
consensus. The two values differ because a mode over 50 subsample fits and a single fit on all 32
rows are different quantities; they are not required to agree.

**`0.55` is non-operative and MUST NOT be used by `predict_bass.py`.** The predictor reads
`model.decision_threshold` (`predict_bass.py:43`) and nothing else.

**0.50 was not adjusted upward, and must not be.** A flat 0.55 across all folds would have scored
*HIGHER* development CV balanced accuracy (0.8200) than the frozen 0.50 (0.7908). Acting on that
would be tuning on development cross-validation, so it was not acted on. The 0.45–0.60 spread
shows the two values sit inside the noise of the threshold-selection procedure at n=32, and that
spread independently corroborates the recorded HIGH overfitting risk.

**Audit of 2026-09-30** (`PI-BASS-FROZEN-THRESHOLD-DOC-CORRECTION-20260930`) re-derived the
threshold from development data only and confirmed: the frozen `decision_threshold = 0.50` is the
unique optimum on the full 32 rows (out-of-fold balanced accuracy 0.825000 at 0.50 vs 0.808333 at
0.55, so the tie-break rule never fired); the frozen scaler mean/scale, coefficient and intercept
reproduce bit-for-bit; and the whole `development_cross_validation` block reproduces exactly. The
field formerly named `threshold_mode` was renamed to
`in_fold_threshold_mode_NOT_the_frozen_threshold` and a `threshold_documentation` block was added
to `FROZEN_PIPELINE.json` and `VALIDATION.json`. **No scientific value, model parameter or
performance result was changed by that correction.**


## Cross-validated results

Confusion matrix aggregated over 50 outer evaluations (so counts exceed 32):

```
                predicted ABSENT   predicted PRESENT
human ABSENT            133                 67
human PRESENT            10                110
```

| metric | value |
|---|---|
| balanced accuracy | 0.7908 |
| sensitivity (recall, BASS present) | 0.9167 |
| specificity (recall, BASS absent) | 0.6650 |
| precision | 0.6215 |
| F1 | 0.7407 |

Per-fold balanced accuracy: mean 0.7958, sd 0.1432, range 0.4167–1.0000. These folds are **not
independent** and n=32, so this is a descriptive spread. No confidence interval, no significance
claim.

## Most informative features

`peak_prominence`, direction: **higher prominence is associated with BASS-ABSENT**, point-biserial
r = **−0.5092**. Next ranked: `subband_energy_share_3`, `subband_energy_share_1`, `spectral_flux`,
`flatness_magnitude`.

In the 16-feature model only **6 of 16** coefficients are sign-stable across folds, and
`peak_prominence` dominates by roughly 60× the median coefficient. The multivariate model is
largely a `peak_prominence` model carrying unstable extra terms.

**Association only.** Correlation is not physical causation, and no claim is made that spectral
prominence causes a listener to hear a Bass attack.

**The PI's scientific question — are stable YES and stable NO distinguishable from FullMix features
independently of PLP and stems? — YES, but modestly, and from a single broadband descriptor.**

## Negative examples

The PI observed many stable-NO targets that sounded off-beat or pre-articulation. **This was not
used.** No timing feature, no candidate-relative distance, no 69.7 ms value, no 100 ms count entered
the model. The distinction was left entirely to the acoustic descriptor.

The outcome is informative: specificity is 0.665, so roughly a third of stable-NO landmarks are
predicted PRESENT. Those off-beat-looking negatives are **not** trivially separable from FullMix
spectral shape at this sample size.

## Overfitting risk — HIGH

- 32 rows against 16 predictors is 2.0 observations per predictor.
- More features made performance *worse* (0.7908 → 0.6883).
- Adding FullMix low-band descriptors lowered balanced accuracy 0.7642 → 0.7333.
- Only 6 of 16 coefficients sign-stable.
- The RBF SVM fell to 0.5842–0.6242, at or below chance, confirming no nonlinear capacity.
- The learning curve was still rising at the largest training size: the model is **data-limited, not
  feature-limited**.

Leakage risk is low: source-neutral FullMix features only, and the upstream Phase A table was
produced the day *before* the human labels existed, so no feature could have been built from them.

## Verdict

**CURRENT FULLMIX FEATURES SHOW BASS SOURCE DISCRIMINATION: PARTIAL.** Above baseline and
reproducible, but asymmetric (0.917 sensitivity against 0.665 specificity), modest margin, wide
per-fold spread, and a frozen feature with an unquantifiable selection advantage.

## Stage boundary

No PLP. No Method L/G. No quarter, measure, or absolute track time. No human tap timing. No off-beat
or temporal rule. No stem-derived predictor and no stem source identity as Ground Truth. No deep
learning or large model search. **No held-out prediction. No held-out label opened.** No Drum. No
scientific promotion. No commit, no push.

**NEXT: frozen held-out prediction and reveal**, separately authorized. Predictions must be computed
and frozen *before* the held-out human labels are opened, and human-unstable held-out cases must be
reported separately rather than counted as binary errors.
