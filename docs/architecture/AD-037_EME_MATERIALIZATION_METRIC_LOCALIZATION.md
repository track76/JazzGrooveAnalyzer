# AD-037 — EME Materialization and Metric Localization

Status: LOCKED

## Decision

ElementaryMetricEvent existence and cardinality are determined by authorized
source-event evidence before metric localization.

The canonical order is:

```text
Preserved source observations
→ authorized source-event materialization
→ ElementaryMetricEvent population
→ metric localization
→ future interpretation
```

Metric association must not determine EME existence or cardinality.

Metric structures may locate an existing EME, relate it to an authorized
BeatReference and derive neutral temporal coordinates. They shall not suppress,
merge or create EME. Multiple distinct EME from one contributor may occupy the
same quarter interval and retain independent identities and observation
lineage.

For the current source-observation materialization contract, every preserved
PulseCandidate independently supports one source-event EME. This represents a
physical temporal event supported by observation; it does not assert symbolic
note identity. Any future consolidation requires independent non-metric
scientific authority and must preserve all supporting observations.

## Metric Localization

Declared-quarter localization records:

- the preceding BeatReference;
- the following in-scope BeatReference when present;
- elapsed physical seconds from the preceding reference; and
- normalized phase `elapsed / quarter_period` in `[0, 1)`.

An event exactly on a reference belongs to that reference with phase zero.
Distinct EME with identical timestamps remain distinct. An event in the final
in-scope interval remains localizable even when the following reference lies
outside the declared scope.

These quantities are geometric and temporal only. They introduce no beat,
offbeat, subdivision, anticipation, delay or groove interpretation.

## Supersession and History

AD-037 supersedes the AD-018 requirements that EME construction depends on a
reconstructed movement, that one contributor/movement pair permits at most one
EME, and that multiple temporal positions in one movement suppress EME as
ambiguous.

AD-018 remains historically authoritative for the motivation to distinguish
physical observations from Domain representation, to preserve contributor and
observation lineage, and to prohibit unsupported musical interpretation.

## Architectural Consequence

The existing Translation and Domain boundaries are sufficient. EME
materialization precedes `BeatReconstructionEngine`; metric localization then
packages all EME into the existing MetricCluster and MetricPoint structures.
No new architectural layer is introduced.
