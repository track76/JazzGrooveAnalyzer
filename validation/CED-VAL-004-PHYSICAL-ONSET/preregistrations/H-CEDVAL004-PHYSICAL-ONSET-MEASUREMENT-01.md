# H-CEDVAL004-PHYSICAL-ONSET-MEASUREMENT-01

Status: **PREREGISTERED — NOT EXECUTED**

Authority: PI approval of `PR-CED-VAL-004-PHYSICAL-ONSET-001`, frozen at
commit `3aee33eb388449f87c0bb4d734e2b2b1d84f70d4`, dataset fingerprint
`704ce5926852a2ff62d9794dbee48156f875016979214cf7ef3ab93aa35ec772`.

## Scientific question

For every controlled source excitation in `CED-VAL-004-PHYSICAL-ONSET`, what
is the earliest sample-addressable physical waveform response causally
attributable to the known event marker?

This study will establish `t_physical` independently of `t_symbolic`,
`t_marker` and `t_JGA`. This document freezes the measurement rule only. It
does not authorize execution.

## Frozen inputs

Execution shall use only the checksum-bound exact marker schedule, canonical
Drums and Double Bass waveforms, source-specific digital-silence controls,
common 44,100 Hz sample clock and sample-zero authority, 8,820,000-frame
scope, event identities, and generation/session provenance frozen by
`PR-CED-VAL-004-PHYSICAL-ONSET-001`.

Before reading source samples, execution must reproduce the dataset and
schedule fingerprints and every applicable asset checksum and technical
property. Any conflict produces `AUTHORITY_CONFLICT` and stops measurement for
the affected authority scope. No asset may be altered.

## Operational physical-onset definition

For event `k` with marker frame `m_k`, define its marker-inclusive causal
search window as:

```text
W_k = {n | m_k <= n < m_k + 352800}
```

That is the exact eight-second post-marker remainder of the frozen ten-second
slot. It is fixed for all 20 events, ends two seconds before the next marker,
and is derived solely from the preregistered schedule.

For stereo channel `c` in the event's canonical source waveform, define:

```text
n_c = min {n in W_k | source[c,n] != control[c,n]}
```

The frozen controls are exact digital zero at every sample, so this is
equivalently the first frame in `W_k` at which channel `c` has a nonzero signed
24-bit integer sample. No rounding, absolute-amplitude threshold, epsilon,
normalization or transformation is permitted.

If either channel has a first-response frame, the event-level physical onset
frame is:

```text
n_physical = min(n_left, n_right)
```

over the channel results that exist. Then:

```text
t_physical = n_physical / 44100 seconds
```

This is the earliest physical response represented anywhere in the preserved
stereo waveform. The exact first-response frame and signed sample value for
each channel remain separately authoritative.

## Digital-zero sufficiency decision

The exact first-nonzero rule is scientifically sufficient for this frozen
controlled configuration. Both same-configuration source controls are exact
digital silence; the assets are integer 24-bit PCM; dither, normalization and
post-processing are absent; canonical and independent source rerenders are
byte-identical; and marker and source share a checksum-bound common clock.
Consequently, any exactly nonzero canonical source sample is a reproducible
physical waveform departure from the authorized no-event state. Internal
interpolation or a low-amplitude pre-peak response is not nuisance evidence to
discard: if it produces a nonzero output after excitation, it is part of the
rendered causal response under this operational definition.

This conclusion is configuration-bound. It does not authorize a general
first-nonzero rule for dithered, noisy, analog, human-performance or otherwise
nonzero-baseline audio.

As an event-local guard, execution must compare the exact two-second
pre-marker interval `[m_k - 88200, m_k)` with the source-specific control. It
must be exact digital zero. A departure does not authorize thresholding or
baseline subtraction; it produces `AUTHORITY_CONFLICT` for that event.

## Stereo and source policy

The common stereo rule is **first nonzero in either channel**. It is chosen
because the stereo asset as a whole has physically responded when either
preserved channel departs from the exact control. Requiring simultaneous or
both-channel response would discard a real unilateral or channel-offset
response and would no longer identify the earliest response represented in
the asset.

No source-specific measurement rule is authorized. The same exact comparison,
window and stereo policy apply independently to Drums and Double Bass. Results
must remain source-separated.

## Frozen statuses and uncertainty

The primary statuses are:

- `VALID_PHYSICAL_ONSET`: at least one channel has a first-response sample and
  all authority and baseline checks pass;
- `NO_PHYSICAL_RESPONSE_FOUND`: neither channel differs from control anywhere
  in `W_k`;
- `CHANNEL_DISAGREEMENT`: auxiliary flag when left and right first-response
  frames differ or one channel has no response; the event onset remains the
  earlier existing channel frame when authority otherwise passes; and
- `AUTHORITY_CONFLICT`: checksum, format, scope, schedule, common-clock,
  provenance or pre-marker-baseline authority fails. No onset is authorized.

The sample-addressable onset is exact on the discrete clock. Because the
immediately preceding sample is verified zero, the underlying continuous-time
transition is localized to `((n_physical - 1) / 44100,
n_physical / 44100]` seconds: one sample period, exactly `1/44100` second.
Preserve channel-first-frame spread in samples and milliseconds when
`CHANNEL_DISAGREEMENT` applies. No further uncertainty estimate, correction or
amplitude significance threshold is authorized.

## Event-level output contract

Future execution must preserve for every event:

- dataset, event and source identities;
- marker frame and exact marker time;
- exact search-window start and exclusive end;
- left and right first-response frame, signed sample value and presence status;
- authorized `n_physical` and exact/decimal `t_physical` where defined;
- marker-to-physical latency in integer samples, exact seconds and decimal
  milliseconds;
- pre-marker baseline verification and source-control identity/checksum;
- canonical source asset identity/checksum;
- channel agreement status and channel spread;
- primary status, uncertainty interval and reason;
- rule ID/version, execution identity, environment and complete provenance;
  and
- deterministic replay and scientific fingerprint.

Marker-to-physical latency is frozen as:

```text
L_samples = n_physical - m_k
L_seconds = L_samples / 44100
L_milliseconds = 1000 * L_samples / 44100
```

It is undefined for `NO_PHYSICAL_RESPONSE_FOUND` and `AUTHORITY_CONFLICT`.

## Replay and firewalls

Execute the complete measurement at least twice. Require exact equality of
input identities, event population, channel frames and signed values,
`n_physical`, exact and derived latency quantities, statuses, uncertainty,
event ordering, artifact checksums and scientific fingerprint. A replay
conflict is an `AUTHORITY_CONFLICT`; values may not be rounded to manufacture
agreement.

The rule may consume only marker, raw source waveform and control authority.
It must not consume or run JGA EME, PulseCandidate, strength, confidence,
AD-038, H02, symbolic-to-EME correspondence, nearest-event logic, prior JGA
errors or musical plausibility. It must not calculate physical-to-JGA error or
validate strength. Ground Truth concealment remains in force until the
physical result is executed, frozen and reviewed by the PI.

CED-VAL-001/002/003, H02, the three-dataset conclusion, strength studies,
Calibration Zero and raw historical results remain unchanged. No H03 is
created. `GEOMETRIC_ONLY` remains production authority. Architecture,
production and production-code impacts are none.

## Future order

1. PI reviews and authorizes this frozen rule.
2. The rule is executed on `PR-CED-VAL-004-PHYSICAL-ONSET-001` and the complete
   physical authority is frozen.
3. The PI reviews the physical authority.
4. Only a separate later authorization may permit JGA comparison or blind
   strength-predictor validation.
