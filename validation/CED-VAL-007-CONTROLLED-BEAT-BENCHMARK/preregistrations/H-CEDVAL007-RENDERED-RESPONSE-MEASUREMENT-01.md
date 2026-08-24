# H-CEDVAL007-RENDERED-RESPONSE-MEASUREMENT-01

Status: **PREREGISTERED — NOT EXECUTED**

Authority: PI approval of
`PR-CED-VAL-007-CONTROLLED-BEAT-BENCHMARK-001`, frozen at commit
`256a15fdde8c4d565e0c0c6995b84c90e8d1e856`, dataset fingerprint
`cd93455778d1484067f9a3caa3037b6467d27c7e8d5a8c0df694658bad2484e9`.

## Scientific question

Can a prospective, deterministic, source-independent measurement rule
establish the earliest rendered response associated with each of the 64 frozen
symbolic events in `MARKER GT` and `DRUM GT`, without JGA, librosa, Essentia,
musical interpretation or post-hoc detector tuning?

The 64 symbolic positions remain `SYMBOLIC_BEAT_GROUND_TRUTH`. This protocol
does not redefine them. It measures, as separate objects, the rendered marker
response and rendered drum response where the waveform supplies sufficient
exact digital evidence.

## Frozen inputs and verification gate

Execution may use only the checksum-bound authority manifest and symbolic
schedule plus these raw assets:

- `CED-VAL-007-CONTROLLED-BEAT-BENCHMARK-v0.1 MARKER GT.wav`, SHA-256
  `7c8c8534944e3d901b0de47f97fab03816f47e6ab62225e63ee3ba12e1c2206f`;
- `CED-VAL-007-CONTROLLED-BEAT-BENCHMARK-v0.1 DRUM GT.wav`, SHA-256
  `c673d2c104eb3eb31012154f1bd84ee81313b4fd36b61bf3913686f43e19bb0c`.

Both must replay as signed 24-bit little-endian stereo PCM, 44,100 Hz,
1,411,200 frames, scope `[0,1411200)`. The authority verifier must reproduce
the dataset fingerprint and the exact 64-event population before source
samples are measured. Any mismatch is `AUTHORITY_CONFLICT` and stops.

## Prospective cell geometry

Let `N = 1411200`, spacing `P = 22050`, half-spacing `H = 11025`, and
`n_i = P*i` for `i = 0..63`. Cells partition the complete file coordinate:

```text
C_0  = [0, n_0 + H)                 = [0, 11025)
C_i  = [n_i - H, n_i + H)           for i = 1..62
C_63 = [n_63 - H, N)                = [1378125, 1411200)
```

Every sample belongs to exactly one event-local cell. No cell may be moved,
resized or replaced after execution begins.

For events `i = 1..63`, the exact pre-event guard is:

```text
G_i = [cell_start_i, n_i)
```

It is exactly 11,025 samples (250 ms). The causal response search is:

```text
S_i = [n_i, cell_end_i)
```

For the first event, `G_0` is unavailable because the render begins at the
symbolic event. Its search is `S_0 = [0,11025)` and any localized result must
carry `INITIAL_FILE_BOUNDARY_NO_PRE_EVENT_GUARD`.

## Exact sample and silence authority

Decode each channel directly as signed 24-bit little-endian integer samples.
No float conversion, gain, normalization, filtering, threshold, epsilon,
absolute-amplitude floor or channel mixing is permitted.

A stereo frame is `EXACT_DIGITAL_SILENCE` iff both channel integers equal
zero. It is `NONZERO_RENDERED_WAVEFORM` iff either channel integer is nonzero.

The rule is source-independent. The same cells, guards, sample representation,
silence definition, search direction and statuses apply to MARKER and DRUM.

## Rendered-response rule

For each event `i > 0`:

1. Require every stereo frame in `G_i` to be exact digital silence.
2. If the guard passes, scan `S_i` in strictly increasing sample order.
3. The rendered-response coordinate is the first frame at which either
   channel is nonzero.
4. Preserve each channel's first nonzero coordinate and signed value. The
   event coordinate is the earlier existing channel coordinate.

For `i = 0`, scan `S_0` from file sample zero and use the same first-nonzero
stereo rule, but preserve the initial-boundary limitation. There is no claim
about samples before the rendered file.

The future primary statuses are:

- `LOCALIZED_EXACT_ZERO_GUARD`: guard passes and a response is found;
- `LOCALIZED_INITIAL_FILE_BOUNDARY`: first event response is found, with no
  pre-event guard authority;
- `UNRESOLVED_PRE_EVENT_ACTIVITY`: any sample in the guard is nonzero;
- `UNRESOLVED_NO_RESPONSE_IN_SEARCH`: guard passes but no nonzero frame occurs
  in the search;
- `UNRESOLVED_INITIAL_FILE_BOUNDARY_NO_RESPONSE`: no first-event response is
  found; and
- `AUTHORITY_CONFLICT`: any identity, format, schedule, coordinate, decoding
  or replay authority fails.

No onset coordinate or displacement is authorized for an unresolved event.

## Tail, overlap, ambiguity and ties

Nonzero decay, overlap, instrument state, DC or noise in a pre-event guard is
not subtracted or ignored. It produces `UNRESOLVED_PRE_EVENT_ACTIVITY`. This
prevents an already-active waveform from being misidentified as the new
event's earliest response.

Read-only preregistration diagnostics, performed without calculating response
coordinates, found exact-zero 250 ms guards for 63/63 non-initial MARKER
events and 0/63 non-initial DRUM events. This evidence motivates no
source-specific relaxation: the protocol preserves unresolved Drum events
rather than inventing a threshold or counterfactual tail model.

The exact earliest-frame rule produces no rank ambiguity. Multiple later
nonzero regions are irrelevant. Distinct left/right first-response frames are
preserved as `CHANNEL_FIRST_RESPONSE_DIFFERENCE`; the earlier coordinate
remains the event response. Equal left/right first-response coordinates are
preserved as `STEREO_FIRST_RESPONSE_TIE`; no channel is preferred.

## Displacements and resolution

For every localized event:

```text
d_signed_samples = n_rendered - n_symbolic
d_absolute_samples = abs(d_signed_samples)
t_rendered = n_rendered / 44100 seconds
d_signed_seconds = d_signed_samples / 44100
d_absolute_seconds = d_absolute_samples / 44100
```

Coordinates and displacements remain exact integers or rational values.
Temporal resolution is one source sample, exactly `1/44100` second. The
underlying continuous transition is localized to `((n_rendered-1)/44100,
n_rendered/44100]` when a preceding exact-zero sample exists. Sub-sample
interpolation is forbidden.

## Future output contract

For every source and symbolic event, future execution must preserve:

- source identity and checksum;
- symbolic beat identity, sample coordinate and exact timestamp;
- cell, guard and search bounds;
- exact guard status and first nonzero guard frame/value if it fails;
- response status and limitation reason;
- per-channel first-response presence, coordinate and signed value;
- rendered-response coordinate and exact timestamp where authorized;
- signed and absolute displacement in samples and exact seconds;
- channel-difference/tie status;
- one-sample uncertainty statement where applicable;
- rule, dataset, schedule, execution and complete provenance identities.

For MARKER and DRUM separately report expected, localized, unresolved,
ambiguous and authority-conflict counts; complete localized signed and
absolute displacement populations; and minimum, linear-interpolated Q1,
median, Q3, maximum, arithmetic mean and population standard deviation in
samples and milliseconds. Empty populations must remain empty; undefined
statistics must be reported as undefined rather than imputed.

## Replay and stop conditions

Execute the complete measurement at least twice independently. Require exact
agreement of input identities, cells, guards, statuses, sample coordinates,
signed values, channel relations, displacement populations, statistics,
event ordering, artifacts and scientific-content fingerprints. Any material
disagreement is `AUTHORITY_CONFLICT`; values may not be rounded or reconciled.

Stop without repair if input authority fails; PCM decoding or coordinate
mapping is ambiguous; a cell cannot be assigned uniquely; execution would
require a threshold, filtering, tail subtraction, source-specific relaxation,
manual selection or musical interpretation; or replay differs.

## Firewalls

No JGA EME, PulseCandidate, H02, strength, librosa/Essentia onset detector,
beat tracker, BPM estimation, listening authority, visual onset selection,
musical interpretation, correction, audio shift or calibration transfer is
permitted. CED-VAL-004 supplies methodological precedent only; none of its
latency values or configuration-specific onset authority transfers here.
Production code, raw assets and historical authorities remain unchanged.
