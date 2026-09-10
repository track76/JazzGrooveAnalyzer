# H-VAL001-DRUM-RECURRENCE-STRUCTURE-01

Status: DESIGN / PREREGISTRATION — BLOCKED FOR RECURRENCE CLAIM; NO EXECUTION.
Date: 2026-09-09.

## Question, audit and authority boundary

Does the accepted response map contain temporally recurrent and multiscale-
consistent periodic structures? This specification freezes a descriptive relational
representation, but does not invent a rule for promoting it to established recurrence.
No accepted map response values were inspected to construct these rules.

F-032 requires reproducible recurrence evidence and explicitly does not prescribe
recurrence tolerances, confidence thresholds or estimators. AD-034 represents
already-supported Candidate Period evidence; it does not authorize discovery from
Fourier coefficients. AD-035's exact consecutive positive frame intervals occurring
at least twice apply to a different observation domain. Its count rule is not
transferred to all-separation coordinates or overlapping-window Fourier responses.
F-031 distinguishes observed periodic relationships from metric hierarchy; numerical
ratios alone do not establish a hierarchy. Historical blocked strength/phase designs
remain limiting prior evidence, unchanged. Native strength preservation is not an
accent or beat interpretation. The accepted map explicitly retains
RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED.

Bindings: sibling H-VAL001-DRUM-RECURRENCE-STRUCTURE-01.authorities.json,
SHA-256 73f8415d4fd6234be276acc2158e498aadbdb0c7b1caa9248882a89e256a9136.
Accepted map scientific fingerprint:
03146e8794151bb91faa938eb3f0f8ea1cfda34a12faaaf84158e820c39e96fc.
Preservation commit 2856c95952ea078fb01d179c2f94e5cb6bd697e3.
Use run_1/production through the accepted root/index/manifest hash chain; run_2
is byte-identical replay evidence, NOT an independent observation population.
No operator execution, new EME, audio, annotations or other input channels.

## 1. Time-indexed representation

Let D={(u,L,T)} be the complete frozen map domain and C_q, M_q, P_q its accepted
complex enclosure, magnitude enclosure and phase status/enclosure. Preserve these
payloads verbatim; do not recompute coefficients or normalize their magnitudes.
For every T define the ordered response profile
R_T = [(u, [(L, q_id, C_q, M_q, P_q, lineage_q)]_{L ascending})]_{u ascending}.
This is a lossless indexing of responses, NOT a recurrence detector. Every accepted
record occurs exactly once in this primary representation. No response threshold,
window preference, rank, confidence, peak or minimum persistence is introduced.

A temporal comparison edge connects successive AVAILABLE centers for the SAME exact
(T,L). Record the positions of those centers in the full U sequence and every skipped
center for which that L was not queried. Such an edge does not interpolate a gap or
assert temporal continuity. Adjacent order is a deterministic indexing convention,
not a persistence window or claim about all nonadjacent comparisons. The full profile
retains all records for later independently authorized analyses.

## 2. Multiscale relations and evidence descriptors

At each (u,T), retain all exact L values and connect successive L in ascending order.
Every relation is descriptive and retains both endpoint records. Do not average,
weight, combine significance, infer support from a majority of scales, or select an
optimal scale. Different Hann supports are different operators; raw magnitude equality
or inequality is not a measure of cross-scale recurrence strength.

For each endpoint preserve contained/boundary/positive EME sets, count and exact time
extent (null when empty), available/requested supports, and generation lineage. For
each edge preserve intersections AND both set differences for those EME sets; also
preserve the exact available-support intersection. This exposes reused observations
and nested windows. Distinct centers/scales are not independent replicates. Candidate-
generating pairs and evaluation contributors remain separate. Do not count the same
pair/EME multiple times as independent confirmation.

A complex rectangle excluding zero is tagged CERTIFIED_NONZERO_RESPONSE; a rectangle
containing zero retains ZERO_CONTAINMENT_NOT_PROOF_OF_EXACT_ZERO. Exact singleton
[0,0]+i[0,0] may additionally be tagged CERTIFIED_EXACT_ZERO, using exact dyadic
endpoint equality only. These are numerical statements, never recurrence support.
All accepted magnitude/complex/phase uncertainty is preserved without tightening.

No binary RECURRENT, MULTISCALE_SUPPORTED or confidence field is authorized. The
recurrence assessment remains INDETERMINATE / RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED
unless a separately reviewed rule supplies that missing scientific inference.

## 3. Phase preservation and narrowly descriptive assessment

The accepted exponential uses GLOBAL absolute t: exp(-2*pi*i*f*t). Thus phase for
fixed T already uses one absolute coordinate frame. Do not introduce u-dependent
phase rotation, unwrapping, phase-locking, extrapolation or an inferred origin.
Window changes alone can change phase; stability is not automatically expected.

Preserve all accepted phase statuses and certified enclosures. On the temporal and
scale edges above, compare phase only when both endpoints are RESOLVED_INTERVAL.
Decode their existing dyadic midpoint/radius into exact rational closed intervals
[m-r,m+r]. If intervals are disjoint, record EXACT_COMMON_ARGUMENT_EXCLUDED; if they
intersect, record COMMON_ARGUMENT_NOT_EXCLUDED. Intersection means compatibility
with the enclosures, not proof of equal underlying phase or recurrent alignment.
No angular distance, near-equality tolerance, circular mean, confidence or trajectory
is computed. Disjointness does NOT reject approximate recurrence; arbitrarily small
phase changes may be disjoint at numerical precision.

If either endpoint has zero containment, record PHASE_COMPARISON_UNRESOLVED_ZERO.
Otherwise if either has BRANCH_CUT_ENCLOSURE, record
PHASE_COMPARISON_UNRESOLVED_BRANCH. Preserve its conservative full-circle enclosure;
do not force a scalar, narrow it or compare branch endpoints as musical alignment.
No phase comparison across different T is claimed: their angles have different
frequency semantics. Cross-frequency phase locking needs separate authority.
Exact rational interval comparison adds no new transcendental numerical evaluation.

## 4. Concurrent coordinate relations, not inferred hierarchy

For every unordered distinct pair of observed period coordinates, sorted by duration
T_a<T_b, retain the exact reduced positive ratio r=T_b/T_a=p/q. Preserve both period
IDs and all coordinate-generation lineage. Label r=2 an exact octave-coordinate
relation, and q=1 an exact integer-coordinate multiple; no musical meaning attaches
to either label. In particular T/2,T,2T are all retained WHEN PRESENT in the frozen
coordinate set. Do not synthesize absent coordinates or query responses at them.
For each T record exact membership of T/2 and 2T (present ID or
NOT_IN_FROZEN_QUERY_DOMAIN). No approximate alias clustering.

All rational-valued T are rationally related. Therefore an unrestricted rational-
relation graph is complete (1,056 vertices, 557,040 unordered edges); connectedness
is a mathematical tautology, not evidence of a physical family. Do not use connected
components as discovered periodic hierarchies, choose a root/fundamental, restrict
ratios to low denominators, or introduce a simplicity preference. Integer/doubling
edges are typed coordinate relations, not privileged levels. Keep a factorized graph
schema and endpoint references rather than duplicating all response records per edge.
Family hierarchy status remains NOT_ESTABLISHED_BY_COORDINATE_RATIO. Establishing
acoustic hierarchical co-organization would require independent recurrence/phase
relationship criteria not supplied by these exact ratios.

## 5. Gaps, absence and uncertainty

Distinguish absent query coordinate (not in D), empty evaluation membership, boundary-
only membership, zero-containing response, certified exact zero and unresolved phase.
None means missing musical events or musical silence. For each window retain the
ordered observed timestamps and every consecutive positive spacing as exact data;
no spacing is declared a 'large gap' by an invented cutoff. Coverage clipping and
unavailable support are retained unchanged. No cycles are manufactured across gaps.

All observations and alternatives remain represented even when phase is unresolved,
responses cancel, support overlaps or a relation is indeterminate. No fill or phrase-
boundary analysis, segmentation or labels are introduced.

## 6. Provenance and deterministic preservation contract

Each primary record references accepted map scientific fingerprint, logical fingerprint,
root SHA, shard name/hash, ordinal, exact query ID and original manifest IDs. Every
edge references its endpoints and the exact comparison rule/version. Preserve source,
asset, EME, supporting PulseCandidate/native-strength, numerical and measurement
lineage through immutable references; do not replace identities. Exact rational
geometry and dyadic comparisons retain normalized integer-string encodings.

Prospective serialization: sorted object keys, compact ASCII-safe canonical JSON;
no floats, clocks, machine paths or performance in scientific identity. Primary order
u,L,T matches accepted map. Temporal edge order T,L,first-u,second-u; scale edge order
T,u,first-L,second-L; ratio edges T_a,T_b. IDs are structured tuples of kind and exact
endpoint IDs, not display names. Logical fingerprint is SHA-256 over canonical records
plus LF in each declared stream. A bounded root binds stream hashes and authority
hashes; operational path/size manifests remain separate. Future execution must use
bounded external streaming; immutable map input is read-only.

## 7. Validation and decision logic (prospective, not executed)

Before any future execution verify all bound input hashes and source provenance. All
4,080,384 accepted map records must be represented exactly once with identical payloads;
edge and coordinate sets must equal the rules above with no omissions/duplicates.
Check every lineage reference, rational ratio, set operation and dyadic comparison
exactly. Do not rerun the Fourier operator. Require one execution and one fresh-process
replay with byte-identical canonical streams/roots/scoring artifacts. Bulk evidence
stays external; bounded source, manifests and checksums in Git. A concrete transport
source binding/capacity plan must precede that future execution.

Any changed source map, payload, rule, ordering, omitted alternative, incorrect exact
comparison or replay mismatch => FAIL_CONTRACT; preserve evidence and STOP, no repair.
Incomplete execution or insufficient storage => STOP_INCOMPLETE, not PASS. Response
ambiguity or absent support => admissible INDETERMINATE, not an implementation failure.
Do not substitute generic response nonzero/count/overlap tests for the scientific
question's missing recurrence criterion.

A mechanically correct execution of this descriptive indexing contract would at most
establish DRUM_PERIODICITY_RESPONSE_RELATIONS_DESCRIBED for the frozen finite map.
It would NOT establish that recurrent or multiscale-consistent structures exist.
DRUM_PERIODICITY_RECURRENCE_STRUCTURE_OBSERVED remains the intended question, not an
outcome that can be authorized merely by lossless re-indexing.

## 8. Exact remaining blocker / PI review

The existing authorities do not define when correlated Fourier responses across time
and changing support constitute recurrence or multiscale-consistent evidence, as
opposed to repeated interrogation of shared EME. They supply neither a justified
approximate phase-consistency criterion nor an independently calibrated response-
sufficiency rule. Numerical enclosure overlap addresses numerical compatibility only.
Exact rational ratios cannot fill this gap. No threshold or fallback is supplied here.

This specification is NOT execution-ready for the requested recurrence claim. PI
review must first choose whether to authorize the strictly narrower descriptive
relation inventory above, or commission a separate prospective recurrence-evidence
criterion and independent controlled falsification before real-map testing. No new
experimental result, tolerance or selection rule has been invented. No map response
values were read during this design; no experiment has executed. No BPM, beat, tactus,
meter/downbeat/bar, groove/swing, Bass/Piano, fills, phrase boundaries or successor
analysis is authorized. STOP for PI review.
