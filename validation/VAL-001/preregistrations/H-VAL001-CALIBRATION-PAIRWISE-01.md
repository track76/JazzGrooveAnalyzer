# H-VAL001-CALIBRATION-PAIRWISE-01

Status: **FROZEN — NOT EXECUTED**

Authority: PI decision, AD-039, `H-VAL001-CALIBRATION-ZERO-01`,
`GT-VAL-001-v1`, SVP-001 and F-030.

## Frozen Scientific Question

For Ground-Truth-authorized symbolic relationships between Piano and Drums,
Double Bass and Drums, and Tenor Sax and Drums in Calibration Zero, what error
does JGA introduce into the measured inter-source temporal relationship?

This is a controlled instrument-calibration question. It does not authorize a
correction or a human-performance interpretation. Voice remains `DEFERRED`.

## Firewall and Execution State

This protocol is frozen before symbolic pair construction or pairwise-error
calculation. The pair authority must be constructed and frozen without loading
JGA timestamps or absolute correspondence outcomes. Pairwise-error calculation
may begin only after a separate PI execution decision and successful authority
verification. Criteria shall not be changed after result access.

## Frozen Input Authority

Execution shall fail closed unless it verifies and binds exactly to:

- Calibration Zero `CED-VAL-001`, `GT-VAL-001-v1`, AD-039,
  `DGR-CED-VAL-001-001` and `PR-CED-VAL-001-001`;
- authoritative MusicXML SHA-256
  `809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778`;
- frozen `CalibrationSymbolicEvent` artifact
  `validation/VAL-001/run_20260823_070702/calibration_symbolic_events.json`,
  SHA-256
  `038a970994dcb42961d115c6b5c7dd2a05c714b52f5fec3a1756133b5cdedd9f`
  and authority fingerprint
  `b682fadc92be106fcf6b6a5379a4ab840c18e2bc8c852e44a4cda96c30488086`;
- frozen absolute correspondence artifact
  `validation/VAL-001/run_20260823_070702/event_level_results.json`,
  SHA-256
  `13fd9baa9510aa16acbec26547b2d732f0133f6090cda3fb5c1159b31d39c875`;
- frozen absolute result SHA-256
  `406f7ad0de0f95bf03272d0f058ab47d27b9f496e55b733453a026d7a9c61062`
  and scientific fingerprint
  `d9ff1dba90cdb8b96e0412d05dd10c8b972f9dd2c2194187addcff4d6bd2050f`;
- frozen input manifest SHA-256
  `71bc3439eddf781c6fed531d29e67340616ca3ab8352904dfa53b68e38c02600`;
- Drums, Piano, Double Bass and Tenor Sax stem checksums recorded in that
  manifest, 44,100 Hz sample rate, 1,865,728 samples per channel, declared
  sample-zero relationship, 512-sample hop, detector/configuration identity,
  PulseCandidate/EME lineage and exact execution environment; and
- source revision `bbe2b6b8357cf2aafa8bc701199065e8d05b19fc` as the completed absolute
  Calibration Zero authority used by this downstream study.

Piano–Drums, Double Bass–Drums and Tenor Sax–Drums are three separate input
authorities. No pair type may borrow a rule, threshold or result from another.

## Frozen Symbolic Pair-Correspondence Rule

Construct pair authority from the frozen `CalibrationSymbolicEvent` artifact
alone, before loading the absolute correspondence artifact:

1. For each authorized non-Drum symbolic event, compare its exact rational
   `t_GT` with every authorized Drum symbolic event.
2. Exactly one Drum event at exactly equal `t_GT` yields one
   `VALID_SYMBOLIC_PAIR`.
3. No Drum event at exactly equal `t_GT` yields one
   `UNMATCHED_SYMBOLIC_PAIR`.
4. More than one Drum event at exactly equal `t_GT` yields one
   `AMBIGUOUS_SYMBOLIC_PAIR`; preserve every candidate identity and select none.
5. Assign deterministic pair identity from the symbolic-authority fingerprint,
   pair type, source symbolic-event identity and Drum symbolic-event identity.
   Order by exact source `t_GT`, source identity, Drum identity and pair ID.
6. Freeze the complete valid, unmatched and ambiguous population and its
   symbolic-pair-authority fingerprint before any JGA pairwise quantity is
   calculated.

Exact equality is a Ground-Truth relationship in this controlled authority. No
geometrically nearest Drum observation, tolerance, optimization, count-forcing
or result-informed rematching is permitted.

A symbolic pair becomes a `VALID_JGA_PAIR` only when both symbolic members have
exactly one `VALID` correspondence in the frozen absolute result. Otherwise its
unmatched or ambiguous status, candidates and lineage are preserved and no
pairwise error is calculated. One-to-one evidence is never forced.

## Frozen Pairwise Quantities

For every `VALID_JGA_PAIR`, preserve exact values and their seconds and
milliseconds projections:

```text
Delta_GT  = t_source_GT  - t_drum_GT
Delta_JGA = t_source_JGA - t_drum_JGA
e_pair    = Delta_JGA - Delta_GT
absolute_e_pair = abs(e_pair)
```

Preserve pair ID/type, both symbolic identities, both EME identities, all four
timestamps, signed and absolute quantities, contributor/source identities,
PulseCandidate/EME lineage, assets, scope, origin, configuration, execution and
authority provenance. Raw symbolic and observed timestamps are immutable.

## Frozen Descriptive Outputs

Report Piano–Drums, Double Bass–Drums and Tenor Sax–Drums independently before
any cross-source summary:

- symbolic pair relationships and valid JGA pair relationships;
- unmatched and ambiguous symbolic/JGA pairs with complete evidence;
- complete signed and absolute `e_pair` populations;
- minimum, maximum, arithmetic mean, median, population standard deviation and
  Q1/Q2/Q3 using linear empirical quantile interpolation;
- first/second temporal-partition results split at the exact midpoint of the
  declared analysis scope;
- deterministic replay; and
- all event-pair records without suppression.

Initial inference is pair-type-specific. No pooled result may replace a
pair-type result.

## Frozen Candidate Pairwise-Bias Criterion

A pair type is `CANDIDATE_PAIRWISE_BIAS` only when all conditions hold:

1. at least 10 `VALID_JGA_PAIR` records overall and at least 5 in each fixed
   temporal partition;
2. exact deterministic replay of authority, statuses and event-level values;
3. a deterministic 10,000-resample nonparametric bootstrap of median signed
   `e_pair`, seeded from the frozen pairwise input-manifest SHA-256, whose
   percentile 95% interval excludes zero for the complete population and both
   temporal partitions;
4. complete-population and partition medians are nonzero and have one
   consistent sign;
5. each partition interval overlaps the complete-population interval;
6. the conclusion is unchanged in a sensitivity result excluding valid pairs
   for which either absolute correspondence cell is immediately adjacent to an
   unmatched or ambiguous cell; primary records remain retained; and
7. correspondence is stable and provenance is complete, with no unresolved
   authority or execution conflict.

This criterion identifies a candidate calibration property only. It cannot
authorize mathematical correction.

## Stability and Outcome Rules

Temporal stability requires the support, sign, interval-overlap, replay and
sensitivity conditions above. `NO_DETECTABLE_PAIRWISE_BIAS` requires sufficient
support and provenance, exact replay, a complete-population interval containing
zero, partition intervals overlapping the complete interval, and an unchanged
sensitivity conclusion.

The only per-pair outcomes are:

- `NO_DETECTABLE_PAIRWISE_BIAS`;
- `CANDIDATE_PAIRWISE_BIAS`;
- `UNSTABLE_PAIRWISE_MEASUREMENT`; or
- `INSUFFICIENT_EVIDENCE`.

`UNSTABLE_PAIRWISE_MEASUREMENT` applies when support is sufficient but neither
of the first two outcomes satisfies the frozen stability conditions.
`INSUFFICIENT_EVIDENCE` applies when mandatory authority, provenance,
correspondence support or minimum N is absent. The overall outcome may be
`MIXED_SOURCE_SPECIFIC_OUTCOME` when pair-type outcomes differ. Zero is neither
favored nor disfavored by these rules.

## Relation to Absolute Calibration Zero

This downstream study preserves and does not overwrite or reinterpret
`H-VAL001-CALIBRATION-ZERO-01`. It evaluates directly whether the combined
absolute measurement component observed for a source and Drums is retained or
cancels in their difference, using only the frozen pairwise quantities and
criteria. No absolute result predetermines a pairwise outcome.

Any future use of a source-difference correction requires frozen results,
independent validation and a separate PI decision. No correction is calculated
or applied here.

## Frame-Resolution Description

The nominal spacing remains:

```text
h = 512 / 44100 seconds ≈ 11.609977 milliseconds
```

For each `e_pair`, compute the integer `k` minimizing `abs(e_pair - k*h)`;
an exact tie selects smaller absolute `k`, then lower signed `k`. Preserve
`k`, residual `e_pair - k*h`, normalized residual and their complete empirical
distributions. Describe frame-related structure only after applying this rule.
Frame spacing is a measurement property, not an error, tolerance or correction.

## Ground Truth Firewall and Raw Immutability

Ground Truth is authorized only to construct the frozen Calibration Zero
symbolic pair authority and evaluate controlled measurement error. It shall not
move or create EME, modify detection, force correspondence, define timing in
human performance or manufacture musical interpretation.

The experiment may create new pair-calibration records only. It shall never
modify or overwrite symbolic Ground Truth, EME timestamps, PulseCandidates,
Drum-relative localizations, controlled assets or existing calibration and
validation artifacts.

## Reproducibility Requirements

Future execution shall preserve:

- this preregistration and its SHA-256;
- a checksum-bound input manifest and exact environment/configuration;
- the symbolic pair authority, all statuses and its scientific fingerprint;
- two complete deterministic executions from identical frozen inputs;
- the complete event-pair artifact, descriptive and bootstrap outputs;
- an artifact checksum manifest covering every preserved result; and
- a scientific fingerprint over canonical event-pair scientific content,
  excluding execution-local timestamps and paths.

Both executions must reproduce pair identities, EME identities, statuses,
exact quantities, statistics, outcomes and scientific fingerprint. A mismatch
prevents a passing record. The result must be independently recomputable from
frozen inputs.

## Production and Execution Exclusions

No experiment execution, production implementation, configuration change,
timestamp correction, correction table, tolerance, event suppression,
Drum-relative change, dependency addition or musical interpretation is
authorized by this preregistration.
