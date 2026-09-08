# H-VAL001-CERTIFIED-SPARSE-QUERY-01 execution

This package implements only the frozen seven-query synthetic numerical validation.
The preregistration and environment binding remain unchanged. The preregistration's
historical environment-pending text is superseded prospectively by the separate
PI-approved binding, not edited retrospectively.

`evaluator.py` contains the generic sparse Hann operator and certified serialization.
It contains no fixture table, expected values, case dispatch or scorer import.
`run.py` supplies the exact frozen input constructions, hashes their provenance,
checks installed binary hashes, and sets 128-bit precision and FLINT threads=1.
`scorer.py` imports neither FLINT nor the evaluator. Its independent closed-form
oracle uses Fraction interval arithmetic, Machin's identity and Taylor remainder
bounds. It reads preserved operator output before evaluating the oracle. Translation,
dilation and superposition are checked against the preregistered reduced formulas.
Code and fixture review preceded execution; no post-result code changes were made.

Only the initial execution and the authorized fresh-process replay are permitted.
Files operator_1/2.json and score_1/2.json retain the complete canonical artifacts.
`result.json` records replay, checksums and final status. Scientific fingerprint
is SHA-256 of the canonical operator artifact, which includes construction manifests,
code hashes and frozen authority hashes. No runtime paths or clocks enter this artifact.

The environment lives in the separately bound, Git-ignored experiment venv.
No project dependencies, production code or historical scientific files were changed.
The complete object-store scan before preservation found no blob >=100 MiB.
Unrelated working-tree changes are excluded from this preservation commit.

Maximum PASS claim: CERTIFIED_SPARSE_COMPLEX_PERIODICITY_REAL_QUERY_EVALUATION_VALIDATED,
limited to the seven frozen fixtures, python-flint 0.9.0 / FLINT 3.6.0 and the
128-bit enclosure/serialization/scoring contract. No authority for real audio,
Drum periodicity, physical phase, frequency discovery, window selection, trajectories,
periodic-level selection, half/double disambiguation, BeatReference, musical phase,
tactus, meter/downbeat, BPM, accompaniment correspondence or visualization follows.
