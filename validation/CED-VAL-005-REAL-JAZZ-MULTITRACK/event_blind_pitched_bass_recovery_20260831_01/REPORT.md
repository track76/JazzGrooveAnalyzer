# CED-VAL-005 event-blind continuous pitched-Bass recovery

## 1. Preregistration

- ID: `H-CEDVAL005-EVENT-BLIND-CONTINUOUS-PITCHED-BASS-RECOVERY-01`.
- Fingerprint: `e53092e289d0ab4f2e5a64abc86eb0a8b549cd26e590462faf89f4e4cc134913`.
- Preregistration commit: `f848538`.

## 2. Transferred scanner authority

Scientific authority was the frozen CED-VAL-006 scanner protocol
`H-CEDVAL006-EVENT-BLIND-CONTINUOUS-PITCHED-BASS-RECOVERY-01`, fingerprint
`eda2bbe72c7a870e00c3d0d1ec5b90e100c29d93bf0d81d33a4141de729c9672`.

The sole signal adaptation was `SAMPLE_RATE_FRONTEND_ADAPTATION`: CED-VAL-006
required deterministic 48 kHz to 44.1 kHz resampling; CED-VAL-005 is already
native 44.1 kHz, so resampling was bypassed and native samples entered the
unchanged 44.1 kHz analysis domain. The input assertion changed from 48,000 to
44,100 Hz. The candidate protocol identifier changed as provenance metadata.
All scientific scanner and evaluator parameters remained unchanged.

Two bounded post-freeze evaluator schema corrections are preserved in
`EVALUATION_REMEDIATION.md` and `EVALUATION_REMEDIATION_2.md`. Neither changed
scientific behavior or the candidate authority.

## 3. Candidate authority

- Controlled-mix SHA-256: `7d9d3f1f07f7760152ce560ae0bbb6f1706b443278a41af4a31dfb2638396a0f`.
- Blind candidates: 661.
- Candidate JSON SHA-256: `c32a6fb232b5615f0566c0495856079a8b77a56dba77e29ec27dc64a20fc6368`.
- Candidate fingerprint: `7c3dbff7bc0282b8031f53a6acd5d365a739056d9e075e1a649b1d829132ce1d`.
- Candidate freeze commit: `b23615a`.
- Candidate replay: byte-identical.

## 4–5. Evaluation counts and metrics

- Original Bass EME: 1,138.
- Frozen htdemucs_ft recovered/missed: 782/356.
- Blind candidates matched to any original Bass: 339.
- Matched to already-recovered Bass: 241.
- Event-blind candidates corresponding to previously missed Bass: 98.
- Unmatched candidates: 322.
- Candidate precision: 0.5128593040847201; Wilson 95% CI
  [0.4747908995545987, 0.5507791063083853].
- Scanner-only all-original recall: 0.29789103690685415.
- Scanner-only F1: 0.3768760422456921.
- Missed-population recall: 0.2752808988764045; Wilson 95% CI
  [0.2314682308776882, 0.32389150859100213].
- Incremental all-original coverage: 0.08611599297012303, or +8.6116
  percentage points.
- Explanatory retrospective combined coverage: 880/1,138 =
  0.773286467486819, compared with frozen htdemucs_ft recall
  0.687170474516696.
- Unmatched candidates per newly corresponding missed observation:
  3.2857142857142856.

The combined quantity is explanatory only. No union or production recovery
was constructed.

## 6. Timing displacement

- Median absolute: 0.023219954648524777 s.
- Q1: 0.011609977324262388 s.
- Q3: 0.03482993197278894 s.
- RMSE: 0.02714371158451402 s.
- Maximum: 0.046439909297077975 s.
- Median signed: 0.0 s.

These are observation-to-observation displacements, not physical-onset errors.

## 7. Independent pitch evidence

Among 98 temporal correspondences to the missed population, 93 (94.90%) were
independently BassDI-pitch-evaluable. Twenty-one were compatible within the
frozen 50-cent, no-octave-folding rule: 0.22580645161290322, Wilson 95% CI
[0.15270154318255835, 0.32066450663678026]. Compatible errors had median 10
cents, Q1 5, Q3 20, and RMSE 18.03 cents.

Across all temporal matches, 327/339 were pitch-evaluable and 83/327 (25.38%)
were compatible. A temporal match does not establish pitch correctness or
unique Double Bass source identity.

## 8–9. Decision gates and classification

`USEFUL_CANDIDATE_RECOVERY` failed: recall, precision, timing, and pitch
evaluability passed, but unmatched/new was 3.286 (>2) and missed-match pitch
compatibility was 22.58% (<50%).

`PARTIAL` failed only its pitch-compatibility condition: 22.58% was below the
frozen 25% minimum. Its missed recall, precision, unmatched/new burden, median
timing, and evaluability conditions passed. No gate was changed.

Final classification:

`EVENT_BLIND_PITCHED_BASS_RECOVERY: INSUFFICIENT`

## 10–11. Replay, integrity, and evidence commit

- Evaluation replay: byte-identical.
- Evaluation JSON SHA-256: `de0cb6e286d5a2976893c9cbf32a80e241ba3bead6e3782b0fc7a6e2957a43cb`.
- Result fingerprint: `fab096aaa7ff45b4d235a7d601b6ebe2a7eb93fa762d45d2cb93a0b87f7d80b7`.
- Both failed technical launches and both bounded remediations are preserved.
- Candidate authority remained byte-identical across all evaluation attempts.

## 12–13. Limitations and source-specificity audit decision

The full mix contains acoustic piano and other pitched instruments. Temporal
correspondence does not validate a Bass event or establish source identity.
The 322 unmatched candidates are an omnibus burden, not proven false acoustic
events. BassDI pitch is an estimator-derived isolated-source proxy, not
symbolic-note or physical-onset Ground Truth. No swing, material, masking,
source-specificity, AD-037/038/040, or RhythmSectionTimingProfile conclusion is
authorized.

Although 98 missed observations received temporal correspondences, the
preregistered minimum candidate-recovery classification was not achieved.
Therefore a separate Bass-versus-acoustic-Piano source-specificity audit is
not gate-justified from this experiment and was not started.

JGA production/scientific implementation was not modified. Nothing was pushed.
