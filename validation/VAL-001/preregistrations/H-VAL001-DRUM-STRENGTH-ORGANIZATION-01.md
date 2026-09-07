# H-VAL001-DRUM-STRENGTH-ORGANIZATION-01

Date: 2026-09-07
Status: PROSPECTIVE DESIGN — BLOCKED — NOT EXECUTION-READY

PI authority: design/preregistration only for recurrent temporal organization
of preserved Drum onset strength jointly with Drum EME timestamps. No challenge
generation, observation execution, scoring or production implementation occurred.
This record is not a completed executable preregistration. Unresolved decisions
below may not be supplied after viewing challenge data.

## Authority and limiting evidence

Baseline: scientific/translation-layer-finalization at
51cedd8dba23906e870f2df6d64382831f4d3e74.
AD-032 authorizes exact strength preservation, not accentual/metrical meaning.
AD-034 and AD-035 authorize neutral candidate evidence, not phase, selection,
local tracking or ranking. References:

- docs/architecture/AD-032_M89_PULSE_STRENGTH_PRESERVATION.md
- docs/architecture/AD-034_M91_CANDIDATE_PERIOD_REPRESENTATION.md
- docs/architecture/AD-035_M92_CANDIDATE_PERIOD_DISCOVERY.md
- validation/VAL-001/run_20260816_195601/report.md (Drum strength unresolved)
- validation/VAL-001/run_20260816_193800/report.md (Drum occupancy preference
  does not establish reference level)
- validation/VAL-001/run_20260809_161637/report.md (level/phase gap)
- validation/CED-VAL-008-VARIABLE-TEMPO-BENCHMARK/run_20260825_102058/report.md
  (controlled observation localization, not a JGA local reference trajectory)

Only Drum findings are relevant here. Historical limiting evidence remains
unchanged. Existing legacy period-halving and event-enumeration code supplies
neither scientific selection authority nor a replacement experiment rule.

## Fixed input representation

Let O = ((id_i, t_i, s_i, p_i)) be all authorized Drum EME and their uniquely
bound supporting detector-strength observations, ordered by (t_i, id_i).
p_i contains source UUID, original asset SHA-256, supporting observation ID,
producer coordinates/configuration and scope. Identity ordering is serialization
only, never a scientific tie-break. Duplicate-time observations remain distinct.
Ambiguous strength-to-EME linkage fails the input gate; no averaging of multiple
supporting strengths is silently introduced.

Preserve original numeric values and their exact binary representation where
applicable. Use exact rational producer coordinates where independently provided;
do not silently substitute a rounded frame timestamp for the original timestamp.
No binarization, strong-event filtering, rescaling, normalization, clipping,
imputation, pooling or detector change is specified. Weak measurable events remain.
Nonfinite or missing required values fail the input gate rather than being dropped.

## Candidate inventory versus selection

Existing AD-035 candidates retain all exact recurring consecutive producer-frame
intervals with at least two occurrences, including every supporting pair. This is
an existing discovery criterion, not an identifiability threshold. Applying that
rule to an EME projection requires demonstrated supporting-population equivalence;
the Core population must not silently be relabeled as EME.

For each supported T, record T/2 and 2T as explicit alias hypotheses, with their
actual support status. Arithmetic generation does not establish observational
support. Deduplicate equal durations without losing derivation provenance.
This finite alias inventory does not claim to exhaust all longer-period alternatives.

No duration is selected by minimum size, central position, recurrence count or
plausible BPM. Candidate trajectories cannot yet be constructed uniquely from
this inventory: local segmentation and correspondence rules remain unresolved.

## Structural obstruction (mathematical reasoning, not experimental result)

For a fixed T and phase phi, a lossless descriptive cycle representation is

  q_i = floor((t_i - phi)/T)
  r_i = t_i - phi - q_i*T
  W_q(T,phi) = ordered multiset of (r_i, s_i, id_i) for cycle q.

IDs preserve lineage and are excluded from comparison of signal-pattern values.
All phi in [0,T) remain admissible absent a scientifically justified restriction.
This representation adds no phase bins or tolerance.

For an ideal exactly repeated pattern of period T, concatenating two cycles
also produces an exactly repeated pattern of period 2T. Rotating the cycle origin
preserves periodicity. Thus a statistic that tests only equality of complete
repeated patterns cannot generally select a unique reference period AND origin.
The smallest fundamental repetition period, even when measurable, is not thereby
the desired pulse unit. This reasoning does not assert that every possible
strength statistic is phase-invariant or that strength can never be informative.

Selecting a maximum-strength phase or the shortest repeating word would add an
untested anchoring/level convention. Strict dominance of an unspecified statistic
does not solve this: the statistic itself encodes which organization is privileged.
Lexicographic ordering, first-event anchoring and numerical tie-breaking cannot
turn equivalent evidence into phase authority. Exact equality of detector strengths
also has no established repeatability guarantee for independently rendered audio.

## Exact unresolved decisions / stop

1. Level statistic: no selected mathematical functional establishes why a
   particular recurrent strength organization should privilege T over T/2 or 2T.
2. Phase statistic: no selected observable pattern feature has independently
   specified meaning as reference zero. A recurrent word alone has cyclic symmetry.
3. Approximate recurrence: no strength-error model or exact structural recurrence
   criterion validated for this measurement path has been established here.
4. Locality: window length, change-point rule, trajectory correspondence, cycle
   count through missing observations and restart authority remain unspecified.
5. Temporal scoring bounds: detector hop is sampling resolution, not localization
   accuracy. Symbolic-to-observed timing includes rendering/measurement behavior;
   no transferable error tolerance is established for the new challenge.

These are prerequisites to executable preregistration, not parameters allowed to
vary during execution. No arbitrary threshold is supplied. No universal
always-INDETERMINATE procedure is presented as a test of identifiable capability.

## Fixed abstention and representation requirements

Equal scientific evidence remains multiple alternatives. Serialization may sort
alternatives deterministically but must never select one. No arbitrary epsilon.
Unsupported level or phase remains INDETERMINATE, with separate statuses for each.
Unknown continuity/cycle count remains a gap or alternative branch, with no
interpolation. A segment restart requires future prospectively defined evidence,
not merely the next observed event.

InternalTemporalReference[k] must retain sequence/segment ID, ordered k, exact
timestamp, explicitly defined local-period interval, separate level/phase evidence,
contributing Drum IDs, source/asset provenance, construction authority, alternatives,
gaps, continuity and uncertainty status. Numeric confidence requires calibration.
Index means sequence position, not meter/downbeat. Inferred positions are not EME.
No concrete trajectory or reference position is generated by this design.

## Five-condition construction requirements (not asset-generation instructions)

A: nested timing recurrence with no distinguishing strength organization; hidden
authority must label the reference as ambiguous, not require one privileged answer.
B: a fixed recurrent strength organization with declared target level and explicit
competing aliases. Its exact strength word and anchor remain BLOCKED by decisions
1 and 2; the condition name cannot establish identifiability by assertion.
C: preserve B's cue identity while changing local spacing; exact transition schedule
and comparison rule must be fixed prospectively after locality is defined.
D: displace the cue's phase and include an earlier contextual Drum event; no first-
event anchoring. Exact offsets require the same phase and measurement specification.
E: add contextual/subdivision observations without changing the intended reference;
preserve all observations. No density-dependent retuning, strength filtering or
post-render adjustment is allowed. Full-word equality may fail under such additions;
this is a hypothesis risk, not permission to discard them.

One independently authored Drum-only family is sufficient in scope. Exact durations,
strength values, repetitions, contextual placements, gaps and renderer configuration
are deliberately not invented while selection/scoring rules remain unresolved.
Consequently these are requirements, not falsely labeled exact completed constructions.

## Hidden authority and freeze order

Before rendering, an independent creator must freeze the symbolic construction,
reference sequences (or ambiguity sets), target levels, phases, transitions, contextual
events, source identities, renderer/configuration and exact numeric scope/origin.
Keep condition identities and labels outside the inference input manifest.

Exact future WAV hashes cannot truthfully be known before generation. Use two stages:
(1) freeze construction and scoring specification before rendering;
(2) bind resulting WAV bytes/checksums and rendering records before inference.
Do not rerender based on detector/candidate results. Missing asset provenance stops.
Neither stage is executed here. Restrict inference to O and measurement authority;
freeze its canonical outputs and replay before opening hidden labels for scoring.
No source score, expected period/count, reference timestamp or condition label is input.

## Frozen high-level evaluation obligations

A: forced unique selection FAIL; retained ambiguity expected.
B: correct level must be identified; wrong alias or abstention means capability
not demonstrated. C: follow declared local change without unsupported alias switching.
D: independently supported phase required. E: reference identity survives density
change. Unsupported unique selection is failure, not repaired after scoring.
Any GT leakage or post-result tuning INVALIDATES the experiment.
Complete input/output lineage and canonical-identical replay are mandatory.
These obligations cannot be executed until the exact decision and scoring functions
above are prospectively specified. There is no experimental PASS/FAIL in this record.

## Scope, next decision and preservation

Minimum next design decision: nominate and justify an explicit observable pattern
functional and its phase anchor as a falsifiable controlled-reference convention,
separating that convention from musical beat identity; then establish its noise,
locality and scoring semantics independently of the five challenge outcomes.
PI approval of the broad cue does not itself supply those mathematical choices.

Even controlled identification would initially establish an internal reference and
neutral recurrence rate 60/T. Musical BPM requires separately justified beat-unit
semantics and generalization authority. Demucs Drum preservation remains 94.83% in
its accepted condition and does not transfer to a complete-observation claim.

The downstream H-VAL001-TEMPORAL-CELL-SINGLETON-01 file remains deferred, untouched,
SHA-256 6507a69c33247da87afe6f5445db0f4d475e7de8386c97b7b6b4fc61fda56ac8.
No accompaniment, Demucs, Bass recovery, JTD, BPM implementation, meter/downbeat
inference or visualization is performed. STOP for PI review; execution is unsafe
until the identified specification gaps are closed prospectively.
