# H-CEDVAL005-REAL-AUDIO-RHYTHM-SECTION-TIMING-PROFILE-01

Status: **PREREGISTERED — NOT EXECUTED**

## Frozen authorities and scientific question

This protocol is bound exclusively to:

- dataset authority `PR-CED-VAL-005-REAL-JAZZ-MULTITRACK-001`, fingerprint
  `d9d6341f837bc5f56054ffd6c91f6be65a7bdbb8043526a9ac70d924a81335af`;
- analytical-source rule
  `PR-CEDVAL005-RAW-TRACK-ANALYTICAL-SOURCE-CONSTRUCTION-01`;
- analytical-input authority `PR-CEDVAL005-ANALYTICAL-INPUTS-001`,
  fingerprint
  `08ac45969fc449503f67ea4e8bda77495c4807e9dd0e0adbe0c37c9cb506b876`;
- locked AD-037, AD-038 and AD-040 architecture; and
- the unchanged production observation configuration that is authoritative at
  execution.

Scientific question: can the existing immutable JGA observational stack
produce a deterministic, provenance-complete absolute-time and Drum-relative
`RhythmSectionTimingProfile` from the frozen CED-VAL-005 real-jazz analytical
inputs without BPM, meter, symbolic Ground Truth, event-correspondence
authority, calibration correction or musical interpretation?

## Frozen inputs and roles

The complete analytical scope is the common distributed-file sample
coordinate from frame 0 through frame 10,068,071 inclusive at 44,100 Hz
(`119858/525` seconds).

- `09_Overheads.wav`, SHA-256
  `0569a396cff95b130042fc71093e8ba3460e3c0fe0034cb86d2158027d585f3a`,
  source `Drums`, experiment-local role `TEMPORAL_REFERENCE`;
- `11_BassDI.wav`, SHA-256
  `2c4c06b9b5d4b18e00000bc2c036207fc68fb722c5854e0a30107ad4594a910b`,
  source `Double Bass`, experiment-local role `ACCOMPANIMENT`.

The role bindings depend on the named dataset, assets, frame scope, source
rule, analytical-input authority and execution identity. Instrument names do
not assign roles automatically.

## Immutable observation and absolute-time authority

Execute the existing JGA observation path without parameter or implementation
change. Preserve the complete source-specific `PulseCandidate` population,
including stable identity, producer coordinate, source/contributor identity,
asset and execution provenance. Do not inspect or use strength for any
scientific decision.

AD-037 governs EME materialization: every preserved PulseCandidate
independently supports one source-event `ElementaryMetricEvent`; metric
association cannot determine EME existence or cardinality. Preserve stable EME
identity, exact immutable timestamp, authoritative producer frame,
PulseCandidate lineage, source/contributor identity, complete scope, asset,
configuration and execution provenance. Multiple EME at one timestamp remain
distinct. No timing correction is permitted, and the timestamp is not claimed
to be sample-accurate physical onset.

Absolute distributed-file time is the primary coordinate. BPM, the Readme's
approximate 246 BPM, meter, measures, beat numbers, symbolic score, chord
changes, form and manual onset annotations are forbidden as analytical input.

## Frozen Drum-relative geometry

Apply AD-038 unchanged to every eligible Double Bass EME against the complete
Drums EME population. For target time `t`, preceding is the last
deterministically ordered Drum EME at `<= t`; following is the first at `> t`;
signed displacement is `t - reference_timestamp`; nearest minimizes absolute
temporal distance. An exact nearest tie remains recorded and uses preceding
only as AD-038's deterministic serialization rule. Stable EME identity orders
other equal-time Drum candidates without removing them.

Preserve each localization identity, target and Drum references, preceding,
following and nearest statuses, signed and absolute displacements, nearest-tie
status, unresolved status, optional `observed_interval_fraction` only where
AD-038 authorizes it, all EME/PulseCandidate lineage, source identity, asset,
scope, rule version and execution provenance. Temporal proximity is geometry
only.

## Correspondence, calibration and interpretation firewalls

Correspondence status is `GEOMETRIC_ONLY`. H02, PulseCandidate strength,
musical event pairing, shared beat identity, synchronized intention and
`AUTHORIZED_EVENT_RELATION` are prohibited.

Calibration applicability is `UNESTABLISHED`. Numerical offsets,
uncertainties or corrections from CED-VAL-001/002/003/004 cannot transfer and
cannot alter timestamps, geometry or identity. Prior calibration may appear
only as separately labelled methodological context.

No rushing, dragging, swing ratio, groove quality, ahead/behind-beat claim,
synchronization quality or performer intention may be inferred or reported.

## Frozen outputs and descriptive rules

For each of Drums and Double Bass preserve and report:

- total PulseCandidates and total EME;
- complete exact timestamp and producer-frame populations and their scopes;
- source/contributor identities and complete lineage/provenance; and
- deterministic replay status.

For Drum-relative geometry preserve and report:

- total eligible Double Bass EME, localized and unresolved counts;
- availability counts for preceding, following and nearest references;
- nearest-tie count and complete relationship-status counts;
- complete signed and absolute displacement populations; and
- for each population: minimum, Q1, median, Q3, maximum, arithmetic mean and
  population standard deviation.

Quantiles use linear empirical interpolation at index `(n - 1) * p` for
`p = 0.25, 0.50, 0.75`; population SD divides by `n`. Empty populations report
statistics as not available and remain explicit. All quantities are
descriptive geometry only.

## AD-040 profile contract

Create exactly one read-only AD-040 `RhythmSectionTimingProfile` after the
authorized EME and AD-038 records exist. Preserve:

- deterministic profile identity and scientific fingerprint;
- represented source identities and the two frozen role bindings;
- total represented EME and exact source-specific counts;
- exact common distributed-file scope and absolute-time origin;
- relationship/correspondence-status counts;
- EME and localization references without replacing their authority;
- calibration applicability `UNESTABLISHED` and uncertainty/limitation
  references;
- asset, observation, input-authority, rule and execution provenance; and
- deterministic replay status.

## Deterministic replay and artifacts

Perform at least two complete independent executions under one frozen
environment and configuration. Require exact agreement of input checksums,
PulseCandidate identities and producer coordinates, EME identities,
timestamps and lineage, sources, AD-038 identities and all reference/status/
displacement values, profile identity, source and relationship counts, all
scientific artifacts and the final scientific fingerprint. Any material
disagreement fails the protocol.

Preserve a checksum-bound input manifest, complete PulseCandidate and EME
populations, complete AD-038 population, source summaries, AD-040 profile,
replay evidence, artifact manifest, report, completion protocol and scientific
fingerprint.

## Visualization contract

Only after the observational profile passes, create one read-only scientific
visualization with absolute distributed-file time on the X axis and fixed
`Drums` and `Double Bass` lanes on the Y axis. Plot every authorized EME at its
immutable timestamp and show only neutral AD-038 connectors where authority
exists. State visibly that timing is observational and frame-resolved, not
physical-onset Ground Truth.

No beat grid, measure, BPM, inferred meter or form, swing label,
rushing/dragging label, correspondence claim or performance-quality judgment
is permitted.

## Success and stop criteria

`PASS` means only that the unchanged JGA stack produces a deterministic,
provenance-complete absolute-time and Drum-relative profile from the frozen
real-audio inputs. It does not establish physical onset, event correspondence,
sample-accurate human microtiming, common hardware clock, synchronization
intention, rushing/dragging, swing, groove, production fitness or
generalization.

Stop with `FAIL` or `INSUFFICIENT_AUTHORITY` if an input authority fails; JGA
requires modification; replay differs materially; source identity or
provenance is lost; AD-037/038/040 requires unauthorized interpretation; BPM,
meter, symbolic input, H02, strength or calibration correction becomes
necessary; or profile construction requires production-behavior change. Do
not repair or retune the experiment to obtain `PASS`.

Microphone bleed may be present. Overheads and BassDI remain recording
representations, not isolated physical sources. Common hardware acquisition
clock, simultaneous capture, absence of editing, physical-onset Ground Truth
and sample-accurate human-microtiming Ground Truth remain unestablished.

Architecture impact: **NONE**. Production impact: **NONE**. Production code,
raw assets and all CED-VAL-001/002/003/004, H01, H02, strength and physical
authority history remain unchanged.
