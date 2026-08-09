# AD-035 — M92 Candidate Period Discovery

Status: LOCKED

## Context

F-032 requires Candidate Periods to originate from reproducible recurrence
evidence before metric interpretation. Campaign 1 experiments
`H-VAL001-C1-03` and `H-VAL001-C1-04` established exact recurrent consecutive
frame intervals as the minimum sufficient first evidence and found no
additional indispensable evidence dimension. The minimum-input audit selected
the existing filtered Core PulseCandidate population.

## Decision

M92 discovers the complete Candidate Period population from ordered filtered
Core PulseCandidate timestamps.

The first production rule is limited to:

1. order PulseCandidates by timestamp;
2. express timestamps on the explicitly configured observation frame grid;
3. calculate consecutive frame intervals;
4. exclude non-positive intervals;
5. preserve every exact positive interval occurring at least twice; and
6. preserve every supporting adjacent observation pair.

No candidate is selected, ranked or assigned musical metric meaning.

## Input

The only scientific input population is the filtered Core PulseCandidate
population. M92 does not consume ElementaryMetricEvent, EnsembleMetricEvent,
BeatReference, Pulse or InternalMetricTimeline.

The PulseCandidate observation frame length is explicit at its producer and is
passed directly into discovery configuration. M92 does not recover it from a
library default.

## Output

M92 produces the immutable `CandidatePeriodPopulation` defined by AD-034. It
preserves:

- all supported Candidate Period durations;
- all supporting occurrence indices and timestamps;
- observation, source and temporal scope;
- seconds as the temporal measurement unit;
- input asset path and content checksum;
- explicit frame length, sample rate and recurrence rule configuration; and
- source revision only when genuinely supplied.

Ordinary pipeline execution leaves source revision absent. It does not
fabricate experiment, validation-run or validation-protocol identities.

## Pipeline Position

Discovery runs immediately after PulseCandidate filtering and before pulse
interval construction, Metric Context, Translation and Domain reconstruction.
The immutable population is preserved independently on `AnalysisContext` and
does not alter or feed the existing reconstruction path.

## Non-responsibilities

M92 defines no beat, tempo, meter, tactus, metric level, selection, ranking,
confidence, stability, persistence, phase analysis, non-consecutive lag
analysis, cross-source candidate type or statistical clustering.

It does not modify `BeatPeriodEstimator`, Translation, Domain reconstruction,
Ground Truth, Comparator, Immutable Analysis Representation or Scientific
Validation Record.

## Validation

Validation requires deterministic immutable output, complete recurrence
occurrence preservation, explicit configuration and exact reproduction of the
accepted C1-03/C1-04 VAL-001 full-mix and controlled-WAV candidate
populations.

## Governing References

- `docs/scientific/foundations/F-031_HIERARCHICAL_METRIC_PERIODICITY.md`
- `docs/scientific/foundations/F-032_CANDIDATE_PERIODS.md`
- `docs/architecture/AD-034_M91_CANDIDATE_PERIOD_REPRESENTATION.md`
- `validation/VAL-001/run_20260809_100843/`
- `validation/VAL-001/run_20260809_1344/`
