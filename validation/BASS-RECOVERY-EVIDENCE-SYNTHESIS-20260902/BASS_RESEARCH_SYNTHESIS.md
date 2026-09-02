# Bass-Recovery / Bass-Observability Research Synthesis

Date: 2026-09-02

Evidence cutoff: `5d35d1306ac9cf519b8de2bf452076d31d4a7e6d`

Companion map: [EVIDENCE_MAP.md](EVIDENCE_MAP.md)

## Scope and epistemic status

This is a read-only synthesis of finalized repository evidence. No audio,
Ground Truth population, candidate stream or dense representation was reopened;
no statistic was recomputed. Statements below are marked as **established**
when directly supported by frozen results, **inference** when they integrate
several observations without proving causation, and **unresolved** where the
available authority cannot decide the question.

The current tree does not contain a separately named finalized
maximum-recoverable-evidence result or the standalone finalized CED-VAL-009
replication record. The frozen cross-dataset report is authoritative for the
CED-VAL-009 counts and effects that it serializes, but this synthesis does not
extend those claims.

## 1. What is established about why the Bass population decreases?

**Established:** the decrease is a reproducible end-to-end observation-system
effect. After frozen source separation and unchanged JGA observation, many
original-stem Bass EME no longer have corresponding separated-stem Bass EME.
It persists after deterministic Demucs execution and float-format variation,
changes with separator model and material, and is larger for Bass than for the
tested Drum control.

**Established:** separation/dynamics processing changes the signal presented
to the detector and changes the detector-native candidate population. Weak
residual signal is often present for compression-recovered observations;
compression also creates candidates, removes prior candidates, relocates local
peaks and changes within-cell competition. Population recovery can therefore
improve while temporal correspondence degrades.

**Not established:** a single causal explanation. The frozen evidence does not
separate acoustic masking in the mix, separator suppression/distortion,
detector threshold/maximality behavior, and competition among simultaneous
sources into independently identified causal contributions.

## 2. Dominant limitation

The evidence supports a **combination**, with different epistemic strengths:

- **Absence of measurable evidence — not supported as a universal dominant
  cause.** Harmonic, pitched, timbral and local-evolution measurements are often
  available at missed coordinates. Yet the direct-mix `NEITHER` audit found
  little Drum-independent attack evidence for its hardest population, so some
  regions remain weak or unavailable under particular representations.
- **Masking — unresolved.** Kick proximity was positively associated with
  preservation in two datasets, falsifying that specific negative-association
  hypothesis. It does not exclude masking by piano, ensemble energy or other
  sources.
- **Source-separation transformation — supported as an observed contributor,
  not an isolated cause.** Models yield different populations; compression and
  separation alter spectral/onset structure and candidate coordinates. The
  studies are end-to-end and do not provide a causal decomposition of the
  separator alone.
- **JGA observation/detection limitation — supported as an observed
  contributor, not a complete explanation.** Adaptive threshold, peak
  relocation, local maximality and wait/rank competition all participate, but
  no one mechanism or native strength measure supplied a prospective rule.
- **Source-attribution ambiguity — supported as the current prospective
  bottleneck.** Pitched candidates and spectral observables can correspond to
  missed Bass coordinates, but Rhodes/Piano and frozen non-event controls show
  comparable or stronger evidence. Event-blind timbre and local evolution both
  ended in attribution-indeterminate classifications.

**Inference:** the most defensible branch-level account is that separation and
mixture conditions transform already heterogeneous, sometimes weak evidence;
the current detector then samples that transformed field incompletely. The
remaining measurable evidence cannot be converted into Bass observations
because its source and timing are not independently identifiable. This is not
a quantified causal allocation.

## 3. Mechanisms falsified or not independently sustained

- Demucs random shift or output float depth as the main cause: not supported.
- A uniformly better tested Demucs model: not supported; response was
  model-dependent and mixed.
- Upward compression as a timing-safe recovery: falsified by degradation of
  every frozen timing bound despite population gain.
- A single dominant detector-native transition mechanism: not supported.
- Native onset strength as a prospective discriminator: not supported.
- A fixed spectral band / simple EQ explanation: not supported.
- Preservation of the original transient structure as the explanation for
  compression recovery: not supported.
- Kick-proximity masking as the tested negative association: falsified in
  direction on CED-VAL-005 and CED-VAL-006.
- RX11 as a superior bounded replacement for htdemucs_ft: not supported.
- A useful, source-specific event-blind pitched recovery rule: not supported
  across datasets; only partial/insufficient correspondence was obtained.
- Known-source Bass/Piano attack-timbre differences as a source-specific
  mixture observable: not supported by the event-blind negative control.
- Upper-partial harmonic strength as Bass-specific evidence: not supported;
  NEGATIVE medians were higher than both Bass populations.
- Adjacent-frame spectral-evolution correspondence as Bass attribution at
  missed coordinates: indeterminate, not positive.

## 4. Independent replication

The following observations replicated across independent datasets or an
independently frozen dataset:

1. Incomplete original-to-separated Bass observation preservation replicated
   on CED-VAL-005 and CED-VAL-006, although its magnitude differed.
2. The tested Kick association replicated in the opposite direction from the
   masking hypothesis: Kick-near Bass observations were more often preserved
   in both datasets.
3. Event-blind pitched scanning found temporal correspondences to missed Bass
   populations in CED-VAL-005 and CED-VAL-006, but usefulness/source-specificity
   gates did not replicate as sufficient.
4. PRESERVED observations had stronger/differentiated upper-partial harmonic
   structure than MISSED observations across CED-VAL-005, CED-VAL-006 and the
   serialized CED-VAL-009 population; CED-VAL-010 independently replicated the
   direction.
5. CED-VAL-010 BassMic secondarily reproduced four known-source BassDI-vs-Piano
   spectral-envelope directions, but other timbre dimensions were heterogeneous.

The CED-VAL-009 statement is limited to the frozen cross-dataset serialization;
the standalone record is unavailable in the current tree for a fuller audit.

## 5. Evidence specifically at MISSED Bass coordinates

- CED-VAL-005: 69/334 pitch-evaluable missed observations had compatible
  pitched mix evidence in the coordinate-conditioned study.
- Event-blind scans corresponded temporally to 127/436 missed observations in
  CED-VAL-006 and 98/356 in CED-VAL-005. Pitch compatibility among evaluable
  missed matches was 39.42% and 22.58%, respectively.
- Compression recovered 140 gross matches in CED-VAL-006; 125 had weak local
  residual level before compression. Net gain was 127 because 13 prior matches
  were lost.
- Across CED-VAL-005/006/009 and independently in CED-VAL-010, MISSED
  observations had weaker upper-partial structure than PRESERVED observations,
  not an absence of all structure.
- CED-VAL-010 mix representations yielded complete availability for all four
  attack-timbre measurements and signed local spectral evolution at 220/220
  MISSED coordinates.

These are coordinate correspondences or measurements. None alone validates a
new Bass event, physical onset or source identity.

## 6. Measurable but not source-specific evidence

The principal examples are harmonic partial structure, low-register pitched
candidates, attack centroid/bandwidth/flatness/high-low balance, and native
adjacent-frame spectral evolution. Their non-specificity is not hypothetical:

- CED-VAL-010 NEGATIVE harmonic medians exceeded both Bass populations.
- Event-blind attack-timbre MISSED-vs-NEGATIVE effects were null or opposite to
  the known-source Bass direction.
- Local signed-evolution correspondence did not distinguish MISSED from
  NEGATIVE; spectral-state correspondence was lower for MISSED.
- In CED-VAL-006, 85.04% of newly corresponding pitched candidates had some
  Rhodes support, including 46.46% Rhodes-dominant support.
- YourMT3 supplied temporal complementarity while labelling the source Electric
  Bass, which cannot be corrected to Double Bass by temporal coincidence.

## 7. What prevents prospective use?

Prospective use lacks four linked authorities:

1. a Ground-Truth-independent way to attribute overlapping measurable evidence
   to Double Bass rather than Piano/Rhodes/other sources;
2. a validated selection or abstention rule for competing candidates;
3. an independently justified decision threshold or prior that generalizes;
4. evidence that added observations preserve the timing distributions required
   by `RhythmSectionTimingProfile`.

The existing alternatives fail at least one of these: oracle separator unions
use original authority, compression damages timing, strength does not
discriminate adequately, pitched scans carry excessive/ambiguous candidates,
and timbre/evolution controls do not establish source specificity.

## 8. Production consequence

**No scientifically justified production change is available now.** A change
would require at least one of Ground-Truth-informed selection, an arbitrary or
unvalidated threshold, unsupported source attribution, acceptance of measured
timing degradation, or a premature change to Core/Translation/Domain authority.

The production consequence is therefore to retain the existing implementation
and its documented limitations. Validation-only representations and oracle
coverage quantities must not be promoted into `RhythmSectionTimingProfile`, a
Bass probability, a detector union or an architectural decision.

## 9. Maximum Defensible Observation boundary

**Yes—within the currently frozen CED material and currently authorized audio
representations, this branch has reached the Maximum Defensible Observation
boundary.** The work has progressed from population loss, through separator and
detector audits, to event-blind pitched, harmonic, timbral and local-evolution
representations with explicit negative controls. Further deterministic
reductions of the same spectra would not supply the missing independent source
authority and would risk retrospective feature search.

This is a boundary of present authority, not a claim that the physical problem
is impossible. The stop rule applies: **STOP this research branch until
genuinely new evidence or independent authority becomes available.** No next
experiment is selected.

## 10. Evidence that could reopen the problem

Reopening is scientifically justified only if it changes the authority or
mechanism, rather than re-encoding the same spectra. Examples include:

- a genuinely independent, provider-authoritative multitrack dataset with
  common-clock Double Bass, competing tonal sources and mix/separated outputs;
- JTD access, if its provenance and annotation authority support the required
  source-specific and temporal comparisons;
- materially improved source-separation technology frozen prospectively and
  evaluated without selecting models on Bass outcomes;
- independently justified temporal/source priors derived outside the current
  CED outcomes;
- controlled physical-acoustic recordings with common-clock excitation or
  source-presence authority, overlapping Bass/Piano conditions and negative
  controls;
- a genuinely independent evidence modality, such as instrument-isolated
  contact pickup, MIDI/performance action, or synchronized visual/string-action
  evidence, with explicit alignment and provenance.

Availability alone is insufficient. Any reopening must preregister how the new
authority resolves source attribution or timing and must preserve negative
controls, uncertainty and event-blind acquisition.

## Decision

### ESTABLISHED

- Bass EME population loss after the frozen separation-to-JGA path is real,
  deterministic under frozen execution, material-dependent and independently
  replicated.
- Separator/dynamics transformations and detector-native threshold/peak/
  competition behavior both alter the observed population.
- Some missed coordinates retain measurable pitched, harmonic, timbral or
  spectral-evolution evidence.
- Preservation is associated with stronger upper-partial structure across
  datasets.
- Current event-blind measurable evidence is not sufficiently source-specific.

### NOT ESTABLISHED

- A unique causal allocation among masking, separator transformation and JGA
  detection.
- Bass identity, physical onset or recovered Bass events from the new evidence.
- A threshold, classifier, composite score, source selector or timing-safe
  production recovery.
- Generalization beyond the frozen recordings and authorities.

### CLOSED / FALSIFIED

- Random-shift/bit-depth explanation; tested Kick-negative masking hypothesis;
  simple fixed-band EQ; transient-preservation explanation; RX11 superiority;
  upward compression as timing-safe recovery; native strength as selector;
  known-source attack timbre or upper-partial strength as sufficient
  source-specific mixture evidence.

### OPEN

- The causal proportions of separator transformation, ensemble masking and
  detector response.
- Whether genuinely independent source authority can make residual evidence
  prospectively attributable without harming timing.
- The standalone CED-VAL-009 and separately named maximum-recoverable-evidence
  authority gaps in the current validation tree.

### PRODUCTION CONSEQUENCE

No production or architecture change is authorized. Preserve current behavior
and limitations.

### STOP / CONTINUE

**STOP.** Do not initiate another Bass-recovery experiment from the current CED
spectral evidence. Continue only after genuinely new independent evidence,
authority, separation technology or modality is approved.
