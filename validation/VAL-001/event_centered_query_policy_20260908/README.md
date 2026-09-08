# H-VAL001-EVENT-CENTERED-QUERY-POLICY-01 — accepted bounded execution

PASS — EVENT_CENTERED_MULTISCALE_PERIODICITY_QUERY_POLICY_VALIDATED.

One complete execution and one fresh-process replay under CPython 3.13.14:
A=18, B=18, C=18, D=30, H=0, I=18, Z=0 query records, total 102 per run.
Each run passed 175 checks with zero failures. All three canonical artifacts
(policy, provenance, score) are byte-identical between runs. Six final
preservation checks also passed. No result-driven changes or additional runs.

## Authority and implementation

The adjacent preregistration H-VAL001-EVENT-CENTERED-QUERY-POLICY-01.md is unchanged;
its SHA-256 is e8f4d2ff17ff445bf9633d9cf52d28af55262c77feeaf54556a3052606542292.
`source_freeze.json` records implementation hashes before execution.

- `constructor.py`: generic Fraction-based policy; no fixtures/expected answers.
- `run.py`: frozen input harness, provenance and source/runtime bindings.
- `oracle.py`: independent frozen pair, radial-shell and endpoint tables;
  no constructor import, pairwise-distance rediscovery or numerical operator.
- `score.py`: exact full-field comparison, transformation-table and addition checks.
- `encoding.py`: shared serialization only; contains no policy/oracle semantics.

Scale pairs retain ordered center/boundary roles; period pairs are unordered and
normalized lexically. Every query retains separate generation and evaluation
roles, complete overlap, and RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED status.
Hann endpoint/positive membership uses exact inequalities, not cosine evaluation.

`run_1` and `run_2` preserve the canonical policy, provenance and scoring artifacts.
`result.json` records counts, final checks and artifact SHA-256 values.
`SHA256SUMS` covers all package files except itself, plus the frozen preregistration.
No scientific fingerprint distinct from these artifact checksums is introduced.

## Limits

PASS concerns only the frozen seven synthetic populations and exact coordinate,
support, reciprocal, boundary/coverage and provenance rules, with deterministic
replay. It does not authorize recurrence, exhaustive continuous frequency coverage,
Fourier-response sufficiency, real Drum application, physical onset accuracy,
measurement-error interpretation, trajectories, periodic-level selection,
half/double resolution, BeatReference, musical phase, tactus, meter, downbeat,
BPM, accompaniment correspondence or visualization. No Fourier response was
computed and no real recording or real Drum EME was accessed for inference.

Historical evidence and unrelated working-tree changes were left untouched.
Only this experiment and its approved preregistration are included in preservation.
