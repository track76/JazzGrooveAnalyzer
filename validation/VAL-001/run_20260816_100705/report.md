# H-VAL001-EME-DRUM-01 — Drum Event Correspondence Audit

## Boundary and procedure

The checksum-bound controlled drum WAV was analyzed twice through the
unchanged production pipeline with `NullSeparator`. Both blind observation
records were byte-identical. The first record was written and its SHA-256 was
frozen before the authoritative MusicXML was loaded.

The preregistered score-to-audio mapping was:

```text
expected seconds = absolute quarter-note position * 60 / 78
```

This follows the declared controlled-dataset origin, `MusicXML score time zero
= WAV sample zero`. The detector timestamp resolution is one 512-sample hop at
44,100 Hz: `0.011609977324263039` seconds. Before comparison, one resolution
cell was fixed as the maximum absolute correspondence error. A match required
a unique edge in both directions; neither symbolic events nor observations
could be reused. The bound was not changed after observing results.

## Result

- Authoritative symbolic drum unique onsets: 63
- Blind PulseCandidates: 63
- Exact timestamp matches: 0
- Unique correspondence matches: 19
- Missed symbolic onsets under the preregistered rule: 44
- Extra PulseCandidates under the preregistered rule: 44
- Symbolic onsets with multiple candidate assignments: 0
- Candidates with multiple symbolic assignments: 0
- Minimum signed matched error: `+0.004270015698587315` seconds
- Maximum signed matched error: `+0.01151229722658087` seconds
- Median absolute matched error: `0.00900750043607168` seconds
- Mean absolute matched error: `0.008893295509837062` seconds

Event correspondence result: **PARTIAL**.

Equal population counts do not establish correspondence. Existing evidence
scientifically establishes 19 event correspondences under the preregistered
measurement-resolution rule. It does not establish identities for the other
44 pairs. Expanding the bound would require a separately authorized detector
localization-error model and cannot be inferred from these outcomes.

The current drum PulseCandidate population therefore cannot be treated as a
complete drum-event TAC. It is partially validated only for the 19 established
correspondences.

No production implementation is justified by this audit. Existing
architecture carried the required observation evidence; the first blocker is
scientific validation of temporal localization, not a missing representation.

