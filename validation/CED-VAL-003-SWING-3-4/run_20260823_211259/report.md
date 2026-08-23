# CED-VAL-003 PulseCandidate Strength Measurement Authority

Study: `H-CEDVAL003-PULSECANDIDATE-STRENGTH-AUTHORITY-01`

Status: **PASS — FROZEN MEASUREMENT AUTHORITY**

The checksum-bound existing observation pipeline recovered exact
lineage-bound `PulseCandidate.strength` for all 112 observations in all 56
frozen `AMBIGUOUS_MULTIPLE_OBSERVED` cells. Two executions within each run and
a second complete run produced identical identities, timestamps, frames,
observation indices, binary64 strength/confidence values, memberships and
scientific fingerprint.

| Source | Recovered / expected | Minimum | Q1 | Median | Q3 | Maximum | Mean | Population SD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Drums | 108 / 108 | 2.1969642639160156 | 3.785744547843933 | 4.940913200378418 | 6.951123237609863 | 16.585954666137695 | 5.861741801102956 | 3.130443749440784 |
| Double Bass | 4 / 4 | 4.470448017120361 | 4.574449062347412 | 9.254493474960327 | 13.933147192001343 | 14.032976150512695 | 9.253102779388428 | 4.7138106192918965 |
| Piano | 0 / 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

Confidence is available through exact PulseCandidate lineage for all records
and is uniformly binary64 `1.0` (`0x1.0000000000000p+0`). It is preserved, not
interpreted as discrimination evidence.

This result establishes only deterministic, provenance-bound, within-source
physical measurement authority for strength in this population. No strength
ordering, selection, threshold, cross-source comparison, Ground Truth access,
correspondence scoring or discrimination test occurred. Historical H02 scores
and unscorable statuses remain frozen. H02, H03, Calibration Zero, raw
observations, architecture, production semantics and production code are
unchanged.

Scientific fingerprint:
`6903decbe3175db300002f148d5e4192f9c51ba8959a6534921675af753aa94d`.
