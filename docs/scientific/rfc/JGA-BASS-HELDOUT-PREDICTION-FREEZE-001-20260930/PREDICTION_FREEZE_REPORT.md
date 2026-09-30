# Held-Out Prediction Freeze

Task: `JGA-BASS-HELDOUT-PREDICTION-FREEZE-001-20260930`
PI authorization: `PI-BASS-HELDOUT-PREDICTION-FREEZE-20260930`

PREDICTION AND FREEZE ONLY. No human-label reveal. No scoring. No performance metric of any kind
is computed or reported in this document, because human answers remain hidden.

## Frozen model

L2 logistic regression, balanced class weights, C=1.0, lbfgs, max_iter=20000, single feature
`peak_prominence`, decision threshold 0.50. No retraining, no tuning, no threshold adjustment,
no feature change.

## Firewall

A `sys.addaudithook` traced every file open during prediction. Answer-bearing open attempts: **0**.
The observed label-free open set was exactly the three authorized inputs: the frozen record, the
Phase A feature table, and the membership-only item/event map.

## Predictions (frozen, pre-reveal)

| item | event_id | feature peak_prominence | standardized | logit | p(BASS_PRESENT) | thr | prediction |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | IDN_F002471 | 28.8385 | -0.239803 | -0.083058 | 0.479247 | 0.50 | BASS_ABSENT |
| 2 | IDN_F001686 | 9.8051 | -0.616674 | +0.565186 | 0.637652 | 0.50 | BASS_PRESENT |
| 7 | IDN_F001741 | 3.7465 | -0.736637 | +0.771530 | 0.683852 | 0.50 | BASS_PRESENT |
| 11 | IDN_F000311 | 164.4460 | +2.445285 | -4.701594 | 0.008999 | 0.50 | BASS_ABSENT |
| 15 | IDN_F001449 | 4.5987 | -0.719763 | +0.742506 | 0.677544 | 0.50 | BASS_PRESENT |
| 19 | IDN_F000091 | 26.6761 | -0.282620 | -0.009410 | 0.497647 | 0.50 | BASS_ABSENT |
| 22 | IDN_F002426 | 3.3399 | -0.744688 | +0.785377 | 0.686838 | 0.50 | BASS_PRESENT |
| 23 | IDN_F000856 | 4.0961 | -0.729715 | +0.759623 | 0.681272 | 0.50 | BASS_PRESENT |
| 25 | IDN_F001607 | 4.7062 | -0.717634 | +0.738843 | 0.676743 | 0.50 | BASS_PRESENT |
| 32 | IDN_F002842 | 31.1997 | -0.193051 | -0.163476 | 0.459222 | 0.50 | BASS_ABSENT |
| 36 | IDN_F001287 | 92.0397 | +1.011609 | -2.235573 | 0.096601 | 0.50 | BASS_ABSENT |
| 37 | IDN_F002181 | 29.5809 | -0.225104 | -0.108341 | 0.472941 | 0.50 | BASS_ABSENT |
| 38 | IDN_F001006 | 4.1872 | -0.727911 | +0.756520 | 0.680598 | 0.50 | BASS_PRESENT |
| 39 | IDN_F001245 | 123.2332 | +1.629254 | -3.297964 | 0.035641 | 0.50 | BASS_ABSENT |
| 44 | IDN_F001058 | 143.2608 | +2.025810 | -3.980068 | 0.018342 | 0.50 | BASS_ABSENT |
| 47 | IDN_F001994 | 113.4403 | +1.435350 | -2.964436 | 0.049059 | 0.50 | BASS_ABSENT |
| 48 | IDN_F001944 | 4.0616 | -0.730397 | +0.760797 | 0.681527 | 0.50 | BASS_PRESENT |
| 53 | IDN_F002694 | 3.4090 | -0.743319 | +0.783024 | 0.686331 | 0.50 | BASS_PRESENT |
| 57 | IDN_F000560 | 13.2005 | -0.549442 | +0.449542 | 0.610530 | 0.50 | BASS_PRESENT |
| 59 | IDN_F001567 | 268.6079 | +4.507738 | -8.249155 | 0.000261 | 0.50 | BASS_ABSENT |

## Provenance

Prediction artifact SHA-256: `ce6bdae79520156ac21b3e17951773d39d5c6b2c4614e0f8310fdac6af39f6c9`

Recorded identically on the canonical SSD volume and the canonical HD archive. The prediction artifact
is immutable by procedure from this point: any modification invalidates the freeze and requires a new
PI decision. It does not license a retry.
