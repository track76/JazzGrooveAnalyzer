# H-VAL001-DRUM-RELATIVE-EME-01

Status: FROZEN BEFORE EXECUTION

Authority: PI-approved neutral Drum-relative EME localization; AD-037; AD-038;
SVP-001.

## Hypothesis

The complete controlled authorized EME population can produce exactly one
neutral Drum-relative localization for every authorized Piano, Double Bass and
Tenor Sax EME while preserving all Drum EME and all target identity, timestamp
and observation provenance.

## Input and Exclusions

The existing controlled audio stems are analyzed without declared tempo,
declared meter, declared phase origin or BeatReference input. The expected EME
populations are Drums 63, Piano 49, Double Bass 27 and Tenor Sax 16. Voice is
deferred. No Ground Truth musical labels enter execution.

## Frozen Acceptance Criteria

- EME populations reproduce as 63/49/27/16 and total 155.
- Exactly 92 non-Drum localization records are produced.
- Losses, merges and creations are zero.
- Target timestamps and identity are unchanged.
- Target and selected Drum observation lineage, source asset, temporal scope,
  origin, rule and execution identity are present.
- An independent implementation reproduces preceding/following identities,
  signed distances, nearest selection and optional interval fraction exactly.
- Two projection executions are identical.
- No declared BPM, meter or BeatReference is supplied or consumed.
- Voice remains deferred.

Failure of any criterion produces `FAIL`; unavailable required evidence
produces `PARTIAL`.
