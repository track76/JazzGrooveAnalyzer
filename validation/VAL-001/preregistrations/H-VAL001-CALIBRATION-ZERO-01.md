# H-VAL001-CALIBRATION-ZERO-01

Status: **FROZEN — NOT EXECUTED**

Authority: AD-039, JGA Scientific Research Constitution, SVP-001, AD-028,
AD-033, AD-037, AD-038 and F-030.

## Frozen Scientific Question

When authoritative symbolic event timing is known, what signed temporal
difference is observed across the complete provenance-bound path:

```text
authoritative symbolic timing
→ controlled rendering
→ physical audio observation
→ JGA detection
→ immutable EME timestamp?
```

This experiment characterizes the measuring system. It does not interpret
human performance timing and does not authorize correction.

## Firewall and Execution State

This preregistration is frozen before event-level symbolic/JGA differences are
inspected. No event-level correspondence result, signed error, absolute error,
distribution or calibration statistic has been computed or accessed while
preparing it.

The experiment shall not execute until the PI separately authorizes execution
of this frozen protocol. Criteria shall not be tuned after result access.

## Calibration Zero Input Binding

Execution shall fail closed unless its manifest binds exactly to:

- Controlled Dataset `CED-VAL-001`, Dataset Generation Record
  `DGR-CED-VAL-001-001` and Provenance Revision `PR-CED-VAL-001-001`;
- Ground Truth identity `GT-VAL-001-v1`;
- authoritative MusicXML at
  `recordings/validation/ground_truth/03 THE COST OF LIVING versione intro + 8 bar.musicxml`;
- MusicXML SHA-256
  `809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778`;
- an event-authority schema/revision produced and frozen as specified below;
- authoritative controlled WAV stems and AD-033 checksums for Drums, Piano,
  Double Bass and Tenor Sax;
- stereo PCM WAV, 24-bit, sample rate 44,100 Hz and exactly 1,865,728 samples
  per channel;
- the declared relationship `MusicXML score time zero = WAV sample zero`;
- contributor, symbolic part and observed SoundSource identities;
- complete effective observation configuration;
- hop length 512 samples and its owning configuration identity;
- detector implementation/version and source revision;
- PulseCandidate and EME identity/lineage;
- numeric analysis scope and temporal origin;
- execution ID, environment, Python/dependency versions and source revision.

Voice remains `DEFERRED` and is excluded from execution unless separately
authorized before a new preregistration is frozen. Obsolete MP3 stems are not
Calibration Zero inputs.

## Ground Truth Event Authority Construction

AD-028 does not currently establish `GroundTruthEvent`. Before any JGA event
timestamp is accessed for comparison, execution shall construct and freeze a
calibration-only symbolic event authority from the bound MusicXML as follows:

1. Preserve original part, measure, voice, staff and note identities and exact
   symbolic onset time from score origin.
2. Exclude rests and tied continuations that do not initiate a new symbolic
   attack. Preserve the exclusion reason and original identity.
3. Within each authorized contributor/source, group all attack-bearing notes
   with exactly equal symbolic onset time into one `CalibrationSymbolicEvent`.
   Preserve every constituent note identity; grouping asserts common symbolic
   onset only, not rendered acoustic identity.
4. Assign deterministic identity from Ground Truth identity, source identity,
   exact symbolic onset and sorted constituent-note identities.
5. Order events by exact symbolic onset then deterministic identity.
6. Freeze the complete per-source population, exact rational timestamps,
   exclusions, schema revision, source checksum and scientific fingerprint.

The event-authority artifact shall be frozen before observed EME timestamps are
loaded into the correspondence stage. If exact onset identity cannot be
constructed without an undocumented assumption, execution status is
`INSUFFICIENT_EVENT_AUTHORITY` and stops before error calculation.

## Frozen Event-Correspondence Rule

Correspondence is contributor-separated and uses no cross-source pooling.
Observed EME are never used to alter the symbolic population.

For each source, let the ordered distinct symbolic event times be
`g_0, ..., g_(n-1)`. Define deterministic symbolic capture cells on the
declared audio scope:

- the boundary between adjacent times `g_i` and `g_(i+1)` is their exact
  arithmetic midpoint;
- the first cell begins at declared scope start;
- the final cell ends at declared scope end;
- ordinary cells are left-closed and right-open;
- an observed timestamp exactly equal to an internal midpoint is
  `AMBIGUOUS_BOUNDARY` and belongs to neither adjacent valid correspondence.

For each symbolic cell:

- exactly one in-cell EME produces one `VALID` correspondence;
- zero in-cell EME produces one `UNMATCHED_SYMBOLIC` result;
- more than one in-cell EME produces one `AMBIGUOUS_MULTIPLE_OBSERVED` result,
  preserving all candidate EME without selecting one.

An observed EME outside the declared scope, on an ambiguous midpoint, or not
consumed by a `VALID` cell is reported as unmatched or ambiguous with its full
identity and lineage. No timing tolerance, nearest-neighbour optimization,
sequence alignment, count-forcing or post-result rematching is permitted.

The midpoint-cell rule is an objective temporal partition, not proof that a
rendered transient and symbolic event are physically identical. Correspondence
limitations remain part of the result. A sensitivity record shall separately
report valid cells immediately adjacent to any unmatched or ambiguous cell;
those events remain in the primary result and are never deleted.

## Primary Event-Level Quantities

For every `VALID` correspondence:

```text
e_i = t_JGA,i - t_GT,i
absolute_error_i = abs(e_i)
```

`t_GT` is the exact authoritative symbolic event time projected to seconds from
the declared common origin. `t_JGA` is the immutable observed EME timestamp.
Both values, signed error and absolute error are preserved in seconds and
milliseconds. `t_JGA` is never modified.

The term error means empirical measurement difference under AD-039. It does
not isolate detector error or imply musical interpretation.

## Frozen Descriptive Outputs

Per contributor/source and overall, preserve and report:

- total symbolic events and total observed EME;
- valid correspondences;
- unmatched symbolic events and unmatched observed EME;
- ambiguous boundary and multiple-observed correspondences;
- complete event-level signed and absolute errors;
- minimum, maximum, arithmetic mean, median, population standard deviation,
  and Q1/Q2/Q3 using linear empirical quantile interpolation;
- complete empirical signed-error and absolute-error distributions;
- frame-offset and frame-residual distributions defined below;
- first/second temporal-scope descriptive partitions defined below;
- results with cells adjacent to correspondence ambiguity identified;
- deterministic replay comparison.

No event, including unmatched or ambiguous evidence, may be suppressed. The
machine-readable record shall retain symbolic identity, exact `t_GT`, EME ID,
exact `t_JGA`, contributor/source, PulseCandidate/EME lineage, correspondence
status, scope, asset and execution provenance.

## Frame-Quantization Description

The frozen nominal frame spacing is:

```text
h = 512 / 44100 seconds ≈ 11.609977 milliseconds
```

For every valid signed error, compute the integer `k_i` minimizing
`abs(e_i - k_i*h)`. An exact equal-distance integer tie selects the integer
with smaller absolute value, then the smaller signed integer. Preserve:

```text
frame_offset_i = k_i
frame_residual_i = e_i - k_i*h
normalized_frame_residual_i = frame_residual_i / h
```

Report the complete empirical distributions per source and overall, including
counts exactly on floating/rationally equivalent frame multiples, residual
quantiles and residual signs. Visualizations shall retain individual
observations.

The descriptive conclusion shall state whether the observed distribution:

- concentrates on frame multiples;
- occurs around frame multiples with residual dispersion;
- exhibits stable signed displacement from frame multiples; or
- does not exhibit visible frame-related structure.

These descriptions shall be based on the preserved offset/residual
distributions, not an assumed error model. No frame-based correction,
tolerance or microtiming threshold is created. Frame spacing remains a
measurement property, not an error estimate.

## Candidate Systematic-Bias Criterion

The following criterion is frozen before result access and identifies only a
**candidate** bias. It cannot authorize correction.

For one source, candidate systematic bias requires all of:

1. at least 10 `VALID` correspondences overall and at least 5 in each of two
   fixed temporal partitions split at the exact midpoint of the declared
   analysis scope;
2. exact deterministic replay of event authority, correspondence statuses and
   all event-level quantities;
3. a deterministic 10,000-resample nonparametric bootstrap of the median
   signed error, using seed derived from the frozen input-manifest SHA-256,
   whose percentile 95% interval excludes zero for the full source and for
   each temporal partition;
4. full, first-partition and second-partition median signed errors with the
   same sign;
5. overlap between each partition's 95% median interval and the full-source
   interval;
6. the same pass/fail conclusion in the sensitivity scope that excludes valid
   cells immediately adjacent to unmatched or ambiguous cells; and
7. no unresolved source-identity, event-authority, correspondence, provenance
   or execution conflict affecting the evaluated population.

Failure to satisfy this conjunction means systematic bias is not demonstrated
for that source. Bootstrap intervals characterize event-population stability
under this frozen analysis; they do not establish rendering/detection causal
decomposition or correction eligibility.

## Source-Specific and Source-Independent Description

Each source is evaluated independently before any overall summary.

- `SOURCE_SPECIFIC_CANDIDATE_BIAS` requires at least one source satisfying the
  candidate criterion and at least one pair of qualifying sources whose
  deterministic bootstrap 95% interval for the difference of median signed
  errors excludes zero.
- `SOURCE_INDEPENDENT_CANDIDATE_BIAS` requires at least two sources satisfying
  the candidate criterion, every pairwise median-difference interval among
  those sources to include zero, and the pooled qualifying-source median
  interval to exclude zero.
- If neither rule is satisfied, no source-specific or source-independent
  candidate bias is reported.

Overall pooled statistics never replace contributor-separated results.

## Pairwise Consequence

For each source pair, report descriptively the difference between their median
signed measurement errors and its frozen deterministic bootstrap interval.
This assesses whether independently estimated source behaviour could affect
observed inter-instrument differences.

No production correction is calculated or applied. Any future use of

```text
Delta_corrected = Delta_observed - (b_A - b_B)
```

requires frozen calibration results, independent validation and a separate PI
decision.

## Rendering-versus-Detection Limitation

This experiment uses fixed rendered assets and observes the combined path from
symbolic time through controlled rendering and JGA measurement. It shall report
**combined rendering/measurement behaviour** unless independent evidence in a
separately authorized design identifies rendering and detection components.
Deterministic replay of fixed audio demonstrates computational repeatability;
it does not establish repeatability across new renders.

## Allowed Scientific Outcomes

The frozen result shall report a bias-evidence outcome and a measurement-
structure outcome. Together they may yield `MIXED_MEASUREMENT_BEHAVIOUR`.
The complete allowed vocabulary is:

- `NO_DETECTABLE_SYSTEMATIC_BIAS`;
- `SOURCE_INDEPENDENT_CANDIDATE_BIAS`;
- `SOURCE_SPECIFIC_CANDIDATE_BIAS`;
- `QUANTIZATION_DOMINATED_MEASUREMENT`;
- `RESIDUAL_OR_UNSTABLE_MEASUREMENT_VARIABILITY`;
- `MIXED_MEASUREMENT_BEHAVIOUR`; or
- `INSUFFICIENT_EVIDENCE`.

The bias-evidence outcome is determined only by the frozen candidate-bias
criteria and is one of `NO_DETECTABLE_SYSTEMATIC_BIAS`,
`SOURCE_INDEPENDENT_CANDIDATE_BIAS`, `SOURCE_SPECIFIC_CANDIDATE_BIAS` or
`INSUFFICIENT_EVIDENCE`.

The measurement-structure outcome is an explicitly descriptive reading of the
complete frame-offset/residual and signed-error distributions and is one of
`QUANTIZATION_DOMINATED_MEASUREMENT`,
`RESIDUAL_OR_UNSTABLE_MEASUREMENT_VARIABILITY`,
`MIXED_MEASUREMENT_BEHAVIOUR` or `INSUFFICIENT_EVIDENCE`. It shall preserve the
underlying observations and state the visible empirical basis; it creates no
correction or accuracy claim. Mixed behaviour is selected when multiple
descriptive structures remain and no single description is adequate.
Insufficient evidence is selected for failed input authority, insufficient
correspondence support, unresolved provenance or other blocked mandatory
evidence.

Negative and unresolved outcomes are valid scientific results.

## Raw Immutability and Ground Truth Firewall

The experiment may create new calibration records only. It shall never modify
or overwrite EME timestamps, PulseCandidates, Drum-relative localization,
controlled assets, Ground Truth sources or existing validation artifacts.

Ground Truth is used only to construct frozen Calibration Zero event authority,
establish correspondence under the frozen rule, and characterize measurement
difference. It shall not create or move EME, tune detection, force
correspondence, manufacture tempo or meter, or introduce musical
interpretation. BPM, meter, measures and musical performance labels do not
enter the experiment.

## Determinism, Artifacts and Reproducibility

The future execution shall preserve:

- unchanged preregistration checksum;
- frozen input manifest and checksums;
- calibration symbolic-event authority and exclusions;
- effective configuration and complete environment provenance;
- two complete deterministic executions from identical inputs;
- event-level correspondence and quantity records for both executions;
- contributor and overall descriptive outputs;
- frame-offset/residual outputs and candidate-bias decision record;
- raw machine-readable results and human-readable report;
- artifact manifest with SHA-256 for every preserved file;
- scientific fingerprint computed from canonical event-level scientific
  content, excluding execution-local timestamps and paths;
- completion protocol recording Ground Truth access, PI authority and every
  frozen acceptance/outcome decision.

Both executions must reproduce symbolic-event identities, EME identities,
correspondence statuses, exact event-level quantities, descriptive statistics,
outcome and scientific fingerprint. Any mismatch is reported and prevents a
PASS calibration record.

The complete result must be independently recomputable from the frozen
repository inputs without altering them.

## Production and Interpretation Exclusions

No production implementation, detector/configuration change, timestamp
correction, correction table, tolerance, event suppression, Drum-relative
change, dependency addition or musical interpretation is authorized. No result
from this future experiment may enter production without a separate PI
decision after the result is frozen and independently validated.
