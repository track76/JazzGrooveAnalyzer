# H-VAL001-AI-VOICE-02 — Blind SOME Voice Proof of Concept

## Scientific question

Can pinned SOME `v1.0.0-baseline` provide reliable **INFERRED** Voice
source-event evidence independently of Basic Pitch, JGA PulseCandidates and
symbolic Ground Truth?

## Blind result

The official model at source commit
`dcfd40f9bfaa7c9649aae01a2795af73946ec5e7` produced 13 inferred events from
the controlled Voice WAV. Two independent CPU executions produced byte-identical
raw arrays, decoded arrays, event serialization and MIDI. The scientific
fingerprint is
`a7670c5501fdda70fe8ce2e3fa7e59ba837323b73a602b81e442a4cc7cc6b2d0`.

All inference, model, environment, cache and raw-array storage is external.
SOME output is INFERRED evidence and neither modifies nor replaces the 150
OBSERVED JGA Voice PulseCandidates.

## Post-freeze validation

Ground Truth was accessed only after the blind result was frozen. The
repository-authoritative symbolic Voice population contains 11 events. Exact
ordered rounded-pitch comparison supports a longest common subsequence of ten
values without using a temporal tolerance. It does not establish event
identity.

SOME materially reduces fragmentation relative to Basic Pitch's 25 events and
19 onset-backed hypotheses. It nevertheless materializes the final rounded
MIDI-67 trajectory as four exactly abutting segments and does not expose one
symbolic MIDI-75 value in the ordered sequence. Whether the latter is merging
or omission is unvalidated because event-level score/audio temporal
correspondence remains unauthorized.

## Outcome

**PARTIAL.** SOME provides reproducible and materially improved Voice
source-event evidence, but residual same-pitch segmentation and an unresolved
missing/merged symbolic event prevent PASS. Production integration is not
scientifically justified. Existing JGA boundaries remain sufficient for a
future experiment-local or approved Translation adapter; no architectural
change is indicated.
