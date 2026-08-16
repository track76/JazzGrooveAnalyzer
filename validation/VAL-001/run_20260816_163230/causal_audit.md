# H-VAL001-AI-VOICE-02-CAUSAL-01 — Frozen SOME Causal Audit

This read-only audit used only the arrays already frozen by
`H-VAL001-AI-VOICE-02`. SOME was not rerun, and no parameter, threshold,
event or model output was changed.

## Terminal MIDI-67 boundaries

All three exactly abutting splits are caused by localized positive output from
SOME's native boundary head. Each rise advances the cumulative decoded
boundary state by one. Across the native seven-frame inspection window at all
three boundaries, activity remains present, MIDI 67 remains the framewise
maximum, both neighboring decoded segments are non-rest, and no chunk boundary
occurs.

The splits are therefore causally explained as native model boundary
decisions within a continuously active same-pitch trajectory. Frozen evidence
does not establish that these model decisions are scientifically erroneous,
and no approved rule authorizes discarding them or merging their events.

## Symbolic MIDI-75 discrepancy

Exact temporal localization of the symbolic event is not authorized. The
audit is consequently limited to the ordered inferred region between the
decoded MIDI-74 and MIDI-72 segments.

MIDI 75 has substantial framewise probability support inside the decoded-74
segment (maximum `0.829603`; median `0.783591`) and is nearly equal to MIDI 74
immediately before the native 74-to-72 boundary. It is never the framewise
maximum and receives no separate boundary. The discrepancy is therefore
classified **C. COMPETING PITCH HYPOTHESIS**: model evidence exists, but the
unchanged decoder does not materialize an independent MIDI-75 segment.

## Decision

The three terminal splits account for three additional inferred segments; the
unmaterialized MIDI-75 accounts for one absent segment. This explains the net
`13 - 11 = 2` population discrepancy without validating event identities.

SOME remains materially better than Basic Pitch for this controlled Voice
source, but the outcome remains **PARTIAL**. Production integration and another
Voice AI model are not justified. The exploratory Voice AI branch can close.
