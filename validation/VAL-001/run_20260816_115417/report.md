# H-VAL001-AI-VOICE-01 — Blind Basic Pitch Voice Proof of Concept

## Scientific question

Can a pinned pretrained Basic Pitch model provide reliable **INFERRED**
source-event evidence for the controlled Voice stem where deterministic
transient observations are strongly fragmented?

## Blind result

Basic Pitch 0.4.0, using the packaged Core ML ICASSP 2022 model and unchanged
`predict()` defaults, produced 25 inferred note events. Two independent
executions produced identical raw-array, canonical note-event, and MIDI
fingerprints. The scientific fingerprint is
`7abc9a2915c10c2a69dd3ea286408ab19e9fcd4a484b720103c3f95be568fa39`.

The blind result was frozen before symbolic Ground Truth access. Raw arrays,
note events, pitch bends, MIDI, environment inventory, and the freeze record
are stored beneath `JGA_EXTERNAL_ROOT`.

## Post-freeze validation

The repository-authoritative MusicXML contains 11 PI-verified Voice symbolic
events. The 25 inferred events therefore disagree in population by +14. Six
chronologically adjacent inferred pairs have exactly abutting boundaries and
the same pitch, providing direct evidence of residual segmentation. Seven
adjacent pairs overlap. No exact duplicate event tuples occur.

No arbitrary score/audio tolerance was introduced. Consequently, individual
misses, extras, or merges are not assigned and event-level symbolic
correspondence remains unvalidated.

## Decision

**PARTIAL.** Basic Pitch materially improves the Voice event-inference problem:
it converts 150 fragmented physical transient observations into 25 stable,
pitch-bearing inferred hypotheses. It does not yet provide a validated 11-event
population, and its residual fragmentation and overlap prevent production
integration.

The existing Core → Translation → Domain architecture can host a future pinned
inference adapter while preserving Core observations and labeling its output
INFERRED. No new architectural layer is demonstrated as necessary.

## Next action

Perform one read-only causal audit of the six exact same-pitch abutting splits
and seven overlaps against the frozen Basic Pitch frame/onset evidence to
determine whether they are model post-processing artifacts or genuinely
separate supported hypotheses; do not tune parameters or use symbolic event
boundaries.
