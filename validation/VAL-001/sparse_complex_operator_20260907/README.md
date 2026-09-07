# Sparse complex operator: exact representation validation

Result: **LOCAL_COMPLEX_PERIODICITY_REPRESENTATION_VALIDATED**.
Scope: the preregistered synthetic sparse measures, 64 unique queries, and
the CPython 3.13.14 Q(zeta_16) exact-arithmetic path only. Comparison tolerance zero.

Authority: ../preregistrations/H-VAL001-SPARSE-COMPLEX-OPERATOR-01.md and its
companion .inputs.json; exact authority and implementation hashes are in freeze.json.
Historical designs were preserved byte-for-byte. No production JGA code changed.

## Execution evidence

The first execution completed before a usage interruption: run_1.json and
score_1.json contained 64 queries and 1329 passing checks. On resumption, all
four authority checksums, frozen source hashes and prepared input checksum were
verified before continuing. Only the pending fresh-process replay was executed.
run_2.json and score_2.json also contain 64 queries and 1329 passing checks.
No mismatch occurred. Total operator evaluations: 128 over 64 unique queries.

Both operator outputs are byte-identical, SHA-256:
72c213a605c63f01b62fa36dc4bb5a12bfa677066432064bd26f6571e2fb0f77.
Both scorer outputs are byte-identical, SHA-256:
2e3044e57ece8e77084fa68122e4b33cbd3ff1e28a19668e1ac9eccd4aeb2f04.
The scientific fingerprint is explicitly defined as the canonical operator-output
SHA-256, not as a fingerprint of musical/audio validity.

Properties: periodic responses (24 component-control records), linearity (8),
translation/phase (8), dilation (8), nested structure (8), superposition (8).
Closed-form oracle agreement, exact symbolic magnitude/phase, constructive addition,
destructive cancellation, complete population and event provenance all passed.
Zero cancellation retains undefined phase. Full checks are in score_1.json.

The resumption included an unsupported `protocol.py --help` invocation. Its
authorization guard rejected the argument before importing the evaluator or
executing any query. It changed no artifact and was not an experiment run.
No implementation or oracle was changed after source freeze or after results.

## Separation and provenance

evaluator.py imports only Fraction and exact_field.py. It receives event records,
query coordinates and parameter authority, never condition labels or oracle answers.
protocol.py supplies the construction/query harness and attaches provenance.
scorer.py is invoked only after outputs exist; its independent polynomial arithmetic
and frozen algebraic tables do not call the evaluator or its window summation.
Source syntax/import checks preceded freeze; no additional query domain was tested.

prepared_inputs.json preserves exact source/derived manifests, event identities,
parent construction hashes, transformations and the 64 fixed query coordinates.
freeze.json binds source files before execution. runtime.json records the environment.
result.json, replay.json and preservation.json preserve final checks and scope.
package_checksums.json additionally binds the complete preserved package, excluding
itself. Historical accepted VAL-001 canonical SHA remains
eeb189217a722679d5f40bef4d809e2b38ab381e9dea81057023dfd3d80e05c7.

## Limits and next action

This result establishes neither real-audio/detector validity nor sparse/full-novelty
equivalence, generic floating-point correctness, frequency search/discovery, window
optimization, trajectory linking, periodic-level selection, half/double resolution,
BeatReference, musical phase, tactus, meter, downbeat, BPM, accompaniment correspondence
or visualization. No audio, detector, Demucs, Bass/Piano or JTD was used.

Smallest recommended next step: PI review and freeze this bounded result as the
mathematical baseline before authorizing any separate sampling/search specification.
No next experiment is begun. The scripts refuse to overwrite completed run artifacts.
