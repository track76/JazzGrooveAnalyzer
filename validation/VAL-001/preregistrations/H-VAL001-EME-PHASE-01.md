# H-VAL001-EME-PHASE-01 — Complete EME Phase-Population Preregistration

Status: PREREGISTERED — NOT EXECUTED

Authority: JGA Scientific Research Constitution, SVP-001, F-030 and AD-037

## Scientific question

Does each complete, authorized contributor-specific EME population exhibit a
reproducible concentration structure in normalized quarter phase, without
assuming musical subdivision, role or label?

This record freezes the analysis procedure before its execution. No phase
population was inspected to choose this procedure.

## Frozen input

The input is the complete AD-037 EME population and metric localization from
`H-VAL001-EME-CARDINALITY-01`, preserved at repository revision
`01da05818c8d2452b00af1870ada50db06ed25a5`. Its frozen `result.json` SHA-256
is `ce684b7062d78c96de4e2520dc9dfbededf605aaf671ec2f03814d97347f5785`:

| Contributor | Authorized EME |
|---|---:|
| Drums | 63 |
| Piano | 49 |
| Double Bass | 27 |
| Tenor Sax | 16 |

The declared quarter timeline has origin `0` seconds, period `10/13` seconds,
55 BeatReferences and scope `[0, 1865728/44100)`. Every EME shall enter the
analysis exactly once. No EME may be removed, merged, duplicated or pooled
across contributors.

Voice is `DEFERRED`: its source-event EME population is not authorized. Once
authorized, Voice shall use this same EME → metric localization → normalized
phase contract. Basic Pitch and SOME output are excluded and the Voice AI
branch remains closed.

## Phase geometry

For EME timestamp `t`, preceding quarter reference `b` and quarter period `T`:

`phase = (t - b) / T`, in `[0, 1)` under AD-037 boundary handling.

The circular representation is `z = exp(2πi phase)`. Circular distance in
turns is:

`d(a, b) = min(|a - b|, 1 - |a - b|)`.

Thus phases near zero and one are adjacent. Exactly coincident phase values
remain separate observations with independent identity and lineage.

The observation timestamp resolution is one 512-sample frame at 44.1 kHz.
Expressed in quarter phase, one frame is exactly
`(512/44100) / (10/13) = 832/55125` turns. A fitted component whose circular
standard deviation is smaller than this measurement resolution is
inadmissible: the evidence cannot resolve that concentration. This physical
bound prevents singular zero-width mixture components without introducing an
outcome-selected tolerance.

## Statistical procedure

Each contributor is analysed independently. Fit these candidate circular
probability models to all of its EME:

1. `K = 0`: the uniform circular distribution (no concentration);
2. `K >= 1`: a finite mixture of `K` von Mises components.

For a population of size `n`, evaluate every integer `K` from 1 through
`floor(n/3)`. A `K`-component mixture has `3K - 1` free parameters. A fitted
model is admissible only when every component has effective membership
`Σ responsibilities >= 3`; this supplies at least one effective observation
per component parameter, and when every component satisfies the measurement-
resolution bound above. An inadmissible fit is not selected. Its observations
remain in all other candidate likelihoods.

Fit by maximum likelihood using deterministic, documented initializations and
a fixed implementation/version. Repeat the complete fit from the identical
input and configuration. The experiment record shall preserve software
versions, initialization scheme, convergence state, model parameters,
log-likelihoods and fingerprints.

Select the admissible model with minimum Bayesian Information Criterion:

`BIC = p ln(n) - 2 ln(L)`.

The uniform model participates in the same selection. An exact BIC tie selects
the smaller `K`; a tie with the uniform model selects uniform. No expected
center, width, component count or musical location enters fitting or selection.

## Stability and uncertainty

Use 2,000 contributor-level nonparametric bootstrap resamples of EME identity,
with replacement and at original sample size. The pseudorandom seed is the
SHA-256-derived integer of the preregistration identifier plus contributor ID;
it shall be recorded before execution.

A selected concentration structure is `STABLE` only when:

- deterministic replay produces identical selected model, parameters within
  the serialized numeric precision and scientific fingerprint;
- the same `K` is selected in at least 95% of bootstrap resamples; and
- every selected component is admissible and can be matched one-to-one across
  at least 95% of bootstrap resamples by minimum total circular center distance.

Report 95% percentile bootstrap intervals for component weight and
concentration. Center intervals are computed after unwrapping each matched
bootstrap center around its full-sample center and are then reported modulo
one. Report the complete bootstrap selection-frequency table. These criteria
are identical for all contributors; lower sample size is reflected by wider
uncertainty or failure to satisfy stability, not by source-specific tuning.

## Tiny components, outliers and failed fits

No observation is classified or removed as an outlier. No residual threshold
is used. A component below the effective-membership admissibility rule makes
that candidate model inadmissible; it does not delete its supporting EME.
Non-convergence makes only that fit inadmissible and must be reported. If no
non-uniform model is both selected and stable, the result is not a stable
concentration structure.

## Contributor comparison

Drums, Piano, Double Bass and Tenor Sax results must be frozen independently
before comparison. Dense contributors receive no additional weight and no
initial ensemble pool is permitted.

Only components that are independently stable may enter a secondary pairwise
comparison. Compare a joint model in which a matched component center is
shared between contributors with the corresponding model in which the two
centers are independent. Select between those models by the same BIC rule and
bootstrap that selection. Report `SHARED_CENTER_SUPPORTED` only when the
shared-center model has lower BIC and is selected in at least 95% of bootstrap
resamples. Otherwise report `CONTRIBUTOR_SPECIFIC_OR_UNRESOLVED`. This is a
geometric comparison and does not establish musical equivalence. Unmatched,
unstable or insufficient-evidence structures do not enter this comparison.

## Ground Truth and interpretation firewall

Symbolic Ground Truth, score positions and musical labels remain unavailable
until every source-level result, bootstrap output and fingerprint is frozen.
Ground Truth shall not choose component number, centers, widths, membership or
parameters. Any later Ground Truth validation or musical interpretation
requires a separate PI gate.

The analysis may describe only circular concentration count, centers,
dispersion, uncertainty, stability and contributor comparison. It shall not
assign beat, offbeat, battere, levare, subdivision, swing, syncopation,
anticipation, delay, groove or behaviour meaning.

## Allowed outcomes

For each contributor, the result may be:

- `NO_STABLE_PHASE_STRUCTURE` (including selection of the uniform model);
- `ONE_STABLE_PHASE_POPULATION`;
- `TWO_STABLE_PHASE_POPULATIONS`;
- `MORE_THAN_TWO_STABLE_PHASE_POPULATIONS`; or
- `INSUFFICIENT_EVIDENCE`.

Different contributors may produce different outcomes. A conventional musical
pattern is neither required nor privileged.

## Architectural and implementation status

This is experiment-local scientific analysis downstream of AD-037:

`source evidence → EME → metric localization → normalized phase → scientific
phase analysis → future musical interpretation`.

It introduces no production component, architectural layer, runtime
dependency or representation. Production implementation is not authorized by
this preregistration.
