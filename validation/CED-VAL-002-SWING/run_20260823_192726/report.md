# H02 Out-of-Sample Validation — CED-VAL-002-SWING

Status: **FROZEN RESULT — PARTIAL_CORRESPONDENCE_EVIDENCE**

The unchanged `H-VAL001-RHYTHM-CORRESPONDENCE-02` rule was applied blind to
raw observations from corrected authority `PR-CED-VAL-002-SWING-002`.
Calibration quantities and symbolic evidence were excluded from candidate
generation.

## Blind freeze

Observed populations were Drums 192, Double Bass 127 and Piano 63.

| Source | Valid signature | Unique target→Drum | Unique Drum→target | Mutual unique | Recurrent Drum | Recurrent source | Candidates |
|---|---:|---:|---:|---:|---:|---:|---:|
| Piano, independent | 61 | 63 | 61 | 61 | 60 | 12 | 11 |
| Piano, cumulative | 61 | 61 | 59 | 59 | 58 | 11 | 11 |
| Double Bass, independent | 125 | 127 | 124 | 124 | 122 | 120 | 114 |
| Double Bass, cumulative | 125 | 125 | 122 | 122 | 119 | 114 | 114 |

The frozen blind population contains 125 candidates and 65 unresolved records.
Unresolved reasons overall: target signature not recurrent 54; reverse nearest
not unique 5; Drum signature not recurrent 4; target boundary 4; Drum boundary
4. Records may carry more than one reason.

Blind fingerprint:
`c053888ade8ddba30dad9abd11f4486dd9083640307d5c49feb409c389e28c08`.

## Post-freeze scoring

Only after blind freeze and replay, corrected CalibrationSymbolicEvent and
exact-equality symbolic-pair authorities scored candidates.

| Source pair | Candidates | TP | FP | FN | Ambiguous candidates | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Piano–Drums | 11 | 4 | 7 | 20 | 0 | 0.363636 | 0.166667 | 0.228571 |
| Double Bass–Drums | 114 | 109 | 3 | 9 | 2 | 0.973214 | 0.923729 | 0.947826 |
| Overall | 125 | 113 | 10 | 29 | 2 | 0.918699 | 0.795775 | 0.852830 |

The frozen classification is `PARTIAL_CORRESPONDENCE_EVIDENCE`. Compared with
CED-VAL-001 (13 candidates, 12 TP, 1 FP; precision 0.923077, recall 0.222222,
F1 0.358209), overall precision is similar and overall recall is higher, but
source-specific evidence is sharply mixed: Double Bass generalizes strongly
while Piano does not preserve conservative precision. The out-of-sample result
therefore provides `MIXED` generalization evidence.

Calibration remains a separate measurement question. Candidate identities and
scoring were not altered by the independently observed pairwise candidate
biases. If a relation is later authorized for temporal measurement, raw
displacement must be interpreted alongside the applicable calibration context;
no correction is currently authorized.

H02 remains experimental evidence. `GEOMETRIC_ONLY` remains production
authority. Raw observations are unchanged and production code was not modified.

Scientific fingerprint:
`ac6df971b4d1fb224c2324fb91cac85c04bb30062f86103f5681293dcd80c89e`.
