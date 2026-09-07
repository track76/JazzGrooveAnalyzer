# H-VAL001-LOCAL-COMPLEX-DRUM-PERIODICITY-01

Date: 2026-09-07
Status: SUCCESSOR DESIGN — NOT EXECUTION-READY — NO EXPERIMENT EXECUTED
Authority: PI authorization for design/preregistration only, in this session.
Repository baseline: 51cedd8dba23906e870f2df6d64382831f4d3e74.

## Hypothesis and historical separation

A provenance-bound local complex-periodicity representation may preserve acoustic
period-and-alignment alternatives in Drum onset-strength evidence under controlled
shifts, local temporal changes and subdivision additions. This is representation
validation, not musical level selection. No argmax, PLP synthesis, beat sequence,
new detector, confidence threshold or production implementation is authorized.

Historical H-VAL001-DRUM-STRENGTH-ORGANIZATION-01.md remains unchanged, SHA-256
bea46dbfe5b1cdcef114d45af86fe65302bfc208e8855de78161419964429089.
Its unresolved strength/phase findings are limiting prior evidence. The deferred
accompaniment preregistration is not executed or modified.

## Literature and scope of mathematical adaptation

Grosche, P. and Mueller, M. (2009), A Mid-Level Representation for Capturing
Dominant Tempo and Pulse Information in Music Recordings, ISMIR, pp. 189–194,
Section 3, equation (2):
https://archives.ismir.net/ismir2009/paper/000007.pdf

Grosche, P. and Mueller, M. (2011), Extracting Predominant Local Pulse Information
from Music Recordings, IEEE TASLP 19(6), 1688–1701:
https://doi.org/10.1109/TASL.2010.2096216
Author publication: https://petergrosche.github.io/publication/grosche-2010-extracting/

The cited local transform operates on a novelty curve; complex magnitude and
phase describe local sinusoidal evidence. A Hann window is used in the 2009
paper, with a robustness/locality tradeoff and several window durations. Its
tempo range, predominant-response selection and downstream PLP are NOT adopted.
The sparse-measure adaptation and identities below are mathematical deductions,
not claims of published validation on JGA EME.

## Input decision: A, sparse weighted event measure

For every Drum observation preserve (id_i,t_i,s_i,lineage_i) exactly. Let

  mu = sum_i s_i delta_(t_i)
  F(u,f;L) = integral w_L(t-u) exp(-2*pi*i*f*t) dmu(t)
           = sum_i s_i w_L(t_i-u) exp(-2*pi*i*f*t_i).

Here t,u,L are in seconds and f is cycles/second. Strength is the preserved native
detector value, not energy, loudness or a beat probability. No normalization,
binarization or strong-event threshold. Weak events and duplicate-time identities
remain; every summand has lineage. Ambiguous EME-to-strength linkage stops input
acceptance. Nonfinite/missing data are not silently removed.

This is the exact Fourier integral of the specified finite atomic measure. It
does not reconstruct the full detector novelty curve or unobserved events. A
regular-grid impulse array gives the same sum only when coordinates and scaling
agree exactly; nearest-bin placement is forbidden. Full-novelty literature results
do not transfer automatically. A is sufficient for testing the representation of
the observed weighted event measure; its fidelity to pre-detection acoustic
components remains an independently testable measurement question. B is not needed
to define this hypothesis and is not introduced.

## Frequency domain and alternative status

Mathematical domain: f in [0,infinity). Negative frequencies follow conjugate
symmetry for real strengths. f=0 records weighted DC mass; its period/alignment
are not defined. All f>0 have coordinate T=1/f, not an authorized musical unit.
The finite sum defines the full continuous-frequency function, including long
periods absent from consecutive-IOI discovery. AD-035 evidence may be cross-linked
but never restricts this domain. No musical BPM range or low-frequency cutoff.

If all authoritative event coordinates lie on one exact lattice of spacing h,
frequency aliases repeat up to origin phase with interval 1/h. A baseband may
represent that equivalence only with explicit alias/origin provenance. Irregular
coordinates do not acquire a Nyquist limit from mean event density. Floating-point
timestamps must not be snapped to create a lattice.

The functional representation is exact but a finite coefficient-output grid is
NOT YET FROZEN. No completeness claim for an arbitrary sampled grid is authorized.
Frequency spacing controls sampling, not actual resolving power. No response is
discarded for being smaller than another. f,2f,f/2 remain distinct queries with
unresolved musical meaning; a query is not automatically evidence of a component.

## Window/locality

Prospective window family, following the cited Hann construction:

  w_L(v) = (1+cos(2*pi*v/L))/2 for |v| <= L/2; 0 otherwise, L>0.

The shape is explicit; L is an unresolved parameter, NOT a runtime choice based
on observed outcomes. Literature offers multiple legitimate supports and does
not identify one preferred support for this sparse Drum hypothesis. Larger L
narrower frequency features/slower localization; smaller L more local but poorer
frequency discrimination. Nominal Fourier scale 1/L is not a timing-error bound
or guarantee of separating close components. A fixed multiscale family could be
specified prospectively, but no arbitrary list is supplied here.

Record every window's intersection with authorized scope. A truncated boundary
window is flagged and not treated as complete. Zero extension outside scope is
an algebraic convention only, never musical absence. No stitching, interpolation,
gap filling or cycle counting is part of this representation. u remains a
continuous coordinate; a finite analysis-time sampling schedule is also pending.

## Phase/alignment

For nonzero F define theta=atan2(Im F,Re F), modulo 2*pi. The associated sinusoid
is cos(2*pi*f*t+theta); its maxima satisfy t=(m-theta/(2*pi))/f for integers m.
These are model-alignment hypotheses, not observed events or beat positions.
At F=0 phase is undefined. With numerical enclosure containing zero, phase remains
uncertain; no arbitrary low-magnitude threshold is introduced. Never unwrap phase
across frequencies, gaps or time without separately authorized continuity rules.

Exact translation identity, with event strengths unchanged and scope/window moved:

  t'_i=t_i+d -> F'(u+d,f;L)=exp(-2*pi*i*f*d) F(u,f;L).

At a fixed u without moving the window, different membership means that identity
need not hold. No first-event origin. Reference m labels no downbeat or meter.

Exact uniform dilation identity for atomic weights unchanged:

  t'_i=a*t_i, a>0 -> F'(a*u,f/a;a*L)=F(u,f;L).

This identity does not claim invariance at fixed L. A piecewise warp is evaluated
by the defining sum; near transitions a window can legitimately contain multiple
periodicities. A unique local tempo curve is not required or generated.

## Five controlled construction templates and scoring obligations

These are exact symbolic families, not finalized numeric audio constructions.
N,T,weights,offsets,transition schedule,L and renderer remain unbound pending
the gates below. They cannot be chosen after candidate or challenge inspection.

A: finite impulse train sum_(j=0..N-1) b delta_(o+j*T), b>0. Independent analytic
finite-sum oracle verifies coefficients, including off-grid frequencies; presence
means agreement with the constructed response, not selection of a tallest peak.
B: sum of independently labeled positive-weight trains at T,2T,T/2 and declared
offsets. Oracle uses the complex sum of component responses. Preserve all queried
alternatives and lineage; do not require every generating period to yield a peak.
C: translate A/B by declared d with common scope translation. Test the exact
complex rotation identity, not ordinary subtraction of wrapped phase angles.
D: piecewise affine monotone time map g applied to the event construction with
declared transition positions and slopes. Within homogeneous portions compare
the local defining sums; across transitions preserve the mixed response. The
uniform-dilation identity supplies a separate exact control when windows scale too.
E: add a declared subdivision train nu to A/B. Test linearity
  F_(mu+nu)=F_mu+F_nu
and complete input lineage. Do not require magnitude preservation, since complex
responses can cancel. Component separation is a scoring oracle privilege, not an
inference input. Observed sums alone need not identify their generating decomposition.

Critical physical limitation: two equal infinite trains separated by T/2 sum to
a train with period T/2; their coefficients at 1/T cancel. Corresponding finite
windows can also cancel or show boundary residuals. Requiring a visible 1/T peak
after every subdivision addition would be scientifically false. Preserve response
and destructive interference, not fabricate recoverability of hidden components.

## Hidden authority and measurement boundary

Before rendering, independent construction authority freezes event schedules,
weights at their actual declared level (symbolic velocity is not detector strength),
component decompositions, transformations, acoustic-source procedure, scope,
source-instance authority and renderer configuration. After generation and before
inference, bind WAV SHA-256 and rendering records. Future byte checksums cannot
be known before rendering. No generation is performed here.

Inference receives only allowed Drum EME/strength/provenance/configuration. It
does not receive condition names, reference schedules, hidden component IDs or
expected counts. Freeze complete representation and deterministic replay before
scoring access. Mathematical identities on already frozen event measures are
representation checks, NOT proof that rendering plus detection obeys the same
transformations. No synthetic event fixture may be reported as detected audio.

The hidden oracle must distinguish authored symbolic events, measured acoustic
events and detected observations. Independent mapping/uncertainty is needed to
compare them. Detector strength is not invariant under rendering changes merely
because symbolic velocity is fixed; omissions/additions cannot be rematched using
desired results. CED-VAL-007/008 are baselines, not this calibration authority.

## Numerical bounds and replay

Exact identities above require no empirical percentage threshold. An executable
implementation must prospectively specify arithmetic precision, transcendental
evaluation and certified rounding/enclosure rules. No arbitrary 1e-6 tolerance.
Deterministic summation order is by (timestamp,EME ID), without using IDs to choose
scientific alternatives. Canonical serialization fixes numeric forms, units,
ordering, undefined phase and parameter lineage. That executable schema is pending.

A useful analytic bound (not a supplied calibration) follows from |w|<=1 and
the global Hann Lipschitz bound pi/L. For matched events with |delta t_i|<=e_ti
and |delta s_i|<=e_si, at fixed u,f,L:

  |delta F| <= sum_i [e_si + |s_i|*(pi/L+2*pi*|f|)*e_ti].

This assumes the same matched population; unmatched contributions need their own
explicit bounds. Numerical evaluation error is additional. Independent e_ti/e_si
are NOT established here. Phase may be bounded only when the resulting complex
enclosure excludes zero; cancellation defeats any universal phase tolerance.
Analysis-grid spacing, hop size and 1/L cannot replace these measurement bounds.

## Proposed neutral representation (not architecture approval)

LocalComplexPeriodicityEvidence, provisional: evidence ID, analysis coordinate u,
f and 1/f when defined, L/window/scope, Re/Im response, magnitude, phase or explicit
undefined/uncertain status, each contributing observation and weighted contribution,
source UUID, original asset SHA, immutable input fingerprint, parameter authority,
arithmetic authority, boundary status, alias relations and unresolved interpretation.
Finite sum/input lineage preserve the functional definition beyond any sampled grid.
No beat-confidence field or selected-winner field. AD-034 remains unchanged rather
than being overloaded with complex-response semantics; final ownership requires
architecture review. BeatReference receives nothing from a correlation maximum.

## Blocking decisions and final disposition

NOT FULLY SPECIFIED; NOT SAFE TO EXECUTE. Exact blockers:
1. Window duration or justified fixed multiscale family and analysis-time schedule.
2. Finite frequency-output coverage/resolution contract for the continuous function.
3. Independent rendering/detector correspondence and strength/timestamp bounds
   for acoustic validation, distinct from mathematical fixture validation.
4. Certified numerical realization and canonical schema for tolerance/replay checks.
5. Numeric challenge and rendering bindings after, not before, those choices freeze.

No winner or generic accuracy criterion resolves these gaps. Prospective acceptance
requires oracle agreement within independently justified bounds, full response and
alternative preservation including cancellations, exact provenance, canonical replay
and no leakage. Missing bounds -> NOT_EXECUTABLE, not empirical failure. Leakage
or post-result tuning -> INVALID. No experimental classification is produced here.

frequency/recurrence rate != musical BPM; complex alignment != musical beat phase.
No tactus, quarter note, meter or downbeat authority follows. Demucs's 94.83% Drum
preservation remains condition-bound. No accompaniment, Demucs, Bass recovery, JTD,
PLP winner selection, downstream reference construction or visualization is performed.
Stop for PI review; preserve this successor separately from all historical evidence.
