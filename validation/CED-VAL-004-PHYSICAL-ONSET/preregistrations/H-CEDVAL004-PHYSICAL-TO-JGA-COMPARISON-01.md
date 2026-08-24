# H-CEDVAL004-PHYSICAL-TO-JGA-COMPARISON-01

Status: **PREREGISTERED — NOT EXECUTED**

Authority: PI approval of frozen physical-onset result
`H-CEDVAL004-PHYSICAL-ONSET-MEASUREMENT-01`, commit
`595393fe3811f4908587544e7ac277e98d5bd2be`, scientific fingerprint
`7b2ec48f0ff0afca54849b5847f5ebd637c8d672eb2b88247ea6a1841af99062`,
and dataset authority `PR-CED-VAL-004-PHYSICAL-ONSET-001`.

## Scientific question

For every frozen physical event in `CED-VAL-004-PHYSICAL-ONSET`, how does the
existing immutable JGA observation layer represent the independently
established first physical waveform response?

The primary signed quantities are frozen as:

```text
e_samples  = n_JGA - n_physical
e_physical = t_JGA - t_physical
e_ms       = 1000 * e_samples / 44100
```

Positive means the JGA coordinate occurs after physical onset, zero means the
coordinates coincide, and negative means the JGA coordinate occurs before
physical onset. The sign may not be changed after execution.

## Separate temporal authorities

The experiment must preserve independently:

- `t_symbolic`: scheduled excitation authority;
- `t_marker`: exact marker coordinate;
- `t_physical`: frozen first causal waveform-response coordinate; and
- `t_JGA`: immutable JGA EME observation coordinate.

No pair may be collapsed. The comparison target is `t_physical` versus
`t_JGA`, never marker versus JGA.

## Authoritative JGA object and temporal representation

The authoritative JGA comparison object is the AD-037
`ElementaryMetricEvent` materialized by
`ElementaryMetricEventBuilder.build_from_observations`. Its immutable
`timestamp` is copied without adjustment from its single supporting Domain
`PulseCandidate.timestamp`; EME identity, supporting PulseCandidate identity,
source identity, observation index, asset checksum, temporal scope and full
lineage must be preserved.

Strength is not timing authority and may not be read, exported, ranked or used
by correspondence. The supporting PulseCandidate is referenced only to prove
lineage and exact timestamp/frame authority.

The current source observation producer uses
`librosa.frames_to_time(onset_frame, sr=44100)` with the default 512-sample
hop. Therefore every authorized `t_JGA` must round-trip uniquely to an integer
frame `f_JGA` and exact frame-coordinate sample:

```text
n_JGA = 512 * f_JGA
t_JGA = n_JGA / 44100 seconds
```

Execution must verify exact producer round-trip from the stored binary64
timestamp. A non-unique frame, a non-frame-consistent timestamp or conflicting
lineage is `AUTHORITY_CONFLICT`; it may not be rounded to force authority.

`t_JGA` has a 512-sample lattice spacing, exactly `512/44100` seconds
(`11.609977324263… ms`). `n_JGA` is the discrete frame coordinate used for
arithmetic, not a claim of sample-level detector precision. Preserve the frame
index, coordinate sample, stored binary64 timestamp/hex, lattice spacing and
the fact that no calibrated per-event confidence interval beyond this frame
resolution is authorized.

## Frozen observation configuration

Future execution must use the existing repository pipeline without tuning.
Before JGA output is opened, freeze environment, configuration, asset hashes,
and at minimum these current producer/materialization hashes:

- `default_analysis_pipeline.py`:
  `04ecdfee536717b977276b91b7e9416701e7a89ce9aa7bc4339917263725ef17`;
- `source_pulse_candidate_builder.py`:
  `5b270f352483dde91448b0958a299c08e51d064ab867bc872ef1cdde37a81c32`;
- `domain_pulse_candidate_adapter.py`:
  `6a3d276bf50534bc6823075a26787c624ab7a8d2ecca58628579fb86658a9330`;
- `elementary_metric_event_builder.py`:
  `137e390a69c9361d5cbfd66908256b2417d76c95d503e7ad2c409cd2e1b66cc2`;
  and
- `elementary_metric_event.py`:
  `d9066db4bfe6ca75e2ce8e1d0a2b8a71ab86853f35d0fc04b8414632fab7da7b`.

The preregistration environment observes Python 3.13.14 and librosa 0.11.0.
Execution must record its actual complete environment. Any required
unsupported source-input handling is a stop condition; production behavior
may not be modified to make the experiment run.

## Frozen correspondence authority

Correspondence is source-separated. Use only Drums EME for Drums physical
events and Double Bass EME for Double Bass physical events. Associate each
frozen physical-event identity with its already-frozen trigger/marker identity,
but do not read `n_physical` when constructing correspondence. For each source,
order its ten exact integer marker samples `m_0 ... m_9`. Construct marker
capture cells over the exact WAV scope `[0, 8820000)`:

- first cell begins at sample zero;
- final cell ends at sample 8,820,000;
- each internal boundary is the exact rational midpoint
  `(m_i + m_(i+1)) / 2`;
- ordinary cells are left-closed and right-open; and
- an EME frame-coordinate sample exactly equal to an internal boundary is
  `AMBIGUOUS_BOUNDARY` and belongs to neither cell.

This transfers the established Calibration Zero midpoint-cell framework while
keeping correspondence independent of the measured marker-to-physical
latency. The cells are determined solely by the preregistered marker schedule
before `n_physical` or JGA output is loaded. They partition source time without
a millisecond threshold and prevent one observation from being assigned across
adjacent controlled-event cells. Marker defines the permissible identity
domain only; it is not the error target. The rule does not select the
observation with minimum physical error.

For each marker-defined event cell:

- zero in-cell EME gives `UNMATCHED_PHYSICAL_EVENT`;
- exactly one in-cell EME gives `VALID_PHYSICAL_JGA_CORRESPONDENCE`;
- more than one gives `AMBIGUOUS_MULTIPLE_OBSERVED`, preserving every EME and
  selecting none; and
- exact-boundary EME gives `AMBIGUOUS_BOUNDARY` and is not consumed.

Every unconsumed or out-of-scope EME is `UNMATCHED_OBSERVED`. Duplicate EME,
equal timestamps, equal distances or any other tie inside a cell remain
`AMBIGUOUS_MULTIPLE_OBSERVED`; no tie-break is permitted. No nearest-event
optimization, strength, confidence, sequence alignment, count forcing,
threshold, physical-error minimization or post-result rematching is allowed.

## Measurements and consistency identity

For every `VALID_PHYSICAL_JGA_CORRESPONDENCE`, preserve exact identities,
lineage and:

```text
e_samples     = n_JGA - n_physical
e_seconds     = e_samples / 44100
e_ms          = 1000 * e_samples / 44100
abs_e_samples = abs(e_samples)
abs_e_seconds = abs(e_samples) / 44100
abs_e_ms      = 1000 * abs(e_samples) / 44100
```

Signed and absolute quantities remain separate. The physical-onset records are
referenced exactly and never recalculated from source audio during this study.

Preserve the secondary decomposition:

```text
marker_to_physical_samples = n_physical - n_marker
marker_to_JGA_samples      = n_JGA - n_marker
physical_to_JGA_samples    = n_JGA - n_physical

marker_to_JGA_samples
= marker_to_physical_samples + physical_to_JGA_samples
```

Verify this identity exactly in samples and exact rational seconds for every
valid record. It is an arithmetic consistency check, not a predictor or a
second correspondence rule.

## Frozen reporting

Report Drums and Double Bass independently before any pooled secondary
description. For each source preserve:

- total frozen physical events;
- total observed EME;
- valid, unmatched-physical, ambiguous-multiple and ambiguous-boundary counts;
- unmatched observed count;
- complete signed errors in samples and milliseconds;
- complete absolute errors in samples and milliseconds;
- signed and absolute minimum, Q1, median, Q3, maximum, arithmetic mean and
  population standard deviation;
- exact-zero, negative and positive signed-error counts; and
- frame indices, sample coordinates, resolution and complete provenance.

Use linear empirical quantile interpolation at `(n - 1) * p`, matching the
established Calibration Zero descriptive convention. Pooled results are
secondary only and may not conceal source behavior. No inferential test or
source-difference claim is authorized.

## Success, failure and replay

`PASS` means the physical authority and raw assets remain checksum-valid, the
immutable untuned JGA path executes, the frozen correspondence rule reports
every outcome, provenance is complete, and replay is deterministic. Error
magnitude, missing observations or ambiguous observations do not themselves
make the protocol fail; they are valid scientific outcomes.

`AUTHORITY_CONFLICT` or protocol failure occurs if input/checksum/frame/lineage
authority fails, unsupported input would require production modification, the
rule cannot be applied as written, results are incomplete, or deterministic
replay disagrees. No correction or retuning is permitted.

Perform at least two complete executions. Require exact agreement of JGA EME
and supporting PulseCandidate identities, observation ordering, stored
timestamps and frame round-trips, correspondence statuses, physical authority
references, signed/absolute errors, summaries, artifact checksums and
scientific fingerprint.

## Firewalls

The experiment layer must not read or emit PulseCandidate strength, and
strength may not influence correspondence, selection, filtering, acceptance,
rejection, ties or scoring. The existing immutable pipeline may internally
produce its ordinary PulseCandidate record and deterministic identity; this
does not authorize the experiment to inspect the strength value. No
strength-max validation is authorized. JGA detection, windows, thresholds,
frame geometry, EME generation, source handling and timing projection may not
be tuned. H02 remains unchanged; no H03 is created.

CED-VAL-001/002/003, Calibration Zero, H02, three-dataset conclusions and all
strength studies remain immutable. `GEOMETRIC_ONLY` remains production
authority. This preregistration has no architecture, production or
production-code impact.

## Future order

1. PI reviews and authorizes this preregistration.
2. Execute the frozen pipeline and correspondence rule at least twice without
   reading strength.
3. Freeze all observations, correspondence outcomes, measurements, replay and
   scientific fingerprint.
4. PI reviews the result before any separately preregistered strength study.
