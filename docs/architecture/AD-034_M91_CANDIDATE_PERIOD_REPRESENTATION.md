# AD-034 — M91 Candidate Period Representation

Status: LOCKED

## Context

F-031 and F-032 define Candidate Periods as pre-interpretive,
observation-derived temporal relations supported by reproducible recurrence
evidence. Campaign 1 experiment `H-VAL001-C1-03` preserved the first controlled
Candidate Population but used an experiment-local discovery protocol.

M91 requires an immutable representation capable of preserving already
produced Candidate Period evidence. It does not authorize a production
discovery protocol.

## Decision

Candidate Period evidence is represented in `jga.core`, which already owns
observable computational representations under the Development Constitution
and the Core–Domain Boundary.

The representation preserves only:

- Candidate Period duration;
- supporting recurrence occurrences;
- observation population, source and temporal scope;
- input, experiment, protocol and source-revision provenance; and
- measurement conditions and reproduction fingerprints.

The population and every nested value are immutable. Decimal temporal values
preserve the supplied evidence without normalization or interpretation.

## Boundary

M91 accepts Candidate Periods already produced by an external scientific
process. It does not discover, generate, rank, select, consume or interpret
them.

The representation is standalone. It does not add Candidate Periods to
`MetricContext`, `AnalysisContext`, the Immutable Analysis Representation or
the current reconstruction path.

## Non-responsibilities

M91 defines no:

- recurrence equality rule, tolerance, threshold or estimator;
- beat, BPM, tempo, tactus, subdivision, meter or metric level;
- confidence, stability, persistence, locality or ranking;
- Candidate Period discovery or selection component; or
- change to `BeatPeriodEstimator` or metric reconstruction.

The discovery procedure recorded by `H-VAL001-C1-03` remains experiment-local
and is not promoted to production authority.

## Validation

Validation instantiates the representation directly from the frozen blind
evidence in `validation/VAL-001/run_20260809_100843/`. It verifies deep
immutability, observation scope, provenance and preserved deterministic
reproduction fingerprints without executing discovery logic.

## Governing References

- `docs/JGA_DEVELOPMENT_CONSTITUTION.md`
- `docs/architecture/CORE_DOMAIN_BOUNDARY.md`
- `docs/scientific/foundations/F-031_HIERARCHICAL_METRIC_PERIODICITY.md`
- `docs/scientific/foundations/F-032_CANDIDATE_PERIODS.md`
- `validation/VAL-001/run_20260809_100843/`
