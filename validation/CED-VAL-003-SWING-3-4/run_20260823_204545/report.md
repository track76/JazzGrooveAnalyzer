# H02 Independent Replication — CED-VAL-003-SWING-3-4

Status: **FROZEN RESULT — PARTIAL_CORRESPONDENCE_EVIDENCE**

The unchanged `H-VAL001-RHYTHM-CORRESPONDENCE-02` rule was applied blind to
raw observations from `PR-CED-VAL-003-SWING-3-4-001`. Symbolic Ground Truth,
declared 3/4/tempo and Calibration Zero quantities were excluded from candidate
generation.

## Blind freeze

Observed populations were Drums 155, Double Bass 100 and Piano 50.

| Source | Valid signature | Unique target→Drum | Unique Drum→target | Mutual unique | Recurrent Drum | Recurrent source | Candidates |
|---|---:|---:|---:|---:|---:|---:|---:|
| Piano, independent | 48 | 50 | 50 | 50 | 48 | 14 | 14 |
| Piano, cumulative | 48 | 48 | 48 | 48 | 48 | 14 | 14 |
| Double Bass, independent | 98 | 100 | 96 | 96 | 96 | 80 | 75 |
| Double Bass, cumulative | 98 | 98 | 94 | 94 | 92 | 75 | 75 |

The blind population contains 89 candidates and 61 unresolved records
(Piano 36; Double Bass 25). Failure-reason occurrences are: target signature
not recurrent 52; reverse nearest not unique 4; target boundary 4; Drum
boundary 4; Drum signature not recurrent 2. Records may carry multiple reasons.

Blind fingerprint:
`a76e37eda621a266832a4fd347b9ac7334a3d12e2c94351dfdc5fa1dd9faa997`.
Two complete blind executions were byte-identical.

## Post-freeze scoring

Only after blind freeze and replay, checksum-frozen CED-VAL-003
CalibrationSymbolicEvent and exact-equality symbolic-pair authority scored the
immutable candidates.

| Source pair | Candidates | Scorable | TP | FP | FN | Ambiguous candidates | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Piano–Drums | 14 | 5 | 3 | 2 | 9 | 9 | 0.600000 | 0.250000 | 0.352941 |
| Double Bass–Drums | 75 | 28 | 26 | 2 | 6 | 47 | 0.928571 | 0.812500 | 0.866667 |
| Overall | 89 | 33 | 29 | 4 | 15 | 56 | 0.878788 | 0.659091 | 0.753247 |

The frozen classification is `PARTIAL_CORRESPONDENCE_EVIDENCE`. Conservative
candidate evidence replicates overall among scorable candidates. Double
Bass–Drums provides supporting replication evidence on this dataset. Piano–
Drums remains materially weaker and does not establish stable conservative
behavior across datasets. Source sensitivity therefore remains evident.

## Post-freeze three-dataset comparison

- CED-VAL-001: 13 candidates, 12 TP / 1 FP, precision 0.923077, recall
  0.222222, F1 0.358209; Piano 11/1 and Double Bass 1/0.
- CED-VAL-002: 125 candidates, 113 TP / 10 FP, precision 0.918699, recall
  0.795775, F1 0.852830; Piano 4/7 and Double Bass 109/3.
- CED-VAL-003: 89 candidates, of which 33 are scorable; 29 TP / 4 FP,
  precision 0.878788, recall 0.659091, F1 0.753247; Piano 3/2 and Double Bass
  26/2 among scorable candidates.

This is `MIXED` generalization evidence: the rule repeatedly finds useful
conservative evidence, particularly for Double Bass–Drums in the two
independent replications, while Piano evidence and scorable coverage remain
dataset-sensitive. Aggregate precision does not override that divergence.
No causal claim is made about meter, swing, density or instrument role.

Calibration remained separate context and did not create, remove, move, rank
or correct candidates. The large unscorable population follows frozen
Ground-Truth correspondence ambiguity and remains preserved; it was not
retuned away.

H02 remains experimental and source-sensitive. Production promotion is not
authorized because three-dataset evidence is mixed, Piano behavior is not
stable, and 56 candidates are unscorable under frozen authority.
`GEOMETRIC_ONLY` remains authoritative. Raw observations and production code
are unchanged.

Scientific fingerprint:
`374ab02a71c0e583bba33b5723550c50c935f4d4fd11722085f1d368170d0987`.
