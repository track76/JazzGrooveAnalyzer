# H-VAL001-CACHED-STREAMING-EQUIVALENCE-01

Date: 2026-09-08
Status: DESIGN ONLY — EXECUTION REQUIRES PI AUTHORIZATION

## Scope and immutable reference

Test computational equivalence only; no real observations, audio, detector,
period selection or musical inference. No implementation or execution in this turn.
Naive reference is the unchanged evaluate() in
../certified_sparse_query_20260907/evaluator.py, SHA-256
0bb74a524ea216639f1f6413d30d6db089584b3ecdba0c192d6e1b77eecd04c7.
Its helper functions and arithmetic order remain unchanged. Harness adds independently
constructed membership/provenance and explicit zero-containment derived from the
serialized rectangle; it does not modify the numerical evaluator.

Use the bound CPython 3.13.14 / python-flint 0.9.0 / FLINT 3.6.0 macOS arm64
environment, binding SHA-256
5242ca974311694e7bf0d20e4459e25336232fc201bc55f80e43e58f7166f468.
Precision=128 bits, FLINT threads=1, linked flint_get_num_threads()==1.
No escalation, parallelism, changed numerical library or algebraic reformulation.

Input fields follow JGA-ACCEPTED-BINARY64-OBSERVATION-INPUT-V1. Freeze original
synthetic JSON tokens by CPython canonical producer serialization from the exact
binary64 fixtures before evaluator execution; preserve bits, hex, integer ratio,
source/field lineage and signed zero. All input values below are exactly binary64-
representable. Query frequencies are exact rational policy coordinates; do not
round them to binary64. Query parameters are not newly observed floating fields.
The reference's arb(str(exact_rational)) conversions and expression trees are
preserved; original finite dyadic input conversion is exact at 128 bits here.

## Four frozen synthetic populations; exactly 21 queries

Events have unique population-qualified IDs and supporting observation IDs
<population>.<event>.pulse. Strength never ranks or selects an event. Each
population has synthetic source/asset construction IDs, not AD-041 real-source IDs.

P: nonuniform/coincident population:
  a: time=0, strength=1
  b: time=1, strength=5/4
  e: time=1, strength=3/2
  c: time=3, strength=7/4
Asset interval [-1,4], observation scope [0,3], both closed, binary64 endpoints.
Use the entire accepted policy: centers {0,1,3}; periods {1,2,3}; frequencies
{1,1/2,1/3}; L(0)={2,6}, L(1)={2,4}, L(3)={4,6}. Exactly 18 queries.
Period pairs: 1:{ab,ae}, 2:{bc,ec}, 3:{ac}; coincident pair {be} retained separately.
Center 1 retains b,e. Every scale retains its center/boundary generation pairs.

N: near cancellation:
  a: time=1/4, strength=1
  b: time=5/4, strength=1099511627777/1099511627776 = 1+2^-40
One query u=3/4, L=2, f=1/2, T=2.
The second strength is binary64 hex 0x1.0000000001000p+0, bits 3ff0000000001000.
Exact mathematical response is -(2^-41)*exp(-i*pi/4). This is construction
context, not a substitute expected ball. Near cancellation is genuinely nonzero.

Z: exact cancellation:
  a: time=1/4, strength=1
  b: time=5/4, strength=1
One query u=3/4, L=2, f=1/2, T=2. Exact mathematical response zero.

R: negative-real branch:
  a: time=1, strength=1
One query u=1, L=2, f=1/2, T=2. Exact response -1.

For N,Z,R, asset/scope are [0,2], closed. Their single query is an explicitly
construction-authorized numerical probe, NOT output of the all-separation policy.
Keep query_origin=CONTROLLED_NUMERICAL_PROBE versus P's EVENT_DERIVED_POLICY.
Probe coordinate-generation lineage references the construction authority; never
fabricate an event pair generating T=2. Evaluation support lineage still retains
event IDs, containment, boundary, positive membership and any overlap with declared
construction input IDs. Input events are not called independent supporting evidence.

Global order: populations P,N,Z,R; within P sort u,L,T numerically. Events sort by
exact timestamp then qualified ID: P.b precedes P.e at their common time.
No added queries or fixture expansion. N's 2^-40 imbalance is part of this new
synthetic fixture, not an alteration of any historical 2^-80 experiment.

## Naive/optimized numerical equivalence

Each path evaluates the same 21 query records exactly once per execution.
Naive calls the frozen function with exact rational strings. Optimized may only:
parse once; memoize exp terms, memberships, Hann and strength-times-Hann;
reuse immutable results; stream; factor provenance. No mathematical shortcut.

For each included event use precisely:
  w = (1 + cos(2*pi*arb(str((t-u)/L))))/2
  amplitude = arb(str(s))*w
  exponential = acb(0,-2*pi*arb(str(f*t))).exp()
  z += amplitude*exponential

Fraction operations occur before Arb conversion, exactly as in reference.
Do not replace a boundary weight by zero, including when analytic Hann is zero.
Do not simplify roots of unity, use conjugate symmetry, recurrence formulas,
binary64 trig, SIMD reductions, grouping of coincident strengths or reassociation.
Every contained event, including boundary events, contributes its own term.
Magnitude/phase functions and exact dyadic serialization remain reference-identical.
Cached objects must not be mutated; accumulator is fresh per query.

Require exact equality per query of real/imag midpoint-radius serialization,
magnitude bounds, zero-containment, phase status/enclosure, contributing-ID order,
requested/clipped/available support, boundary/positive membership, generation and
evaluation lineage, overlaps, and expanded canonical scientific record bytes.
Derive zero containment by exact rational endpoints of serialized real/imag balls.
Z must retain unresolved-zero status and R the frozen conservative branch status.
No enclosure overlap or tolerance substitutes for equality. Preserve all 21 records.

## Cache keys and deterministic execution

All keys are typed canonical tuples containing environment-binding hash, precision
128, algorithm/reference hash and input-manifest hash. Reset caches between paths
and between complete executions. No persistent cross-run state.

- Parsed input: (population,event ID,field ID,producer bits); preserve each identity
  even if numeric values coincide.
- Exponential: (population,event ID,exact t,exact f). Do not deduplicate across
  coincident IDs or populations in this minimal test.
- Membership: (population,u,L,asset interval,observation scope). Store ordered
  contained IDs, boundary/positive sets, coverage and generation roles.
- Hann: (population,u,L,event ID,exact t).
- Amplitude: Hann key plus exact strength and strength-field lineage.

Keys use reduced rational pairs and full authority identities, never approximate
float keys, display names or musical labels. Lazy populate on first canonical
query use; retain scalar caches until path completion. No eviction policy.
P has 12 event/frequency exponential keys and six membership keys; N/Z/R add
five exponential keys and three membership keys. Thus optimized exponential count
must be 17 and membership builds 9. P has 21 included event/window pairs; N/Z/R
add 5: optimized Hann and amplitude calculations each 26. Accumulations are
P=63 plus N=2,Z=2,R=1: 68 per path. Naive exponential/Hann/amplitude counts are
68 each. Naive membership scans occur once per query, 21 times. Counters measure
calls, not estimated costs. Count contracts validate cache mechanics, not speed.

## Logical provenance and streaming format

Each logical record consists of query identity/coordinates, certified payload,
explicit status, and complete input/generation/evaluation/coverage provenance.
scientific_status=RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED. Implementation/path
identities remain in separate execution manifests, not inside logical equivalence
payloads. Both implementations' hashes remain preserved; never conceal differences.

Common encoding: UTF-8 JSON, sorted keys, compact separators (',',':'),
ensure_ascii=True, no trailing newline. All scientific rationals are reduced
[numerator_string,positive_denominator_string]; all integer metadata use canonical
decimal strings. Dyadics use odd mantissa/exponent strings, zero=(0,0). No floats,
NaN, clocks or absolute paths in canonical scientific artifacts.

Shared manifests:
- inputs.json: ordered populations/events, binary64/field lineage and scope;
- periods.json: ordered coordinate-generation records with all pairs or explicit
  controlled-query authority;
- windows.json: ordered (population,u,L) records including membership, coverage,
  center IDs and scale-generation lineage;
- each manifest row has content ID SHA-256 of its canonical row body excluding ID.

Optimized result rows contain query tuple ID, numeric payload, scientific status
and input/period/window content references. Expansion replaces references with
complete row bodies under fixed input_provenance, period_provenance and
window_provenance keys; no pruning or loss of multiplicity. Expansion must exactly
match naive full logical record bytes. All references must resolve uniquely;
unknown references, conflicting content IDs or cycles fail.

Stream shards contain JSON arrays of exactly four query rows, except final shard.
Four is a finite test device to force cross-population and partial-shard boundaries,
not a proposed production optimum. Exactly six shards with sizes 4,4,4,4,4,1.
Names shard-000000.json through shard-000005.json. No compression or timestamps.
Write incrementally with canonical '[' + comma-separated canonical rows + ']';
never retain all result rows in the optimized writer. Maximum buffered rows=4.
Shared manifests are small finite catalogues and may be held in memory. Final
index.json lists shard relative names, SHA-256, row counts, first/last query IDs,
manifest hashes and total 21, in canonical order. No OS directory enumeration order.

Bulk naive rows, optimized manifests, shards and replay copies live outside Git
under the existing JGA_EXTERNAL_ROOT/experiments/H-VAL001-CACHED-STREAMING-EQUIVALENCE-01/.
Run directories run_1 and run_2 must be newly created; never overwrite evidence.
Git preserves preregistration, source/input freeze, bounded index/hash manifests,
scoring and descriptive performance records. Freeze external root availability
before execution; no bulk data in Git. External absolute paths are operational
metadata only; artifact identity uses relative paths and hashes.

## Performance protocol (descriptive only)

One full execution and one fresh-process replay. Each execution uses a fresh naive
worker then a fresh optimized worker, fixed order, same bound environment and one
FLINT thread. Neither shares caches. A driver/scorer does not evaluate extra queries.
No warm-up fixture executions, repetitions for tuning or calibration passes.

Use perf_counter_ns wall-clock measurements around each worker's complete input
parse, evaluation and artifact finalization; separately time evaluation and writing
where instrumentation can do so without reordered arithmetic. Record macOS
resource.getrusage(RUSAGE_SELF).ru_maxrss in bytes per worker (includes interpreter
and libraries; not claimed as isolated cache size). Record entry counts for each
cache, arithmetic counters, peak buffered-row count, per-file and total canonical
bytes, shard boundaries and completed query count. Serialized bytes derive from
actual files, not an assumed bytes-per-record multiplier. Use OS accounting only;
no surrogate real-data benchmark.

Timing/RSS measurements go into separate operational performance.json records;
they are EXPECTED to vary and excluded from scientific replay byte comparisons.
No speedup, memory-size or throughput threshold affects scientific equivalence PASS.
The fixed buffer limit, shard population/order, cache-key correctness and actual
call-count contract are deterministic implementation requirements, not performance
ranking. An incomplete run cannot PASS regardless of measured speed.

## Independent scoring and replay

Freeze harness, naive hash, optimized code, synthetic manifest, expansion schema
and scorer hashes before execution. Scorer must not call either evaluator to
manufacture expected numerical answers. Compare already-frozen path outputs.
Independently check P against the accepted policy's frozen I pair/shell/coverage
semantics with the specified ID relabel; N/Z/R against their explicit query inputs.
Check all field/source lineage and generation/evaluation overlap separately from
numeric comparison. Sharing only canonical encoding is allowed; do not share
optimized membership/cache generation as the scorer's membership oracle.

Require two separate equality gates:
1. naive versus expanded optimized, all 21 logical records and query order;
2. fresh-process replay, byte identity of optimized input/period/window manifests,
   all six shards, index, logical-record fingerprints and canonical scoring output.
Also require naive scientific output replay identity. Scientific scorer output
contains exact comparisons and hashes only, no performance values or clocks.
Counters must satisfy the frozen counts in each execution. Validate no missing,
duplicate or dangling records, coincident-ID collapse, boundary term elision,
cache contamination or unresolved provenance.

Any scientific equality, status, identity, ordering, completeness, arithmetic-count,
streaming-contract or replay mismatch -> FAIL. Preserve evidence and stop without
repair/rerun. No empirical tolerance, parameter tuning or alternative test domain.
Slow performance alone is not a scientific FAIL; report it descriptively.

Maximum future PASS: CACHED_STREAMING_PERIODICITY_EVALUATOR_EQUIVALENCE_VALIDATED,
only these synthetic queries, bound environment, frozen cache/streaming rules and
exact logical-record equivalence. No real Drum execution, recurrence, sufficient
periodicity, selection, BeatReference, tactus, musical phase, meter/downbeat, BPM,
accompaniment correspondence or visualization authority follows.

## Readiness

Scientific design is specified for implementation following PI authorization.
Before any execution bind external storage availability and new run locations,
freeze actual implementation hashes and verify the existing numerical environment.
No executable optimized evaluator or experiment was produced/run in this design
turn. No essential numerical rule is left to be chosen from outcomes.
