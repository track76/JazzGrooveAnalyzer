# H-VAL001-BINARY64-CERTIFIED-INPUT-01

PASS — BINARY64_CERTIFIED_OBSERVATION_INPUT_ADAPTER_VALIDATED.

Exactly one eleven-fixture execution and one fresh-process replay under the frozen
CPython 3.13.14 / python-flint 0.9.0 / FLINT 3.6.0 environment, precision 128 bits,
FLINT threads=1. Each run passed 101 checks, zero failed: 202 scoring checks total.
Eight finite inputs were accepted and the three nonfinite inputs rejected as
preregistered. All six final preservation checks passed. Before adapter execution,
the independent integer IEEE decoder also verified the literal expected table.
No repairs, tuning, precision escalation, real-input adaptation or additional runs.

## Evidence and firewall

- inputs.json: exact pre-execution construction manifest, tokens and diagnostics.
- source_freeze.json: hashes of input manifest and adapter/harness/scorer sources.
- adapter.py: generic bit classification, lossless finite conversion, exact Arb
  input, signed-zero provenance; no expected answers, fixture dispatch or oracle.
- run.py: verifies bound runtime/binary hashes and source freeze; invokes adapter
  once per fixture; derives zero-origin scope from accepted F/H records.
- scorer.py: imports neither adapter nor FLINT. Uses independent frozen literal
  tables and integer/rational IEEE decoding, including separate float32 decoding.
- table_consistency.json: pre-execution independent oracle consistency result.
- run_1 and run_2: canonical adapter, scope/provenance and scoring artifacts.
- result.json: final decision, fixture statuses, preservation checks and hashes.
- SHA256SUMS: full package checksums plus frozen preregistration, excluding itself.

JSON numeric spellings are provenance only. Exact producer bits and dyadic values
are preserved; Arb containment uses exact rational endpoint comparisons. +0/-0
share rational zero but retain distinct original bits. Nonfinite values never
receive scientific ratios or enclosures. No approximate phase/period computation.

Scope aliases reference F (+0) and H (accepted binary64 duration). The diagnostic
3/10 is distinct and outside the accepted closed clipping interval. No sample-
rational substitution, nonzero-origin generalization or physical-accuracy claim.

## Claim limits

PASS covers only the frozen adapter fixtures, exact dyadic reconstruction,
certified conversion, signed-zero preservation, expected nonfinite rejection,
zero-origin scope semantics and canonical deterministic provenance. It does not
validate every binary64 encoding, physical onset/timing truth, recovery of upstream
information, recurrence, periodicity sufficiency, frequency discovery, window
optimization, real Drum periodicity, trajectories, level selection, half/double
resolution, BeatReference, musical phase, tactus, meter/downbeat, BPM,
accompaniment correspondence or visualization.

Frozen preregistration bytes and all historical evidence remain unchanged.
Unrelated working-tree changes are excluded from the preservation commit.
