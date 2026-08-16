# H-VAL001-RHYTHM-STRENGTH-01 — Blind Strength Role Discrimination

Status: PREREGISTERED — NOT EXECUTED

## Question and frozen input

Can AD-032-preserved onset strength discriminate the immutable SHORT and LONG
families from `H-VAL001-RHYTHM-TEMPO-01`? Inputs are the exact 63 Drums, 27
Double Bass and 49 Piano EME identities/timestamps frozen there, their single
supporting Domain PulseCandidate, its unchanged Core onset strength, and the
eight immutable candidate identities. No candidate is regenerated.

Strength is `librosa.onset.onset_strength` at the already-frozen detected
frame, calculated from the checksum-bound isolated stem by the existing
`SourcePulseCandidateBuilder`, then copied unchanged by AD-032. Recovery must
reproduce every supporting deterministic PulseCandidate identity; otherwise
the result is `INSUFFICIENT`.

## Frozen statistic

For source events `(t_i,s_i)`, scope `S`, and candidate period `P`, center
strength within the scope, `d_i=s_i-mean_S(s)`, and calculate the origin-
invariant strength/phase association

`A(P,S) = |sum_i d_i exp(2π i t_i/P)| / sum_i |d_i|`.

If the denominator is zero, evidence is insufficient. Candidate uncertainty is
handled exactly as previously: evaluate every integer-frame period in its
frozen measurement interval. The blind nuisance origin is every integer residue
in `[0,P)`; it changes only the complex angle, not `A`, and the invariant
magnitude must agree for every origin. No phase or event is selected or removed.

Compute `A` independently for FULL scope and the exact EARLY/LATE timestamp
halves already frozen by the parent experiment. For each of the twelve frozen
SHORT:LONG 1:2 relations, compare every admissible short-period value with
every admissible long-period value in FULL, EARLY and LATE. A relation favors a
family only if every comparison in every scope is strictly in that direction;
an exact tie or mixed direction is unresolved.

A source prefers one family only if all twelve relations favor that family. It
is otherwise `EQUIVALENT_UNRESOLVED`. Equal-source consensus prefers a family
only with at least two source preferences and no opposite preference; opposite
preferences yield `SOURCE_DISAGREEMENT`; no two-vote family yields
`EQUIVALENT_UNRESOLVED`; failed integrity/replay yields `INSUFFICIENT`.

Execute twice. Exact serialized statistics, source decisions, consensus and
scientific fingerprint must match. Freeze and checksum the blind result before
Ground Truth access.

## Firewall

Ground Truth, 78 BPM, 4/4, declared timeline/phases, symbolic evidence, Voice,
Tenor Sax and AI evidence are excluded. The procedure assigns no metric or
musical role except its allowed blind family classification. Post-freeze
Ground Truth validation cannot alter the result.
