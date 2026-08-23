# PR-CED-VAL-004-PHYSICAL-ONSET-GENERATION-01

Status: **FROZEN GENERATION PROTOCOL — NO ASSETS CREATED**

Authority: PI approval following
`H-CEDVAL003-STRENGTH-MAX-CORRESPONDENCE-VALIDATION-01`, frozen result commit
`daaac23`; AD-039; JGA Knowledge Model; SVP-001; F-030.

## Dataset identity and purpose

Proposed dataset: **`CED-VAL-004-PHYSICAL-ONSET`**.

The dataset shall prospectively establish independent physical authority for:

```text
symbolic event identity/time
→ exact common-clock marker sample
→ independently measured first causal acoustic waveform response
→ later JGA observation
```

It is a physical-onset calibration/authority dataset, not an H02 dataset. This
protocol authorizes no asset creation, rendering, physical-onset measurement,
JGA execution or predictor scoring.

## Minimum sources

The minimum source population is **Drums and Double Bass**. Those are the two
sources represented in the frozen 56-cell ambiguity and strength-predictor
question, and strength has no cross-source authority. Both must therefore be
validated independently. Piano has zero cells in that frozen population and
is not scientifically necessary to answer the current question; including it
would expand source-specific scope without equivalent evidence. Piano may be
added only by later explicit authority and may not be silently appended to
this dataset.

Use exactly two identical controlled excitations per source, the minimum that
permits a within-source repeatability comparison: Drums-1, Double-Bass-1,
Drums-2, Double-Bass-2. The material is non-musical. Meter, tempo, swing,
harmony and realistic performance are neither required nor authorized as
experimental factors.

## Common-clock generation

Generate one offline multichannel session at **44,100 Hz, 24-bit integer PCM,
with dither disabled**, in which the marker channel and both unmodified source
channels share one audio engine, sample clock, sample-zero origin and exact
sample count. Export/split the marker and source
channels deterministically from that single render; do not independently
re-render stems. The generation manifest must bind the session, audio engine,
virtual instruments, versions, presets, routing, sample format and event
schedule.

No post-render shift, trim, normalization, resampling, detected-onset
alignment, time-stretch or metadata rewrite is permitted. Any unequal scope or
unbound sample-zero relation fails dataset authority.

## Symbolic and marker authority

The minimal symbolic control source is a checksum-bound event schedule with:

- deterministic symbolic event ID;
- source ID (`Drums` or `Double Bass`);
- exact rational trigger time and exact target marker sample index;
- controlled note/excitation identity and duration where applicable; and
- deterministic ordering with no same-source simultaneous events.

The schedule need not encode meter or other musical structure. If a conventional
symbolic container is used, an accompanying canonical event manifest remains
the timing authority.

Use one separate mono marker/reference channel. Each scheduled event produces
one single-sample positive impulse of exact signed 24-bit integer amplitude
**4,194,304** at its target sample index; every other marker sample is digital
zero. The canonical event manifest maps each
marker sample one-to-one to its symbolic event and source. Events are globally
non-simultaneous, so marker identity is unambiguous. The marker is never mixed
into a source waveform and is never supplied to JGA.

Marker authority establishes controlled excitation/trigger identity only. It
is **not** physical-onset authority and does not authorize
`t_marker = t_physical`.

## Event isolation and control baseline

Use four fixed **10-second event slots** (total exact scope 40 seconds /
1,764,000 samples), chosen before rendering and without JGA
output. Place each marker exactly 2 seconds after its slot begins, leaving an
8-second post-marker response interval. Marker indices are therefore 88,200,
529,200, 970,200 and 1,411,200 for Drums-1, Double-Bass-1, Drums-2 and
Double-Bass-2 respectively. Emit only one source event in a slot; the other
source remains untriggered.

The configured event duration must end early enough to preserve the complete
release within the slot. During authority freeze, a non-JGA check must verify
that the final pre-marker control interval and final slot interval are
consistent with the applicable control baseline. Failure means the generated
dataset is not authority-ready; spacing may not be silently retuned.

Generate one equal-scope, no-event control render for each source using the
same engine, preset, routing, sample format and common-clock schedule but with
all source excitations disabled. These checksum-bound control waveforms are the
baseline authority. Event-specific pre-marker intervals are preserved as local
controls but do not replace the separate source controls.

## Physical-onset authority reserved for a separate protocol

After asset freeze, a separately preregistered non-JGA measurement must derive
`t_physical` from each source waveform relative to its marker and source-control
waveform. That rule must be deterministic, sample-addressable,
provenance-bound, source-specific where necessary, frozen before predictor
scoring and capable of reporting uncertainty. It must identify the **first
causal waveform response**, not the strongest peak.

The future rule must define baseline equivalence/deviation and uncertainty
before inspecting strength predictions. It may not use JGA EME,
PulseCandidate, strength, AD-038 geometry, H02, midpoint cells, nearest-event
selection or musical plausibility. If deterministic control equivalence cannot
be established, physical authority remains unresolved.

## Waveform preservation and measurable quantities

Preserve each complete unmodified source channel across its full common scope:
pre-marker state, first causal response, complete attack envelope, later
transient peaks, sustain where configured, decay and release. Do not trim to an
onset or reduce an event to one peak.

Preserve separately:

- `t_symbolic`: scheduled symbolic trigger time;
- `t_marker`: exact marker sample on the common clock;
- `t_physical`: later independently measured first causal response;
- `t_JGA`: later immutable JGA observation time.

This permits symbolic-to-marker latency, marker-to-physical-response latency
and physical-to-JGA observation error. If generation intentionally makes
`t_symbolic` and `t_marker` identical, that equality must be an explicit,
verified generation fact, not an assumption.

## Expected minimum assets

No asset is created now. A future authority-freeze must expect:

1. canonical symbolic/event schedule and, if used, its symbolic container;
2. mono sample-accurate marker WAV;
3. unmodified Drums waveform;
4. unmodified Double Bass waveform;
5. equal-scope Drums no-event control waveform;
6. equal-scope Double Bass no-event control waveform;
7. generation/export configuration and environment record;
8. event/marker/source provenance manifest; and
9. asset checksum and dataset-fingerprint manifest.

Every audio asset must preserve exact sample rate, format, channel count,
sample count, scope and sample-zero relation. Freeze all SHA-256 values, marker
indices, event/source identities, tool versions, routing, presets and
deterministic replay evidence. Generate the complete render twice; require
byte-identical assets or stop and characterize the reproducibility limitation
before dataset authority can pass.

## Blindness, historical and publication firewalls

The frozen strength-max rule must not influence event content, schedule,
rendering, baseline, marker or physical-onset rule. Required future order:

1. this generation protocol is reviewed;
2. assets are generated and frozen;
3. physical-onset authority is separately preregistered, executed and frozen;
4. strength predictors are generated blind where applicable and frozen;
5. physical Ground Truth is revealed;
6. predictors are scored without retuning.

The method record must allow publication to reconstruct what was triggered,
its exact marker sample, the first physical response, the JGA observation and
uncertainty between all layers.

CED-VAL-001/002/003 and their limitations remain unchanged. H02 is unchanged,
no H03 exists, historical Calibration Zero is unchanged, `GEOMETRIC_ONLY`
remains production authority, and architecture/production/code impacts are
none.
