# H-VAL001-PRODUCTION-STREAMING-HARNESS-01

Date: 2026-09-08
Status: DESIGN ONLY — PI EXECUTION AUTHORIZATION REQUIRED

## Scope and reference authority

Validate operational packaging, lazy enumeration, bounded live state and exact
logical-record equivalence. No real Drum input, audio or musical interpretation.
The reference is cached_streaming_equivalence_20260908/optimized.py (relative to
validation/VAL-001), SHA-256
4c8de35da8f06cee8ca1a29b3cceedf2b40b068fcfc08c5da81277f33dd1db52,
accepted at commit 013e3307204c0eca8c8082efac24fc9e16947997.
Reuse its exact arithmetic expressions, conversions, term order, numerical
serialization and phase/zero rules, and the accepted logical provenance schema.
Use CPython 3.13.14 / python-flint 0.9.0 / FLINT 3.6.0 / 128 bits / threads=1,
with numerical binding SHA-256
5242ca974311694e7bf0d20e4459e25336232fc201bc55f80e43e58f7166f468.
No precision escalation, pruning, ranking, approximation, reordered reduction or
algebraic identity replaces an arithmetic operation. Reference code stays immutable.

## Prospective operational choices

Production shards contain 4096 rows except the final partial shard. This fixed
power-of-two record budget reduces file count by 1024 relative to the four-row
synthetic test. It does not define a scientific time/frequency scale or accuracy.
At 4,080,384 rows it yields 997 shards: 996 full and one of 768 rows.
This is an operational choice, not a demonstrated optimum. No post-result resizing.

Binary file I/O buffers are 65536 bytes; one record may exceed this buffer and is
written incrementally. Hold at most one expanded record and one compact record;
never buffer a complete shard. Cache limits below are likewise operational resource
budgets and cannot change which events/queries are evaluated.

## Frozen synthetic fixtures

Three fixtures serve distinct purposes; performance is not musical validation.

E — exact numerical/semantic regression:
Reuse all 21 queries and the four P,N,Z,R synthetic populations frozen in
H-VAL001-CACHED-STREAMING-EQUIVALENCE-01.md, SHA-256
86dd410c57c8bf9e6ac5958fbd80e284f50901808aa3519bff89fd383ee8d444,
and its inputs.json without altering values or lineage. Preserve P's full 18-query
population and the three explicitly controlled numerical probes, their order,
coincident IDs, Hann boundaries, overlap, near cancellation, exact zero and branch
case. Each path evaluates E exactly once per complete execution. One 21-row shard
in the new production format; reference output may retain its prior formatting.

C — bounded-cache pressure:
One synthetic population C with events C.a at time 0, strength 1 and C.b at time 1,
strength 1/2, each with distinct C.<name>.pulse supporting observation ID. All are
exact binary64 values, preserved with original canonical JSON tokens, bits, hex
and exact ratios. Asset and observation scope are [0,2], closed; source/asset are
explicit synthetic construction identities.

Exactly 8193 controlled queries: u=0, L=2, T=j/8192 and f=8192/j for integer
j=1..8193 in increasing j. Rational coordinates remain exact and are NOT a
production frequency grid. Query origin is CONTROLLED_NUMERICAL_PROBE; coordinate
authority is this construction, with no fabricated pair-derived period.
Each query contains C.a and boundary C.b, positive membership {C.a}; C.b retains
its separately evaluated numerical Hann term. Requested support [-1,1], asset-
clipped/available [0,1]; unavailable [-1,0), no padding or recentering.
Generation/evaluation overlap references construction input IDs {C.a,C.b}, with
no independently confirmed recurrence. Three production shards: 4096,4096,1.
8193 frequencies force cache eviction beyond the 4096-entry exponential budget.
Both implementations evaluate exactly these 8193 queries; no Fourier oracle or
period-selection result is inferred from this synthetic family.

S — scale stress of serialization/enumeration only:
Exactly 4,080,384 transport records. Use the 21 complete E reference logical
records after E equivalence passes as immutable templates. For ordinal k starting
at zero, emit {transport_ordinal:decimal_string(k), template_index:decimal_string(k
mod 21), logical_record:template[k mod 21]}. The optimized stream uses its equivalent
E templates with immutable provenance references, expanding to this exact envelope.
This tests a large transport workload, NOT 4,080,384 independently inferred
observations. Repeated logical query IDs are intentional and are not recast as a
unique scientific population. Transport ordinals are unique and strictly ordered.
No extra Fourier calls occur in S; it cannot establish large-domain numerical
correctness or a real-data runtime estimate. Each generator computes k and k mod
21 lazily. 997 shards as above. The reference comparator uses streaming expansion
of its 21 templates, never a 4M-row list or 4M-item expected-answer table.

Per execution: E=21 and C=8193 numerical queries per path, total 8214; S=4,080,384
transport rows per path, zero additional evaluator calls. Two complete executions
only: original plus fresh-process replay. Fixture order E,C,S, stop on any failure.

## Bounded production state

Enumerate centers, each center's scales and periods as ordered iterators over
pre-frozen compact catalogues. No Cartesian query list, query-result list or full
shard-index list. For C iterate j; for S iterate k. For E use the declared finite
query catalogues. Exact query order equals the reference order.

Parsed event cache: at most 63 event records, with all numeric/field lineage.
Events are never grouped by coincident time. The capacity covers the proposed
future 63-event input but does not authorize it. Larger inputs are out of this
bounded contract; stop explicitly, never discard observations.

Membership cache: current (population,u,L) only, preserving center/contained/
boundary/positive sets, coverage and generation metadata. Release on transition.
Hann and amplitude caches: current window only, each at most 63 entries.
All terms recomputed after eviction with the identical expression tree.
Exponential cache: deterministic LRU capacity 4096 event/frequency entries;
lookup marks most-recent use, first miss computes exactly once and insertion
then evicts the least-recent entry if necessary. Never mutate cached Arb/acb values.
Keys retain the full frozen input/environment/precision/algorithm authority and
exact event/frequency coordinates from the accepted cache-key specification.
Eviction is not pruning; every query and included event is evaluated.

Retain only compact input/period catalogues and one center's scale catalogue;
stream window-manifest entries in canonical order as windows are first encountered.
Records reference input hash + ordinal or content hash from these manifests.
No in-memory map of all window records or all queries. A content ID must retain
its canonical body hash; ordinal location is only an access aid, never authority.

Maximum live result state is one logical and one compact record, one shard's
count/hash/first/last ID, and one index entry. Retain 21 templates only in S.
This is a structural bound, not a promised RSS byte limit. Declare catalogue
size and maximum record size in measurements; do not hide them in cache totals.
Reference unbounded caches are permitted for E/C only, measured separately.

## Canonical files and incremental index

Preserve accepted canonical record encodings: exact rationals and dyadics as
normalized integer-string pairs, immutable IDs, sorted object keys, compact JSON,
UTF-8 ASCII-safe bytes, no floats/NaN/clocks/absolute paths in scientific artifacts.
Scope and physical/numerical statuses remain unchanged. Scientific status is
RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED.

Each shard is a canonical JSON array: write '[' then canonical rows separated by
commas then ']'; no trailing newline. Names shard-000000.json upward (minimum six
digits). Compute SHA-256 incrementally. Close final shard before emitting its
index entry. No empty shard for an exact multiple or empty suffix.

index.json is canonical JSONL (explicit new index schema, not the earlier monolithic
JSON index): one canonical JSON object per shard, each followed by LF, including
last. Fields: name, sha256, rows, first_id, last_id. Append each completed entry
immediately; never hold previous entries. A bounded root.json stores schema ID
JGA-STREAMING-INDEX-JSONL-V1, total rows, shard count, final index SHA-256 and hashes
of input/period/window manifests. Its own JSON encoding has no trailing newline.

Input and period manifests may be canonical arrays of compact catalogue records;
window manifest is canonical JSONL, one content-addressed body per first window
encounter. root.json declares all encodings explicitly. Reference and production
physical encodings may differ; complete logical expansion must not.

Logical fingerprint = SHA-256 of canonical logical records, each followed by LF,
in declared order. E/C hash scientific logical records; S hashes transport envelopes.
No implementation-specific hashes enter compared logical records; execution
manifests separately preserve both implementations, code/input/environment hashes.
No performance values enter canonical scientific records or fingerprints.

Bulk files remain external under
JGA_EXTERNAL_ROOT/experiments/H-VAL001-PRODUCTION-STREAMING-HARNESS-01/run_1/
and run_2/, with reference/production and E/C/S subdirectories. Directories must
be new; never overwrite. Git stores source freeze, preregistration, bounded result,
root/index fingerprints and summary checksums, not shards or large manifests.
Validate external space/availability before execution; no repository fallback.

## Independent comparison and deterministic checks

Before any execution freeze code, exact fixtures, environment and source hashes.
Reference arithmetic is the unchanged accepted optimized evaluator, with a separate
harness supplying the declared query order. Production changes only enumeration,
cache lifetimes, buffers and physical packaging. No shared production cache or
index-construction logic supplies the comparison oracle. Common exact numerical
helpers and canonical scalar encoding may be reused with explicit hashes.

Score E and C record by record: expanded canonical byte equality for every field,
including numerical real/imag balls, magnitude, zero/phase, membership/boundary,
coverage, identity, overlap and provenance. Independent frozen E membership tables
and C's declared constant memberships/coverage guard against common lineage errors.
Verify all reference/production orders and final logical fingerprints exactly.
Only after E passes may its templates feed S. S compares every expanded envelope,
ordinal and template identity plus final fingerprint. No sample-only scoring.

Verify exact row/shard counts; all manifest references resolve uniquely; body and
file hashes agree; indexes match real shard contents and first/last IDs; no omitted,
duplicate, reordered or fabricated records. C must trigger nonzero LRU evictions;
cache capacity must never exceed 4096. E/C counters must agree with actual execution
and preserve complete event accumulation; do not require identical exponential
counts across eviction policies. S evaluator-call count must be zero.

Validate structural memory contracts through source audit and explicit high-water
counters: no full query/index/result collection, one-window caches, bounded LRU,
bounded row buffers and incremental index emission. File-system artifact counts
separate preregistered files from OS sidecars. Never include AppleDouble bytes in
canonical scientific-size metrics.

One full execution and one fresh-process replay, resetting caches and directories.
Require byte-identical production manifests, shards, index/root, expanded logical
fingerprints and scientific scoring artifacts. Reference logical fingerprints also
must replay identically. Performance records are separate and may differ.

## Resource protocol (descriptive)

Each fixture/path runs in a fresh worker, reference then production, same environment,
FLINT threads=1. S workers may load their path's 21 already-accepted E templates;
no new evaluator execution. No timing warm-up or extra repetitions.
Record perf_counter_ns full wall time (parse through final close/hash), peak
resource.getrusage(RUSAGE_SELF).ru_maxrss in macOS bytes, and actual cache/eviction/
recomputation high-water counters. Record arithmetic calls and accumulation count,
peak buffered rows, catalogue/template counts and index entries buffered.

Count canonical bytes by explicit declared filenames only. Report bytes/query for
E/C and bytes/transport-row for S, separately for result rows, shared manifests,
shard delimiters, indexes and roots. Shard delimiter overhead for a nonempty N-row
array is exactly N+1 bytes; no float estimate. Record each fixture's shard count,
canonical file count, total actual filesystem file count, OS sidecar bytes, index
size, and externally allocated disk usage where obtainable. Logical output bytes
and allocated disk bytes are not interchangeable. Preserve measurements without
using them to choose a new shard size or cache policy.

No RSS/runtime/storage/speedup threshold affects scientific equality PASS. Failure
to finish leaves evidence incomplete and cannot PASS. Structural capacity, ordering
and buffer-contract violations are implementation failures even if RSS appears low.
Resource measurements do not establish a real-input performance bound.

## Decision and readiness

Any exact record, payload, membership, provenance, order, fingerprint, streaming,
capacity or replay mismatch -> FAIL. Preserve evidence and STOP, no repair/rerun
without PI decision. No epsilon, precision escalation, pruning or post-result tuning.
Expected LRU recomputation is permitted and must remain observationally identical.

Maximum future PASS: PRODUCTION_STREAMING_PERIODICITY_HARNESS_VALIDATED,
limited to these synthetic numerical and transport fixtures, resource contracts,
operational packaging and deterministic bounded-memory execution structure.
No real Drum execution, recurrence, period selection, BeatReference, musical phase,
tactus, meter/downbeat, BPM, accompaniment or visualization authority follows.

Ready for PI review and subsequent implementation authorization. Before execution,
bind external capacity/new directories and freeze actual source/environment identity.
No experiment execution or production harness implementation occurred in this turn.
