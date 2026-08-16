# H-VAL001-RHYTHM-ROLE-01 — Frozen Result

Status: COMPLETE

Blind classification: `EQUIVALENT_HIERARCHICALLY_UNRESOLVED`

## Frozen evidence

The experiment retained all complete AD-037 EME populations: Drums 63
(`bdd60958...51ed`), Double Bass 27 (`80896b76...6164`) and Piano 49
(`357be2d0...72a2`). It imported, without regeneration, the four SHORT and
four LONG common-period identities frozen by `H-VAL001-RHYTHM-TEMPO-01`.

Every admissible integer-frame period and origin residue was evaluated as a
nuisance parameter. Neutral Poisson occupancy recurrence lengths were chosen
by the preregistered BIC rule over full, early and late scopes. The source vote
used SHORT-family persistence only; phase concentration was descriptive and
did not decide role.

## Blind organization result

| Source | SHORT full/early/late organization | LONG full/early/late organization | Source decision |
|---|---|---|---|
| Drums | all four `1/1/1` | all four `1/1/1` | `SHORT_FAMILY_PREFERRED` |
| Double Bass | `1/1/1`, then three `8/4/1` | two `4/4/1`, two `4/4/4` | `EQUIVALENT_OR_UNRESOLVED` |
| Piano | `1/1/1`, then three `8/1/1` | all four `4/4/4` | `EQUIVALENT_OR_UNRESOLVED` |

Only Drums supplied a family preference. Equal-source consensus requires two
votes and therefore remained hierarchically unresolved. The result does not
assign metric role. It shows source-specific higher-order occupancy structure,
including stable LONG-family length 4 for Piano and two Bass candidates, but
that evidence does not satisfy the frozen family-decision rule.

The full exact BIC model populations, nuisance origins, phase geometry and
2,000-resample intervals are preserved in `blind_result.json`. Early/late
replay is the preregistered temporal-persistence test. A second complete run
was scientifically identical.

## Firewall and post-freeze validation

Ground Truth, declared tempo/meter/timeline, normalized declared phases,
symbolic evidence and melodic/AI evidence were not accessed during blind
execution. Voice remains `DEFERRED`.

Blind result SHA-256:
`c674a2b9ddd9831b9babbdaf9e01b659c1ca044e5d90928bd5a7ee149eb7eda0`.

Scientific fingerprint:
`02912d34d5a5aeafa00b41131863a79b7ece77934e338bb3c923ff174298f5c7`.

Only after freeze, `GT-VAL-001-v1` revealed the authoritative reference. The
LONG family contains its reference period, but the blind criterion selected
neither family. Validation is therefore `UNRESOLVED`; metric-reference role is
not scientifically justified, autonomous BPM remains `PARTIAL`, and production
integration is not justified.
