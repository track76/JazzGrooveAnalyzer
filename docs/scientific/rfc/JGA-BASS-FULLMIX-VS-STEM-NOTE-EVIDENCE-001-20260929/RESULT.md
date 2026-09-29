# Result — JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-001-20260929

**Verdict: `PASS_WITH_RECORDED_DEVIATIONS`** (VALIDATION.json)

## What was run
Identical extractor code on the full mix and the isolated bass stem over the identical
frozen interval, then temporal connected-component matching at four preregistered
tolerances. No pitch-based decision of any kind was applied to matching.

## Extraction
| arm | events | density |
|---|---|---|
| full mix | 458 | 13.150/s |
| bass stem | 442 | 12.690/s |

## Matching
| family | components | edges | full-mix coverage | stem coverage | unmatched F | unmatched S | crossings | both-F0 pairs |
|---|---|---|---|---|---|---|---|---|
| T0 | 614 | 286 | 62.4% | 64.7% | 172 | 156 | 0 | 227 |
| T1 | 572 | 328 | 71.6% | 74.2% | 130 | 114 | 0 | 255 |
| T2 | 523 | 377 | 81.4% | 83.9% | 85 | 71 | 8 | 293 |
| T4 | 326 | 647 | 92.1% | 95.9% | 36 | 18 | 111 | 502 |

The T0 population has p95 = 70 cents; this is a legitimate distinct-population result under the same
preregistered formula and is not to be reconciled with the T1 value.

T1 is the preregistered primary point. Widening tolerance raises coverage and raises
ambiguity at the same time; the direction of travel is the only safe reading.

## Pitch (T1, ALL_F0_BOTH_VALID, n=255)
Preregistered rounded-index quantiles (index = round(f * (n - 1)) on the sorted
population, clamped to [0, n-1]): min 0, p25 0, median 0, p75 10, p95 60, max 330.
These values are NOT conventional nearest-rank order statistics; the preregistered formula is
preserved exactly and the scientific values are unchanged.
Exactly zero cents for 139 of 255 pairs (54.5%); within 10 cents for 163 (63.9%).
VALIDITY_QUALIFIED low-register pairs at T1: 17. No threshold was applied in either population.

## What this does and does not show
This is convergent computational evidence of temporal correspondence between two dependent
representations of the same mixdown. It is **not** verification of notes, **not** Ground
Truth, **not** independent confirmation, and **not** an accuracy measurement. No independent
replication was performed. See LIMITATIONS.md.

## Deviations
Six process deviations (DEV-1..DEV-6) are recorded in EXECUTION_PROVENANCE.json. The
significant one is DEV-3: `export_family.py` used the wrong stem node offset and was caught
by cross-checking against the frozen SSD results, then corrected. No reported number comes
from the defective code path.
