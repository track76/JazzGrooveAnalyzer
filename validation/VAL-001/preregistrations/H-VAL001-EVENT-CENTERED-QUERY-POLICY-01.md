# H-VAL001-EVENT-CENTERED-QUERY-POLICY-01

Date: 2026-09-08
Status: PREREGISTERED DESIGN ONLY — PI EXECUTION AUTHORIZATION REQUIRED

## Authority and bounded claim

PI authorizes this successor coordinate/provenance design, not execution.
The accepted numerical baseline at c326d10885915469b6814ab7add947fd75ed4070
and its frozen preregistration/environment binding remain unchanged.
This experiment does not call the complex operator, evaluate trigonometry,
use audio, or read real Drum EME. Synthetic time units have no musical meaning.

AD-032 preserves native strength without interpretation. AD-034 preserves
Candidate Period evidence; AD-035 discovers recurring consecutive frame intervals
from filtered PulseCandidates, not EME. This policy does not extend that authority:
its separations are query coordinates, not established F-032 Candidate Periods.
References: docs/architecture/AD-032_M89_PULSE_STRENGTH_PRESERVATION.md;
docs/architecture/AD-034_M91_CANDIDATE_PERIOD_REPRESENTATION.md;
docs/architecture/AD-035_M92_CANDIDATE_PERIOD_DISCOVERY.md;
docs/scientific/foundations/F-032_CANDIDATE_PERIODS.md.

## Frozen synthetic input (seven populations)

All intervals below are closed. All timestamps and coordinates are exact rationals.
No strengths are required: the tested policy must not consume or rank strength.
Local event names a,b,c,d,e are qualified by population ID for unique record IDs.
Ancestral keys identify preserved observations across controlled transformations;
these synthetic identifiers are not AD-041 real-source authorities.

| Population | Events name:time | Asset interval | Observation scope | Parent mapping |
|---|---|---|---|---|
| A | a:0, b:1, c:3 | [-1,4] | [0,3] | none |
| B | a:1/2, b:3/2, c:7/2 | [-1/2,9/2] | [1/2,7/2] | B.x -> A.x; translation +1/2 |
| C | a:0, b:3/2, c:9/2 | [-3/2,6] | [0,9/2] | C.x -> A.x; dilation 3/2 |
| D | a:0, b:1, d:2, c:3 | [-1,4] | [0,3] | a,b,c -> A namesakes; d new |
| H | a:1 | [-1,4] | [0,3] | none |
| I | a:0, b:1, e:1, c:3 | [-1,4] | [0,3] | a,b,c -> A namesakes; e new |
| Z | no events | [-1,4] | [0,3] | none |

A simultaneously supplies basic, nested-separation, boundary, coverage and overlap
challenges. D adds one intermediate event. I tests coincident identities without
losing the base positive separations. H and Z test singleton and empty populations.
The small normalized integers define finite combinatorial counterexamples, not
an empirical time scale. B and C use nonidentity rational transformations; their
values authorize no real-data tuning parameter.

## Exact production construction

Use CPython 3.13.14 standard-library Fraction/integer arithmetic only. No floats,
rounding, approximate equality, frame snapping, trigonometry or tolerance.

For a population with events (id,t), asset A_s and observation scope O:
1. Require O subset A_s, valid ordered endpoints, unique IDs, and all events in O.
2. U is the set of distinct t. Every u retains all event IDs at u.
3. At u, L(u) is the set of 2*abs(t-u)>0. For each L preserve every
   (center-event ID, boundary-event ID) pair realizing that distance.
4. T is every distinct abs(t_j-t_i)>0 for unordered distinct-ID pairs.
   Store every generating pair and its exact timestamps. Exclude zero pairs
   from T, retaining them separately as coincident-pair provenance.
5. f=1/T exactly. No additional frequencies, alias closure, ranking or selection.
6. Output one query for each (u,L,T) in U x L(u) x T. Center/scale/candidate
   catalogues are retained even when the query population is empty.

Requested support W=[u-L/2,u+L/2]. Available support is W intersect O intersect A_s.
Store W, W intersect A_s, available support and their exact unavailable set
complements. Complement pieces carry open/closed endpoints; subtraction must not
incorrectly mark an available endpoint unavailable. Empty intersections are null.
Separate asset truncation from observation-scope truncation, using exact set
inclusion. Never change u or L, renormalize, pad, or invent observations.

Contained IDs have t in W and available scope. Boundary IDs satisfy abs(t-u)=L/2.
Positive-weight IDs satisfy abs(t-u)<L/2. Hann is strictly positive in its open
support and exactly zero at endpoints; classification uses this analytic fact,
not numerical cosine. Do not compute actual Hann weights or Fourier responses.
All input events lie within O, so unavailable support contributes no invented IDs.

No observations -> empty U,L,T,F and query catalogues. One unique timestamp -> one
center retaining every coincident ID, no positive scale or period and no queries.
No fabricated zero-length window. Event-centered positive windows contain their
center; an empty query support is therefore unreachable for these valid inputs.
This is not a claim about arbitrary externally supplied centers.

## Independent expected coordinate/provenance oracle

Scorer must not import the generator or repeat pairwise-distance discovery.
Use these frozen tables and the specified exact transformations. Pair labels are
unordered, normalized by event-ID lexical order; retain multiplicity of ID pairs.

A: U={0,1,3}; T={1,2,3}; frequencies {1,1/2,1/3}.
Period generators: 1:{ab}; 2:{bc}; 3:{ac}.

D: U={0,1,2,3}; T={1,2,3}; frequencies {1,1/2,1/3}.
Period generators: 1:{ab,bd,dc}; 2:{ad,bc}; 3:{ac}.

I: U={0,1,3}; T={1,2,3}; frequencies {1,1/2,1/3}.
Period generators: 1:{ab,ae}; 2:{bc,ec}; 3:{ac}.
Coincident pair: {be}. Center 1 retains {b,e}. No zero period.

H: U={1}, center IDs {a}; T and all positive scales empty.
Z: all catalogues empty. Neither H nor Z has queries.

The following independent radial shells determine scale and membership expectations.
Each entry is radius:{IDs}; all radii are listed including zero.

| Population | Center | Ordered shells |
|---|---|---|
| A | 0 | 0:{a}, 1:{b}, 3:{c} |
| A | 1 | 0:{b}, 1:{a}, 2:{c} |
| A | 3 | 0:{c}, 2:{b}, 3:{a} |
| D | 0 | 0:{a}, 1:{b}, 2:{d}, 3:{c} |
| D | 1 | 0:{b}, 1:{a,d}, 2:{c} |
| D | 2 | 0:{d}, 1:{b,c}, 2:{a} |
| D | 3 | 0:{c}, 1:{d}, 2:{b}, 3:{a} |

For I replace b with {b,e} in A's shells. For each positive shell r:
L=2r; boundary IDs are that shell; positive IDs are the union of earlier shells;
contained IDs are their union. Scale-generating pairs are the Cartesian product
of zero-shell IDs and boundary IDs. Thus no distance test is repeated in scorer.

B expectations: translate A centers, every pair timestamp and every interval
endpoint by 1/2; retain A radii, scales, T and f; relabel with B IDs/parent links.
C expectations: multiply A centers, radii, scales, T, pair timestamps and interval
endpoints by 3/2; multiply f by 2/3; relabel with C IDs/parent links.
Membership and overlap sets correspond under these explicit ID mappings.

Exact independent support endpoints (W; available W intersect [0,3]):

| Center | Radius | Requested | Available |
|---|---|---|---|
| 0 | 1 | [-1,1] | [0,1] |
| 0 | 2 | [-2,2] | [0,2] |
| 0 | 3 | [-3,3] | [0,3] |
| 1 | 1 | [0,2] | [0,2] |
| 1 | 2 | [-1,3] | [0,3] |
| 2 | 1 | [1,3] | [1,3] |
| 2 | 2 | [0,4] | [0,3] |
| 3 | 1 | [2,4] | [2,3] |
| 3 | 2 | [1,5] | [1,3] |
| 3 | 3 | [0,6] | [0,3] |

Use only rows corresponding to each population's shell table. Asset-clipped
intervals differ from requested only for (0,2):[-1,2], (0,3):[-1,3],
(3,2):[1,4], (3,3):[0,4]. All other rows remain W at the asset stage.
The endpoint table and exact interval set differences determine all coverage flags
and unavailable pieces, without a duplicated window-generation implementation.

Query counts: A=18, B=18, C=18, D=30, I=18, H=0, Z=0; total=102.
These are coordinate/provenance records, not operator evaluations.

## Provenance roles and overlap

Each population manifest retains exact events, scope, asset interval, synthetic
construction authority and parent mapping. SHA-256 binds canonical manifest bytes.
Each coordinate retains population ID, exact value, generating IDs, generating
pair timestamps when applicable, and transformation lineage. Center identities
are (population,u); scale identities (population,u,L); period identities
(population,T); query identities (population,u,L,T). Use exact tuple encodings,
not display labels or floating values.

For every query keep separate center, scale-generation and period-generation
roles. Evaluation membership is separately contained/boundary/positive ID sets.
For each of the two generator roles store:
- union of generating event IDs;
- intersection with contained, boundary and positive ID sets;
- for each generating pair, its endpoint intersection with each membership set.

Oracle overlap expectations are intersections of the frozen pair/shell tables,
not independently claimed recurrence. A concrete required witness is
A,u=0,L=2,T=1: contained {a,b}, boundary {b}, positive {a}; period pair {ab};
overlap contained {a,b}, boundary {b}, positive {a}. The boundary event generates
the scale but has zero weight. No role is relabelled independent confirmation.
Every query has scientific_status=RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED.

## Controlled invariants and scoring

A covers nonuniform timestamps and nested T=1,2 (also T=3). Do not suppress any.
B/C must satisfy the full exact transformations above, including coverage and
lineage. D must contain all original centers, each old center's scales, periods,
frequencies and generating pairs under parent mapping. Existing full membership
sets need not remain equal: additions can change them. I must preserve all IDs,
exclude zero from positive coordinates, and retain coincident provenance.

Scorer uses independently frozen tables only after candidate output is serialized.
It checks full exact catalogue/query equality including every provenance field,
not just counts or subset agreement. It additionally checks the transformation and
addition invariants, canonical encodings and manifest hashes. Generator receives
only input populations/scopes/provenance; expected tables and condition-purpose
labels are scorer-only. A harness may attach case labels after generation.

Any unequal set, rational, mapping, interval, flag, status, canonical byte sequence,
missing/duplicate query, provenance error or replay mismatch -> FAIL. Preserve
failure and stop; no retuning or repair/rerun without PI decision. No percentages,
epsilon or numerical confidence threshold. PASS requires all seven population
checks, all 102 query records and all transformation/provenance/replay checks.

## Canonical serialization and replay

Runtime: CPython 3.13.14 standard library; Fraction/integer coordinate arithmetic.
Rationals serialize as [numerator_string,positive_denominator_string], reduced,
zero=["0","1"]. Integers are base-10 canonical strings, no leading plus/zeros.
UTF-8 JSON, sorted object keys, compact separators (',',':'), ensure_ascii=True,
no trailing newline. No floats, NaN, wall-clock times or filesystem paths in
scientific bytes. Source/build hashes and input authority hashes are retained.

Population order A,B,C,D,H,I,Z. Centers/periods/scales sorted by exact numeric
value; query order population,u,L,T. Events sorted (timestamp,ID); ID sets and
normalized pair lists lexically sorted. Frequency values remain attached to their
period record. Interval pieces sorted by lower then upper endpoint. Empty sets
are []; unavailable/empty intervals use null, not invented numeric coordinates.
Input manifest and code hashes bind production and scorer versions before execution.
Scoring artifact retains every comparison outcome, totals and input-output hashes.

After separate PI authorization: one complete seven-population/102-query execution
then one fresh-process replay. Require byte-identical canonical generated output,
scoring artifacts and provenance manifests. Record SHA-256 of each; no additional
runs or expanded fixture domain. This preregistration contains no test execution.

## Decision scope and readiness

Maximum future PASS: EVENT_CENTERED_MULTISCALE_PERIODICITY_QUERY_POLICY_VALIDATED,
limited to these synthetic populations, exact coordinate/support/separation rules,
provenance and deterministic replay. It does not establish recurrence, exhaustive
continuous coverage, Fourier-response sufficiency, real Drum application, physical
timing accuracy, trajectory tracking, level selection, half/double disambiguation,
BeatReference, musical phase, tactus, meter/downbeat, BPM, accompaniment or graphics.

All finite fixture and oracle choices are specified prospectively. No empirical
parameter or unresolved numerical tolerance is needed for this bounded claim.
Ready for implementation/execution only after PI authorization. No new architecture,
production implementation, real-data query or experiment execution is authorized now.
