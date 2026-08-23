# H02 Three-Dataset Scientific Conclusion

Status: **FROZEN — PI-AUTHORIZED EVIDENCE SYNTHESIS**

Authority: PI acceptance of frozen H02 results at commits `02a8452`,
`61cc6fd` and `59b604a`; AD-037, AD-038, AD-039, AD-040, F-030 and SVP-001.

## Frozen Scientific Status

`H-VAL001-RHYTHM-CORRESPONDENCE-02` is frozen as:

```text
EXPERIMENTALLY_SUPPORTED
SOURCE_SENSITIVE
REPLICATED_FOR_DOUBLE_BASS_DRUMS_UNDER_TESTED_CONTROLLED_CONDITIONS
NOT_GENERALIZED_FOR_PIANO_DRUMS
NOT_PRODUCTION_AUTHORIZED
```

H02 identifies useful blind accompaniment–Drum temporal-comparison candidates
from raw observational temporal structure without BPM, meter, measures,
BeatReference, symbolic inference input or an arbitrary millisecond threshold.
It does not establish universal correspondence, musical equivalence,
synchronization intent or stable source-independent performance.

## Independently Preserved Dataset Evidence

### CED-VAL-001

Classification: `LOW_RECALL`. Scientific fingerprint:
`2bf5ddb3c40620c3ddf5ebf8cbf7aad6d6ed74d770481d8eb921b579ad96c082`.

- Overall: 13 candidates, 63 unresolved, 0 ambiguous candidate, 1 unscorable
  symbolic relation; TP 12 / FP 1 / FN 42; precision `0.923077`, recall
  `0.222222`, F1 `0.358209`.
- Piano–Drums: 12 candidates; TP 11 / FP 1 / FN 25; precision `0.916667`,
  recall `0.305556`, F1 `0.458333`; 37 unresolved.
- Double Bass–Drums: 1 candidate; TP 1 / FP 0 / FN 17; precision `1.000000`,
  recall `0.055556`, F1 `0.105263`; 26 unresolved and 1 unscorable symbolic
  relation.

This is positive-but-conservative evidence from H02's first evaluation scope,
not an independent replication. Its Calibration Zero context reported
source-independent candidate absolute bias and no detectable Piano–Drums or
Double Bass–Drums pairwise bias; calibration fingerprint `d9ff1dba…`.

### CED-VAL-002-SWING

Classification: `PARTIAL_CORRESPONDENCE_EVIDENCE`; generalization `MIXED`.
Scientific fingerprint:
`ac6df971b4d1fb224c2324fb91cac85c04bb30062f86103f5681293dcd80c89e`.

- Overall: 125 candidates, 65 unresolved, 2 ambiguous/unscorable candidates,
  4 unscorable symbolic relations; TP 113 / FP 10 / FN 29; precision
  `0.918699`, recall `0.795775`, F1 `0.852830`.
- Piano–Drums: 11 candidates; TP 4 / FP 7 / FN 20; precision `0.363636`,
  recall `0.166667`, F1 `0.228571`; 52 unresolved and 2 unscorable symbolic
  relations.
- Double Bass–Drums: 114 candidates, 112 scorable; TP 109 / FP 3 / FN 9;
  precision `0.973214`, recall `0.923729`, F1 `0.947826`; 13 unresolved,
  2 ambiguous/unscorable candidates and 2 unscorable symbolic relations.

Calibration Zero independently reported source-specific candidate absolute
bias, mixed measurement behaviour and candidate pairwise bias for both pairs;
fingerprint `d4b0b18766cf2c69a367014704f2c2dc4429d977cdf8ddd27d767276b603d4e7`.

### CED-VAL-003-SWING-3-4

Classification: `PARTIAL_CORRESPONDENCE_EVIDENCE`; generalization `MIXED`.
Scientific fingerprint:
`374ab02a71c0e583bba33b5723550c50c935f4d4fd11722085f1d368170d0987`.

- Overall: 89 candidates, 61 unresolved, 56 ambiguous/unscorable candidates,
  55 unscorable symbolic relations; 33 candidates were scorable; TP 29 / FP 4
  / FN 15; precision `0.878788`, recall `0.659091`, F1 `0.753247`.
- Piano–Drums: 14 candidates, 5 scorable; TP 3 / FP 2 / FN 9; precision
  `0.600000`, recall `0.250000`, F1 `0.352941`; 36 unresolved,
  9 ambiguous/unscorable candidates and 9 unscorable symbolic relations.
- Double Bass–Drums: 75 candidates, 28 scorable; TP 26 / FP 2 / FN 6;
  precision `0.928571`, recall `0.812500`, F1 `0.866667`; 25 unresolved,
  47 ambiguous/unscorable candidates and 46 unscorable symbolic relations.

Calibration Zero independently reported source-specific candidate absolute
bias and mixed measurement behaviour; both pairwise outcomes were
`INSUFFICIENT_EVIDENCE` after mandatory sensitivity support. Fingerprint:
`589ee3c15783556bd0e5b7b6df53822dff56c1eddfb6d17476aa3152adef5270`.

The 56 ambiguous/unscorable candidates and 55 unscorable symbolic relations
remain evidence, not TP, FP or FN. They limit precision/recall inference to the
33 scorable candidates and materially limit completeness of CED-VAL-003's
generalization assessment. They do not authorize rematching or retrospective
reinterpretation.

## Cross-Dataset Conclusions

The arithmetic aggregate is descriptive only: 227 blind candidates, 169
scorable, TP 154 / FP 15 / FN 86, precision `0.911243`, recall `0.641667` and
F1 `0.753056`. It is not a pooled estimate of universal performance and cannot
hide source, dataset, ambiguity or Calibration Zero differences.

Double Bass–Drums strong source-specific behavior replicated across the two
independent controlled datasets on which substantial scorable populations
were available:

- CED-VAL-002: precision `0.973214`, recall `0.923729`, F1 `0.947826`;
- CED-VAL-003: precision `0.928571`, recall `0.812500`, F1 `0.866667`.

This is replication under tested controlled conditions, not universal
validity. CED-VAL-001's one conservative Bass candidate remains preserved in
its original scope and neither establishes nor contradicts population-level
replication.

Piano–Drums does not show stable conservative behavior across the three
datasets. Its precision is `0.916667`, `0.363636` and `0.600000` respectively.
No Piano-specific rule or explanation is authorized. An explicit AD-040
`ACCOMPANIMENT` assignment declares analytical inclusion only; it does not
imply that evidence or rules validated for one accompaniment source generalize
to another.

Source sensitivity is therefore demonstrated descriptively. Aggregate
performance does not establish a source-independent correspondence model.

CED-VAL-003 demonstrates useful Double Bass–Drums evidence on a controlled 3/4
swing source without providing meter or tempo to H02. Neither 3/4 nor swing is
established as a cause of any result difference.

## Calibration, Production and Interpretation Firewalls

Every Calibration Zero remains independent, provenance-bound context.
Calibration evidence did not create, remove, move, rank, correct or score H02
candidates. No mathematical correction is authorized; raw timing remains
authoritative.

Production promotion is not justified. AD-040 `GEOMETRIC_ONLY` remains
authoritative; no candidate becomes `AUTHORIZED_EVENT_RELATION`. H02 is
unchanged, H03 does not exist, AD-040 is unchanged, and no source-specific
production rule is created.

## Ranked Remaining Uncertainty

1. **Ambiguity/scorability authority:** CED-VAL-003 leaves 56 candidates
   unscorable, limiting what its apparently conservative evidence can support.
2. **Piano–Drums source sensitivity:** its cross-dataset variation remains
   unexplained and cannot be attributed to density, role, meter or swing.
3. **Production validity:** tested controlled evidence does not establish
   behavior on human recordings or define a promotion gate.
4. **Double Bass scope:** strong replication exists under two controlled
   conditions, but universal or human-performance generalization is untested.

The smallest next falsifiable question is whether CED-VAL-003's unscorable H02
candidates are limited by frozen calibration-correspondence authority rather
than by missing blind candidate evidence. A preregistered, read-only authority
audit must classify the provenance-bound causes without rematching, changing
H02 or rescoring existing outcomes. This addresses the largest current loss of
scientific information before rule development or production consideration.

## Scientific History

The non-retroactive record remains:

```text
H01 preregistration and zero-candidate falsification
→ frozen failure audit
→ removal of exact cross-source signature equality only
→ H02 preregistration and CED-VAL-001 evidence
→ independent CED-VAL-002 authority, correction history and Calibration Zero
→ unchanged blind H02 mixed generalization result
→ further replication requirement
→ independent CED-VAL-003 authority and Calibration Zero
→ unchanged blind H02 replication
→ three-dataset conclusion
```

Negative, partial, ambiguous, insufficient, superseded and positive evidence
remains recoverable. Architecture impact and production impact are **NONE**.
