# Prospective operational acceptance — completed

Classification: **CONDITIONALLY_VALIDATED_GEOMETRIC_OPERATIONAL_PATH**.
The PI explicitly resolved the stereo preparation stop documented below.
The new production chain was executed twice; historical results were not
relabeled as this acceptance.

Open these operational figures first:

1. [Absolute analyzable timeline](figures/absolute_timeline.png) — 3240 × 1260 px.
2. [Drum-relative analyzable timing](figures/drum_relative_timing.png) — 3240 × 1440 px.

SVG versions have the same basenames. Figures contain only Demucs-derived
observations; they do not overlay independent reference observations. SVG IDs
trace each point through [plot-data](figures/plot_data.json) to a canonical EME.
All coordinates are canonical seconds or their exact multiplication by 1000.
No jitter, connecting trajectories, smoothing, or inferred metric grid is used.

| Source | Reference | Operational | Matched | Reference-only | Operational-only | Preservation | Precision | F1 | Median absolute / RMSE (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Drums | 909 | 874 | 862 | 47 | 12 | 94.8295% | 98.6270% | 0.966910 | 5.297 / 7.690 |
| Double Bass | 1055 | 534 | 526 | 529 | 8 | 49.8578% | 98.5019% | 0.662052 | 6.023 / 20.818 |
| Piano | NOT_ESTABLISHED | 381 | NOT_ESTABLISHED | — | — | NOT_ESTABLISHED | — | — | NOT_ESTABLISHED |

These are observable-evidence measurements under the frozen matcher, not
percentages of all musical notes or physical-onset accuracy. Maximum matched
absolute displacement is 23.002 ms for Drums and 189.025 ms for Double Bass.
Full signed/absolute distributions and every unmatched timestamp are preserved
in [preservation.json](preservation.json). Uniform missingness and its cause
are not established. No compensation is applied.

AD-038 localizes 915 accompaniment EME (534 Bass + 381 Piano). AD-040 represents
1789 EME including 874 Drum references; all 915 relationships are GEOMETRIC_ONLY.
For matched Bass observations, nearest Drum identity is preserved in 507/516
scorable comparisons, preceding in 426/519, following in 418/511. Unmatched
references remain unscorable. Aggregate operational populations include Piano;
the independent reference contains only Drums and Bass. Aggregate differences
must not be interpreted as Piano preservation.

Reference resolution is 512/48000 seconds; separated resolution is 512/44100
seconds. Cross-grid numerical differences do not confer sub-frame physical
onset authority. The controlled mix is a deterministic derived mix, not a
provider/commercial mix or common acquisition-clock/physical-onset authority.

The authoritative prospective result is
[canonical_operational_report.json](canonical_operational_report.json), SHA-256
`6ff7a92dc32ebf77c52e75bd6cd6f9f8456308481ccc889fd6550a4dd14b58b3`,
scientific fingerprint
`620feb2e561637dc3e269bef262e309daec8cfa846aae3a84c3a5c32b7c07f02`.
Both original run reports remain preserved. Their runtime path locators differ;
as preregistered, only those locators are externalized to execution records
before creating the byte-identical canonical scientific report. No source,
asset, observation or geometry fields are excluded from scientific replay.
The report's fingerprint is recalculated for this explicitly defined projection.

All six original WAVs are retained separately for both new executions under
`$JGA_EXTERNAL_ROOT/experiments/CEDVAL006-AD041-HTDEMUCS6S-OPERATIONAL-20260907/`.
Every pair is byte-identical and matches the frozen M2 output bytes. Source
UUIDs are stable across runs and independent of those checksums. The prepared
input checksums are additional representation provenance, not replacement
WAV identities.

The first separation completed but the initial enumerator also counted macOS
AppleDouble sidecars. This integration failure occurred before observation;
`run_1_resume_authority.json` binds the untouched newly generated WAVs used to
resume after the enumerator fix. No separation or detector parameter changed.

Historical reports omit strength/confidence. Exact prepared-signal bytes and
all timestamp/strength/confidence values were therefore independently checked
against the frozen historical preprocessing code and unchanged detector on the
same new output assets: [preparation_replay.json](preparation_replay.json).
The historical report's available timestamps/frame/sample/index populations
also match exactly for Drums/Bass. No missing historical values were fabricated.

Verification: 15 focused handoff/report tests passed; 633 scientifically
relevant broader regressions passed; 3 strengthened handoff tests passed.
Two fresh rendering processes produced byte-identical PNG/SVG/plot-data.
See [result.json](result.json), [PROTOCOL.json](PROTOCOL.json), and
[visualization verification](figures/visualization_verification.json).
Re-run `verify_preparation_replay.py`, `validate.py`, two `render.py --output`
executions (repository figures and a temporary directory), then `finalize.py`
for artifact verification. `execute.py` runs production separation and is not
needed merely to inspect or verify preserved reports; it refuses overwriting
new execution directories. Its explicit first-run resume is checksum-bound.

Recommendation: a separate PI-authorized internal BPM investigation may be
considered only with a preregistered scope acknowledging these observed-subset
and reference limitations. This acceptance establishes no BPM validity. No BPM,
JTD, recovery, tuning or musical interpretation work was performed.

The architecture is documented in
[the AD-041 operational binding](../../../docs/architecture/AD-041_HTDEMUCS6S_OPERATIONAL_BINDING.md).
The original preimplementation authority snapshots below and their status
strings record when they were frozen; they do not override this completed
prospective result. Prior administrative stops remain historical facts.

---

## Preserved preimplementation diagnostic record

# AD-041 Demucs operational reintroduction — prospective authority

Status: **AUTHORITY ESTABLISHED; OPERATIONAL HANDOFF BLOCKED**.
This is not an end-to-end acceptance result or a scientific failure.

The PI authorization of 2026-09-07 resolves the prior parent-binding and model
selection stop. The baseline is `8e6a626ef00c4e51f2769a051180a080704e24f8` on
`scientific/translation-layer-finalization`. No historical identities,
fingerprints, reports, or model parameters are changed.

## Prospective decision

[parent_source_authority.json](parent_source_authority.json) records the exact
PI-issued opaque authority/key pair and independently verified mixture asset.
[separator_authority.json](separator_authority.json) freezes the previously
tested M2 `htdemucs_6s` configuration and all six model-declared output keys.
The UUID derivations are exactly those of
[AD-041](../../../docs/architecture/AD-041_DIRECT_INPUT_AUDIOSTEM_METRIC_SOURCE_IDENTITY.md).
Neither input/output asset hashes nor paths participate in source identity.
The UUIDs in this package are prospective contract values, not evidence of
successful propagation through an implemented pipeline.

[authority_verification.json](authority_verification.json) records read-only
verification of the controlled mix, cached model manifest/checkpoint, and all
twelve preserved WAV assets from the two M2 executions. Each pair's SHA-256
matches. No historical separation experiment was repeated.

Piano is authorized as a model-declared operational source. Its independent
reference denominator, preservation percentage, and timing-preservation error
remain NOT_ESTABLISHED. No new Piano population has been measured.

## Observed implementation blocker

The current Demucs adapter loads WAV files with `mono=False` and passes their
stereo arrays directly into AudioStem. SourcePulseCandidateBuilder then calls
`librosa.onset.onset_detect` with its default `sparse=True`. That API rejects
two-dimensional input. The synthetic, non-scientific interface probe in
[probe_stereo_handoff.py](probe_stereo_handoff.py) reproduces:

```
ParameterError: sparse=True (default) does not support 2-dimensional inputs. Either set sparse=False or process each dimension independently.
```

This failure is independent of the UUID values. The existing separator unit
test creates mono dummy outputs; its successful result does not establish this
stereo handoff. The existing real separator integration test stops at stem
creation and likewise does not establish observation production.

The historical reporting service independently loads each WAV through
AnalysisPipeline, whose AudioPreprocessor averages channels and peak-normalizes
the signal before NullSeparator presents it to the source detector. In
contrast, the mixture pipeline preprocesses the mixture before separation;
that operation does not preprocess the subsequently created stereo stems.

There are also mechanical provenance handoffs to address: the current pipeline
passes a single mixture asset hash into the candidate adapter; domain
reconstruction selects a single asset hash for EME materialization; and the
canonical reporting service requires direct-input identity preservation.
Those cannot correctly serialize three separate output asset identities as-is.

## Concrete proposed boundary requiring scientific clarification

Reuse the existing AudioPreprocessor independently for each authorized output
WAV (channel mean, then peak normalization), followed by the unchanged source
detector and AD-037 path. Preserve the separated UUID through that observation
view and retain the original output WAV checksum as independent asset identity.
Collect the resulting sources for unchanged AD-038/AD-040/report projection.
Do not change sparse detection, merge channel detections, or invent a channel
selection rule. Preserve every native Demucs output unchanged.

This would reuse the historical per-file observation preparation, but it is a
change to the currently wired Demucs-to-detector path, beyond identity fields
alone. Under AGENTS.md sections 5, 7 and 8, approval of that explicit signal
preparation boundary is required before implementation; it is not inferred
from authorization of separator configuration or source identity.

No production code or detector configuration was changed. Preregistration of
the executable acceptance remains pending this boundary decision. Historical
matching evidence remains available by reference to the
[M2 result](../bass_preservation_phase2_20260825_01/result.json); it is not
relabeled as prospective operational acceptance. No acceptance threshold was
created, and no BPM or other deferred research was started.

All prospective reporting remains GEOMETRIC_ONLY and ANALYZABLE OBSERVATIONS
ONLY. Absence of an observation does not establish musical absence.

## Verification

Run the bounded synthetic probe from the repository root:

```sh
PYTHONPATH=src .venv/bin/python validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/demucs_operational_reintroduction_20260907/probe_stereo_handoff.py
```

`checksums.json` binds the files in this package. The accepted VAL-001 canonical
report remains SHA-256
`eeb189217a722679d5f40bef4d809e2b38ab381e9dea81057023dfd3d80e05c7`,
with scientific fingerprint
`e3d73705306ccc0e96ec78020a54f34aa4e8f267337afa6b7bd56b74fc4fdc4d`.
