# CED-VAL-003 H02 Ambiguity / Scorability Authority Audit

Audit ID: `AUD-CEDVAL003-H02-SCORABILITY-01`

Status: **PASS — FROZEN READ-ONLY AUDIT**

The audit deterministically joined all 89 frozen blind candidates, all 61
blind unresolved records, all frozen score records, all 56 unscorable
candidates and all 55 unscorable symbolic relations to checksum-bound
Calibration Zero event/pair authority. No candidate or score changed.

## Candidate-level result

| Source | Blind | Scorable | Unscorable | Drum calibration unresolved | Source calibration unresolved |
|---|---:|---:|---:|---:|---:|
| Piano | 14 | 5 | 9 | 9 | 0 |
| Double Bass | 75 | 28 | 47 | 45 | 2 |
| Overall | 89 | 33 | 56 | 54 | 2 |

All 54 Drum-side cases and both Double Bass-side cases are directly caused by
`AMBIGUOUS_MULTIPLE_OBSERVED` Calibration Zero capture cells. All candidates
have complete blind identity/lineage evidence. There are zero candidate-
discovery limitations, zero mixed limitations, zero indeterminate cases and
zero identity/provenance join failures.

Exact symbolic-pair authority is already available for 42 of the 56 candidate
cases (Piano 3; Double Bass 39), but absolute event authority remains
unresolved and therefore the scoring chain stops before adjudication. Absence
of exact symbolic-pair authority is not the cause of candidate unscorability:
when both event identities are valid, absence of a symbolic pair produces the
already-frozen FP classification rather than an unscorable status.

## Symbolic-relation result

The 55 frozen unscorable symbolic relations comprise:

- Double Bass–Drums: 44 with valid source authority and Drum
  `AMBIGUOUS_MULTIPLE_OBSERVED`;
- Double Bass–Drums: 2 with source `AMBIGUOUS_MULTIPLE_OBSERVED` and valid
  Drum authority;
- Piano–Drums: 8 with valid source authority and Drum
  `AMBIGUOUS_MULTIPLE_OBSERVED`; and
- Piano–Drums: 1 with both sides `UNMATCHED_SYMBOLIC`.

The candidate-level and symbolic-relation populations are distinct frozen
views and are not forced into one-to-one correspondence.

## Scientific implication

The 56 candidates demonstrate that H02 blind discovery evidence exists. Their
unscorability primarily limits validation, not discovery. It does not imply
that the candidates are correct. CED-VAL-003 precision, recall and F1 remain
unchanged and must remain explicitly qualified as applying only to the 33
scorable candidates.

The primary authority limitation is the Drum Calibration Zero population:
54 of 56 unscorable candidates reference Drum EME whose symbolic identity
cannot be selected because their capture cells contain multiple observations.
No observation is removed and no alternative matching is inferred.

H02, H03, Calibration Zero, TP/FP/FN, raw observations, AD-038/040 and
production authority are unchanged. `GEOMETRIC_ONLY` remains authoritative.

Audit scientific fingerprint:
`34dafe335a0965ff2321bfc176386b974f1ee5a0425e153894e96bde8f939348`.
