# H-VAL001-BEATREF-01 — Controlled BeatReference Timeline Validation

## Result

**FAIL.** JGA derives the declared quarter period correctly as exact `10/13`
seconds and generates timestamps analytically as `origin + index * period`.
One timeline is shared across the analysis, and BeatReference reconstruction
does not depend on EME creation.

The current origin is the first 50 ms ensemble-consensus centroid at
`0.046439909297052155` seconds. This is observation-derived physical timing,
but no authorized evidence assigns it quarter-note phase. Its metric use is
therefore **UNSUPPORTED**.

The engine creates one BeatReference per pre-EME consensus group. For the
controlled MP3, 77 preserved observations produce 74 consensus groups and 74
BeatReferences. The resulting timeline ends at `56.20028606314321` seconds,
`13.96028606314321` seconds beyond the reported 42.24-second audio scope.
Movement count is consequently source-density-dependent.

Two complete runs reproduce timestamps exactly but not BeatReference UUIDs,
because the UUID input includes nondeterministic PulseCandidate identities.
BeatReferences also do not retain the declared authority identity, checksum,
numeric scope or origin status.

## Ground Truth boundary

CED-VAL-001 declares `MusicXML score time zero = WAV sample zero` for the five
authoritative WAV stems. It does not establish that the analyzed MP3 sample
zero has the same origin. Ground Truth therefore exposes the missing origin
authority but cannot be used to rewrite the already captured runtime
timeline.

## Implementation decision

No production correction is made. Correcting count, identity or provenance
without an authorized origin and numeric temporal scope would not satisfy the
scientific contract. Introducing those missing authorities or inventing an
observation-to-grid association rule is outside the approved validation task.
