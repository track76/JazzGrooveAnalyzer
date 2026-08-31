# PR-CEDVAL006-PHASE3-DETECTOR-NATIVE-EVIDENCE-CAPTURE-01

Status: **PREREGISTERED — NOT EXECUTED**

This validation-only study reruns the unchanged source-specific JGA onset
builder on the frozen unprocessed and Phase-3 processed Bass inputs. It
captures the native onset frame, its 512-sample frame-start coordinate, the
timestamp, and the onset-envelope value already associated with each detected
candidate. It changes neither production code nor detection semantics.

Captured candidates must exactly reproduce the frozen canonical observation
index, frame, sample coordinate and timestamp. Ground Truth is used only after
capture for the frozen A/B/C1/C2/D/E retrospective labels and evaluation.
No threshold is optimized and no selection rule is implemented.

The prospective discriminator outcome uses two frozen descriptive gates: a
conventional large absolute Cliff's delta (at least 0.474) for B versus D
native strength, or unique-strength-maximum agreement in at least 75% of
processed multi-candidate cells. A negligible effect below 0.147 together
with no-better-than-50% agreement yields `NO`; all intermediate evidence is
`INDETERMINATE`. Full authority, replay, serialization and firewall details
are in the adjacent JSON.
