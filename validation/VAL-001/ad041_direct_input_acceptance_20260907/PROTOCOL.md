# VAL-001 prospective AD-041 direct-input acceptance

Decision authority: user continuation instructions dated 2026-09-07 and
[AD-041](../../../docs/architecture/AD-041_DIRECT_INPUT_AUDIOSTEM_METRIC_SOURCE_IDENTITY.md).
Baseline: `2b016ee050ab70c436caff7d856f02bc1dd671c0` on
`scientific/translation-layer-finalization`; AD-041 architecture commit
`9038dbd1e5c973bf9a4a32b5cc740e557a473cb0`.

The generated local bootstrap declared `aae86a1` and was stale. The user
explicitly superseded that declaration with the baseline above. Its historical
metadata is retained; the previous administrative stop is not experimental
evidence. This prospective record preserves the clarification in the repository.

Use only the checksum-bound [direct-input authority](../authorities/AD-041_DIRECT_INPUT_SOURCE_INSTANCE_AUTHORITY_V1.json)
(SHA-256 `b3a76361f30a0dbbc0b79cd15b4a7485ec66b95c42d2cd2c076cb783ee9da347`).
UUID inputs are exclusively its opaque authority ID and source-instance key.
Labels identify validation partitions, never source identity inputs.

AD-041 DERIVED IDENTITY FOR NON-NULL SEPARATORS:
DEFERRED — SEPARATOR AUTHORITY NOT YET ESTABLISHED.
No separated-output identity is authorized or validated here.

Capture a new baseline execution from the exact preserved HEAD, without
rewriting any historical evidence. Compare corrected execution against this
baseline: 63 Drums, 49 Piano, 27 Double Bass EME, 76 accompaniment relationships,
all GEOMETRIC_ONLY. Require exact non-identity scientific field equality,
including strengths/confidence, producer coordinates, temporal scope/origin,
reference timestamps, displacements, boundary and tie behavior, and roles/assets.
Operational wall-clock creation times are excluded explicitly. Identity-dependent
UUIDs and fingerprints may change; no other scientific change is permitted.
Stop on unexpected scientific changes; do not compensate or tune.

Only after the invariance gate passes, project authoritative seconds to
milliseconds by multiplication by 1000 and require canonical byte-identical
replay, distinct preserved source identities (all display names may be Mix),
relocation/rename invariance, and independent asset identity.

The report describes only ANALYZABLE observations supported by sufficient
evidence relative to the authorized Drum reference. It does not reconstruct
missing events, claim complete-performance coverage, infer timing for
NOT_ANALYZABLE material, or treat missing evidence as musical absence. It makes
no groove, swing, rushing, dragging, beat, tactus, meter, downbeat or BPM claim,
and establishes no physical-onset or human-microtiming Ground Truth.
Scientific status remains GEOMETRIC_ONLY.

## Execution and replay

The baseline snapshot was executed with `PYTHONPATH` pointing exclusively to
`src` exported by `git archive 2b016ee050ab70c436caff7d856f02bc1dd671c0 src`
in a temporary directory. It is a new baseline execution, not a modified
historical result. `snapshot.py baseline <new-file>` captures the baseline;
`snapshot.py corrected <new-file>` captures the bound prospective path.
`invariance.py` compares these records exactly with the explicit identity-field
exclusions visible in its source. EME and supporting-observation IDs are mapped
to their asset/timestamp or asset/index/timestamp counterparts before comparison;
source-dependent UUIDs and fingerprints are excluded. Operational creation
wall-clock values are recorded as excluded, not compared as observations.

After the gate passed, the valid millisecond projections in the paused report
service WIP were retained and completed prospectively. Commit `727b76e` was
inspected, not merged, cherry-picked or published. The paused acceptance folder
was not overwritten. The new acceptance independently verifies all three
partitions, including both accompaniment populations; it does not inherit the
paused script's source-name partition assumptions or status-count assertion.

From the repository root, replay to a fresh directory without overwriting
preserved records:

```sh
PYTHONPATH=src .venv/bin/python validation/VAL-001/ad041_direct_input_acceptance_20260907/acceptance.py /private/tmp/jga-ad041-new-replay
```

The script verifies the preserved identity gate, runs the public CLI twice,
requires byte equality, and compares an independent pipeline capture with the
canonical report. The complete final non-identity content is compared against
the identity-gated execution, with every new millisecond field checked exactly.
The CLI argument `--source-identity LABEL=AUTHORITY=KEY` binds a display label to
caller-provided opaque authority; `--expected-sha256 LABEL=SHA256` independently
binds the asset. Neither label nor checksum enters the source UUID derivation.

The validated source manifest and checksums are preserved alongside the results.
Absolute input paths are locators included in the canonical execution report;
relocation preserves source and asset identity, while the recorded locator may
change. Exact byte replay uses the same invocation and environment.
