# H-CEDVAL003-STRENGTH-MAX-CORRESPONDENCE-VALIDATION-01

Status: **FROZEN — NOT YET SCORED**

Authority: PI approval of
`H-CEDVAL003-WITHIN-CELL-STRENGTH-DISCRIMINABILITY-01`, result commit
`b26a07e`, scientific fingerprint `902c9a7d…`; frozen CED-VAL-003 Calibration
Zero at commit `3f2a368`.

## Frozen scientific question

For the 56 frozen CED-VAL-003 `AMBIGUOUS_MULTIPLE_OBSERVED` cells, does the
observation identified before Ground Truth access as the
`UNIQUE_STRENGTH_MAXIMUM` coincide with the observation, if any, uniquely
supported by frozen Calibration Zero Ground Truth authority?

## Frozen predictor and population

The predictor is frozen in `frozen_strength_max_predictors.json`, derived only
from discriminability result SHA-256 `35904ceb…` and fingerprint `902c9a7d…`.
For each cell it preserves exactly one already-frozen maximum EME and
PulseCandidate identity. It contains no Ground Truth, Calibration Zero status,
symbolic identity, symbolic time, H02 score or correspondence outcome.

Expected population: Drums 54 cells, Double Bass 2, Piano 0, overall 56 cells
and 112 contained observations. No predictor may be recomputed, added, removed
or changed after Ground Truth access.

## Ground Truth scoring authority

After this preregistration is committed, scoring may open only the frozen
CED-VAL-003 Calibration Zero event authority
`run_20260823_203324/event_level_results.json`, SHA-256 `3c2d2230…`, whose
symbolic-event authority fingerprint is `3d97ff35…` as frozen by the accepted
Calibration Zero result. The authority may adjudicate a predictor only when an
existing frozen cell record uniquely identifies exactly one contained observed
EME as its `VALID` correspondence. `AMBIGUOUS_MULTIPLE_OBSERVED`,
`AMBIGUOUS_BOUNDARY`, unmatched or otherwise non-unique authority is
`UNSCORABLE`. No nearest choice, tolerance, optimization, rematching or manual
interpretation is permitted.

## Frozen scoring and metrics

- `STRENGTH_MAX_CORRECT`: a uniquely authorized observed EME exists and its ID
  equals the frozen predictor EME ID;
- `STRENGTH_MAX_INCORRECT`: a uniquely authorized observed EME exists in the
  frozen cell and its ID differs from the predictor;
- `UNSCORABLE`: existing frozen authority cannot uniquely adjudicate the cell.

Report total, scorable, unscorable, correct, incorrect and exact accuracy
`correct / scorable` independently for Drums and Double Bass, then overall.
Accuracy is null when scorable is zero. Precision, recall and F1 are not used.

Frozen outcome classification:

- `INSUFFICIENT_SCORABLE_EVIDENCE` if overall scorable count is zero or any
  populated source has zero scorable cells;
- `SUPPORTS_STRENGTH_AS_CORRESPONDENCE_PREDICTOR` only if every cell is
  scorable and every prediction is correct;
- `DOES_NOT_SUPPORT_STRENGTH_AS_CORRESPONDENCE_PREDICTOR` only if all populated
  sources have scorable evidence and no prediction is correct;
- `PARTIAL_SOURCE_SPECIFIC_SUPPORT` for every other mixture of scorable
  correct/incorrect or incomplete source-specific evidence.

These exact logical outcomes are frozen before scoring and do not introduce a
post-result numerical threshold.

## Firewalls and replay

Ground Truth scores only the frozen predictor. It cannot create/move an EME,
alter a cell or predictor, combine strength with any other quantity, or change
historical Calibration Zero/H02 evidence. Execute the complete join and scoring
twice and require identical predictors, joins, statuses, counts, accuracies and
scientific fingerprint. Preserve all 56 case records and artifact checksums.

Historical H02 unscorable statuses, TP/FP/FN, metrics and three-dataset
conclusion remain unchanged. H02 is unchanged, no H03 is created, no timing
correction or production promotion is authorized, `GEOMETRIC_ONLY` remains
authoritative, and architecture/production/code impacts are none.
