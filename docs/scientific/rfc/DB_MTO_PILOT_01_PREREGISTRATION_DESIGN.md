# DB-MTO-PILOT-01 — Double Bass Multidimensional Timbre Observability Pilot

**Preregistration/design draft • 2026-09-10 • BLOCKED / NOT EXECUTION-READY**

## 1. Authority, question and stopping point

**Decision:** The PI accepted the provisional ontology and authorized preparation of this bounded preregistration/design. Identity Card v1.0 remains unfrozen. There is no authorization to implement measurements, generate calibration audio, record, execute, train, classify instruments or reopen BPM research.

**Observed Fact:** The authoritative [completeness/reconstruction audit](DOUBLE_BASS_IDENTITY_CARD_COMPLETENESS_RECONSTRUCTION_AUDIT.md) has SHA-256 `723eb1c92f4e4b25b9ae176a383142fd975177da2c97d2c1ddb2907cfff12907`. The preserved [Phase I report](DOUBLE_BASS_INSTRUMENT_IDENTITY_PHASE_I_RESEARCH.md) has SHA-256 `d11166600f7d910a5bd86a708132aaf4b9c4f49789e872506c36b2a0a8325d0c`. Both were verified before drafting. The accepted audit supplies the ontology and literature authority; this document does not conduct or claim additional literature research.

**Assumption — proposed experiment type:** Measurement characterization, not a confirmatory scientific PASS/FAIL test. Twenty repeated notes can describe the observed within-condition distribution; a scientifically justified repeatability tolerance or precision/power guarantee is not available. No such tolerance is invented here.

**Scientific question:** Can the selected multidimensional physical/acoustic observables be measured with sufficient repeatability and provenance under one bounded isolated Double-Bass capture condition to justify carrying them forward into later identity/invariance experiments?

Here, “sufficient” remains a later PI judgment against reported measurement uncertainty and the requirements of the next study. The pilot itself will characterize errors, variability and missingness. Completion does not automatically answer “yes.”

**Logical Inference — essential STOP:** The accepted evidence does not specify an independently qualified partial-tracking/residual estimator, calibrated uncertainty propagation, or a deployed independent contact/damping authority. Exact hardware geometry and personnel are also unknown. This draft records the supported design and explicit unresolved contracts. It is not a sealed, runnable preregistration. Work dependent on those contracts stops here; their scientific support cannot be fabricated from a plausible algorithm name.

The [Research Constitution](../JGA_SCIENTIFIC_RESEARCH_CONSTITUTION.md), [Knowledge Model](../foundations/JGA_KNOWLEDGE_MODEL.md), [F-030](../foundations/F-030_SCIENTIFIC_KNOWLEDGE_RECORD.md) and [SVP-001](../JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md) remain governing authorities. Throughout, unapproved protocol choices/equations are **Assumptions (design proposals)**, not validated observations or scientific Decisions. Repository checks are Observed Facts. Literature labels retain their meanings from the accepted audit.

| Mission-alignment item | Bounded position |
|---|---|
| Direct contribution | Prerequisite evidence for later defensible source-event attribution; no timing recovery claim now. |
| Missing evidence | Multidimensional observations with quantified measurement limits and within-condition variability. |
| Existing insufficiency | Audit Section 8 identifies coarse summaries/onset candidates, not qualified partial, residual or modulation trajectories. |
| Smallest proposed acquisition | One condition, twenty notes, five background controls, two simultaneous audio channels; separate calibration and authority contracts. |
| Architectural impact | None now. This is a research-record concept, not an approved runtime model. |
| Complexity | One design document. No new tool, dependency, dataset registration or experimental artifact. |

## 2. Coverage rules and complete ontology disposition

Each row has exactly one role:

- **MEASURED_IN_PILOT:** a planned acoustic endpoint, not an assertion that the implementation exists or that data have been obtained. Unresolved methods block its execution.
- **CONTROLLED_ONLY:** a prospectively fixed acquisition/performance condition; compliance is documented but its causal acoustic effect is not estimated.
- **PROVENANCE_ONLY:** supplied metadata or authority records, not audio-derived evidence.
- **NOT_OBSERVABLE_FROM_CAPTURE:** the specified causal quantity cannot be independently identified from the proposed pressure recordings.
- **DEFERRED_WITH_JUSTIFICATION:** intentionally outside this pilot, with the reason stated.

Parent roles describe the principal domain-level question. Explicit child roles govern the listed subdomains; a parent role is not inherited over an explicit child. Thus D01 may be controlled while a linked acoustic proxy is measured, without promoting the proxy to physical force. Each semicolon-separated item in a child row has that row's single role. Subdomain identifiers below are local traceability labels, not changes to the accepted ontology.

### 2.1 All sixteen parent domains

| Domain | Parent role | Pilot interpretation |
|---|---|---|
| D01 Excitation/contact | CONTROLLED_ONLY | Ordinary pluck condition; acoustic proxies belong to O03/O05, not a contact-force inversion. |
| D02 String mechanical state | CONTROLLED_ONLY | One unchanged string/setup; physical motion decomposition is unavailable. |
| D03 Boundary/coupling network | CONTROLLED_ONLY | Boundaries held fixed; no admittance or coupling estimate. |
| D04 Coupled resonator system | NOT_OBSERVABLE_FROM_CAPTURE | No independent structural/air modal authority. |
| D05 Radiation/spatial transfer | NOT_OBSERVABLE_FROM_CAPTURE | Two acquired views do not establish a radiation pattern or efficiency. |
| D06 F0/register evidence | MEASURED_IN_PILOT | O02 periodicity support; O03 qualified frequency/F0 alternatives. |
| D07 Complex partial structure/trajectories | MEASURED_IN_PILOT | O03; qualified harmonic departures and unresolved alternatives. |
| D08 Spectral-envelope structure | MEASURED_IN_PILOT | O04; acoustic envelope view, not a physical body filter. |
| D09 Observed transient/build-up | MEASURED_IN_PILOT | O01/O03/O05; waveform and spectral evolution. |
| D10 Whole-note envelope/release | MEASURED_IN_PILOT | O05; acoustic change, not physical damping time inferred as fact. |
| D11 Partial/band decay | MEASURED_IN_PILOT | O06; effective acoustic decay, not intrinsic loss. |
| D12 Residual/nonharmonic structure | MEASURED_IN_PILOT | O07; decomposition-relative evidence. |
| D13 Modulation/coherence | MEASURED_IN_PILOT | O08; continuous modulation evidence, subject to available support. |
| D14 Performance/mechanical history | CONTROLLED_ONLY | Fixed performance condition; acoustic level measured separately. |
| D15 Instrument/acquisition/environment context | PROVENANCE_ONLY | Factor/authority ledger; explicit controlled and measured children below. |
| D16 Human perceptual validation | DEFERRED_WITH_JUSTIFICATION | No human recognition or timbral judgment experiment. |

### 2.2 Every physical subdomain

| Child ID | Subdomain(s) | Exact role | Reason / destination |
|---|---|---|---|
| D01.a | Pluck location/region; direction | CONTROLLED_ONLY | One predeclared marked region/direction; actual specification blocks capture. |
| D01.b | Contact force; displacement; energy | NOT_OBSERVABLE_FROM_CAPTURE | No force/displacement instrumentation; do not infer from amplitude. |
| D01.c | Contact compliance; contact extent; finger/contact properties | NOT_OBSERVABLE_FROM_CAPTURE | Pressure audio does not uniquely identify these properties. |
| D01.d | Physical release/contact timing | PROVENANCE_ONLY | Independent evaluator-only annotation, pending authority contract. |
| D01.e | Acoustic excitation/release evidence | MEASURED_IN_PILOT | O03/O05, linked to D09; no duplicate observation or causal label. |
| D01.f | Bow friction; bow force/speed/location | DEFERRED_WITH_JUSTIFICATION | Arco absent from the selected articulation. |
| D01.g | Slap/percussive excitation; collision mechanism | DEFERRED_WITH_JUSTIFICATION | No intentional slap. Unexpected bursts retained by O07 without causal attribution. |
| D02.a | Speaking length; termination state | CONTROLLED_ONLY | Same open A string and setup; no stopping-position variation. |
| D02.b | Linear density; core/outer diameter/geometry; material; winding; Young's modulus | PROVENANCE_ONLY | Only independently supplied specifications, each with source/unknown flag; no new material measurements. |
| D02.c | Tension; effective stiffness; intrinsic loss | NOT_OBSERVABLE_FROM_CAPTURE | Acoustic frequency/decay does not uniquely identify these quantities. |
| D02.d | Two transverse polarizations; torsion; longitudinal coupling | NOT_OBSERVABLE_FROM_CAPTURE | No motion sensors; acoustic splitting is not motion-mode identification. |
| D02.e | Wear/age/use; maintenance | PROVENANCE_ONLY | Custodian log, unknown allowed; no aging law. |
| D02.f | Nonlinear mechanical regime; amplitude-dependent tension | NOT_OBSERVABLE_FROM_CAPTURE | Frequency drift alone does not identify its physical cause. |
| D03.a | Nut/open-finger boundary; afterlength; tailpiece; neck; endpin/floor support configuration | CONTROLLED_ONLY | No setup change; record fixed configuration. No claim all mechanical states are constant. |
| D03.b | Bridge admittance; directional transfer; energy-exchange paths | NOT_OBSERVABLE_FROM_CAPTURE | No calibrated force/velocity response. |
| D03.c | Other-string tuning; other-string damping state | CONTROLLED_ONLY | Same setup; other strings deliberately damped in all note attempts. |
| D03.d | Sympathetic paths; delayed other-string resonance | DEFERRED_WITH_JUSTIFICATION | Deliberate damping suppresses this experimental condition; possible leakage is not assigned to a string. |
| D04.a | Structural modes: frequency, damping/Q, mode shapes, coupling | NOT_OBSERVABLE_FROM_CAPTURE | Acoustic peaks and tails lack independent modal identity. |
| D04.b | Air-cavity modes: frequency, damping/Q, shape, structural coupling | NOT_OBSERVABLE_FROM_CAPTURE | No cavity/structural separation authority. |
| D04.c | Soundpost; bass bar; body configuration | PROVENANCE_ONLY | Existing setup description where known; no disassembly or modal inference. |
| D04.d | Resonator nonlinearities/model regime | NOT_OBSERVABLE_FROM_CAPTURE | Residual signal does not establish body nonlinearity. |
| D05.a | Frequency/direction-dependent radiation transfer; radiation efficiency | NOT_OBSERVABLE_FROM_CAPTURE | No spatial array or source-force/radiation calibration. |
| D05.b | Orientation; microphone/listener distance and geometry | CONTROLLED_ONLY | Fixed marks and capture ledger; performer motion departures logged. No listening test. |
| D05.c | Near/far-field classification | PROVENANCE_ONLY | Known geometry documented; field-regime label remains unknown unless independently justified. |
| D05.d | Full spatial response / directivity reconstruction | DEFERRED_WITH_JUSTIFICATION | Separate controlled measurement required; not needed for the selected acoustic endpoints. |

### 2.3 Every acoustic, conditioning and perceptual subdomain

| Child ID | Subdomain(s) | Exact role | Reason / destination |
|---|---|---|---|
| D06.a | Periodicity support; F0 alternatives; first-partial presence; uncertainty | MEASURED_IN_PILOT | O02/O03; preserve alternatives and absence of support. |
| D06.b | Absolute Hz; pitch-relative indexing | MEASURED_IN_PILOT | O03/O04, conditional on supported F0; never force nominal A1 into the estimator. |
| D06.c | Nominal pitch/register label | CONTROLLED_ONLY | Open A1, nominal 55 Hz; hidden acquisition condition, not measurement authority. |
| D07.a | Frequency/amplitude trajectories; phase/time reference | MEASURED_IN_PILOT | O03 plus exact complex transform O01; STFT bins are not automatically partials. |
| D07.b | Inharmonicity; comb departures; frequency splitting | MEASURED_IN_PILOT | O03 continuous deviations/alternatives; no universal stiffness coefficient fit. |
| D07.c | Track support; gaps; competing assignments | MEASURED_IN_PILOT | O03 with explicit unresolved states; no gap-filling by musical expectation. |
| D08.a | Absolute-frequency envelope; pitch-relative envelope; irregularity | MEASURED_IN_PILOT | O04; interpolation is a stated observation convention, not a physical resonance estimate. |
| D08.b | Acoustic resonant-region candidates | MEASURED_IN_PILOT | O04 spectral maxima/support; no body/cavity labels. |
| D08.c | Centroid; slope; spread; rolloff scalar summaries | DEFERRED_WITH_JUSTIFICATION | Optional compressions would add little to the present trajectory question; full envelope retained. |
| D09.a | Waveform morphology; tonal/residual components; build-up | MEASURED_IN_PILOT | O01/O03/O05/O07, preserving their shared provenance. |
| D09.b | Band/partial onset distributions | MEASURED_IN_PILOT | O05 continuous rise/support curves; discrete onset times blocked until qualified. |
| D09.c | Separate string/body transient attribution | NOT_OBSERVABLE_FROM_CAPTURE | No independent decomposition of physical causes. |
| D10.a | Attack; decay; sustain if present; damping-transition shape; offsets; remaining tails | MEASURED_IN_PILOT | O05 curves; do not impose ADSR phases or forced offset times. |
| D11.a | Local partial/band decay slopes; curvature; fitted-model residuals | MEASURED_IN_PILOT | O06; estimator/time-scale choices remain blocked. |
| D11.b | Double-decay model selection | DEFERRED_WITH_JUSTIFICATION | No justified change-point/model-selection contract; preserve curves for a later preregistered comparison. |
| D12.a | Time-frequency residual; colored/impulsive structure; noise floor; decomposition error | MEASURED_IN_PILOT | O07 and O01 background evidence. |
| D12.b | Collision/friction candidate ownership | NOT_OBSERVABLE_FROM_CAPTURE | Bursts can be represented; their physical cause is not independently identified. |
| D13.a | AM/FM; beating-compatible structure; relative phase; cross-partial/band synchrony | MEASURED_IN_PILOT | O08; no forced coherent-source or beating-cause label. |
| D13.b | Full two-dimensional spectral-temporal modulation representation | DEFERRED_WITH_JUSTIFICATION | Requires additional axes/smoothing/uncertainty calibration; first retain full time-frequency evidence and local trajectories. |
| D14.a | Performer; articulation; string/position; nominal effort; damping action; no intentional vibrato | CONTROLLED_ONLY | One condition, not invariance. Actual force/effort remains unmeasured. |
| D14.b | Acoustic level | MEASURED_IN_PILOT | O05 in digital units; pascals/SPL only with independently qualified calibration. |
| D14.c | Prior-note/contact history; incidental events | PROVENANCE_ONLY | Custodian logs order and deviations; observer does not receive expected event times. |
| D14.d | Legato/transition-state effects | DEFERRED_WITH_JUSTIFICATION | Isolated repeated notes; no transition experiment. |
| D15.a | Individual bass; string-set/setup/session/performer identifiers | PROVENANCE_ONLY | Custodian provenance, withheld from blind measurement. |
| D15.b | Channel type; microphone/pickup choice; geometry; gain/filter/compression; room/support | CONTROLLED_ONLY | Fixed raw microphone chain; no pickup input; hardware bindings unresolved. |
| D15.c | Climate; actual hardware settings; calibration records; transformations | PROVENANCE_ONLY | Record independently; unknown values do not become inferred observations. |
| D15.d | Background/pre-onset/acquired-channel evidence | MEASURED_IN_PILOT | O01/O05; separate channels, no averaging or source-transfer inference. |
| D15.e | Factorial variation/invariance across any conditioning factor | DEFERRED_WITH_JUSTIFICATION | One-condition pilot cannot test it. |
| D16.a | Dissimilarity; brightness; noisiness; roughness judgments | DEFERRED_WITH_JUSTIFICATION | No perceptual task/participant authority. |
| D16.b | Recognition; human confidence/abstention; listener expertise | DEFERRED_WITH_JUSTIFICATION | Outside observability and explicitly unauthorized claims. |

### 2.4 Cross-cutting layers

| Layer | Role | Treatment |
|---|---|---|
| Provenance: asset/channel identity, transformations, methods/settings, units/timebase, authority | PROVENANCE_ONLY | Required for every endpoint, including failed/missing observations. |
| Uncertainty/missingness: support, resolution, background, censoring, conflicting fits, unavailable measurements | MEASURED_IN_PILOT | Recorded separately per endpoint; unknown uncertainty is explicit, not zero. |
| Invariance: factors tested, populations, held-out domains and counterexamples | DEFERRED_WITH_JUSTIFICATION | No invariance tested; attach scope restriction to every result. |

This inventory retains every conceptual subdomain named in audit Section 6 and its explicit completeness additions. Deferred/no-capture fields remain in the coverage ledger; they are not fabricated as zero-valued observations.

## 3. Capture design and unresolved acquisition bindings

**Assumption — fixed proposed sample design:** Twenty note attempts and five room-only control captures, all retained. Five consecutive blocks each contain four note attempts followed by one room-only capture. This fixed count is inherited from the earlier pilot scale; it supports descriptive characterization, not a guaranteed precision target. No optional stopping, best-take selection, or replacement until a desired result appears. A failed attempt reduces usable support; it does not trigger a replacement. More data require a prospective amendment/new series.

| Capture element | Exact proposed procedure | Unresolved binding / limit |
|---|---|---|
| Instrument/player | One real acoustic Double Bass, one player, one string set, one session | Actual identities and access/rights not supplied: B01. |
| Pitch/string/articulation | Open A string, nominal A1/55 Hz; ordinary pizzicato, no intentional vibrato/slap; other strings damped | Actual tuning documented before/after by custodian; not passed into frequency estimation. |
| Pluck condition | One marked region and declared direction/finger action, one nominal comfortable effort | Position relative to bridge, region width, direction and instructions must be sealed before capture: B01. No unsupported force constancy. |
| Audio | Two simultaneous raw microphone channels on a common clock, 48,000 samples/s, signed 24-bit PCM; no normalization, denoising, AGC, compression or post-EQ | Mic/interface IDs, response, gains, hardware filters and channel delay calibration: B01/B02. |
| Geometry | Fixed instrument/endpin/floor and mic positions/orientations throughout | Coordinates in a stated instrument-centered frame and permitted geometry uncertainty: B01. No invented distances. |
| File duration | Each attempt/control is 8 s = 384,000 samples/channel | A truncated or corrupt file is retained as a deviation, not padded to appear complete. |
| Performance cues | Twenty pluck-cue slots `1.50 + 0.05 i` seconds, i=0..19, assigned once each to note attempts by a custodian-sealed permutation; silent damping cue 4 s after each pluck cue; record through 8 s | Seal permutation procedure/seed and assignment before capture; keep assignment and cue traces evaluator-only (B06). Cues are instructions, not actual physical authority. |
| Background | First 1 s reserved prospectively for pre-onset background; five full room-only controls with player/setup present and no deliberate sound | Early/incidental sound can contaminate background. Preserve it and flag after independent review; do not silently select a quieter interval. |
| Decay/post-damping | Intended 4 s between cues and at least 1.55 s after the damping cue | Actual physical times define available free-decay/post-damping support at evaluation. Shorter-than-intended support is reported, not extrapolated. |
| Between captures | Fully damp strings, then at least 10 s after the previous file ends before the next starts | This is a procedural pause, not proof that room/mechanical energy is zero. Preserve background evidence. |
| Independent annotation | Synchronized non-audio contact/release and damping authority, preferably nonperturbing | Sensor/video, synchronization and annotation uncertainty unresolved: B03. No audio-onset detector can supply its own authority. |

The two channels are separate observations of one take, not forty independent notes. Their purpose is to reveal capture-view sensitivity and preserve a second acoustic projection. They are not mutual ground truth. One-microphone substitution changes the design and needs a prior amendment; this document does not silently permit it.

Every attempt receives an opaque identifier before analysis. Reorder files for delivery using a custodian-held permutation distinct from the cue assignment; preserve the original sequence only in the authority ledger. Supply whole files, not event-centered crops. The observer receives audio, sample format/timebase and anonymous channel mapping, not cue times, expected pitch, note/control labels, instrument/player names or physical annotations. Public protocol knowledge alone cannot enforce blindness; actual implementation/configuration and input access must be audited against these restrictions. The varied cue schedule reduces a fixed-time shortcut but never becomes event authority or permission to restrict measurements to expected cue slots.

## 4. Common mathematical and replay contract

All equations define proposed **acoustic observations**, not a timbral-identity formula. No code is provided or executed. The design distinguishes an exact mathematical target from an unqualified estimator.

### 4.1 Exact basic signal views

For channel c, let x_c[n] be the signed PCM integer divided by 2^23; retain original bytes separately. No detrending/normalization is applied to this base view. Sample time is t_n=n/F_s relative to file start. The calibrated acquisition clock error is additional to the nominal sample spacing; sample precision is not onset accuracy.

Proposed deterministic multiresolution transform:

`X_c,N[m,k] = sum(n=0..N-1) w_N[n] x_c[mH+n] exp(-i 2πkn/N)`

where `w_N[n] = 0.5 - 0.5 cos(2πn/N)`, `H=240` samples, and only complete frames are used. No zero-padding, implicit edge extension, resampling or centered-library padding. Store frame start/end plus center `(mH+(N-1)/2)/F_s`; frequency is `k F_s/N`. Keep complex coefficients and the exact phase convention (local frame-start reference). Do not compare phase values across different conventions as if interchangeable.

| View | N / duration | Hop | Bin spacing | Purpose and limit |
|---|---|---|---|---|
| Short | 960 / 20 ms | 5 ms | 50 Hz | Transient/local energy structure; not separate low-bass harmonics. |
| Long | 9,600 / 200 ms | 5 ms | 5 Hz | Candidate partial/envelope structure; no claim that 5-Hz spacing resolves two components 5 Hz apart. |
| Sensitivity | 7,680 / 160 ms | 5 ms | 6.25 Hz | Prespecified window-sensitivity view, not an independent replicate. |

These are proposed observation scales carried forward from Phase I, not validated bass-specific optima. Calibration may show they are insufficient. If so, stop and amend before real-note measurement; do not choose windows by the resulting bass trajectories. Effective resolution includes window response, duration, noise and signal nonstationarity, not just bin spacing.

Define `P[m,k]=|X[m,k]|²/sum(w²)` as a stated window-normalized power proxy, not pressure spectral density. Define windowed RMS `E_N[m]=sqrt(sum(w[n]² x[mH+n]²)/sum(w[n]²))`. No claim that these match existing whole-stem JGA magnitude-weighted descriptors.

### 4.2 Uncertainty has separate components

For each value/trajectory retain: timebase/geometry/calibration uncertainty from independent records; local background evidence; estimator uncertainty if independently characterized; resolution/support limits; between-method/window sensitivity; and between-take variability. These must not be collapsed into one confidence number. A window-sensitivity range is not a probability interval. Repeated natural plucks estimate performance-plus-acquisition variability, not measurement error alone.

No supplied evidence supports a particular noise distribution, confidence-interval construction or universal SNR threshold. Therefore no Gaussian error bar, percentage coverage, noise subtraction floor or binary resolvability cutoff is imposed. Calibration uncertainty is `UNKNOWN` until B02/B05 are resolved. Store continuous background-to-observation comparisons alongside values; uncertainty may remain unquantified, which prevents a fidelity claim.

### 4.3 Deterministic replay

Every endpoint requires raw asset hash/channel mapping; exact specification/configuration hash; code revision and environment/dependency/numerical-backend versions if later implemented; window/filter/estimator parameters; frame supports, units, ordering and boundary conventions; and full failure records. Deterministic algorithms must reproduce identical outputs under the same pinned environment, apart from separately excluded administrative timestamps. No tolerance silently substitutes for same-environment replay.

Any future randomized uncertainty method needs a fixed documented generator, seed, draws and ordering, approved before execution. None is selected here. Cross-platform floating-point equivalence is a different numerical qualification and remains blocked until its comparison contract is approved. Raw integer replay and measurement numerical stability must both be reported.

## 5. Measured endpoint specifications and essential gaps

The coverage role MEASURED_IN_PILOT identifies the intended endpoint set O01–O08. **It does not authorize filling an unresolved specification during execution.** All eight must have a sealed method/calibration contract before this multidimensional design can run. Exact basic views below are specified; unresolved higher-level estimators are explicitly not invented.

### O01 — Recorded waveform and complex time-frequency evidence

- **Input:** Each entire channel of every anonymous note/control file, unprocessed.
- **Representation/method:** x_c[n], X_c,N[m,k] and P from Section 4; direct specified finite sums/DFT convention, complete frames only.
- **Resolution:** Sample spacing 1/48,000 s; all three transform supports as specified. Independent clock accuracy remains B02.
- **Uncertainty/noise:** Preserve raw first-second and room-only power distributions, per channel; electronic/calibration floor separate from environmental variation. No assumption these controls are stationary throughout a note.
- **Missingness:** Corrupt/truncated samples, unavailable channel or frame-edge support become explicit missing ranges. No interpolation. Digital saturation is a capture-quality flag; analogue overload needs independent chain qualification.
- **Replay:** Section 4.3 plus PCM decoding, complex layout and transform scaling.
- **Status:** Mathematical observation defined; acquisition/calibration qualification pending. This is not a partial tracker or a source decomposition.

### O02 — Periodicity/F0-context evidence

- **Input:** Complete long and sensitivity frames of O01, each channel independently.
- **Representation:** For every integer lag `l=1..floor(N/2)`, normalized lag similarity `r(l)=sum(y[n]y[n+l])/sqrt(sum(y[n]²)sum(y[n+l]²))`, where `y[n]=w_N[n]x[mH+n]` and both sums use `n=0..N-l-1`. Store the full lag curve and frequency coordinate `F_s/l`, not only its largest peak. Zero denominator is missing/undefined.
- **Method/resolution:** Direct lag sums on specified frames; lag spacing one sample, nonuniform reciprocal-frequency spacing; 5-ms frame advance. This is periodicity support, not an unambiguous fundamental estimator.
- **Uncertainty/noise:** Background lag curves, window sensitivity, calibration on known missing-fundamental/inharmonic and noise examples. Do not convert r into an uncalibrated probability.
- **Missingness:** Weak/multiple similarities remain curves/alternatives. No nominal-55-Hz constraint; no “best peak” declared authoritative.
- **Replay:** Section 4.3 plus overlap/denominator convention above.
- **Essential gap:** Selecting a supported F0 alternative with quantified error, and fusing it with O03, has no qualified method/selection contract yet (B04/B05). Until resolved, only the lag-support curve is defined, not F0 truth or first-partial ownership.

### O03 — Complex partial trajectories and harmonic departures

- **Input:** O01 long/sensitivity views and original waveform; O02 support only. No nominal pitch, score, source label or hidden contact times.
- **Mathematical target:** For each supported component j, a time-local complex trajectory `z_j(t)=A_j(t) exp(i phi_j(t))`, with `f_j(t)=(1/2π)d phi_j(t)/dt` only where differentiable/phase support permits. Preserve candidate components not assigned to an integer harmonic. For each supported F0 alternative, retain `delta_jh(t)=f_j(t)-h F0(t)` in Hz and assignment alternatives. No fixed bass stiffness law or forced integer labeling.
- **Resolution:** Proposed long/sensitivity frame supports and 5-ms advance; interpolation does not add temporal/frequency resolving power. Short-view information may describe build-up but must not be presented as independently resolved bass partials.
- **Numerical method:** **UNRESOLVED B04:** peak/component estimation, joint fitting, phase convention conversion/unwrapping, track association, splitting/merging, derivative estimation and gaps. STFT coefficients alone are not this object. The accepted research supports the target, not a qualified JGA estimator.
- **Uncertainty/noise:** **UNRESOLVED B05:** independently benchmarked amplitude/frequency/phase errors and ambiguity under close partials, drift, decays and noise. Preserve multiple fits and continuous support rather than inventing a cutoff.
- **Missingness:** Unsupported F0/index, phase ambiguity, track gap, overlapping/unresolved components, censored tail and inadequate duration are distinct. Do not bridge gaps or initialize from hidden pitch.
- **Replay:** Section 4.3 plus deterministic association/tie-breaking, optimizer initialization/stopping and branch identifiers, once approved.
- **First-partial evidence:** Requires frequency evidence at the supported F0, not merely autocorrelation or the existence of higher harmonics. May remain unresolved.

### O04 — Spectral-envelope evolution

- **Input:** O01 power/complex spectra and, for partial-relative views, qualified O03 amplitudes/frequencies.
- **Mathematical target:** Preserve measured frequency/amplitude knots `(f_j(t), A_j(t))` and a declared acoustic interpolation `S(f,t)`. A proposed simple view is linear-amplitude piecewise-linear interpolation between supported neighboring knots, with no extrapolation outside them; retain unsmoothed spectral data alongside it. Store a conditional pitch-relative view `S(h F0(t),t)` for each supported F0 alternative. This interpolation is not the unique physical spectral envelope.
- **Irregularity view:** Interior-knot deviation from the line joining adjacent supported knots at that knot's frequency; store signed deviation in amplitude units and neighbor supports. Endpoints/absent neighbors are undefined. Do not invent a global irregularity score.
- **Resolution/method:** O03 long/sensitivity supports, piecewise-linear interpolation convention as above; frequency support is actual knot spacing, not a dense plotting grid. No invented resonance widths from interpolation maxima.
- **Uncertainty/noise:** Propagate knot/assignment uncertainty when qualified; retain alternate envelope views and background. **B04/B05 block knot selection and uncertainty**, including which gaps permit interpolation. Until fixed, store knots without filling ambiguous gaps.
- **Missingness:** No partial-relative view without supported F0; missing regions remain masked; spectrum maxima may be described acoustically but never as body/cavity modes.
- **Replay:** Section 4.3 plus exact knot sets/order, interpolation/gap decisions and units.

### O05 — Transient, temporal envelope and release evidence

- **Input:** Entire waveform and O01; qualified O03/O07 only for their explicitly derived partial/residual views.
- **Representation:** E_N[m] at short/long/sensitivity scales; per-bin P[m,k] and qualified A_j(t) build-up/decay. Preserve continuous curves through the entire capture, including pre-onset and post-damping portions. A basic envelope change is `(E_N[m+1]-E_N[m])/0.005` in digital-amplitude units/s with both frame supports attached.
- **Method/resolution:** Exact sums and adjacent-frame difference; 20/200/160-ms support and 5-ms sampling. This is a scale-specific envelope-change observation, not an instantaneous physical derivative or a 5-ms onset accuracy claim.
- **Uncertainty/noise:** Raw background distributions, timebase uncertainty, window sensitivity and digital/analogue overload qualification. No dB SPL or force conversion without independent calibration. No presumed noise-floor subtraction.
- **Missingness:** Retain apparent plateaus, multiple rises and tails. No forced sustain/ADSR segmentation. A threshold-defined acoustic onset/offset is **UNRESOLVED B04/B05** and is not required to draw the continuous curves.
- **Authority:** Only after output freeze may an evaluator compare acoustic build-up with independent physical release/damping intervals. Different physical/acoustic times are not automatically estimator errors.
- **Replay:** Section 4.3 plus all curve/difference supports. No authority-centered cropping during measurement.

### O06 — Partial-specific and band-supported decay

- **Input:** Supported O03 amplitude trajectories and O01/O05 frequency-local energy curves. Any frequency bands must be explicitly bound before use; no unstated filterbank.
- **Mathematical target:** Scale-specific local slope/curvature of `log A_j(t)` where A is positive and supported; if a local model `log A=a+b t` is used, preserve b, its time support and full residuals. b is an acoustic decay/growth rate, not intrinsic mechanical damping/Q. No artificial epsilon in log(0).
- **Resolution/numerical method:** Underlying long/sensitivity support and 5-ms samples are specified; **local-fit duration, weights, derivative/curvature operator and eligible support are UNRESOLVED B04**. Overlapping frames must not be counted as independent fit evidence.
- **Uncertainty/noise:** Required calibration on known decays, beating and truncation; tail censoring and room contribution explicit. Fit covariance requires qualified error assumptions (B05), not a default regression standard error.
- **Missingness:** Unsupported/zero amplitudes, too-short trajectories and noise-dominated ambiguous tails remain missing or ambiguous without forced decay constants.
- **Replay:** Section 4.3 plus fit windows/weights and support/eligibility decisions once sealed.
- **Optional future hypothesis:** The earlier common-envelope comparison is deferred until its model/decision contract is separately specified; nonparallel decay is not a prerequisite for pilot success.

### O07 — Residual/nonharmonic structure

- **Input:** Original channel and a qualified O03 synthesis of its estimated components.
- **Mathematical target:** `r_c[n]=x_c[n]-s_hat_c[n]`, with r's full waveform, the specified transforms X_r and power proxies P_r. Preserve r and fitting error independently of any colored/impulsive annotation. No assumption the residual is stochastic noise or a distinct source.
- **Numerical method:** **UNRESOLVED B04:** phase-continuous component synthesis, overlap/add, component count and fit model. Exact subtraction is defined only after s_hat is independently specified. Saving all residual makes closure tautological; closure is an integrity check, not physical decomposition validation.
- **Resolution:** Same sample/transform supports as O01; residual validity limited by estimator support. Frequency bins need no harmonic labels.
- **Uncertainty/noise:** Independently generated tonal-only, noise-only, mixed and transient controls must expose leaked tones/absorbed noise and model error (B05). Background recorded separately; no plugin reference.
- **Missingness:** No qualified synthesis means `METHOD_UNQUALIFIED`, not “all sound is residual noise.” Ambiguous components remain explicit in both fit and residual records.
- **Replay:** Section 4.3 plus exact synthesis conventions and component/phase lineage.

### O08 — Modulation and coherence

- **Input:** Qualified O03 amplitudes/frequencies/phases and O05/O07 curves; no hidden source or articulation labels.
- **Mathematical targets:** On each declared contiguous support W, amplitude fluctuation `a_j(t)=A_j(t)-mean_W(A_j)` and frequency fluctuation `v_j(t)=f_j(t)-mean_W(f_j)`; preserve these curves in their original units. A cross-trajectory lag-correlation view is normalized covariance over their common valid support. Constant/zero-variance trajectories yield undefined correlation, not perfect coherence. Relative phase is meaningful only for a declared pair and shared reference; raw phase differences are not source identity.
- **Numerical method/resolution:** **UNRESOLVED B04:** W, detrending beyond the specified centering, lag range, smoothing, phase-pair convention and any modulation-rate spectrum. Rate resolution depends on valid trajectory duration, not 5-ms sampling alone. Do not report magnitude-squared coherence from a single unsmoothed periodogram as a validated grouping measure.
- **Uncertainty/noise:** Controls must include independent/common AM/FM, close-frequency beating, stable tones, estimator-induced fluctuations and gaps (B05). Correlation is continuous evidence, not a coherent-source decision.
- **Missingness:** Too-short support, absent modulation, zero variance, unresolved tracks and unknown phase reference retained distinctly. No compulsory vibrato/beating label.
- **Replay:** Section 4.3 plus support masks and lag/normalization convention once sealed.

## 6. Literature and reconstruction provenance for every measured endpoint

Source IDs below refer to the **exact citations and access qualifications in accepted audit Section 14**. They are not new source claims. “Unknown” is preserved where direct support is absent. This table accompanies every endpoint via evidence_basis; it supplies no expected numerical output.

| Endpoint / measured domains | Scientific physical evidence | Psychoacoustic evidence | Research-system reconstruction | Vendor-documented practice |
|---|---|---|---|---|
| O01 / D09, D15, uncertainty | S4 pluck measurements; S10 acquired spatial variation | S14/S15 time-region information | R5 time-varying/residual representation | V2/V3 multiple capture perspectives |
| O02 / D06 | S3 string frequency context | S12 controlled-pitch timbre; no validation of this lag estimator | R1/R2 pitched string models | V1/V5 pitch-conditioned sampling |
| O03 / D06–D07; D01 acoustic proxy | S3/S4 nonideal string structure; S5/S6 motion qualifications | S13 spectral-temporal simplification; S14 build-up | R1/R3/R5 motion/trajectory modelling | V4 continuous string controls; no documented necessity of retained phase for bass recognition |
| O04 / D08 | S1/S4 excitation/transfer contributions | S11–S13 envelope/fine structure; S17 pitch/dynamic dependence | R5 time-varying spectra | V1/V5 layered samples; exact envelope estimator UNKNOWN |
| O05 / D09–D10, D14 level, D01 proxy | S4/S5 excitation/decay | S14/S15 temporal information | R1/R3 contact/release modelling | V1/V3/V5 attacks/releases |
| O06 / D11 | S4/S9 conditional acoustic decay | S13 amplitude-evolution changes; bass-specific necessity UNKNOWN | R2/R5 losses/trajectories | V6 piano decay modelling, explicitly adjacent-instrument evidence |
| O07 / D12 | S8 nonlinear contact, adjacent instruments | S16 spectral-temporal percepts; bass residual diagnosticity UNKNOWN | R5 sinusoidal/residual decomposition | V2/V3 finger/mechanical/release noise |
| O08 / D13 | S10 motion confounds; S22 beating/grouping context | S13/S16/S22 modulation-related results | R3/R5 time evolution | V4 vibrato/portamento; V6 piano beating |

For each entry, the bibliography's claim type remains SCIENTIFICALLY_ESTABLISHED, RESEARCH_SYSTEM_DOCUMENTED or VENDOR_DOCUMENTED as appropriate. The proposed measurement convention itself remains INFERRED_HYPOTHESIS/Assumption until qualified. Scientific motivation does not validate a numerical method. No plugin output, vendor label, sample library or perceptual resemblance is ground truth. Measurements must never be tuned to resemble a plugin.

## 7. Calibration, missingness and evaluation authority

### 7.1 Independent calibration prerequisites — not executed

**Assumption:** Before real-note measurement, a separately authored calibration specification must supply known frequency/amplitude/phase/decay/modulation signals, structured transients, noise and intentionally ambiguous cases. It must cover sample-clock and channel response limits, isolated/close/inharmonic components, incomplete duration and zero-input cases. The generator must not reuse the estimator's decomposition/trajectory code. Known mathematical signals validate numerical estimands, not bass identity or physical source causation.

**Unsupported essentials B02/B05:** Exact signal parameter grid, analog chain checks, independent generator/reference implementation, uncertainty truth/coverage and assessment tolerances are not provided by the accepted audit. They remain unfilled. No default threshold or simulated dataset is generated to bridge this gap. If calibration motivates method changes, revise and seal the protocol before observing real-note results; calibration-development data must not be represented as independent validation data.

### 7.2 Missingness and continuous evidence

Per observation, retain a value when it remains interpretable, plus independent status/reasons. Proposed status vocabulary: `AVAILABLE_WITH_SUPPORT`, `AMBIGUOUS_ALTERNATIVES`, `INSUFFICIENT_DURATION`, `FRAME_OUTSIDE_CAPTURE`, `CHANNEL_UNAVAILABLE`, `UNDEFINED_ZERO_DENOMINATOR`, `PHASE_REFERENCE_UNKNOWN`, `BACKGROUND_CONTAMINATED`, `CAPTURE_OVERLOAD`, `METHOD_UNQUALIFIED`, `UNCERTAINTY_UNQUALIFIED`, `NOT_IDENTIFIABLE_FROM_CAPTURE`.

Status does not act as an undeclared SNR gate. Below/near-background evidence is reported continuously unless an independently justified censoring rule has been sealed. A reason record must identify the operation/authority that produced it. Multiple reasons may accompany a value; they are distinct from the single ontology coverage role. Nonmeasured ontology fields remain in the coverage ledger, not in a fabricated numerical record.

### 7.3 Separation of authorities

| Authority | Responsibilities | Forbidden information flow |
|---|---|---|
| Capture custodian | Instruments, capture manifest/hash, calibration chain, exact configuration, take/control labels, sequence, sensor/video/cue traces and synchronization | No labels, nominal F0, actual contact times or curated crops supplied to measurement generation. |
| Measurement implementer/operator | Implements only the sealed method; consumes anonymous permitted audio and acquisition-format metadata; produces all endpoints/missingness and immutable output manifest | Cannot select expected notes/partials from custodian metadata or alter method after seeing evaluation. |
| Calibration/reference authority | Independently specifies known mathematical targets and chain qualification, before real-note measurements | Does not generate reference using the estimator under test or tune criteria to real bass outcomes. |
| Scoring/evaluator | After output hash freeze, joins hidden authority; evaluates timing support, calibration discrepancies, capture deviations, repeatability and unresolved evidence | Cannot rewrite measured trajectories or grant “correct” labels because they resemble the expected instrument. |

Actual people/roles and access boundaries are B03/B06. If one person must hold several roles, a documented separation/access procedure must be approved before execution; independence is not asserted merely by renaming files.

Human annotations, if used, are physical-event/support annotations only: contact disengagement and damping contact, each as an interval with clock/visibility uncertainty. Exact video frame convention, synchronization, reviewer count, disagreement treatment and occlusion rules are **UNRESOLVED B03**. No “sounds like bass,” ideal attack shape or perceptual recognition annotation enters measurement authority. Video cannot supply true acoustic partial amplitudes. A second microphone or agreement between two estimators is corroboration, not independent acoustic ground truth.

## 8. Repeatability and characterization outputs

**Assumption — fixed analysis plan:** Twenty attempted notes are the experimental units. Report all attempts, five controls, all channels and all endpoint availability. Adjacent frames, partials and channels are dependent views, not additional subjects. No sample-size expansion based on apparent stability.

For each endpoint, preserve all take trajectories in capture coordinates and their support/missingness masks. The evaluator may additionally plot them relative to the independent physical-release interval after output freeze; alignment uncertainty must remain visible. Do not use dynamic time warping, onset snapping, loudness matching or frequency normalization to hide natural variation. Any pitch-relative views retain original Hz/amplitude data.

For scalar coordinates or prespecified common-support trajectory samples, report available n, all values, median, range and order statistics. Define the empirical distribution explicitly as `F_N(z)=count(value<=z)/N` for the available takes at that coordinate; report unavailable count alongside it. Quartiles, if displayed, use the inverse empirical CDF with no interpolated quantile convention. These are descriptive summaries, not confidence intervals or proof that twenty samples characterize a population.

Do not select common support retrospectively to maximize agreement. Capture-relative fixed supports can be summarized now; the exact post-authority alignment/support rule for partial-based repeatability is blocked with B04/B06. Display later-time attrition and competing assignments. For rates/slopes whose endpoints differ, compare only declared matching supports, and show unmatched observations rather than discarding them.

Separate four reports: same-environment computational replay; independently calibrated numerical error/limitations; between-channel sensitivity; and between-take variability. The last contains performer and acquisition variation as well as any estimator error. No post-result repeatability cutoff, combined timbre vector, weighted score, accuracy percentage or universal PASS label is allowed.

Possible outcomes are informative: unstable estimates despite stable calibration; model ambiguity; inadequate duration; persistent capture contamination; no supported modulation; or high natural take variability. A successful measurement-characterization pilot may reveal that an endpoint should not be carried forward. A favorable result is not predetermined.

## 9. Proposed neutral observation record

**Assumption — research serialization concept, not production schema:** Prefer `TimbreObservationRecord` with a pilot context reference; avoid embedding an acoustically recognized source class in the type name. This is consistent with Observation-before-Interpretation and the [Core–Domain boundary](../../architecture/CORE_DOMAIN_BOUNDARY.md), whose inspected document is marked Draft. Existing approved architecture remains authoritative; no new Core/Translation/Domain class is created.

| Field | Required meaning |
|---|---|
| observation_id; pilot_id | Stable opaque record ID and DB-MTO-PILOT-01 revision reference. |
| ontology_domain; subdomain; observable_type | Domain/child mapping and O01–O08 operation; shared derived views link rather than duplicate evidence. |
| capture_id; channel_id; source_provenance | Anonymous asset/channel hashes and lineage; externally attested source identity held separately. |
| time_support | Sample-index intervals, frame origins/centers, seconds/timebase reference, actual window support. |
| frequency_support | Hz bins, lag-to-frequency coordinates, component supports/alternatives; optional conditional harmonic index with parent F0 reference. |
| measured_value_or_trajectory; units | Raw numeric/complex arrays or immutable artifact references; no unlabelled dB or phase. |
| uncertainty | Separate calibration/timebase/background/estimator/sensitivity components and their methods; unknown explicitly allowed. |
| resolvability_status; reason_records | Continuous support plus missingness/ambiguity; no unqualified binary confidence. |
| capture_authority | Opaque reference available during measurement; full independently supplied metadata joined only after freeze. |
| measurement_authority | Specification/config/code/environment hashes, numerical method/version, permitted inputs and replay contract. |
| calibration_authority; evaluation_authority | Independent reference IDs; evaluation attachment separate from immutable observation. |
| conditioning_factors | Post-freeze authority attachment or opaque reference during generation; never an estimator prior. |
| evidence_basis | Physical/psychoacoustic/research-system/vendor source IDs, claim classifications and limits from Section 6. |
| scientific_status | Draft proposal now; later direct recording versus derived estimate versus unqualified method distinguished. Never “validated identity.” |
| parent_observation_ids; processing_history | Derived-view dependencies, transformations, support and failure lineage. |

Keep acoustic outputs, privileged capture metadata, and evaluation conclusions in separate immutable records joined by opaque identifiers. An observation cannot become source authority by carrying an externally supplied “Double Bass” label. No identity probability, musical function, event recovery or source-separation field is introduced.

## 10. Maximum claim and explicit exclusions

**Assumption — maximum favorable claim, only after resolving blockers and obtaining data:**

> Under the recorded one-instrument, one-player, one-string, one-pitch, one-articulation and acquisition condition, the specified research measurement path produced reproducible multidimensional acoustic observations with the reported calibration limitations, uncertainty, missingness and within-condition variability. Those results provide condition-bound evidence for deciding which observables warrant later identity/invariance experiments.

The claim is limited to the actual qualified endpoint subset, capture and method revision. Without independently qualified advanced endpoints, one cannot report success for this whole pilot by substituting RMS/STFT summaries. If production JGA is not the measured path, no production-JGA fidelity claim follows. With no prespecified repeatability tolerance, the report cannot say a scientific PASS threshold was met.

No claim is authorized for Double-Bass-class identity, classification, individual-instrument identification, perceptual equivalence, human recognition/expertness, invariance across any held-fixed factor, same-pitch discrimination, source attribution in mixtures, masked-event recovery, source separation, physical force/material/modal inference, or Identity Card v1.0 readiness. No musical timing function, BPM or BeatReference authority follows.

```text
TIMBRE OBSERVABILITY != DOUBLE-BASS IDENTITY
DOUBLE-BASS IDENTITY != EVENT RECOVERY
EVENT RECOVERY != SOURCE SEPARATION
```

Each transition requires an independently authorized experiment and independent evidence.

## 11. Execution blockers and PI review disposition

| Blocker | Essential unresolved contract | Required resolution before sealing/execution |
|---|---|---|
| B01 Capture binding | Real resources, pluck region/direction, mic/room geometry, fixed setup/gains and permissions | PI/custodian supplies and seals actual acquisition manifest; no invented hardware values. |
| B02 Acquisition metrology | Sample clock, channel response/delay, background/overload and any absolute acoustic calibration | Qualified independent capture/calibration procedure with stated units/uncertainty. Without it, limit digital-unit claims explicitly. |
| B03 Independent physical authority | Personnel, sensor/video, synchronization, event definition, annotation/disagreement/occlusion uncertainty | Seal a noncircular authority procedure; cue times and audio detector outputs cannot substitute. |
| B04 Advanced numerical definitions | F0 selection, component tracking/phase, support/gaps, decay fits, synthesis/residual and modulation operators | Select and scientifically justify exact methods and parameters; accepted evidence motivates targets but supplies no approved estimator contract. |
| B05 Independent calibration/uncertainty | Parameter cases/reference generator, identifiability tests, uncertainty propagation and numerical assessment criteria | Complete separately authored calibration specification before implementation/execution; no post-bass-result tuning. |
| B06 Evaluation/replay contract | Actual operator/evaluator separation, supported-coordinate repeatability/alignment, deterministic artifact format and environment qualification | Seal access, evaluation and immutable replay requirements. Do not derive tolerances from observed outcomes. |
| B07 Scientific/operational approval | Characterization status, proposed fixed 20+5 schedule, endpoint scope and any amendments | PI approves a completed revision; separate authorization for implementation, calibration, capture and execution remains mandatory. |

**Decision requested for later PI review:** Resolve or commission resolution of B01–B06, and accept/revise characterization status and scope in B07. This draft deliberately stops before selecting unsupported advanced algorithms, sensors or tolerances. It does not ask the PI to approve an experiment whose essentials are silently unspecified.

**Execution-ready: NO.** The design deliverable is complete as a blocker-bearing preregistration draft; the preregistration is not complete enough to execute. No pilot was run and no observation, calibration result, training artifact or accepted evidence was created or modified.

**Observed Fact — document integrity:** The coverage ledger contains sixteen parent rows and fifty-five subdomain rows, each with exactly one coverage role, plus the three cross-cutting layers. Local document links resolve; both authoritative source hashes remain unchanged. These checks validate document integrity only, not the proposed measurements.

**STOP FOR PI REVIEW.**
