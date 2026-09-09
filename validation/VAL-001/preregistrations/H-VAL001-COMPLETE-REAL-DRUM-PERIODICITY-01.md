# H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01

Date: 2026-09-08. Status: PREREGISTERED DESIGN; execution requires PI authorization.

## Claim and scope

Observe the COMPLETE accepted VAL-001 direct-input Drum sparse complex response
map using existing validated policy/arithmetic/packaging. This is observation,
not recurrence validation or beat selection. No audio loading, detection,
separation, calibration, annotation, accompaniment or scientific retuning.
Every logical observation has scientific_status
RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED. Neither a generated frequency nor nonzero
or large response independently establishes recurrence. No ranks or maxima.

Maximum PASS claim:
VAL001_COMPLETE_REAL_DRUM_LOCAL_COMPLEX_PERIODICITY_MAP_OBSERVED.

## Immutable authority binding

Sibling H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01.inputs.json:
SHA-256 ba21b73d7fe122b29b522f442a3724a89b8fec96549a34b39db62bb7830b29e7.
This freezes all 63 EME IDs, unique supporting PulseCandidate IDs, original JSON
numeric tokens, producer binary64 bits, float.hex equivalents, exact ratios,
field JSON pointers and separate sample/frame diagnostics. No confidence field
is used as strength. EME and observation timestamps must have identical bits.

Sibling H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01.authorities.json:
SHA-256 6ac578c7ea5e8f9367682ca3a46e8ce0e7d0733c1b95eab9ad8937c91575c9b4.
This binds actual repository paths and SHA-256 values for input, source authority,
producer implementation provenance, policy, adapter, evaluator, environment,
production harness, prior acceptance and resource evidence. Verify every entry
before implementation binding and before each run; no authority substitution.

Canonical accepted report SHA-256:
eeb189217a722679d5f40bef4d809e2b38ab381e9dea81057023dfd3d80e05c7.
Accepted scientific fingerprint:
e3d73705306ccc0e96ec78020a54f34aa4e8f267337afa6b7bd56b74fc4fdc4d.
Source UUID c46d6cb9-b99c-5bd6-8d81-656dc1ad48ec; authority
VAL-001-DIRECT-INPUT-SOURCE-AUTHORITY-V1; opaque key VAL001_SOURCE_001.
Asset SHA-256 d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd.
Asset identity does not generate source identity.

Accepted policy commit d7a55b8512cbf9ec1f4a90fd9188e8e1800bb177;
binary64 adapter ca339e858acb81f4d9527121b581c6342ca01437;
cached evaluator 013e3307204c0eca8c8082efac24fc9e16947997;
production harness 7ac46f91d0917c9071f49d5f2f4e30533e9182a2.
These bounded synthetic validations are prerequisites, not existing real-map evidence.

## Numeric and scope contract

Preserve accepted binary64 timestamps, native AD-032 strengths and duration as
exact dyadic values. Original JSON spellings are serialization provenance, not
new exact-decimal coordinates. Use bound adapter semantics: bits -> exact
integer ratio -> Arb; retain signed zero. Reject nonfinite values. No float
arithmetic creates derived query coordinates; use exact Fraction arithmetic.
No uncertainty is added/removed as a physical claim.

Temporal origin and analysis-input scope start are +0.0, per accepted zero-origin
scope authority. End and asset bound are the accepted binary64 42.30675736961451
seconds, exactly encoded in inputs.json. Asset sample count 1,865,728 and sample
rate 44,100 are diagnostic authorities; their rational quotient must not replace
the accepted duration in clipping. Scope and asset interval are closed. Support
may extend outside; intersect as the validated policy specifies, never recenter,
pad, invent events or infer musical silence. Retain all input measurement and
producer provenance through immutable manifest references. The canonical report's
historical role name TEMPORAL_REFERENCE does not authorize a beat in this experiment.

## Complete query order and population

Population ID: VAL001_DIRECT_DRUM_COMPLETE_01 (experiment namespace only; does not
replace source UUID). Input events ordered by (exact timestamp, EME ID lexical).
Centers U are sorted distinct exact timestamps ascending. At each u, supports L
are sorted distinct positive 2*abs(t-u), ascending. Periods T are sorted distinct
positive abs(t_j-t_i), ascending; frequency is exact reciprocal 1/T. Enumerate
nested loops u, then L, then T. Canonical query ID is [population_id,u,L,T], with
normalized rational coordinates; ordinal is zero-based enumeration position,
not scientific source identity. Frequency order is consequently descending.

All generating period pairs are unordered distinct-ID combinations with lexical
ID order, grouped by exact separation; every pair and its timestamp/parent lineage
is retained. Scale pairs preserve ordered center/boundary roles, lexical order
within roles. Coincident identities are never merged or omitted. Membership sets
are lexical EME-ID lists; accumulation order remains timestamp then ID.

Exact mandatory counts: 63 centers; 1,056 periods; 3,864 center-specific scales;
4,080,384 queries; 133,195,392 accumulated event terms including boundary terms.
There are 1,953 unordered distinct event pairs. Recompute counts without evaluating
responses before either run; mismatch stops. No materialized 4M-query list.
No regular grid, range, preferred scale, filtering, threshold, suppression or
selection. Coordinates are a finite query policy, not exhaustive frequency coverage.

## Numerical execution

Use bound CPython 3.13.14/python-flint 0.9.0/FLINT 3.6.0 on macOS arm64,
128-bit precision; flint.ctx.threads=1 and linked flint_get_num_threads()==1.
Binding SHA-256 5242ca974311694e7bf0d20e4459e25336232fc201bc55f80e43e58f7166f468.
Verify executable and linked binary hashes as the accepted worker does.

Reuse unchanged optimized.py and certified evaluator scalar helpers bound by
manifest. For each event in frozen order, include iff abs(t-u)<=L/2. Evaluate
Hann (1+cos(2*pi*(t-u)/L))/2, then strength*weight, then the complex exponential
exp(-2*pi*i*f*t), and accumulate exactly as the accepted expression tree. Keep
boundary events in numerical accumulation even though mathematical Hann weight
is zero. No algebraic reformulation, reordered reduction or precision escalation.

Cache namespace retains numerical/source/algorithm authority. Parsed events <=63;
Hann and amplitude caches current window only, <=63; deterministic exponential
LRU <=4096. Eviction recomputes the identical expression; it never prunes.
Use immutable cached values; no batching/vector approximation or parallelism.
Preserve real/imag balls, magnitude bounds, zero containment and accepted phase
rules verbatim: zero-containing enclosure -> UNRESOLVED_ZERO_CONTAINMENT;
negative-real branch-cut possibility -> BRANCH_CUT_ENCLOSURE with conservative
full-circle enclosure; otherwise RESOLVED_INTERVAL. Valid unresolved phase or
cancellation is an observation, not a failure or permission to drop the query.

## Logical provenance and packaging

Reuse the accepted logical schema: query_id; input_provenance;
window_provenance; period_provenance; generation_evaluation_overlap; numeric;
scientific_status. Input manifests bind the exact freeze and supporting pulse
identities/strength fields. Period manifests retain T,f, every generating pair,
exact pair timestamps, parent/source lineage and coincident-pair information.
Window manifests retain center IDs, scale pairs, contained/boundary/positive
memberships, requested/asset-clipped/available intervals and unavailable pieces.
Generation/evaluation overlaps retain all generating IDs and every pair's
membership intersections as in the validated constructor. Overlap is not
independent confirmation. Any record-specific data must survive expansion.

Use unchanged streaming.Writer packaging and canonical scalar encoding. Sorted
object keys, ASCII-safe compact UTF-8 JSON, no NaN/floats/clocks/absolute paths in
canonical scientific content. Exact rationals and dyadics use normalized integer
strings. Lists preserve frozen order. Field tokens remain strings.
4096 rows per JSON-array shard: 997 shards, 996 full plus final 768 rows.
65536-byte I/O buffers; one expanded/compact record and index entry, no full query,
result or index collection. Compact catalogues and one center's scales only.
Incremental canonical JSONL index.json; shard names shard-000000.json onward.
Each index entry binds filename, SHA-256, rows, first/last IDs. Root schema
JGA-STREAMING-INDEX-JSONL-V1 binds row/shard counts, index hash and manifest hashes.
Inputs/periods are canonical compact catalogues; windows.jsonl is streamed on
window transition. Content references must resolve and match hashes exactly.

The previous worker's fixture dispatcher is synthetic-only. A future experiment-
local driver must supply these frozen real inputs and lazy queries to the unchanged
validated evaluator/cache/writer, plus a streaming contract validator. Before any
response, freeze hashes of that driver/validator and all transitive sources in a
separate implementation binding. Do not edit historical implementation or bind an
unreviewed arithmetic change. This is mechanical integration, not authority to
change policy. PI execution authorization and this preflight binding are required.

## External execution and capacity

External root: /Volumes/SSD Track/JGA/experiments/H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01/
First output: run_1/production/
Fresh-process replay: run_2/production/
Locations are reserved prospectively; do not create or execute in this design turn.
Require new destinations with no existing artifacts; never overwrite/delete partial
or historical evidence. No bulk output in Git or repository fallback.

Immediately before run_1 require >=640 GiB free external storage. Immediately
before run_2 require >=384 GiB free, in addition to preserving completed run_1.
Budgets: 256 GiB each execution plus 128 GiB unconsumed safety margin. At each
closed shard check free capacity; if below 128 GiB stop incomplete, preserving
existing bytes, without pruning or resizing. Record free bytes, mount identity,
actual paths, disk errors, elapsed time and peak RSS separately from science.
Capacity exhaustion is not scientific negative evidence. 10h/run, 20h total and
1GiB RSS are planning allowances, not scientific thresholds or guaranteed bounds;
no timeout-based PASS and no automatic parameter change. Resource projection is
bound in authorities.json; recheck storage regardless of the earlier benchmark.

## Execution, validation and replay

Exactly one complete run_1, followed only after its contract validation succeeds
by one fresh-process run_2 with empty caches and identical environment. No naïve
real run or benchmark real responses. No interpretation-dependent checkpoint.

Stream-validate every row: exact expected query ID/order and counts; all numerical
fields structurally valid/finite as required; every input ID/ratio/strength/source
binding; exact membership and boundary roles; all generating pairs/overlaps;
coverage; hash-resolving provenance. Membership/counts are exact rational geometry,
not inferred from numerical magnitude. Validate every shard hash, canonical encoding,
endpoints and counts, all manifests/root/index and absence of extra/missing rows.
A streaming validator must not load the full output or re-evaluate Fourier responses.

Logical fingerprint = SHA-256(concatenation of canonical expanded logical records,
each followed by LF in frozen order). Store per-run fingerprint and all physical
hashes. Replay requires byte-identical production shards, manifests, index, root,
logical fingerprint and canonical scoring artifact. Check every byte/file, not a
sample. Scoring content excludes paths/run labels/performance/clocks; these belong
to separate operational evidence. Scorer records check totals/failures and bound
scientific hashes. No independent hidden reference labels or musical oracle.

Scientific fingerprint = SHA-256 of canonical scientific_fingerprint_input.json
containing experiment ID, preregistration/input/authority-manifest SHA-256 values,
implementation-binding SHA-256, logical fingerprint, root SHA-256, scoring SHA-256,
query count and scientific status. Use the same material for both runs and require
byte identity. Output fingerprints cannot be known before execution; this freezes
their exact construction, not invented expected values. Preserve a bounded final
replay result binding both runs. Performance measurements are excluded.

## Decision and preservation

PASS only if both full populations, all contract/provenance/serialization checks
and complete byte-identical replay succeed. Zero tolerance for exact equality;
no success percentages or numerical-width thresholds are added. This does not
independently prove physical phase accuracy or recurrence sufficiency.

STOP_PREFLIGHT: authority/input/source/strength linkage or geometry count mismatch;
nonfinite/rejected input; environment/source mismatch; unresolved integration;
unavailable storage; existing run location. Do not execute responses. Preserve
reason and request PI decision; do not repair authority.

FAIL_CONTRACT: numerical evaluation failure/nonfinite uncertified payload;
incorrect/incomplete logical population asserted as complete; wrong arithmetic,
provenance, membership, ordering, serialization, hashes or replay mismatch. Preserve
failure and stop immediately. No patch-and-rerun, precision change or rule relaxation.

STOP_INCOMPLETE: interruption, process termination, disk exhaustion or I/O failure
leaves no complete acceptance. Preserve partial evidence and exact process/filesystem
state; do not promote partial artifacts or restart without PI review. If an original
process remains active, leave it active and inspect its eventual result. Never call
an incomplete run PASS. Any actual scientific contract mismatch remains FAIL even
if interruption also occurred. Fresh execution after failure requires new PI decision.

After PASS, preserve all bulk evidence externally and bounded implementation,
manifests, checksums, score/replay records and summary in Git, leaving unrelated
changes untouched. Check no Git blob >=100MiB; commit/push/fetch scientific branch
and verify HEAD equality/ahead-behind 0/0 if authorized by the execution decision.
No historical accepted evidence is rewritten.

Unauthorized even after PASS: recurrence sufficiency, preferred/winning period,
exhaustive continuous-frequency coverage, trajectory linking, half/double resolution,
beat level, BeatReference, musical phase, tactus, meter/downbeat, BPM, groove/swing,
rushing/dragging, physical onset accuracy, complete performance coverage,
Bass/Piano correspondence or final visualization. Absence of an observation does
not establish musical absence. Stop for PI review; this document executes nothing.
