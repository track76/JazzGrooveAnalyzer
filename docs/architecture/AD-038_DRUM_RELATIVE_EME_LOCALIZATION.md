# AD-038 — Neutral Drum-Relative EME Localization

Status: LOCKED

## Decision

The immediate minimum scientific path is:

```text
absolute audio timeline
→ authorized ElementaryMetricEvent population
→ neutral Drum-relative localization
→ later scientific comparison
```

Every authorized non-Drum EME is localized against the preserved Drum EME
population as observed physical timestamps. Drum EME are not assigned musical
or metric meaning. Localization never determines EME existence, contributor
classification or cardinality.

For target timestamp `t`, the preceding Drum EME is the last deterministically
ordered Drum EME whose timestamp is `<= t`; the following Drum EME is the first
whose timestamp is `> t`. Signed distances are `t - reference_timestamp`.
The nearest reference minimizes absolute temporal distance. A tie between the
surrounding references is recorded and selects the preceding reference only as
a deterministic serialization rule. Other equal-time candidates use stable
EME identity ordering and remain preserved in the input population.

The optional geometric quantity

```text
(t - preceding_timestamp) / (following_timestamp - preceding_timestamp)
```

is produced only when both references exist and have different timestamps. It
is named `observed_interval_fraction` and carries no musical interpretation.

## Absolute Time and Provenance

The exact numeric EME timestamp remains authoritative. `HH:MM:SS.mmm` is a
deterministic presentation projection only. Each localization preserves target
and selected Drum EME identity, contributor/source identity, supporting
PulseCandidate observation lineage, asset identity, temporal scope, temporal
origin, rule version and execution provenance.

Voice remains deferred, not excluded.

## Architectural Consequence

The existing architecture is sufficient. Drum-relative localization is a
separate downstream Representation projection from authorized EME. It does not
consume, replace or alter BeatReference, declared tempo, meter, MetricCluster,
reconstructed-measure or existing representation behavior. No new
architectural layer is introduced.
