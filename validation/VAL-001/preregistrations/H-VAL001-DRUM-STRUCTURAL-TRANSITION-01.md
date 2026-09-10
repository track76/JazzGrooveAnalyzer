# H-VAL001-DRUM-STRUCTURAL-TRANSITION-01

Date: 2026-09-09. DESIGN ONLY. No execution authorized by this document.
Status: proposed bounded descriptive channel; structural-transition significance
NOT_ESTABLISHED. STOP for PI review before implementation or execution.

## Purpose and audited authority

Describe measurable local changes in the already accepted Drum observation sequence,
independently of periodicity responses. Fills, setups, crashes and phrase/section
transitions are PI motivation only; they supply no labels, locations, periods or rules.

AD-032 preserves native onset strength without musical/accentual/behavioural semantics.
SourcePulseCandidateBuilder records detector times and onset_strength at detected
frames. These are sparse detector measurements, not loudness, physical attack truth,
Drum-class identities, continuous novelty or a texture representation. Accepted
binary64 authority preserves numerical values, not physical precision.

BehaviourDensityDescriptorBuilder operates on BehaviourObservation timelines and
computes pulses/(pulses+duration). This is not an established raw-Drum event-rate or
structural-change authority. BehaviourChangeEvent and StableRegionDetector operate
on behaviour frames; the existence of those types does not validate transition
inference from the present sparse EME. Do not reuse their semantic event labels or
promote implementation defaults into scientific authority.

No independently bound spectro-temporal/texture-change observable for this input was
established by this audit. Audio checksum authority alone does not supply a spectral
feature, frame policy, normalization or transition rule. Texture/Drum-class/crash
identification is therefore NOT_AVAILABLE_IN_THIS_EXPERIMENT, not silently added.

Sibling H-VAL001-DRUM-STRUCTURAL-TRANSITION-01.authorities.json binds audited sources
and prospective input authority; SHA-256:
8de42067ebfc0381fac5e6fd5795965d9964da7202b6e0f3feca3df152f89fda.

## Strict input boundary

Use only the accepted direct-input Drum EME, their unique supporting PulseCandidate
IDs/native strengths and source/asset/measurement provenance from the bound canonical
report. Exactly 63 EME and 63 supporting observations. Select by source UUID
c46d6cb9-b99c-5bd6-8d81-656dc1ad48ec, instance VAL001_SOURCE_001, not by musical role.
Do not read any accompaniment, AD-038/AD-040 localization, symbolic/metric/reference
or periodicity-response fields into the analysis process. A future input adapter
must provide an allowlisted Drum-only projection and bind its checksum BEFORE any
contrast calculation. Original report bytes remain immutable.

Timestamps and strengths retain original JSON tokens, bits, exact binary64 dyadic
ratios, supporting identities and measurement limitations. No confidence substitution.
No onset detection, audio processing, recalibration or accepted-evidence recomputation.

## Exact neutral contrast representation

Order observations by exact timestamp then EME ID. Let distinct times be
x_0 < ... < x_(m-1), and G_j the complete set of coincident observation IDs at x_j.
Coincidence grouping is an index only: retain every ID and strength. No averaging or
choice among coincident events. Let S_j be the empirical measure of native strengths
in G_j: S_j = (1/|G_j|) sum_(i in G_j) delta_(s_i). This exact empirical normalization
only represents observed multiplicity, not loudness or probability of a musical event.

Retain all m groups, all m-1 positive gaps d_j=x_(j+1)-x_j and their endpoints.
Optionally named reciprocal spacing r_j=1/d_j is an exact local spacing descriptor,
NOT tempo, beat rate or complete-performance event density. Group cardinality is
reported separately. Do not count detected events as all performed events.

Every interior index j=1..m-2 is an UNSELECTED_CANDIDATE_SITE, regardless of values.
Its location is the observed x_j and its evidence span is [x_(j-1),x_(j+1)]. It is
not an estimated physical change point. Preserve:
- d_(j-1), d_j and exact signed difference d_j-d_(j-1);
- r_(j-1), r_j and exact signed difference r_j-r_(j-1);
- all strengths/IDs in G_(j-1), G_j, G_(j+1);
- full empirical strength-CDF contrasts H_left(z)=CDF(S_j)(z)-CDF(S_(j-1))(z)
  and H_right(z)=CDF(S_(j+1))(z)-CDF(S_j)(z).

Represent each step function exactly by its values at every distinct strength in
the union of its two groups, in ascending numerical order; below minimum it is zero
and at/above maximum it is zero. Retain multiplicities and endpoint provenance.
No maximum distance, ranking, significance statistic, feature weighting or aggregate
transition score is computed. For singleton groups this reduces to a description
of two native-strength values, not a well-estimated population distribution.

Also retain the complete ordered adjacent-group CDF contrasts (m-1), including
endpoints. All site vectors are retained together as multiple observable dimensions;
no conjunction or weighted combination promotes them to a detected transition.
For the accepted 63 distinct-time input: 63 groups, 62 gaps, 62 adjacent strength
contrasts and 61 interior candidate sites. Verify these geometry-only counts before
future execution; mismatch stops rather than changing rules.

Adjacency is the smallest local evidence span requiring no chosen duration/hop,
number of bars, expected tempo or window scale. It supplies no invariance to detection
missingness and does not claim that this span captures every physical change.
Do not smooth, resample, interpolate, merge sites or add windows after inspection.
No value-based filtering, even for exactly zero contrasts. Exact differences are
numerical descriptions, not decisions that a physical structural change occurred.

## Structural change versus candidate versus interpretation

OBSERVABLE_CONTRAST means the exact difference between accepted numerical observations.
UNSELECTED_CANDIDATE_SITE means an interior observational location at which contrasts
can be described; it is not positive evidence that a transition is present.
STRUCTURAL_TRANSITION_STATUS remains INDETERMINATE / NOT_ESTABLISHED at every site.
No site is promoted solely by a nonzero difference. No abrupt/gradual labels are
assigned: the ordered contrast sequence preserves the data relevant to those future
hypotheses, but no timescale, noise model or persistence rule currently authorizes
that classification. All candidate alternatives remain; no preferred location.

Ends have ONE_SIDED_EVIDENCE_ONLY. If fewer than three distinct timestamps are present,
no interior sites can be constructed; preserve inputs and mark INSUFFICIENT_CONTEXT.
No division by zero: coincident timestamps remain in groups, never zero-length rate
intervals. Preserve exact gaps and scope truncation; no 'large gap' cutoff. Missing
observation is not silence, a rest or a structural boundary. Sparse detection and
unestablished physical-timing/strength uncertainty propagate unchanged.

## Independence firewall

The procedure receives no T, frequency, phase, periodicity magnitude, map-derived
query/window/center selection or response status. Its centers are derived afresh
from the accepted Drum timestamps, not copied from the periodicity query policy.
No accepted periodicity responses were inspected for this design. No comparison
with that map, including post-hoc overlays/correlations, occurs in this experiment.

This is computational/decision independence, NOT statistical independence: channels
A and B share underlying Drum EME, native strengths, detection limitations and source.
A later independently preregistered comparison must account for that shared provenance;
it cannot count B as an independent replication of A merely because code is separate.
Fills, phrase boundaries and section/bar groupings are never supplied or inferred.

## Provenance, arithmetic and prospective validation

Every group/gap/contrast/site carries structured identity from its kind and complete
ordered EME IDs, source UUID/asset hash, input projection/report SHA, PulseCandidate
strength lineage, exact timestamp/strength fields, scope and construction authority.
Empirical-CDF coordinates are native-strength coordinates, not thresholds selecting
observations. Calculations use exact rational arithmetic on binary64 dyadics; no Arb
or transcendental evaluation is required and no floating-point tolerance is introduced.

Canonical artifacts: input projection, groups, gaps, adjacent strength contrasts,
interior candidate sites, endpoint statuses, provenance and bounded root/hash manifest.
Sorted object keys, compact ASCII-safe UTF-8 JSON; rationals as reduced integer-string
pairs; lists ordered by timestamp/EME ID, then strength coordinate where applicable.
No clocks, machine paths or performance data in canonical science. Logical SHA-256
is over canonical records followed by LF in each declared stream. No visualization.

Before future execution bind implementation/independent exact scorer sources and
verify input authority/projection and counts. The scorer must independently check
set/multiplicity conservation, rational gaps/reciprocals/differences, every CDF step,
all sites (including zero contrasts), provenance and all prohibited-input exclusions.
One execution plus one fresh-process replay; require byte-identical canonical
artifacts/scoring and complete provenance. Any mismatch or leakage => FAIL, preserve
and STOP without repair/restart. Incomplete evidence => STOP/INSUFFICIENT, never PASS.
These are prospective requirements, not executed tests or existing validation claims.

## Decision, readiness and maximum scope

The exact contrast-inventory calculation is mathematically specified without a
threshold. After PI review and source/input binding it can support a bounded
representation-level execution. A mechanical PASS would establish only
DRUM_LOCAL_OBSERVATION_CONTRAST_PROFILE_DESCRIBED for this finite population.
It would not establish a valid detector of physical structural transitions.

The broader requested transition-observation capability is NOT execution-ready:
there is no demonstrated measurement/noise model or independently validated rule
separating a meaningful structural change from normal detected-event variability or
selective missingness. Neither AD-032 nor behaviour-frame code resolves this gap.
Abrupt/gradual and texture interpretations have additional unsupported scale/feature
requirements. Do not invent a cutoff, call all sites transitions, or use periodicity
agreement to fill that gap. PI must review the narrower descriptive scope before
execution, or authorize separate controlled evidence for transition significance.

This is one design only, not a new research program. No experiment or comparison was
executed. No beat/BPM/tactus/meter/downbeat/bar or four-bar assumption, phrase/section,
fill, groove/swing, Bass/Piano or A-vs-B analysis is authorized. Accepted evidence
remains unchanged. STOP for PI review.
