# H-VAL001-C1-13 — Blind Phase-Conditioned Strength Audit

## Preregistered procedure

The unchanged production pipeline reproduced PulseCandidate timestamp,
strength, confidence and source evidence for every authoritative controlled
audio asset. Exact frame residues modulo 33, 66 and 132 were preserved without
selecting a phase origin. Raw strength was neither normalized nor ranked and
was never compared across sources.

Metric-reference assignment required an already-authorized, preregistered,
literature-grounded relation mapping phase-conditioned strength to metric role
while rejecting both adjacent hierarchy levels. Absence of that relation was
preregistered as `FAILED TEST`.

## Blind result

**FAILED TEST**

Existing onset-strength observations were reproduced deterministically, but
JGA authority contains no non-arbitrary rule converting their source-specific
phase distributions into metric-reference role. Creating a rule from these
outcomes was prohibited. No candidate was selected.

Blind result SHA-256: `eb17682f25233c50f08bf98d38689be55e45e48303edc9bbe65ff34e5b5c55b0`.

## Candidate hierarchy evidence

Counts are exact consecutive Candidate Period occurrences reproduced by the
unchanged pipeline; zero means absent in that source population.

| Source | PulseCandidates | 33 | 66 | 132 |
|---|---:|---:|---:|---:|
| full_mix | 77 | 7 | 8 | 0 |
| double_bass | 27 | 8 | 0 | 2 |
| drums | 63 | 19 | 15 | 0 |
| piano | 49 | 13 | 3 | 3 |
| tenor_sax | 16 | 0 | 0 | 0 |
| voice | 150 | 0 | 0 | 0 |

Every PulseCandidate's raw strength and exact phase residues are preserved in
`blind_result.json`. These are physical observations, not accent or metric
roles.

The strength-bearing replay does not reproduce the historical C1-04
33-frame counts for the full mix (`7` versus `16`) or piano (`13` versus `6`).
The relevant 66- and 132-frame counts agree. Because the frozen C1-03/C1-04
occurrences do not preserve strength, current strength observations cannot be
scientifically attached to every established historical occurrence without a
separately justified correspondence relation. That relation is outside this
experiment and is prohibited by the branch stop.

## Post-blind comparison

Only after the blind record was written and frozen was
`GT-VAL-001-v1` loaded. It specifies
78 quarter BPM and a
reference duration of `0.7692307692307692307692307692` seconds. Agreement is not
applicable because the blind test selected no metric-reference candidate.
Ground Truth did not alter the blind result.

## Scientific conclusion and branch stop

Phase-conditioned onset strength does not currently provide an authorized
blind discriminator among 33, 66 and 132 frames. Autonomous metric-reference
inference remains scientifically unresolved. Under the approved hard stop,
this metric-reference discrimination branch is closed and deferred.

The shortest architecture-consistent route to useful timing analysis is to
accept an explicitly declared, provenance-bound metric context as Domain input
while preserving Candidate Periods and PulseCandidates as observed/derived
evidence. Declared context must remain labeled as declared and must never be
reported as automatically recognized.
