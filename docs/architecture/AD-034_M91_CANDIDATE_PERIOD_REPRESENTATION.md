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
- minimum runtime input and execution provenance; and
- the temporal unit and explicit discovery configuration required to recover
  the evidence.

The population and every nested value are immutable. Decimal temporal values
preserve the supplied evidence without normalization or interpretation.

## M91.1 Responsibility Correction

M91.1 separates general Candidate Period evidence from scientific-validation
record metadata under F-030 and SVP-001.

The general representation does not require:

- experiment identity;
- validation run identity;
- scientific-validation protocol identity; or
- first and repeated execution fingerprints.

Those values belong to completed experimental and validation records. A
runtime Candidate Period population remains capable of participating in
reproducible science by preserving its evidence, scope, input content identity,
temporal unit and explicit discovery configuration. Proof of repeated
execution is attached by the scientific record when such validation occurs.

Input asset path and checksum remain runtime provenance. Source revision is
preserved when available but is not fabricated by ordinary production
execution.

Measurement conditions used by a discovery procedure are preserved as
explicit population-level discovery configuration. They are not intrinsic
fields of an individual Candidate Period and must not be recovered silently
from implementation defaults.

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
immutability, observation scope, runtime provenance, explicit discovery
configuration and compatibility with the preserved experimental population
without executing discovery logic. Experimental reproduction fingerprints
remain preserved by the source validation record.

## Governing References

- `docs/JGA_DEVELOPMENT_CONSTITUTION.md`
- `docs/architecture/CORE_DOMAIN_BOUNDARY.md`
- `docs/scientific/foundations/F-031_HIERARCHICAL_METRIC_PERIODICITY.md`
- `docs/scientific/foundations/F-032_CANDIDATE_PERIODS.md`
- `validation/VAL-001/run_20260809_100843/`
