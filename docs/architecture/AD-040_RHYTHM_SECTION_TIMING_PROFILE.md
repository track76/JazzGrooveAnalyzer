# AD-040 — Rhythm Section Timing Profile

Status: LOCKED

## Decision

`RhythmSectionTimingProfile` is reserved as a provenance-bound, read-only
analytical projection over existing immutable JGA observations. It provides an
auditable absolute-time profile of sources explicitly assigned to the Rhythm
Section Timing Core. It does not determine EME existence, alter observation
geometry, establish event correspondence or introduce musical interpretation.

For the current controlled dataset, the authorized analytical assignments are:

- Drums: `TEMPORAL_REFERENCE`;
- Double Bass: `ACCOMPANIMENT`;
- Piano: `ACCOMPANIMENT`;
- Tenor Sax: outside this core, with melodic/lead analytical role; and
- Voice: `DEFERRED`.

These are scoped analytical assignments, not immutable instrument ontology.
Absolute recording time is the profile's primary temporal coordinate.

The profile is not a beat, meter or measure model, a groove interpretation or
a performance-quality judgment.

## Provenance-Bound Analytical Role Assignment

A source enters a Rhythm Section Timing Core only through an explicit role
assignment binding:

- source and asset identity;
- declared temporal scope and temporal origin;
- analytical role;
- assignment rule/version;
- execution identity; and
- scientific authority and provenance.

Instrument name never assigns analytical role. Piano, Guitar, Bass or any
other instrument is not permanently classified as accompaniment by identity.
No automatic role inference, AI classification or general role-classification
system is authorized.

The contract is extensible without architectural change: rhythm guitar,
percussion or another source may enter a future core through a separately
authorized, provenance-bound `ACCOMPANIMENT` assignment. A source may receive
different assignments under different assets, scopes or scientific authority.

## Existing Raw Authority

AD-037-authorized EME and AD-038 `DrumRelativeEMELocalization` are sufficient
raw inputs. AD-040 does not duplicate timestamps, EME, observation lineage or
Drum-relative localization when immutable identities can be referenced.

No second localization representation or algorithm is required. The profile
is a downstream view composed by reference from existing authority.

## Minimum Read-Only Profile Contract

A future profile may reference only the minimum evidence needed for its scope:

- deterministic profile identity and scientific fingerprint;
- provenance-bound analytical role assignments;
- temporal scope and absolute temporal origin;
- target EME identity, exact immutable timestamp and contributor/source;
- relevant Drum EME identities and exact immutable timestamps;
- existing Drum-relative geometric-localization identity or stable key;
- correspondence status;
- optional independent authorized-event-relation evidence identity;
- calibration applicability status;
- Calibration Zero experiment, result and fingerprint references;
- uncertainty-evidence references;
- asset and observation provenance;
- PulseCandidate/EME lineage references;
- projection rule/version; and
- execution identity.

Fields already authoritative in immutable EME, localization or calibration
records shall be referenced by identity rather than copied. A serialized view
may include deterministic presentation projections, but those projections do
not replace authority.

## Correspondence Firewall

The following distinction is permanent:

```text
GEOMETRIC RELATIONSHIP != AUTHORIZED TEMPORAL CORRESPONDENCE
```

`DrumRelativeEMELocalization` expresses only observed timestamp geometry. Its
preceding, following and nearest Drum references, signed displacement and
observed interval fraction do not establish a shared musical event, metric
position or intended synchronization point.

`AUTHORIZED_EVENT_RELATION` requires independent provenance-bound evidence
that explicitly identifies the target EME and Drum EME. A geometric relation
shall never be promoted to authorized correspondence, and authorized
correspondence shall never rewrite raw geometry.

The minimum correspondence-status vocabulary is:

- `GEOMETRIC_ONLY` — neutral geometric evidence exists; no independent event
  relation is authorized;
- `AUTHORIZED_EVENT_RELATION` — independent provenance-bound evidence names
  the target and Drum events;
- `UNRESOLVED` — available evidence does not support a unique authorized
  relation; and
- `NOT_APPLICABLE` — correspondence is outside the record's analytical
  purpose, including reference-lane records where no target/reference pairing
  is asserted.

Calibration applicability is a separate property and shall not be encoded in
correspondence status.

## Calibration Context Contract

AD-039 and the frozen Calibration Zero studies govern calibration evidence.
The profile may reference:

- calibration experiment and result identity;
- scientific fingerprint;
- source-pair type;
- frozen classification;
- applicability conditions; and
- uncertainty evidence.

Current controlled evidence records `NO_DETECTABLE_PAIRWISE_BIAS` under the
frozen criterion for Piano–Drums and Double Bass–Drums, and
`INSUFFICIENT_EVIDENCE` for Tenor Sax–Drums. The current core does not include
Tenor Sax.

Calibration context never modifies an EME timestamp, Drum-relative geometric
quantity or event identity. No mathematical correction is authorized.

## Three-Level Epistemic Firewall

The profile preserves three non-overwriting levels:

1. **RAW OBSERVATION** — immutable EME timestamps, identities, lineage and
   neutral Drum-relative geometry;
2. **CALIBRATION CONTEXT** — independently validated, provenance-bound
   measurement evidence, applicability and uncertainty; and
3. **MUSICAL INTERPRETATION** — not authorized by this decision.

Each later level may reference but shall never overwrite an earlier level.

## Temporal and Window Authority

Absolute recording time remains authoritative. The profile remains fully
usable without BPM, meter, measure boundaries, beat numbers or formal
sections.

Future fixed-duration windows are permitted only as explicitly declared
display or descriptive aggregation scopes. Window duration and boundaries
must be provenance-bound and carry no inherent musical meaning.

## Reserved Visualization Contract

A future view may use absolute recording time on the X axis and fixed Drums,
Double Bass and Piano lanes for the current controlled profile. Every in-scope
EME retains its exact temporal position. Visual encoding may distinguish
`GEOMETRIC_ONLY`, `AUTHORIZED_EVENT_RELATION` and `UNRESOLVED` evidence.

Calibration evidence must appear as separate context and may not move plotted
raw timestamps. This decision does not authorize visualization implementation
or rendering.

## Simplicity and Architectural Consequence

When a scientifically simpler path produces equivalent evidence, the simpler
path must always be preferred.

Accordingly, AD-040 introduces no new architectural layer, duplicate
localization model, general role classifier, correction subsystem, threshold,
clustering or BPM/meter dependency. The reserved profile is a downstream
Representation/Analysis projection that preserves existing dependency
direction and authority boundaries.

Architectural impact is a new read-only contract only. Production impact is
**NONE**. No production implementation is authorized.

## Scientific History

F-030 preservation applies to the complete auditable chain:

```text
EME validation
→ absolute event timeline
→ neutral Drum-relative geometry
→ descriptive nearest-Drum distance analysis
→ Calibration Zero
→ pairwise Calibration Zero
→ Rhythm Section Timing Core
```

Negative, partial and unresolved results remain part of the scientific record.
This decision does not rewrite prior evidence or imply that the path was
predetermined.

## Relationship to Existing Authority

- AD-037 continues to govern EME existence and cardinality.
- AD-038 continues to govern neutral Drum-relative geometry.
- AD-039 continues to govern Calibration Zero, raw immutability, uncertainty
  and correction authority.
- F-030 continues to govern scientific-history preservation and
  reproducibility.

All prior authority remains intact and independently applicable.
