# EXEC-CEDVAL007-RENDERED-RESPONSE-20260824-210717

Status: **PASS — EXACT DETERMINISTIC RESPONSE MEASUREMENT**

The frozen exact-integer protocol executed twice in fresh processes with
identical scientific artifacts and fingerprint
`c915eb4a63b9f7e9a3650eef1ce28d52b6bc956da485ec3b5ae7451e87ab29a2`.

## Frozen outcome

`MARKER` localized all 64 expected events. Every response occurred one sample
after its symbolic coordinate; both channels shared the same first-response
coordinate in all 64 cases. Signed and absolute displacement are therefore
uniformly one sample, exactly `10/441` ms (approximately
0.022675736961451 ms), with population standard deviation zero.

`DRUM` localized only event zero under the preregistered initial-file-boundary
status. That response occurred one sample after the symbolic coordinate, with
an exact stereo first-response tie. All 63 later events are
`UNRESOLVED_PRE_EVENT_ACTIVITY`; the exact-zero guard failed and the protocol
correctly prohibited response searching or fallback localization. The single
localized displacement is one sample, exactly `10/441` ms. This result does
not imply that later Drum responses are absent.

## Authority separation

- Symbolic positions remain `SYMBOLIC_BEAT_GROUND_TRUTH`.
- Marker measurements are `RENDERED_MARKER_RESPONSE`.
- Drum measurements are `RENDERED_DRUM_RESPONSE` where localized.
- Unresolved Drum events have no rendered coordinate or displacement.

No latency correction, JGA, external tracker, H02, strength, musical
interpretation, production change, raw-asset change or historical-authority
change occurred.
