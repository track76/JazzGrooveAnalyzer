# H02 CED-VAL-002-SWING Out-of-Sample Scientific Conclusion

Status: **FROZEN — PI ACCEPTED**

Authority: PI review of the frozen out-of-sample result at commit
`61cc6fdfd3a0234331735a51d821ffa5cc367822`, scientific fingerprint
`ac6df971b4d1fb224c2324fb91cac85c04bb30062f86103f5681293dcd80c89e`,
AD-037, AD-038, AD-039, AD-040, F-030 and SVP-001.

## Frozen Scientific Conclusion

`H-VAL001-RHYTHM-CORRESPONDENCE-02` demonstrated that blind observational
temporal structure can recover useful accompaniment–Drum temporal-comparison
candidates without BPM, meter, measures, BeatReference, symbolic input during
candidate generation or an arbitrary millisecond threshold.

The rule's frozen scientific status is:

```text
EXPERIMENTALLY SUPPORTED
SOURCE-SENSITIVE
CONSERVATIVE IN SOME CONDITIONS
NOT PRODUCTION-AUTHORIZED
```

Independent corrected dataset `PR-CED-VAL-002-SWING-002` provides strong
source-specific evidence for Double Bass–Drums under the tested conditions,
but Piano–Drums did not preserve conservative behavior. H02 is therefore not
demonstrated to be a source-general accompaniment correspondence rule. Overall
precision cannot replace or hide contributor-specific evidence.

## Frozen Evidence

### CED-VAL-001

- blind candidates: 13;
- true positives: 12;
- false positives: 1;
- precision: `0.923077`;
- recall: `0.222222`; and
- F1: `0.358209`.

This remains positive-but-conservative, low-recall evidence from the dataset
on which H02 was first evaluated.

### CED-VAL-002-SWING

Observed EME populations were Drums 192, Double Bass 127 and Piano 63. H02
produced 114 Double Bass candidates and 11 Piano candidates. These are frozen
observations; neither event density nor analytical role is established as the
cause of the source-specific result.

Piano–Drums:

- TP 4 / FP 7 / FN 20;
- precision `0.363636`;
- recall `0.166667`; and
- F1 `0.228571`.

Double Bass–Drums:

- TP 109 / FP 3 / FN 9;
- precision `0.973214`;
- recall `0.923729`; and
- F1 `0.947826`.

Overall:

- TP 113 / FP 10 / FN 29;
- precision `0.918699`;
- recall `0.795775`; and
- F1 `0.852830`.

The frozen classification is `PARTIAL_CORRESPONDENCE_EVIDENCE`; generalization
evidence is `MIXED`. Double Bass–Drums constitutes strong independent evidence
for this tested dataset. It does not establish universal Bass–Drums
correspondence. Piano–Drums supplies negative/partial source-specific evidence
that must remain visible and must not be optimized away.

Similar aggregate precision across CED-VAL-001 and CED-VAL-002-SWING does not
establish stable cross-source behavior.

## Production and Calibration Firewalls

Production promotion is not justified. AD-040 `GEOMETRIC_ONLY` remains the
authoritative production status. H02 candidates remain experimental evidence
and are not `AUTHORIZED_EVENT_RELATION`.

CED-VAL-002 Calibration Zero independently found source-specific and pairwise
measurement behavior. That evidence did not create, delete, move, select or
rescore H02 candidates. Correspondence evidence and measurement calibration
remain separate scientific questions. No mathematical correction is
authorized.

H02 is unchanged. No H03, Piano-specific rule, Bass-specific rule, threshold,
tolerance, recurrence modification, mutual-nearest modification or
calibration-derived correspondence adjustment is created.

## Mandatory Further Independent Validation

At least one further genuinely independent controlled dataset is required
before production promotion may be reconsidered. Replication—not rule
optimization—is the next scientific step.

The minimum dataset must:

1. be checksum-bound and unused in H01/H02 construction, audit or prior
   evaluation;
2. contain independently rendered Drums, Double Bass and Piano sources;
3. preserve an authoritative common controlled temporal origin;
4. provide deterministic, checksum-bound symbolic Ground Truth concealed
   during blind inference;
5. undergo its own provenance-bound absolute and pairwise Calibration Zero;
6. execute the complete frozen H02 rule unchanged and blind-first;
7. freeze candidates, unresolved evidence, fingerprints and deterministic
   replay before Ground Truth access; and
8. preserve Piano–Drums and Double Bass–Drums scoring separately as well as
   overall scoring.

Variation in temporal texture is scientifically desirable, but musical
content must not be chosen to favor H02. No result from CED-VAL-001 or
CED-VAL-002 may tune the replication rule.

## Scientific History

The publication-relevant history remains non-retroactive:

```text
H01 preregistration
→ zero-candidate falsification
→ frozen failure-mode audit
→ removal of exact cross-source signature equality only
→ H02 preregistration
→ CED-VAL-001 positive-but-conservative evidence
→ independent validation requirement
→ CED-VAL-002-SWING construction
→ PI correction with superseded authority preserved
→ corrected dataset authority
→ independent Calibration Zero
→ unchanged blind H02 out-of-sample execution
→ mixed source-specific generalization evidence
→ further independent replication required
```

This sequence is not a linear success narrative. Negative, partial, positive,
superseded and unresolved evidence remains preserved. Architecture and
production impact are **NONE**.
