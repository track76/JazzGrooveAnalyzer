# H-VAL001-CERTIFIED-SPARSE-QUERY-01

Date: 2026-09-07
Status: PROSPECTIVE NUMERICAL PREREGISTRATION — ENVIRONMENT BINDING PENDING
Design only. No fixture evaluation, implementation, dependency installation or
real-data application occurred. Execution requires subsequent PI authorization.

## Scope and immutable authority

Validate certified evaluation of the finite sparse Hann-windowed Fourier operator
at the seven rational queries below, beyond the previously tested Q(zeta_16) domain.
All inputs are synthetic; time units and strengths are dimensionless constructions.
Arbitrary-query means these finite specified queries, not proof for every real number.
Rational phase angles can belong to larger cyclotomic fields: this is not a claim
that rational fixtures are transcendental or admit no algebraic representation.

Preserve H-VAL001-SPARSE-COMPLEX-OPERATOR-01.md, SHA-256
ca5f7f082875f297df3374f8cacc485d86132e299f434f70eb3267f91b501f1e.
Accepted baseline commit f5baf6b1e2f687699e36e81e1dd1e4eeea117828 and scientific
fingerprint 72c213a605c63f01b62fa36dc4bb5a12bfa677066432064bd26f6571e2fb0f77
remain confined to their exact 64-query domain. No historical design is revised.

## Certified library and independent source authority

Prospective evaluator: python-flint 0.9.0 arb/acb under CPython 3.13.14, single
thread. Official numerical references, inspected 2026-09-07:
https://python-flint.readthedocs.io/en/latest/arb.html
https://python-flint.readthedocs.io/en/latest/acb.html
https://arblib.org/using.html (historical semantics; Arb is now part of FLINT).

Arb represents a real interval by midpoint/radius; acb combines real and imaginary
intervals. Rational conversion and arithmetic enclose their mathematical values.
mid()/rad()/man_exp() permit exact finite dyadic serialization; decimal display
is not used as scientific serialization. arg() near the negative real axis may
produce a wide enclosure; the branch handling below is explicit.

Observed environment: python-flint absent from both inspected system and project
Python environments. Versioned wheel/source SHA-256, actual bundled FLINT version,
binary/library hashes, platform and availability of the required APIs must be
bound prospectively BEFORE execution. No substitution of another version or an
uncertified float implementation is allowed. This missing build binding prevents
an execution-ready claim today; no numerical fixture result is needed to close it.

## Frozen operator semantics

  F(u,f;L)=sum_i s_i*w_L(t_i-u)*exp(-2*pi*i*f*t_i)
  w_L(v)=(1+cos(2*pi*v/L))/2 if |v|<=L/2; otherwise 0.

Store every input as reduced rational numerator/denominator. Decide window support
using exact rational comparisons, not uncertain ball comparisons. Construct each
remaining rational constant directly as an enclosing arb rational; never pass
through binary64. Use arb.pi() and acb.exp() for the complex exponential and arb
cosine for the Hann factor. Do not use fixture-specific trig simplification in
the evaluator. Compute each term then sum in (exact timestamp,event ID) order.
No normalization, event suppression, threshold, search or musical interpretation.

## Precision contract

Evaluator initial precision = maximum precision = 128 bits. No escalation.
This is a fixed computational resource contract, not a scientific accuracy
threshold. The deliberately constructed 80-bit imbalance below leaves 48 nominal
working bits beyond its scale; this arithmetic headroom is not asserted as an
achieved error bound. Correctness derives from enclosure, not the bit count.
No convergence stopping rule is needed for a fixed-precision evaluator.
If the resulting enclosure cannot exclude zero, retain uncertainty. Do not raise
precision after seeing a difficult fixture. Every output must be finite; NaN,
infinity or failed conversion fails the bounded experiment.

## Seven exact fixtures: one operator query per row

Each event is assigned a unique ID consisting of case letter and zero-based
position in the listed event order. Coincident events remain separate. Parent
IDs for B/C identify A's corresponding events; D retains A's two parent links.
Define e=1/1208925819614629174706176 = 2^-80 exactly.

| Case | Event (timestamp,strength) pairs | u | f | L |
|---|---|---|---|---|
| A | (-17/126,2/5), (53/126,2/5) | 1/7 | 2/11 | 5/3 |
| B | (31/1638,2/5), (941/1638,2/5) | 27/91 | 2/11 | 5/3 |
| C | (-17/84,2/5), (53/84,2/5) | 3/14 | 4/33 | 5/2 |
| D | (-17/126,2/5), (1/7,1/5), (53/126,2/5) | 1/7 | 2/11 | 5/3 |
| E | (-65/84,1), (89/84,1208925819614629174706177/1208925819614629174706176) | 1/7 | 3/11 | 11/3 |
| F | (-65/84,1), (89/84,1) | 1/7 | 3/11 | 11/3 |
| G | (11/6,2/7) | 11/6 | 3/11 | 5/3 |

A's events are u +/- L/6, hence both Hann factors equal 3/4. Its nonzero
phase/frequency is outside the old sixteenth-root query domain. B translates A
by d=2/13 including window center. C dilates A by a=3/2 including window length
and inverse frequency. D adds the center impulse of weight 1/5 to A.
E/F's symmetric offsets are +/-11/12, with Hann factor 1/2 and frequency-offset
product +/-1/4. E has a rational near-cancellation imbalance; F cancels exactly.
G lies exactly on the negative-real branch ray. No extra queries are authorized.

## Independent closed forms (scorer only)

Let R=(3/5)*cos(10*pi/99), alpha=-4*pi/77 and beta=-89*pi/154.
R>0 because 0<10*pi/99<pi/2. Expected coefficients, magnitudes and phases:

| Case | Coefficient | Magnitude | Principal phase |
|---|---|---|---|
| A | R*exp(i*alpha) | R | alpha |
| B | R*exp(i*(alpha-8*pi/143)) | R | alpha-8*pi/143 |
| C | R*exp(i*alpha) | R | alpha |
| D | (R+1/5)*exp(i*alpha) | R+1/5 | alpha |
| E | (e/2)*exp(i*beta) | e/2 | beta |
| F | 0 | 0 | undefined |
| G | -2/7 | 2/7 | pi, modulo 2*pi |

The scorer must use these algebraically reduced forms, never reimplement the
Hann/event summation as its oracle. Translation, dilation and linearity are
verified through these closed forms; mutual overlap of two loose output balls
is not a proof of the required relation. No expected answers enter the operator.

## Independent rational interval oracle

Scorer uses CPython Fraction/integer arithmetic only, not python-flint or the
evaluator's numerical functions. It computes rigorous intervals for the above
closed forms by the following fixed method:

1. Bound pi using Machin's identity pi=16*atan(1/5)-4*atan(1/239). Each atan
   interval is between consecutive partial sums of its alternating series
   sum_(k=0..N-1) (-1)^k*x^(2k+1)/(2k+1). Alternating-series remainder and sign
   give rigorous rational endpoints; interval linear combination bounds pi.
2. Form the required rational multiples of this pi interval with exact interval
   arithmetic. Sine/cosine are Taylor polynomials through degree 2N+1 / 2N,
   respectively, evaluated on the argument interval with outward-exact rational
   interval operations. Add symmetric Lagrange remainder bound
   M^(degree+1)/(degree+1)!, with M=max absolute argument endpoint. Derivatives
   of sin/cos on the real line are bounded by 1; this bound is independent of
   implementation error. No floating-point values are used.
3. Multiply/add the resulting rational intervals to bound Re/Im and the direct
   closed-form magnitude. Phase intervals are rational multiples of the pi
   interval; F has no phase oracle and G is handled modulo the branch below.
4. N starts at 64 and follows ONLY 64,128,256,512,1024. Stop at the first N at
   which the required exact interval inclusions can be certified. This is scorer
   proof refinement; it never changes evaluator precision, output or parameters.
   At N=1024 without a proof, record CONTAINMENT_NOT_CERTIFIED and no PASS.
   Do not interpret inability to prove containment as proof the true value lies
   outside. No additional precision choice is authorized within this experiment.

Known rational zeros and G's rational coefficient/magnitude are exact singleton
oracle intervals, avoiding an unnecessary approximate limit. A nonempty overlap
alone is insufficient: require the entire independent oracle interval be contained
in the evaluator's exported coordinate enclosure. Inclusion proves containment of
the true response; disjoint intervals prove failure. This test can conservatively
reject a correct but insufficiently certified result, never authorize from overlap.

## Magnitude, zero and branch semantics

Let C=X+iY be the exported closed rectangle. Define zero containment by the exact
endpoint predicates 0 in X AND 0 in Y. Calculate magnitude endpoints using the
certified acb abs_lower()/abs_upper() operations on C; serialize them exactly.
Require 0<=lower<=upper and oracle magnitude inclusion.

If zero is contained: phase_status=UNRESOLVED_ZERO_CONTAINMENT; no scalar phase
and no resolved angle interval. F must have this status. E may have it: truthful
near-cancellation uncertainty is allowed and must never be silently resolved.

If zero is excluded and C intersects the negative-real branch ray (X contains
negative values and Y contains zero), report phase_status=BRANCH_CUT_ENCLOSURE.
Return an explicitly full-circle enclosure modulo 2*pi, plus the exact rectangular
coefficient evidence. Represent its endpoints by a certified outer enclosure of
[-pi,pi] and tag full_circle=true; do not present it as a precise linear phase.
This conservative branch handling is deliberate; no branch-splitting heuristic.
G must use this branch status (including an exact negative-real singleton).

Otherwise use certified acb arg(), status=RESOLVED_INTERVAL, branch convention
(-pi,pi]. Require finite enclosure, proper angular width less than 2*pi certified
using an independent pi lower bound, and inclusion of the closed-form phase oracle.
A/B/C/D must exclude zero and resolve; E must follow its actual zero/branch predicate.
Serialize C without widening by exporting each component's exact midpoint and
radius. Exact rational endpoints midpoint +/- radius govern all predicates.
Magnitude/phase APIs operate on this same original C; no reconstruction or
endpoint-rounding loop is permitted. Serialize the resulting phase ball exactly.

No coefficient/magnitude relative-error threshold is imposed. Finite containment,
required nonzero/phase coverage and proper-interval versus full-circle semantics
prevent a vacuous universal phase claim. No angular error is interpreted physically.

## Canonical serialization and replay

Use exact dyadic midpoint/radius pairs for coefficient and phase balls, obtained
from mid()/rad() then man_exp(). Magnitude bounds returned by abs_lower()/abs_upper()
must be exact finite dyadic values, exported with man_exp(); unsupported or inexact
extraction blocks execution. Normalize m*2^e by removing
all factors of two from nonzero integer m; canonical zero is (0,0). Encode m and
e as decimal integer strings. This avoids dependency on decimal pretty-printing.
All radii must be nonnegative. The scorer derives rational endpoints exactly from
the serialized midpoint/radius; serialization introduces no additional widening.

Canonical UTF-8 JSON: sorted keys, separators (',',':'), ensure_ascii=True, no
trailing newline; rational inputs use reduced numerator/positive-denominator
strings. Events order by exact timestamp then ID; result records order A..G.
Store all seven measure/query manifests with construction SHA-256, parent IDs,
parameter authority, code hashes, precision, library/build binding and all input
lineage. No clock/path/randomness in scientific bytes. Environment data separate.
Expected values and transformation labels remain scorer-only. Case labels are
attached by the harness after evaluation; operator receives only measure/query
and provenance. Scorer accesses frozen operator output before constructing oracles.

After separate authorization: one seven-query execution plus one fresh-process
seven-query replay, same pinned runtime and libraries. Require byte-identical
canonical operator/scoring results and SHA-256, including oracle proof depth/status.
The normalized dyadic encoding is the prospective canonical layer; unsupported
exact extraction APIs stop before execution, rather than using decimal approximations.

## Decision

PASS only if all seven coefficients/magnitudes are certified by independent
containment proofs, phase/zero/branch predicates and oracle checks pass, every
query and lineage appears exactly once, all manifests verify and replay is byte
identical. F must retain unresolved zero phase; G must retain branch ambiguity.
No threshold tuning or fallback. Proven disjointness or contract/replay mismatch
-> FAIL_NUMERICAL_VALIDATION. Unproved inclusion at maximum oracle budget ->
CONTAINMENT_NOT_CERTIFIED (no PASS). Leakage/post-result tuning -> INVALID_EXPERIMENT.
No numerical result is asserted by this design.

Maximum PASS claim:
CERTIFIED_SPARSE_COMPLEX_PERIODICITY_REAL_QUERY_EVALUATION_VALIDATED,
only these seven synthetic rational fixtures and the frozen build/enclosure contract.
REAL_QUERY names query evaluation, not real-audio validity or arbitrary-real proof.

No real Drum evidence, detector validity, physical phase, sparse/full-novelty
equivalence, exhaustive search, window choice, tracking, winner selection,
BeatReference, tactus, meter/downbeat, BPM, accompaniment or visualization authority.
The prospective later VAL-001 application still requires PI authorization.

## Remaining gate

The mathematical fixtures and numerical rules are specified. Execution is NOT
ready until python-flint 0.9.0 availability, exact distribution and linked-FLINT
identity/checksums, deterministic single-thread build and required APIs are bound
in a prospective environment annex. Do not choose a different implementation or
revise this design after evaluating fixtures. No installation or fixture probing
is authorized in this design-only turn. Stop for PI review.
