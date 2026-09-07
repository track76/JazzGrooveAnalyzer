# H-VAL001-SPARSE-COMPLEX-OPERATOR-01

Date: 2026-09-07
Status: PREREGISTERED — EXECUTION-READY DESIGN — NOT EXECUTED
Execution requires the PI's next authorization. No operator implementation or
experiment is included in this design task.

## Authority and maximum claim

PI decision authorizes this narrower representation-only design. Baseline branch
scientific/translation-layer-finalization, HEAD
51cedd8dba23906e870f2df6d64382831f4d3e74.
PASS maximum: LOCAL_COMPLEX_PERIODICITY_REPRESENTATION_VALIDATED, strictly within
the exact synthetic construction and exact-arithmetic query domain below.
This means REPRESENTATION-LEVEL VALIDITY, never AUDIO-TO-REPRESENTATION VALIDITY.

The previous H-VAL001-LOCAL-COMPLEX-DRUM-PERIODICITY-01.md remains unchanged,
SHA-256 0eb3732a0b9cd3d43ad1ea3016a8d1a46841ead6738a7c17094eb5acf8f5bb15.
Earlier strength and accompaniment designs remain unchanged and unexecuted.

Literature basis: Grosche and Mueller, ISMIR 2009, pp. 189–194, Section 3,
equation (2), https://archives.ismir.net/ismir2009/paper/000007.pdf;
Grosche and Mueller, IEEE TASLP 19(6), 1688–1701, 2011,
https://doi.org/10.1109/TASL.2010.2096216.
The local Fourier operator is adapted to an exact finite atomic measure. Neither
published novelty extraction nor PLP winner selection is implemented or validated.

## Exact input, units and operator

The companion H-VAL001-SPARSE-COMPLEX-OPERATOR-01.inputs.json fixes literal
event IDs, rational times and rational weights. It is construction authority,
not audio evidence. T=1 normalized time unit; weights are dimensionless test
scalars, not detector strength measurements. Negative coordinates are legitimate
synthetic coordinates; no nonnegative-audio-domain constraint is imported.
Companion byte SHA-256:
c340e6bc7041c475b9f9f7989c94e662b22b2ce135c5e09040b60b298c2e20f5.

  mu = sum_i s_i delta_(t_i)
  F_mu(u,f;L) = sum_i s_i w_L(t_i-u) exp(-2*pi*i*f*t_i)
  w_L(v) = (1+cos(2*pi*v/L))/2 for |v|<=L/2; zero otherwise.

MU: times -2,-1,0,1,2, all weights 1.
NU: times -3/2,-1/2,1/2,3/2, all weights 1/2.
RHO: times -2,0,2, all weights 1/2.
Keep coincident-time event identities separate; sum contributions without merging
their lineage. No normalization or deletion of weak/zero-weight contributions.

Queries: u=0, L/T in {4,8}, f*T in {1/4,1/2,1,2}, Cartesian product (8 queries).
These are oracle-selected mathematical coordinates, never a production grid.
The supports exercise boundary-zero weights at L=4 and nonzero outer weights at
L=8; frequency coordinates exercise a longer scale, nested rates and exact zeros.
There is no claim these scales are musically optimal or cover all frequencies.

## Exact numerical domain — no empirical tolerance

Use CPython 3.13.14 (the inspected local runtime) and only standard-library
fractions.Fraction, integer arithmetic, json and hashlib for authoritative
arithmetic/serialization. Record full runtime/platform and implementation SHA.
No binary floating-point trigonometry, numpy, learned model or approximate oracle.

Let z=exp(i*pi/8). All required responses belong to Q(z), with irreducible
cyclotomic polynomial Phi_16(z)=z^8+1. Represent each value canonically as eight
rational coefficients (c0,...,c7) for sum c_j*z^j. Reduce powers by z^8=-1;
z^16=1. This is exact, unbounded-rational arithmetic: tolerance = zero.
The embedding is specifically z=cos(pi/8)+i*sin(pi/8), not another conjugate root.

For a rational angle r with 16*r integral:
  exp(-2*pi*i*r)=z^(-16*r)
  cos(2*pi*r)=(z^(16*r)+z^(-16*r))/2.
Every query, translated query and dilated query below satisfies this property.
An unsupported angle must fail explicitly; no rounding or approximation fallback.
Input fractions remain exact and unrounded, including during transformations.

Conjugation sends z to z^-1. Re Z=(Z+conj Z)/2 and Im Z=(Z-conj Z)/(2*z^4).
Magnitude-squared Q=Z*conj Z is exact. Magnitude is serialized as the nonnegative
formal sqrt(Q); no approximate decimal is required. Phase is undefined if Z=0;
otherwise retain the exact unit-direction expression Z/sqrt(Q) and the formal
principal atan2(Im Z,Re Z) convention (-pi,pi]. Validate phase transformations by
complex rotation, not approximate angle subtraction or branch-sensitive unwrap.
These exact symbolic forms validate phase semantics without transcendental rounding.
No floating-point production evaluator is validated by this experiment.

## Independent closed-form oracle

Set r=sqrt(2)=z^2-z^6, c1=cos(pi/8)=(z+z^-1)/2,
c3=cos(3*pi/8)=(z^3+z^-3)/2 and C=1+(c1+c3)/2.
The following real responses follow by pairing symmetric positive/negative events
and substituting their Hann weights. This table is frozen before implementation.
Columns always correspond to f=(1/4,1/2,1,2).

| Measure | L | Responses |
|---|---|---|
| MU | 4 | (1, 0, 2, 2) |
| MU | 8 | (0, 1-r/2, 3+r/2, 3+r/2) |
| NU | 4 | (1/2, 0, -1, 1) |
| NU | 8 | (r*(c1-c3)/4, 0, -C, C) |
| RHO | 4 | (1/2, 1/2, 1/2, 1/2) |
| RHO | 8 | (0, 1, 1, 1) |

An independent scorer constructs this table as algebraic constants, not by
re-running the operator's event/window summation. Operator and scorer share only
the declared exact field semantics, never the event-evaluation routine or result
files. Audit each oracle expression against the paired-event derivation before
execution. No modification based on observed test errors is allowed; a discovered
specification error invalidates that run and requires a prospective successor.

The independent algebraic derivation, valid at u=0, is:
  M_4(f)=1+cos(2*pi*f)
  M_8(f)=1+(1+r/2)*cos(2*pi*f)+cos(4*pi*f)
  N_L(f)=w_L(1/2)*cos(pi*f)+w_L(3/2)*cos(3*pi*f)
  R_4(f)=1/2
  R_8(f)=1/2+(1/2)*cos(4*pi*f).
For N, w_4(1/2)=(1+r/2)/2, w_4(3/2)=(1-r/2)/2,
w_8(1/2)=(1+c1)/2 and w_8(3/2)=(1+c3)/2. These yield the table directly.

## Six properties, exact constructions and expected responses

A — periodic measure: evaluate MU at all 8 queries; compare to the MU oracle row.
Also evaluate NU/RHO (8 each) as independent component controls for later tests.

B — linearity: MU+NU+RHO, disjoint union retaining all 12 IDs. At all 8 queries
compare to the sum of the THREE FROZEN ORACLE rows. Separately verify equality
to the sum of the frozen component operator results. Oracle agreement is mandatory;
internal consistency alone is insufficient.

C — translation: translate MU by d=1/4, strengths unchanged; evaluate u'=1/4,
same f,L. Expected Z'=z^(-4*f)*M_L(f), where M is the MU oracle. Exponents are
integers for all four f. This is
  F_(translated MU)(u+d,f;L)=exp(-2*pi*i*f*d)*F_MU(u,f;L).
Require nonzero transformed cases and exact complex phase rotation; zero cases
retain undefined phase. Scope/event support translates with the window.

D — dilation: apply a=3/2 to all times of MU+NU, weights unchanged. Evaluate
u'=0, f'=f/a, L'=a*L. Expected Z'=M_L(f)+N_L(f) from the frozen table. This is
  F_(dilated measure)(a*u,f/a;a*L)=F_measure(u,f;L).
Atomic weights gain no Jacobian factor. This does not claim fixed-window invariance
or local trajectory tracking. The non-power-of-two factor tests rational coordinate
handling without importing a metrical or octave interpretation.

E — nested structure: MU+RHO (8 distinct observations, including coincident times),
with finite component spacings 1 and 2. Evaluate all 8 queries, retaining all
responses including zeros. Closed-form expected rows:
  L=4: (3/2,1/2,5/2,5/2)
  L=8: (0,2-r/2,4+r/2,4+r/2).
No period is selected and no peak prominence is required.

F — subdivision superposition: MU+2*NU, multiplying NU weights by exactly 2 while
retaining their IDs/parent weights. Expected rows:
  L=4: (2,0,0,4)
  L=8: (r*(c1-c3)/2,1-r/2,3+r/2-2*C,3+r/2+2*C).
Verify both oracle equality and linearity. At L=4,f=1, responses 2 and -2 cancel
EXACTLY: total phase is undefined. At L=4,f=2, constructive addition produces 4.
No requirement to recover a hidden component from a canceled aggregate response.

Minimum expected result population: 3 component controls x 8 = 24 records,
plus B,C,D,E,F x 8 = 40 records; total 64. Unique record key is
(case_id,u,f,L). Both cancellation and nonzero phase-shift coverage are mandatory.

## Provenance, authority separation and checksums

Before execution, freeze this specification SHA and companion-file byte SHA.
Each MU/NU/RHO construction checksum is SHA-256 of canonical UTF-8 JSON containing
its authority_id, measure_id, units and literal event triples. Derived measure
manifests contain exact transformed triples, construction operation/parameters,
parent checksum and per-event parent IDs; hash these before operator execution.
Fixture IDs are synthetic identities, never AD-041-authorized real Drum UUIDs.

The operator API receives only the measure, explicit query parameters and parameter
authority. It must not receive case labels, expected answers or transformation
relations. The scoring harness owns query coordinates; giving them to the operator
is necessary evaluation, expressly NOT autonomous discovery or a hidden-input claim.
Oracle correctness does not depend on secrecy; it depends on independently specified
closed forms and separation from the evaluated computation. No investigator blinding
claim is made: the specification is public and no challenge audio exists.

Each result retains query/parameter authority, input/derived construction checksums,
source measure ID, every event's exact time/weight/window contribution and parent
lineage, complex/magnitude/phase form and numerical authority. Zero-window events
remain in the input manifest with zero contribution. There is no audio asset SHA;
construction-byte identity must not be relabeled as an audio asset identity.

## Canonical serialization and deterministic replay

Canonical JSON: UTF-8, sorted object keys, separators (',',':'), ensure_ascii=True,
no NaN, no optional whitespace and no trailing newline. Every rational is a reduced
string 'numerator/positive_denominator', including zero '0/1'. Field vectors always
have 8 entries. Events sort by exact time then ID; results sort by case ID then
exact rational u,f,L. IDs order records only, never select scientific alternatives.
All sums use exact arithmetic. Magnitude/phase expressions use fixed tagged objects
containing canonical field vectors, not variable textual simplifications.

Mandatory value tags: complex_field_vector; magnitude_squared_vector;
magnitude={kind:nonnegative_sqrt,radicand_vector:Q};
phase={status:UNDEFINED} at zero or
{status:EXACT_SYMBOLIC,kind:principal_atan2,real_vector:R,imag_vector:I} otherwise.
No wall-clock time, random UUID or local filesystem path enters canonical scientific
bytes. Runtime metadata is stored separately and checksum-bound.

Run the complete frozen 64-query population once and replay once in a fresh process
with identical inputs/runtime. Require byte-identical canonical operator outputs
and scorer results and equal SHA-256. Audit that every expected key appears exactly
once and all construction/parameter/lineage hashes verify. Record implementation
and scorer source hashes before either run; no adjustment between runs.

## Frozen decision and remaining scope

PASS requires exact field equality for every oracle response and transformation,
all 64 records, all required phase/cancellation checks, provenance verification,
and byte-identical replay. No percentage threshold or approximate fallback.
Any algebraic mismatch or missing/duplicate record -> FAIL_REPRESENTATION_VALIDATION.
Oracle leakage into the evaluated operator, post-result tuning or changed frozen
inputs -> INVALID_EXPERIMENT. Unsupported runtime/domain -> NOT_EXECUTED until
prospective resolution, not an empirical failure or permission to change arithmetic.
Report all property outcomes, not merely an aggregate PASS.

No mathematical/numerical blocker remains for this exact finite test domain.
Pending actions are implementation under separate execution authorization and the
mechanical freeze of implementation/fixture manifests, not new scientific choices.
This design does not validate arbitrary irrational timestamps/frequencies, a generic
floating-point implementation or all possible measures from finite examples.

Still DEFERRED: sparse EME versus continuous novelty; detector measurement robustness;
window choice/adaptation; finite time-frequency search; automatic discovery; trajectory
linking; level ambiguity; beat-unit/tactus authority; BPM semantics. No BeatReference,
musical phase, audio validity, Drum beat tracker or source-completeness claim follows.
No Bass/Piano, audio, Demucs, JTD, Bass recovery or visualization is used.

STOP for PI authorization before implementation or execution.
