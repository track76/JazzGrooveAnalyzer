# Double Bass Identity Card — Completeness and Reconstruction Audit

**Research/design proposal • 2026-09-10 • STOP FOR PI REVIEW**

## 1. Decision brief and authority

**INFERRED_HYPOTHESIS — conclusion:** The proposed 18-domain card is a strong inventory of relevant phenomena, but is not ready to freeze as a validated Double-Bass-class identity representation. Its main deficiencies are mixed causal and observational levels, insufficient treatment of interacting mechanical states, and no empirical demonstration of sufficiency or class invariance. The revised ontology below is sufficiently developed for PI review and bounded observability-protocol design. It is not yet sufficient evidence for class recognition, attribution, or recovery.

**Recommended PI decision:** Approve preparation of a preregistration for the **Double Bass Multidimensional Timbre Observability Pilot**, using this ontology as a revisable research draft. Defer the v1.0 freeze and experimental execution until the measurement, authority, and acceptance contracts in Section 13 are resolved.

**Decision — existing authority:** The PI authorized a new research/design document, additional literature research, and static observability assessment. This does not authorize DB-ID-PILOT-01, its successor, implementation, model training, schema adoption, or alteration of accepted evidence. The [Phase I report](DOUBLE_BASS_INSTRUMENT_IDENTITY_PHASE_I_RESEARCH.md) remains preserved, with SHA-256 `d11166600f7d910a5bd86a708132aaf4b9c4f49789e872506c36b2a0a8325d0c`. This audit supplements it; it does not overwrite or retroactively amend it.

**Observed Fact — repository provenance:** Static inspection used HEAD `2856c95952ea078fb01d179c2f94e5cb6bd697e3` and the existing working tree. The [bootstrap](../../../artifacts/JGA_BOOTSTRAP.md) explicitly distinguishes prospective continuation authority from stale historical metadata. Pre-existing recording, output, and validation changes are outside this task. No audio, plugin, synthesis, classifier, training, or experimental run was performed.

The [Research Constitution](../JGA_SCIENTIFIC_RESEARCH_CONSTITUTION.md), [Knowledge Model](../foundations/JGA_KNOWLEDGE_MODEL.md), [F-030](../foundations/F-030_SCIENTIFIC_KNOWLEDGE_RECORD.md), [SVP-001](../JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md), and [Core–Domain boundary](../../architecture/CORE_DOMAIN_BOUNDARY.md) govern this proposal. Its mission contribution is conditional: faithful source evidence could support later event attribution. Existing onset and coarse-spectrum measurements cannot establish that contribution. The smallest next experiment addresses measurement fidelity; architectural impact now is zero and complexity is one document. Prior Bass-recovery limitations, AD-037/038/040, accepted periodicity evidence, and the BPM/BeatReference boundary remain unchanged.

## 2. Evidence rules, coverage, and limits

Every external finding and prospective scientific claim has one of the following statuses. Status attaches to the **claim**, not automatically to an entire paper or product:

| Required status | Meaning in this audit |
|---|---|
| SCIENTIFICALLY_ESTABLISHED | A bounded mechanism or empirical result supported by scientific literature; never a declaration of universal Double Bass identity or JGA success. Primary technical reports retain their non-journal qualification. |
| VENDOR_DOCUMENTED | An identified manufacturer documents a control, sampling practice, or implementation claim. Accuracy and perceptual necessity have not been independently verified here. |
| RESEARCH_SYSTEM_DOCUMENTED | A research publication or official research-system manual explicitly represents a mechanism. Model inclusion alone does not establish physical accuracy or perceptual necessity. |
| INFERRED_HYPOTHESIS | A proposed ontology, transfer from another instrument, measurement design, invariance expectation, or masking prediction requiring validation. |
| UNKNOWN | Available evidence does not resolve the claim or the implementation is undocumented/inaccessible. |

Repository findings are separately labelled **Observed Fact**, as required by the JGA Knowledge Model; they are not scientific validation. Inferences correspond to Logical Inference or Assumption there. Existing authority is a Decision; proposed PI decisions are not approved Decisions. In tables, `S`, `V`, `R`, `H`, and `U` abbreviate the five statuses above, respectively. A cell containing separate labelled claims does not promote one claim's status to another. All ontology/design tables are **H** unless a component statement is explicitly assigned another status.

**Observed Fact — audit method:** Searches and reference-following covered bass admittance and modes; stiff, wound, torsional and contacting strings; bow/pluck excitation; floor coupling and radiation; controlled timbre/resynthesis and recognition studies; pitch/dynamic variation and masking; Modalys, waveguide and nonlinear synthesis; and official bass, cello, electric-bass and piano manuals. Sources were checked on 2026-09-10 through publishers, institutional/author manuscripts, official technical documentation, and the preserved Phase I source audit. Bibliography entries identify access and study scope. No search-engine crawl date is used as a publication date.

This is a bounded topical audit, not a systematic review with exhaustive database exports, independent screening, or a meta-analysis. Priority went to direct bass research, controlled listening experiments, and documented implementations. Existing Phase I references are reused where they answer the question; new evidence addresses the completeness gaps. No vendor demos were assessed, and no independent ranking of product fidelity was performed. “High-fidelity reconstruction” denotes the systems' reconstruction objective, not an audited quality award.

**UNKNOWN — principal evidence gaps:** No source located in this audit establishes a Double Bass population signature after crossing instrument, string set, performer, pitch, effort, articulation, microphone, room, and session. No located result establishes JGA masked-event recovery or a bass-versus-cello/electric-bass/piano recognition bound. These are audit gaps, not claims that no relevant publication exists anywhere.

**INFERRED_HYPOTHESIS — operational meaning of “complete enough”:** Coverage of known mechanisms is only the first test. A future sufficiency claim requires showing, within a declared population and acquisition scope, that retaining the proposed evidence supports the specified recognition/attribution task and that meaningful omitted evidence does not explain systematic failures. Controlled cue removal and constrained resynthesis should test information loss, with human judgments and held-out source comparisons where relevant. Saving the original waveform or an unrestricted residual can reproduce a recording without explaining identity. No finite audit can prove universal completeness, and no single fidelity metric closes that gap.

## 3. Pillar A: physical completeness audit

### 3.1 Causes, observables, and percepts are different objects

**SCIENTIFICALLY_ESTABLISHED:** Bass bridge admittance is a force-to-velocity response, whereas a microphone records pressure after radiation and propagation. Those are different measurements [S1, S2]. **INFERRED_HYPOTHESIS:** A future card should link these measurements, not substitute one for the other. A spectral peak alone cannot identify a body mode, string material, plucking force, or another string's contribution.

The following causal chain is a conceptual dependency map, not an identity formula:

```text
gesture/contact + initial mechanical state
             ↕
string motion ↔ bridge/boundaries ↔ coupled body/air/other strings/support
                                      ↓
                               radiated pressure
                                      ↓
                        room/position/microphone/chain
                                      ↓
                            recorded observations
                                      ↓
                 separately tested perceptual/source judgments
```

The feedback arrows matter. A one-way source/filter approximation can be useful in specified regimes, but cannot automatically explain coupled damping or nonlinear contact.

### 3.2 Detailed physical findings and gaps

| Mechanism audited | Finding, status, and evidence | Card implication / limitation |
|---|---|---|
| Length, tension, linear density | **S:** These jointly govern the ideal string's frequency scale; stiffness and boundary choices alter that approximation [S3; R2]. | **H:** Preserve independently measured length and construction metadata. Identical F0 does not imply identical string parameters. |
| Diameter, material, winding, Young's modulus | **S:** Core stiffness and total mass must be distinguished for wound strings. The published stiff-string comparison includes a bass reference case but explicitly omits winding from its simulations [S3]. | **H:** Separate core/outer diameter, linear density, effective bending stiffness, material and winding. Do not infer one homogeneous Young's modulus from a bass recording. |
| Loss mechanisms | **S:** Frequency-dependent losses and termination coupling affect plucked-string decay; measured synthesis comparisons expose limitations of simplified losses [S4]. | **H:** Keep effective acoustic decay distinct from internal string damping, contact loss, radiation loss and room decay. |
| Two transverse polarizations | **S:** Plucked-string measurements show polarization-related complexity [S4]. **R:** Two-polarization bow/contact models explicitly represent both directions [R3]. | **H:** Add motion polarization and directional coupling as physical subdomains; one mono partial track cannot identify them uniquely. |
| Torsion | **S:** Bowed-string measurements show torsional motion coupled through bow friction; direct acoustic radiation of torsion can be weak [S5]. Direct bass work compares wound steel and gut behavior [S6]. | **H:** Retain torsion even when indirectly audible. Do not label every noninteger component a torsional resonance. |
| Longitudinal motion and geometric nonlinearity | **S:** Plucked-string synthesis/measurement research addresses additional motion and nonlinear components [S4]. | **H:** Retain amplitude-dependent tension, longitudinal/transverse interaction and departures from linear superposition. Bass-specific magnitude and perceptual relevance remain **U**. |
| Pluck position, direction, displacement and energy | **S:** Initial excitation and string response jointly shape a pluck [S4]. **R:** Modalys explicitly represents interacting objects, access positions and a force-controlled release [R1]. | **H:** Record contact location and direction separately from effort. Force, displacement and energy are related but not interchangeable measurements. |
| Finger/contact and release mechanics | **R:** Physical models can represent finite contact and detachment, rather than an instantaneous ideal impulse [R1, R3]. | **H:** Include contact compliance, extent, sliding and release history. Their bass-class diagnosticity is **U**. |
| Bow excitation | **S:** Nonlinear friction and onset establishment are part of bowed-string physics [S5, S7]. **R:** R3 includes bow, stopping finger and fingerboard interactions. | **H:** Separate arco excitation regimes from pizzicato; retain bow force/speed/location and establishment of periodic motion. |
| Slap and collisions | **S:** Contact simulations with physical comparisons support nonlinear string/fingerboard interaction in adjacent instruments, including electric bass [S8]. | **H:** Retain collision locations, repeated contacts and residual bursts. Acoustic Double Bass parameter transfer requires measurement. |
| Bridge and body transfer | **S:** Direct bass measurements resolve instrument-dependent input-admittance structure [S1]. | **H:** Keep complex transfer, direction and coupling losses. A universal fixed bass resonance band is unsupported. |
| Soundpost, bass bar and bridge-island interaction | **R:** Violin finite-element research explicitly studies their interacting effects [R4]. | **H:** Include them within structural/coupling parameters, not standalone identity scores. Specific bass effect sizes and separability from audio are **U**; violin frequency regions are not bass constants. |
| Nut, stopped finger, afterlength, tailpiece, neck and support | **S:** Boundary conditions matter to stiff-string models [S3]; endpin/floor interaction is directly measured for bass [S2]. | **H:** Add a boundary network with open/stopped state, afterlength and support configuration. Separate neck-specific bass attribution from the measured floor result. |
| Structural and cavity modes | **S:** Bass work supports modal/admittance structure and differing radiation efficiencies [S1]. | **H:** Treat structural and air motion as coupled subdomains. Store frequencies, damping/Q, mode shapes and coupling only when independently supported. |
| Resonator nonlinearities | **U:** This audit does not establish a universal nonlinear bass-body law or a normal-playing threshold. | **H:** Preserve model regime, amplitude dependence and unexplained residuals; do not assume body nonlinearity merely because bow/contact is nonlinear. |
| Cross-string and sympathetic response | **S:** Coupled-string decay is conditional, and double decay is not automatic [S9]. **V:** Piano reconstruction documents sympathetic string behavior [V6]. | **H:** Include other strings' tuning/damping state and delayed ringing. A bass ringing tail alone cannot prove which string produced it. |
| Radiation and position | **S:** Orchestral measurements show note- and motion-dependent directivity [S10]. | **H:** Preserve frequency-dependent spatial response and orientation. Two microphones can expose viewpoint sensitivity but cannot establish a full radiation pattern. |
| Near/far field and environment | **H:** Distance and direction must accompany acoustic comparisons; local pressure and a far-field radiation estimate are not interchangeable. Floor support belongs upstream as well as room propagation downstream [S2, S10]. | **H:** Use controlled spatial measurements for radiation claims; ordinary recordings retain only the acquired projections. |
| Age/wear and climate | **U:** No sufficiently controlled bass-string aging law or universal temperature/humidity correction was established here. | **H:** Record string age/use, maintenance, temperature and humidity when available. Do not make “old strings sound like X” an identity rule. |

**INFERRED_HYPOTHESIS — completeness consequence:** Winding, torsion, two-direction motion, contact state, and boundary/history deserve explicit subfields. They do not all deserve independent acoustic feature axes. A physically complete forward model can contain parameters that are neither perceptually necessary nor identifiable from an ordinary recording.

## 4. Pillar B: perceptual completeness audit

| Evidence/task | Bounded finding and status | Consequence for the card |
|---|---|---|
| Timbre spaces | **S:** Controlled scaling supports multiple shared dimensions plus sound-specific and listener-dependent contributions [S11, S12]. | **H:** No universal three-, five-, or eighteen-dimensional perceptual space should be assumed. |
| Equalized pitch/loudness | **S:** Synthetic-tone experiments isolate contributions of attack, centroid and spectral fine structure under controlled pitch/loudness conditions [S12]. | **H:** Timbre differences can remain when pitch is controlled, but this does not establish a four-instrument bass discrimination rule. |
| Resynthesis simplification | **S:** For seven tested instruments, changing spectral-envelope detail and time-varying normalized spectra was salient; effects of amplitude/frequency simplification depended on instrument [S13]. | **H:** Preserve individual partial evolution and fine structure before reducing them to summaries. No Double Bass was in that seven-instrument set. |
| Removed/truncated attack | **S:** Onset-region tonal build-up and rapidly varying transients make different contributions in an identification experiment [S14]. Whole-tone and onset-removed similarity also share useful information [S15]. | **H:** String and body “attacks” should not be treated as independently observed microphone components. Retain waveform, tonal build-up and residual time courses. |
| Spectral versus spectro-temporal cues | **S:** Perceptual tone ratings relate to spectral and temporal modulation structure [S16]. | **H:** Retain modulation across frequency and time, not just frame-to-frame scalar flux. |
| Pitch/dynamic dependence | **S:** A sustained-tone acoustic study finds envelope position/shape affected by F0, register and dynamic level [S17]. It is not a human constancy experiment. | **H:** Keep absolute-frequency and pitch-relative views; level normalization alone cannot remove playing-dynamic timbre. |
| Human constancy and expertise | **S:** Pitch-range recognition and timbre-sequence studies show task- and training-dependent constancy [S18, S19]. S13 found only a modest musician advantage in its resynthesis discrimination task. | **H:** No universal expert accuracy or octave limit transfers to bass. Separate bass experts, other musicians and non-musicians later. |
| Masking and grouping | **S:** Auditory filtering, onset asynchrony and simultaneous-source beating affect hearing/grouping in controlled tasks [S20–S22]. | **H:** Evidence can be locally obscured or ambiguously grouped; “harmonic” does not identify a source. |
| Instrument recognition in mixtures | **S:** A virtual-orchestral study reports instrument-identification behavior in controlled mixtures [S23]. | **H:** Mixture recognition is a relevant later benchmark, not event-recovery authority or a transferable bass accuracy figure. |

**SCIENTIFICALLY_ESTABLISHED — apparent disagreement:** S13 found spectral evolution salient in natural-tone resynthesis comparisons, while S12 found spectral flux less salient/context-dependent in its synthetic timbre-space manipulation. These are different stimuli, changes and tasks. Neither establishes that an arbitrary library's “spectral flux” is always diagnostic.

**INFERRED_HYPOTHESIS — required distinction:** The following are cause–observation–percept links to test, not synonyms:

| Physical cause candidate | Acoustic observable | Perceptual correlate to measure independently |
|---|---|---|
| Contact/release and energy transfer | Rise shape, band/partial build-up, residual burst | Abruptness, attack quality, source recognition |
| Excitation spectrum filtered by coupled resonators | Envelope position/shape, centroid, irregularity | Brightness and timbral dissimilarity |
| Modal loss and changing boundary state | Partial/band decay, curvature and release changes | Ringing/damped character, duration impressions |
| Friction/collision plus unmodelled signal | Structured residual and tonal/residual balance | Noisiness; residual energy alone is not perceived noise |
| Detuning, motion, nonlinear interaction | Frequency deviations, beating, AM/FM and cross-band modulation | Fluctuation, roughness, pitch clarity under specified conditions |

**UNKNOWN:** Direct bass-specific causal rankings of these percepts across dynamics, performers and recordings remain unresolved. A scalar brightness score cannot stand in for source identity. Absolute phase is not proposed as a stable perceptual label; retaining complex signal evidence permits later waveform/interference analysis without prematurely discarding it.

## 5. Pillar C: documented reconstruction systems

### 5.1 Research systems and technical implications

| System / source | Explicitly documented representation | Status | What it motivates; what remains unsupported |
|---|---|---|---|
| IRCAM Modalys bi-string, 3.7 [R1a] | Length, tension, density, radius, Young's modulus, constant/frequency loss, mode count, two transverse directions | RESEARCH_SYSTEM_DOCUMENTED | Retain physical string state and loss; no claim that this simple object fully models a wound bass string. |
| Modalys pluck connection, current manual [R1b] | Separate plucker/string accesses; initial positions; release-force limit; optional interaction weight; two-mass plucker example | RESEARCH_SYSTEM_DOCUMENTED | Release/contact matters to reconstruction. Example parameters are not measured bass-finger constants. |
| Modalys finite elements and resonance object [R1c–d] | Mesh/material/boundary-driven modes; alternatively imported frequency, amplitude and bandwidth data | RESEARCH_SYSTEM_DOCUMENTED | Separate a physical modal model from a fitted resonance description. The single-point resonance object has no spatial information. |
| Digital waveguides [R2] | Traveling waves, boundary interactions and signal-processing representations; loss/dispersion extensions | RESEARCH_SYSTEM_DOCUMENTED | Preserve propagation, losses and boundary state. A lossless one-dimensional string is a special case, not a complete bass. |
| Commuted synthesis [R2] | Under linear time-invariant assumptions, body filtering can be factored into excitation processing | RESEARCH_SYSTEM_DOCUMENTED | Convolution/resonance modelling is legitimate in bounded regimes. It does not generally replace bidirectional or nonlinear coupling. |
| Nonlinear bowed-string synthesis [R3] | Two polarizations, nonlinear contact/friction, bow hair, stopping finger and distributed fingerboard interaction; energy-based numerical treatment | RESEARCH_SYSTEM_DOCUMENTED | Add gesture and contact-state history. A stable numerical model is not proof of perceptual fidelity or bass-class discriminability. |
| Stiff-string model comparison [S3] | Euler–Bernoulli, shear and Timoshenko formulations compared for representative strings | RESEARCH_SYSTEM_DOCUMENTED | Record approximation regime and model discrepancy. More complex mechanics is not automatically necessary in every observation band. |
| Spectral modelling synthesis [R5] | Time-varying deterministic sinusoidal component plus stochastic residual | RESEARCH_SYSTEM_DOCUMENTED | Preserve partial trajectories and residual evolution; decomposition is not unique physical source separation. |
| Measured pluck/synthesis comparison [S4] | Physical parameterization checked against measured plucked-string transients | SCIENTIFICALLY_ESTABLISHED | Reconstruction errors are scientifically informative; successful matching of a recording still does not isolate class identity. |

### 5.2 Commercial systems: explicit documentation only

| Representative system | Documented findings | Evidence status | Unknown or bounded claims |
|---|---|---|---|
| VSL legacy Upright Bass [V1] | Patch-specific velocity layers/alternations; pizzicato and snap variants; release and performance articulations | VENDOR_DOCUMENTED | Counts are patch-specific. Continuous pluck-position modelling, physical sympathetic coupling and body convolution: **UNKNOWN**. |
| Ample Bass Upright [V2] | Product page lists 13 sampled articulations and neck/body/room microphones plus DI; older main-panel manual documents release/noise, string/position and vibrato controls | VENDOR_DOCUMENTED | String/fingering selection is not proof of plucking-location sampling. Current implementation of each legacy control and bass-specific resonance internals: **UNKNOWN**. |
| Spectrasonics Trilian acoustic/electric basses [V3] | Multichannel acoustic-bass sampling; documentation describes repeated takes by note/velocity, round-robin order, actual legato performances and release-noise samples | VENDOR_DOCUMENTED | Exact layer/take counts for each bass patch, physical sympathetic solver, body IR and continuous excitation model: **UNKNOWN**. |
| SWAM-S solo strings, including bass/cello [V4] | Manufacturer declares physical synthesis without prerecorded samples, waveguide basis, friction modelling and real-time bow/position/vibrato/pizzicato controls | VENDOR_DOCUMENTED | Exact equations, coupling topology, calibration, sympathetic-string coverage and solver details: **UNKNOWN**. No independent fidelity result is asserted. |
| VSL Solo Cello [V5] | Legacy VC_pizz lists three velocity layers and four alternations; other patches document secco/snap/col-legno and releases. Current solo-string documentation includes attack/release and transition options | VENDOR_DOCUMENTED | Legacy and current libraries are different documents, not one combined implementation. No inferred physical solver. |
| Pianoteq [V6] | Manufacturer documents hammer/string interaction, inharmonicity, partial decay, unison beating, sympathetic/duplex resonance, damper behavior, soundboard/radiation and microphone controls | VENDOR_DOCUMENTED | Exact numerical internals and comparative quality remain **UNKNOWN**. Vendor exclusivity claims about what only modelling can reproduce are not adopted. |

### 5.3 Coverage ledger for requested reconstruction dimensions

Each positive entry below is **VENDOR_DOCUMENTED** or **RESEARCH_SYSTEM_DOCUMENTED**, as indicated by its source class. “Unknown” means this audit did not verify the narrower claim; it does not mean the product lacks it.

| Requested dimension | Verified example and scope | Limit / hypothesis generated |
|---|---|---|
| Multisampling; pitch-dependent sound | V1, V3, V5 sample maps/takes | **H:** Maintain pitch-conditioned timbre rather than transpose one template. |
| Velocity/dynamic layers | V1, V3, V5 | **H:** Playing dynamics change sound; MIDI velocity is a control, not an acoustic unit. |
| Round robin / random variation | V3 explicitly describes different takes and ordering | **H:** Repetition variability belongs in distributions. It is not class evidence by itself. |
| Releases and decay | V1, V3, V6 | **H:** Keep release events separate from an arbitrary synthesizer ADSR parameter. |
| Attack variation; pizzicato variants | V1, V5; contact-controlled excitation in R1 | **H:** Attack is a family of time courses, not one scalar. |
| Articulations and transitions | V2, V3, V4, V5 | **H:** Add gesture/state history and transition provenance. |
| Plucking-position variation | R1's access-based excitation; V4 explicitly documents bow position | Sampled plucking-position coverage in the audited commercial basses: **UNKNOWN**. Do not rename fret/string position as pluck position. |
| Finger/string/mechanical noise | V2, V3 | **H:** Retain structured residuals; noise can carry performer/session information too. |
| Sympathetic resonance | V6 explicitly; generic coupling in R1/R2 | Commercial acoustic-bass physical implementation: **UNKNOWN** in inspected documents. |
| Body resonance and radiation | R1 resonance/modal objects; V6 physical-model controls | **H:** Retain causal resonance and acquired pressure separately. |
| Resonance convolution | R2 commuted synthesis | A commercial bass body-IR implementation: **UNKNOWN**. Convolution reverb is not evidence of body convolution. |
| Physical and nonlinear modelling | R1–R3; V4 and V6 declarations | **H:** Add state, interaction and model-regime metadata, not a list of presumed vendor equations. |
| Hybrid sampling/modelling | R2's factored measured/filter/excitation approaches motivate hybrids; V3 explicitly combines samples with engine articulation/envelope processing | An exact physics-plus-sampling solver in V3 or V2: **UNKNOWN**. Sampling plus effects alone is not proof of physical hybrid modelling. |

### 5.4 Cross-instrument reconstruction comparison

**INFERRED_HYPOTHESIS:** Most synthesis requirements are generic. Partial decay, inharmonicity, release, sympathetic behavior and microvariation occur in several string instruments. Their presence cannot identify Double Bass.

| Instrument | Documented reconstruction emphasis | Candidate difference at matched nominal F0, requiring validation |
|---|---|---|
| Double Bass | Pizzicato/arco/contact behavior, multi-perspective acoustic capture, conditional body/string response | Joint distribution of excitation, envelope, partial evolution and acoustic resonator response |
| Cello | Closely related bowed/plucked and transition mechanisms | Body/envelope scale and string-dependent evolution may differ, but broad overlap is expected; it is a critical hard negative |
| Electric Bass | Finger/slap/legato/noise and pickup-oriented sampled sources | Pickup/amp transfer versus acoustic radiation may distinguish a capture, but must not become a recording-chain shortcut |
| Piano | Hammer excitation, unisons where present, dampers, sympathetic/duplex response and soundboard | Attack/decay/frequency patterns may differ; low piano notes need not contain three-string unisons |

**UNKNOWN:** None of these product comparisons supplies a controlled perceptual test that a dimension is necessary, sufficient, or unique to Double Bass. Realism, reconstruction error, within-class fidelity and class identification require different evaluation tasks.

## 6. Final proposed ontology: 16 parent domains, hierarchical subdomains

**INFERRED_HYPOTHESIS — final proposal for review:** Use linked physical, acoustic, conditioning and perceptual records. These are parent domains, not sixteen independent numerical coordinates. Shared underlying data should be referenced by derived views rather than duplicated or counted repeatedly.

| ID / layer | Proposed domain and mandatory conceptual subdomains | Justification |
|---|---|---|
| D01 Physical | **Excitation/contact:** pluck location/direction, force/displacement/energy where independently known, contact compliance/extent, release; bow friction/force/speed; collision/slap | Excitation and release alter modal input; physical controls are not uniquely recoverable from pressure [S4, S5; R1, R3]. |
| D02 Physical | **String mechanical state:** length, linear density, core/outer geometry, material/winding, tension, effective stiffness/loss; two transverse polarizations, torsion and longitudinal coupling; wear metadata | A harmonic string is an approximation; construction, motion type and model regime matter [S3–S6]. |
| D03 Physical | **Boundary and coupling network:** nut/finger, bridge admittance and directional transfer, afterlength/tailpiece, neck, endpin/floor, other-string tuning/damping and sympathetic paths | Coupling changes energy exchange and decay; its components are interacting, not independent filters [S1, S2, S9]. |
| D04 Physical | **Coupled resonator system:** structural and air-cavity subdomains; mode frequency, damping/Q, shape and coupling; soundpost/bass-bar/body configuration; model regime | Air and structural modes remain distinct physical contributions within a coupled system [S1; R1, R4]. |
| D05 Physical/acquisition interface | **Radiation/spatial transfer:** frequency/direction-dependent pressure transfer, efficiency, orientation and distance; near/far-field qualification | A microphone samples a spatial projection, not an intrinsic complete spectrum [S10]. |
| D06 Acoustic context | **F0 and register evidence:** estimated periodicity/F0 alternatives, observed first partial, uncertainty, absolute Hz and pitch-relative indexing | Context is needed to compare timbre while avoiding pitch as the class label [S12, S17]. |
| D07 Acoustic | **Complex partial structure and trajectories:** frequency, amplitude and retained phase/time reference; inharmonicity, splitting, departures from a harmonic comb; track support and gaps | Fine structure and time variation warrant retention; decomposition/physical ownership remain uncertain [S3, S13; R5]. |
| D08 Acoustic derived view | **Spectral-envelope structure:** absolute-frequency and pitch-relative envelopes, irregularity, resonant regions; centroid/slope/spread/rolloff only as summaries | Shape and fine structure affect perceptual judgments; a centroid is not an envelope [S11–S13, S17]. |
| D09 Acoustic | **Observed transient and build-up:** waveform morphology, tonal/residual components, band/partial onset distribution; optional independently supported string/body attribution | The recorded onset mixes causes; tonal build-up and fast transients need separate views [S14, S15]. |
| D10 Acoustic derived view | **Whole-note temporal envelope and release:** attack/decay/sustain if present, damping transition, offsets and remaining tails | A pizzicato note need not have stationary sustain; source decay and room tail differ [S4, S15]. |
| D11 Acoustic derived view | **Partial/band-specific damping evolution:** local slopes, curvature, double-decay candidates and fitted-model residuals | A common envelope can hide nonparallel evolution; acoustic decay is not intrinsic damping [S4, S9, S13]. |
| D12 Acoustic | **Residual/nonharmonic structure:** time-frequency residual, collisions/friction candidates, colored/impulsive content, noise floor and decomposition error | Reconstruction and contact studies require more than harmonics; residual is not automatically stochastic noise [S8; R5]. |
| D13 Acoustic derived view | **Modulation and coherence:** AM/FM, beating, cross-partial/band synchrony, spectral-temporal modulation; relative phase where justified | Modulation can affect percepts/grouping; interference and performer motion can imitate source modulation [S10, S16, S22]. |
| D14 Conditioning | **Performance and mechanical history:** performer, articulation, string/position, physical effort versus acoustic level, damping/vibrato, prior notes/contact and transition state | A note depends on how and from what state it was produced; history was insufficiently explicit in the flat list [R3; V1–V5]. |
| D15 Conditioning | **Instrument/acquisition/environment factorial context:** individual bass, string set, setup, session, channel type, mic/pickup, geometry, gain/filter/compression, room/support/climate | The same acoustic evidence can encode individual instrument or acquisition instead of class [S1, S2, S10, S17]. |
| D16 Perceptual validation | **Task-specific human response:** dissimilarity/brightness/noisiness/roughness judgments, recognition, confidence/abstention and listener expertise under specified controls | Perceptual diagnosticity cannot be declared from descriptor availability or synthesis realism [S11–S19]. |

**INFERRED_HYPOTHESIS — cross-cutting layers:**

- **Provenance:** raw asset and channel identity, transformation lineage, method/version/settings, external authority, units and timestamps. Distinguish externally supplied source labels from acoustically inferred hypotheses.
- **Uncertainty/missingness:** confidence support, time/frequency resolution, noise/censoring, conflicting fits and unavailable measurements. Use “not measured,” “not resolvable,” “below acquisition floor,” “ambiguous cause,” and “outside validated scope”; never replace missing evidence with zero.
- **Invariance:** tested conditioning factors, population and held-out domains, effect/uncertainty estimates and counterexamples. No field is marked source-invariant on theoretical grounds alone.

**INFERRED_HYPOTHESIS — storage principle:** A neutral evidence item needs phenomenon, observation or authority type, time/channel scope, conditioning, method, units, uncertainty and provenance. It may link competing physical explanations and later class-support hypotheses. `SOURCE_IDENTITY_EVIDENCE` is a conceptual output name only; it confers neither source-instance authority nor a musical role.

### Traceability from the original eighteen domains

| Original proposal | Disposition |
|---|---|
| 1 Excitation | Retain/expand as D01. |
| 2 F0 | Retain as D06 context, not a class determinant. |
| 3 String identity | Expand as D02 mechanical state; individual string-set identity also D15. |
| 4 Partials + 5 inharmonicity/microstructure | Merge as D07, retaining all subfields and model deviations. |
| 6 Spectral envelope | Retain as D08, explicitly derived from richer observations. |
| 7 String transient + 8 body transient | Merge into D09 observed transient; string/body cause remains optional independently supported annotation linked to D01–D04. |
| 9 Temporal envelope | Retain as D10, explicitly including damping/release. |
| 10 Partial decay | Retain as D11 linked to D07, avoiding duplicate independent evidence counts. |
| 11 Structural + 12 cavity resonances | Place as distinct children of D04 coupled resonator system; neither is discarded. |
| 13 Bridge/body transfer + 16 sympathetic resonance | Place as distinct paths within D03 boundary/coupling network. |
| 14 Noise | Retain/expand as D12 residual with model-error qualification. |
| 15 AM/FM/coherence | Retain/expand as D13 including spectro-temporal modulation and interference qualifications. |
| 17 Radiation | Retain as D05. |
| 18 Factorial conditioning | Split into D14 performance/history and D15 instrument/acquisition/environment. |
| Added | Explicit perceptual-response layer D16; polarization/torsion/longitudinal and nonlinear regime in D02; full boundary/history context in D03/D14; retained complex phase/time/channel support in D07. |
| Removed | No physical phenomenon. Removed assumptions of independent string/body transient observability, independent uncoupled air/body modes, and any implication of a flat additive identity vector. |

## 7. Convergence matrix

This is one joined matrix presented in two panels for readability; join on D01–D16. **No combined score or automatic inclusion vote is defined.** A reconstruction checkmark is not a perceptual necessity result. All expected invariance and masking entries are **INFERRED_HYPOTHESIS**, including when mechanism support is scientific.

### 7.1 Three pillars and current observability

Current-state codes expand exactly as follows: `NOW = OBSERVABLE_NOW`; `PART = PARTIALLY_OBSERVABLE`; `NEW = REQUIRES_NEW_REPRESENTATION`; `CTRL = REQUIRES_CONTROLLED_MEASUREMENT`; `NOAUDIO = UNOBSERVABLE_FROM_STANDARD_RECORDING`; `NV = NOT_YET_VALIDATED`. NOAUDIO refers to unique identification of the stated physical quantity from ordinary pressure audio, not absence of any acoustic effect. All proposed identity uses are NV.

| Domain | Physics support | Psychoacoustic support | Reconstruction support | Current JGA observability | Evidence status of proposed identity use |
|---|---|---|---|---|---|
| D01 | S: excitation/contact [S4, S5, S8] | S: onset information [S14]; U: unique mechanism recognition | R: R1/R3; V: V4 | PART for event candidates; CTRL/NOAUDIO for forces/contact | H; NV |
| D02 | S: stiffness/motion [S3–S6] | U: bass-specific material/torsion diagnosticity | R: R1–R3 | CTRL; NOAUDIO for unique material/tension inversion | H; NV |
| D03 | S: bass mobility/support; coupled decay [S1, S2, S9] | U: bass-class necessity of particular path | R: R1/R2; V: V6 | CTRL; NOAUDIO for full network inversion | H; NV |
| D04 | S: measured bass modes [S1] | U: universal bass modal signature | R: R1/R4 | CTRL; NEW for qualified mode records | H; NV |
| D05 | S: dynamic directivity [S10] | U: bass recognition benefit after control | V: V2/V6 | CTRL; NOAUDIO for full pattern from mono | H; NV |
| D06 | S: vibrating strings [S3] | S: controlled-pitch timbre studies [S12] | R: R1/R2; V: V1/V5 | NEW for supported F0 trajectories | H; NV |
| D07 | S: nonideal string spectra [S3, S4] | S: resynthesis discrimination [S13] | R: R5 | NEW | H; NV |
| D08 | S: excitation/transfer [S1, S4] | S: envelope/brightness studies [S11–S13] | R: R5; V: V6 | PART: global centroid/spread/rolloff; NEW: envelope | H; NV |
| D09 | S: excitation establishment [S5, S7] | S: onset manipulations [S14, S15] | R: R1/R3; V: V1/V5 | PART: derivative/onset times; NEW: morphology/build-up | H; NV |
| D10 | S: losses/contact [S4] | S: temporal attributes [S15] | V: V1/V3/V6 | PART: duration/RMS; NEW: time envelope | H; NV |
| D11 | S: conditional decay [S4, S9] | S: envelope simplification [S13] | R: R2/R5; V: V6 | NEW; CTRL to identify intrinsic losses | H; NV |
| D12 | S: contact phenomena [S8] | S: spectral-temporal percept relations [S16]; U: bass noise necessity | R: R5; V: V2/V3 | NEW; ZCR is not residual decomposition | H; NV |
| D13 | S: beating/motion [S10, S22] | S: modulation/grouping [S16, S22] | R: R5; V: V4/V6 | NEW | H; NV |
| D14 | S: dynamic/register dependence [S17] | S: task-dependent constancy [S18, S19] | R: R3; V: V1–V5 | CTRL; NEW for structured conditions/history | H; NV |
| D15 | S: instrument/support/spatial variation [S1, S2, S10] | U: complete bass nuisance-invariance result | V: V2/V3/V6 | PART: asset/provenance; CTRL/NEW: factorial context | H; NV |
| D16 | Physical cause must be linked, not equated | S: controlled human studies [S11–S19] | U: demo realism does not validate this layer | CTRL; NEW for linked listener records | H; NV |

### 7.2 Future measurement, invariance and masking

Masking labels are hypotheses about **target-attributable evidence**, not merely a visible feature in the mixture. None currently merits an unconditional LIKELY_ROBUST designation. Metadata may survive mixing unchanged without providing audible event evidence.

| Domain | Candidate future observable / controlled measurement | Expected invariance hypothesis | Masking robustness hypothesis and condition |
|---|---|---|---|
| D01 | Video/contact sensing for release/gesture; acoustic build-up as a qualified correlate | Primarily articulation/performer/effort dependent | UNKNOWN: external gesture authority is not recoverable mixture evidence. |
| D02 | Measured geometry/density/construction; controlled vibration/polarization tests; acoustic departures from a model | Some stability within one string/setup; poor candidate for universal class constants | UNKNOWN: weak indirect effects and nonunique inverse mapping. |
| D03 | Complex directional bridge admittance; controlled other-string damping; support comparisons | Instrument/setup/string-state dependent | CONDITIONALLY_OBSERVABLE: isolated tails or modulation may survive, but identifying the coupling path needs independent support. |
| D04 | Force-response modal tests, vibration/pressure measurements; mode shape and damping uncertainty | Relative within-instrument stability; modal frequencies vary across basses | CONDITIONALLY_OBSERVABLE: exposed resonance regions/tails may remain; excitation gaps and room modes confound attribution. |
| D05 | Calibrated spatial pressure ratios, orientation and multichannel transfer | Highly view- and frequency-dependent | CONDITIONALLY_OBSERVABLE: multiple calibrated channels may help; mono cannot reveal a missing spatial pattern. |
| D06 | F0 alternatives with uncertainty; observed partial frequency and periodicity support | Deliberately changes with pitch; not class-invariant | LIKELY_FRAGILE: equal-F0 overlap gives no ownership; missing fundamental alone does not imply absent target. |
| D07 | Supported amplitude/frequency/phase trajectories with split/merge/gap flags | Conditional trajectory families, not invariant values | CONDITIONALLY_OBSERVABLE: exposed partials or differing microtrajectories; exact common partials remain ambiguous. |
| D08 | Envelope versus Hz and harmonic index; irregularity and compact descriptors | Shape may generalize conditionally; register/dynamics/chain remain confounds | LIKELY_FRAGILE: mixture envelopes combine sources; partial spectral glimpses may still help. |
| D09 | Multiresolution waveform, band and partial build-up; residual bursts | Strong articulation/effort dependence | LIKELY_FRAGILE: simultaneous attacks obscure ownership; onset asynchrony can help. |
| D10 | Acoustic amplitude/band envelope and release intervals with noise-floor censoring | Effort, damping and room dependent | LIKELY_FRAGILE: mixture envelope is not a source envelope. |
| D11 | Local partial/band decay slopes and curvature; competing models and uncertainty | String/partial/coupling conditioned | CONDITIONALLY_OBSERVABLE: sustained exposed partials help; masks or beating can mimic decay change. |
| D12 | Residual time-frequency structure, tonal/residual ratios, burst timing and error bounds | Technique/performer/chain dependent | LIKELY_FRAGILE: low-energy noise is easily hidden or confused with another source. |
| D13 | AM/FM depth/rate, coherence across supported tracks, spectral-temporal modulation | Performer/motion/history dependent; relational cues potentially useful | CONDITIONALLY_OBSERVABLE: common evolution may support grouping; mixtures can manufacture beating/coherence. |
| D14 | Custodian-recorded articulation, effort, string/position and preceding-state log | A conditioning variable, not an invariant identity feature | UNKNOWN: known history is context, not proof of a current hidden event. |
| D15 | Capture/setup metadata and controlled channel/room changes; transformation lineage | Identifies nuisance factors to cross or hold out | UNKNOWN: metadata survives, but cannot establish acoustic target presence. |
| D16 | Blinded discrimination/naming and attribute ratings, expertise strata and abstention | Depends on task, listener and familiarity | UNKNOWN: bass-specific masked human performance must be measured. |

## 8. Current JGA observability: static implementation evidence

**Observed Fact:** The following code was inspected; code presence is not proof of runtime coverage or validated measurement fidelity.

| Current component | What it actually represents | Relevant card coverage / genuine gap |
|---|---|---|
| [SignalRepresentation](../../../src/jga/observation/signal_representation.py) | Samples, sample rate, duration | **OBSERVABLE_NOW:** acquired waveform/timebase. Preserving raw samples is not extracting D06–D13. |
| [BasicFeatureExtractor](../../../src/jga/source_understanding/basic_feature_extractor.py) | Whole-input duration/RMS/sign-crossing fraction; one magnitude FFT and magnitude-weighted centroid, bandwidth and 95% rolloff | **PARTIALLY_OBSERVABLE:** D08/D10 summaries. No tracked spectral envelope, partials or per-note evolution. Variable name `total_energy` does not change magnitude weighting into power weighting. |
| [BasicTransientDetector](../../../src/jga/dsp/transient_detector.py) | Absolute first difference threshold crossings, returned as times | **PARTIALLY_OBSERVABLE:** D09 event candidates. Not a physical onset authority, transient decomposition or source label. |
| [BasicOnsetDetector](../../../src/jga/dsp/onset_detector.py) and [candidate builder](../../../src/jga/engines/source_pulse_candidate_builder.py) | Onset candidates; builder uses onset strength | **PARTIALLY_OBSERVABLE:** candidate times/strength. No established string/body or source-specific attribution. |
| [BassClassifier](../../../src/jga/source_understanding/classifiers/bass_classifier.py) | Low centroid/rolloff rules; family BASS and `instrument=None` | **NOT_YET_VALIDATED** for Double Bass identity; not a physical-perceptual card. Heuristic confidence is not demonstrated calibration. |
| [AudioStem](../../../src/jga/core/audio_stem.py) | Source/provenance fields including asset hash and transformation provenance; compatibility fields can be unauthorized | **PARTIALLY_OBSERVABLE:** provenance foundation. Source-instance authority is not acoustic class recognition; no complete D14–D16 record. |

**INFERRED_HYPOTHESIS — genuinely missing representations:** uncertainty-bearing F0/partial tracks; multiresolution transient and spectral-envelope trajectories; per-partial decay and modulation; structured residuals with decomposition error; linked physical measurements and factorial capture history; and independently obtained perceptual records. Standard recordings cannot uniquely supply string material, Young's modulus, contact force, modal shapes or full directivity. These require external measurement/metadata and may remain unknown.

**Observed Fact:** A supplementary text search across `src/jga` for F0/partial tracking, common pitch estimators, STFT/spectrogram, MFCC, spectral flux/flatness, inharmonicity, Hilbert analysis, admittance and directivity found only the existing centroid/rolloff feature and rule references among those search terms. **UNKNOWN:** Search terms and static inspection do not establish that no related utility exists anywhere under another name. The matrix states the capabilities of the inspected, Phase-I-relevant paths; no new global runtime capability is assumed. No production changes are proposed for approval in this document.

## 9. Same-pitch identity and confound protection

**INFERRED_HYPOTHESIS:** The shortest useful four-way comparison must include real **Double Bass, Piano, Electric Bass and Cello**, at shared nominal fundamentals within their actual playable ranges. Do not use the initial A1 pilot note as the four-way condition: it is below the standard cello's lowest open string. A later common-range note such as D2 is a candidate, subject to instrument/setup verification. Use several shared pitches eventually; one matched note tests only that local condition.

At matched F0, D07–D13 may preserve differences in relative amplitudes, inharmonicity, envelope regions, attack build-up, partial decay, structured residual and modulation. D03–D05 may help explain those differences after controlled measurement. These are theoretical candidates, not demonstrated discriminators. Cello pizzicato and electric-bass fingerstyle are particularly important comparisons so the task does not reduce to bowed versus plucked versus struck articulation. Arco bass/cello need their own later comparison.

**INFERRED_HYPOTHESIS — required protections, not achieved protection:**

| Shortcut | Required design control before a class claim |
|---|---|
| Pitch/register | Shared measured F0 conditions, overlapping register strata, held-out pitches and both Hz/pitch-relative views. Do not pitch-shift recordings to manufacture the primary evidence. |
| Loudness versus effort | Independently record effort/dynamic condition and acoustic level; retain raw calibrated captures plus declared level-matched listening/analysis copies. Equal RMS does not ensure equal perceived loudness. |
| Individual bass or string set | Multiple basses and string sets with entire instruments held out; avoid all strings/instruments nested perfectly within one performer or chain. |
| Performer | Cross players and basses where feasible; hold out players; document any uncrossed combinations. |
| Microphone/room/session | Cross capture factors with classes; hold out whole sessions/chains/rooms. Simultaneous microphones of one performance stay in one statistical group. |
| Electric pickup shortcut | Declare whether the target class includes DI, amplified and acoustic capture. Compare capture strata and include controls that expose simple acoustic-versus-DI decisions. |
| Articulation/history | Match feasible articulations across instruments, preserve open/stopped and damping states, and test later transitions separately. |
| Sample-library fingerprints | Real captures are the primary authority; hold entire libraries/recording sessions out if synthetic material is used in an auxiliary analysis. |
| Data leakage | Split by independent instrument/player/session units before segmentation or augmentation. Keep source labels and event authority hidden from blind observation. |

**Conclusion — INFERRED_HYPOTHESIS:** The design specifies protections but has not demonstrated them. The isolated pilot controls nuisances locally; it cannot prove invariance to them. A one-session observation model can still encode that session perfectly. Class evidence requires later crossed sampling, held-out validation and counterexamples.

## 10. Smallest successor: Multidimensional Timbre Observability Pilot

**INFERRED_HYPOTHESIS — proposed identifier:** `DB-MTO-PILOT-01`, a successor concept, not an approved replacement preregistration. DB-ID-PILOT-01 remains unexecuted and unauthorized. Its partial-evolution question is useful but too narrow to establish multidimensional observability; retain that comparison as one endpoint within the successor.

### 10.1 Bounded question and acquisition concept

Can a future research measurement path faithfully preserve several independently justified acoustic domains in repeated isolated bass notes, with explicit measurement error and missingness, without requiring the physical causes or class label to be inferred?

**Smallest proposed acquisition:** One real acoustic bass, one performer, one documented string set, ordinary open-A1 pizzicato, no intentional vibrato, other strings deliberately damped, one fixed pluck region/direction and nominal effort. Preserve the Phase I scale: **20 repeated notes plus five room-only captures**. Each capture provisionally contains one second before excitation, four seconds of free decay, deliberate damping, and one second afterward. These timings and counts are logistical draft values, not thresholds, sufficient power claims, or musical timing authority.

Use simultaneous, unprocessed **two-microphone** captures at documented positions, provisionally 48 kHz/24 bit. The first channel is the primary observation; the second reveals viewpoint sensitivity and helps audit signal evidence, but is not an independent event authority or a full directivity measurement. Document channel response, gain, clipping/noise floor, relative delay, synchronization and geometry. If only one microphone is available, narrow spatial claims explicitly before preregistration.

A separate custodian obtains synchronized release/contact and damping authority from a suitable independent channel, such as time-calibrated high-frame-rate video or a validated contact/optical sensor. Instrumentation must not materially alter the pluck; any perturbation must be checked and documented. The independent channel's uncertainty must be compatible with the planned onset question. Supply anonymous whole captures to the observer, not ground-truth-centered crops. Keep labels, exact authority times and privileged sensor streams hidden until observation outputs are frozen.

**Limits deliberately retained:** D01–D05 physical causes are controlled/logged or unknown; this smallest pilot does not perform modal, torsional, material or full spatial identification. Other-string damping makes sympathetic behavior out of scope, not absent from the ontology. No listener experiment is bundled into the smallest acquisition. A separate mechanical or perceptual follow-up is needed if the PI requires those domains to PASS too.

### 10.2 Simultaneously assessed domains and references

| Endpoint family | Domains / observation | Independent check and limitation |
|---|---|---|
| Pitch/partial evidence | D06–D07: F0 alternatives, resolved partial amplitudes/frequencies, track support/gaps | Analytic calibration signals and a separately specified reference estimator; record agreement and shared failure risk, not “ground truth” from consensus. |
| Spectral structure | D08: time-varying envelope and irregularity in absolute/relative views | Compare with directly inspectable time-frequency data and known calibration spectra; test dependence on window and smoothing choices. |
| Transient and temporal evolution | D09–D10: waveform/band/partial build-up, envelope and damping transition | Hidden physical authority with uncertainty; acoustic onset delay relative to contact is a result, not automatically an error. |
| Partial decay | D11: local slopes/curvature and nonparallel evolution | Calibrated decay signals; compare flexible trajectories with a fixed spectrum multiplied by one common envelope. Nonparallel evolution is not required for every partial. |
| Residual structure | D12: tonal/residual evolution and transient residue | Known sinusoidal/noise calibration controls; held-out residual/closure assessment. Reconstructing input by saving all error is bookkeeping, not proof of a valid physical decomposition. |
| Modulation | D13: observable beating/AM/FM/coherence with resolution bounds | Known AM/FM and close-frequency controls; stable/single-tone controls expose invented modulation. Absence of measurable modulation is valid. |
| Context and reliability | D14–D15 and cross-cutting layers | Capture ledger, noise-only controls, two-channel sensitivity and repeated-note uncertainty; no inference of class invariance. |

**INFERRED_HYPOTHESIS — calibration and analysis design:** Future calibration stimuli are measurement checks, not synthetic Double Bass training data or event authority for real notes. They must cover resolvable and intentionally unresolved partials, noninteger components, decays, known modulation and noise. The tools that generate reference signals must be independent of the estimator under test sufficiently to expose shared assumptions. No such stimuli are generated in this audit.

Use multiresolution analysis; do not force one window to resolve both contact transients and low-F0 partial structure. Preserve the earlier pilot's short/long-window idea only as an initial sensitivity plan. Window lengths, smoothing, track assignment, censoring and eligible time regions must be chosen from the measurement target and calibration evidence before confirmatory evaluation. Zero-padding is not new resolving power. Silence, unresolvable tracks and unexpected nonharmonic components remain explicit outcomes.

There is no classifier and no identity formula. Future research implementation, calibration execution and acquisition each need authorization. If development data are used to choose estimators or tolerances, separate a fresh confirmatory capture set; the 20-note pilot cannot retrospectively become a held-out validation set.

### 10.3 PASS contract and scientific meaning

**INFERRED_HYPOTHESIS:** Do not freeze arbitrary numeric tolerances here. Before a formal PASS is possible, preregistration must define domain-specific estimands, accuracy/precision tolerances justified by independent calibration and the next scientific question, uncertainty coverage, eligible evidence, repeatability summaries, negative-control behavior and multiplicity treatment. Report each required endpoint separately; extra descriptors cannot compensate for a failed required domain. Use FAIL, INCONCLUSIVE or NOT_MEASURABLE where appropriate. A note's natural variability is not estimator error.

**If PASS, it would establish exactly this:** Under the recorded one-bass/one-player/one-string/one-pitch/one-articulation/capture conditions, the specified research path met its preregistered measurement-fidelity and uncertainty requirements for the designated acoustic domains and correctly handled the specified missing/negative controls. It could additionally establish condition-bound nonparallel partial evolution if that endpoint passes. The claim applies to the tested representation and acquisition domain, not automatically to production JGA.

**It would NOT establish:** Double-Bass-class recognition; discrimination from any other instrument; individual-bass identification; source invariance across pitch, dynamics, strings, players, instruments or rooms; perceptual necessity/sufficiency or expert equivalence; unique physical recovery of modes/materials/contact force; sympathetic or arco/slap coverage; simultaneous-source attribution; masking robustness; missed-event recovery; readiness to freeze a universal Identity Card; any musical function or BeatReference authority.

**INFERRED_HYPOTHESIS — interpretation:** This is a multidimensional **measurement/representation validation**, extending descriptor checks to trajectories, residuals and uncertainty. It does not test instrument identity itself. A later identity claim needs competing source classes and population controls; a later perceptual claim needs listeners or an independently validated perceptual assay.

## 11. Shortest defensible validation sequence

Every stage below is **INFERRED_HYPOTHESIS**, contingent on preceding evidence and separate PI authorization. Mechanism, acoustic observability, perceptual relevance and class attribution remain separate endpoints.

| Phase | Minimum scientific purpose | Gate and safeguards |
|---|---|---|
| I — Multidimensional isolated observability | DB-MTO-PILOT-01 and required calibration; optional separately approved mechanical/perceptual modules | Per-domain fidelity/uncertainty evidence; no class claim. |
| II — Within-instrument variation | Register/pitch, effort, strings/positions, damping, pizzicato variants, then arco/slap and transitions | Explain observed conditional changes and failure regions; preserve calibration and held-out takes. |
| III — Between-bass variation / class invariance | Cross real basses, players and string sets with capture factors; include listener work for claimed perceptual dimensions | Separate stable class candidates from individual/performer/chain effects. Within-bass-class consistency alone cannot establish specificity. |
| IV — Same-pitch cross-instrument discrimination | Bass versus piano, electric bass and cello at shared pitches and feasible matched articulations/levels | Hold out whole instruments/players/sessions and nuisance conditions; targeted cue-removal/resynthesis and human tasks test diagnosticity. |
| V — Simultaneous-source discrimination | Controlled independently captured sources, target present/absent, same/different F0, synchronized/asynchronous onsets | Test source attribution at matched false-attribution rates; independent mix authority, source/gain/phase provenance and abstention. |
| VI — Masked-event recovery | Increasing masker severity, missing onset cues and held-out combinations; compare frozen baseline with identity-assisted path | Hidden independent event authority; calibrated rejection, false attribution, unresolved evidence and independently adjudicated unobservability. |
| VII — Drum adaptation | Ride → Hi-Hat → Snare → Kick → Toms → other Cymbals | New physics/perception audit and observable design for each source; no automatic harmonic-string descriptor transfer. |

**INFERRED_HYPOTHESIS — efficient sequencing:** Plan eventual crossed acquisition metadata now, so Phase I files remain scientifically interpretable later. Do not expand the first experiment into a population classifier. Introduce perceptual cue ablations before asserting perceptual identity sufficiency; objective reconstruction error alone cannot replace them. Each gate may revise or reject domains.

## 12. Masked-event hypothesis, limits, and Drum boundary

**INFERRED_HYPOTHESIS:** Conditioned timbral evidence may improve attribution of some independently real bass events missed or ambiguous in the current onset path. The defensible comparison is incremental correct source-event attribution at a controlled false-attribution operating point, with a frozen baseline and identical permitted input. Source detection in a long excerpt is not event recovery.

**SCIENTIFICALLY_ESTABLISHED:** Auditory-filter overlap and grouping experiments support conditional perceptual masking/segregation, not automatic physical separation [S20–S22]. Harmonic/percussive separation is an orientation-based decomposition whose bass attacks can enter the percussive output [R6]. **INFERRED_HYPOTHESIS:** No HPSS component may be treated as a source-labelled bass or drum stem merely from that decomposition.

**INFERRED_HYPOTHESIS — identifiability limit:** At a shared time/frequency component, a microphone observes the combined complex contribution. Multiple source assignments can explain it; phase cancellation may reduce target evidence further. A matched timbral prior does not prove a new event occurred. Missing fundamental, exposed upper partials, onset asynchrony, source-specific evolution or spatial differences may help conditionally; exactly shared/obscured trajectories can remain undecidable. Separators can introduce artefacts and need independent attribution checks.

Future controlled testing must include:

- Target-present and target-absent trials, including isolated masker attacks, prior target tails, handling noise and plausible non-bass confusers.
- Same- and different-pitch overlap, common partials, relative phase/onset variation, and increasing frequency- and time-dependent masking severity. A single global target-to-masker level does not characterize all cue visibility.
- Independent isolated-source capture and event authority, held by a custodian; observer outputs frozen before evaluation. Neither score timing, expected groove, source filenames nor reference-channel event times enter the observer.
- Correct-source event matches, wrong-source matches, unsupported target candidates, duplicate detections, timing uncertainty, abstention and misses. Report false attributions per candidate and per unit time, and all authorized-event denominators.
- A separate **unresolved** category and independent, condition-specific **unobservability adjudication**. A system miss, failure of a listener, or low signal-to-masker ratio does not prove genuine unobservability. Physically removed target energy is a structural control; audibility and mathematical identifiability are different questions. Undecidable cases remain undecidable.

**UNKNOWN:** No domain in the masking matrix has a validated bass-event recovery benefit. An evidence-preserving card prepares this test through time-local support, uncertainty, provenance and competing explanations; it cannot guarantee its success.

**INFERRED_HYPOTHESIS — Drum adaptation:** Carry forward causal/observable/perceptual separation, crossed variability and independent authority. Replace string-specific mechanics with source-appropriate modal/contact behavior. Ride needs strike region, implement, energy, damping and nonlinear spectral evolution; Hi-Hat additionally needs openness, pedal state and inter-cymbal contact. Snare requires membrane/wire/cavity interactions; Kick/Toms require membrane/shell/cavity and damping; other cymbals require their own geometry/contact audit. Cymbal nonlinear research motivates this separation [S24]. Do not require integer partials or even a meaningful F0.

**Decision boundary:** Recognized Ride/Hi-Hat → timekeeping periodicity → candidate temporal reference → BeatReference/BPM remains a later, separately authorized research sequence. Nothing here begins it or infers musical function from timbre.

## 13. Unresolved questions and PI decisions before preregistration

**UNKNOWN — scientific questions:** Which conditional cue combinations distinguish the bass class after nuisance control? Which observations preserve perceptually diagnostic information rather than only reconstructing a session? How much additional value comes from body/air measurements, torsion, sympathetic response or spatial data? Can physical damping be separated adequately from room/coupling loss? Which nonlinearities matter in ordinary pizzicato? What is the required cross-register/effort/chain generalization scope? Can target-specific evidence survive same-pitch overlap at useful false-attribution rates? This audit supplies no numerical answers.

**INFERRED_HYPOTHESIS — decisions/blockers requiring explicit resolution before preregistration:**

1. **Scientific claim and ontology status:** Endorse the conditional source-evidence objective and revise/approve this draft hierarchy. Confirm that pilot success means acoustic observability, not identity or permission to freeze v1.0.
2. **Class and articulation boundary:** Define acoustic Double Bass membership and treatment of electric upright, acoustic bass guitar, DI/amplified/processed bass, extensions and nonstandard tuning. Confirm ordinary pizzicato first and separate arco/slap/transition coverage.
3. **Pilot scope and resources:** Choose the two-microphone core or explicitly narrowed alternative; confirm real bass/player/string access, room, capture rights and repeat count. Decide whether any physical-mode or listener module is essential now; if so it is an added experiment with its own question/resources.
4. **Independent authority:** Appoint custodian and evaluator; select synchronized contact/release/damping instrumentation, characterize perturbation and clock uncertainty, define what physically counts as an event and separate it from acoustic onset.
5. **Measurement contract:** Name required versus exploratory domains, reference methods, units, acoustic-level calibration, channel response, bandwidth/resolution, censoring, track eligibility, fitting and model-discrepancy rules. Force, intrinsic damping and modal identity require appropriate independent measurements.
6. **Acceptance and statistical contract:** Decide precision/effect goals from the intended inference and calibration evidence; define per-domain PASS/FAIL/INCONCLUSIVE/NOT_MEASURABLE, negative controls, uncertainty coverage, exclusions, denominators, multiplicity and stopping. No retrospective threshold selection from evaluation data.
7. **Development versus confirmatory separation:** Decide whether this is explicitly exploratory or a formal validation pilot. Specify independent calibration/development data and a fresh held-out set if choices are tuned; group repeated channels/segments by original event/session.
8. **Nuisance-control commitments:** Plan feasible crossing/holdouts for basses, performers, strings, pitch, effort, chain and room. Confirm common-range real bass/piano/electric-bass/cello access before later discrimination preregistration; the initial pilot cannot supply this authority.
9. **Perceptual claims:** Decide timing and task of human validation, participant expertise strata, stimulus controls, loudness matching and applicable consent/review requirements. Until then D16 is unmeasured, and no human-equivalence or perceptual-sufficiency claim is possible.
10. **Physical evidence access:** Decide whether detailed soundpost/bass-bar, age/wear, sympathetic and radiation claims are necessary to the pilot. If necessary, obtain the missing bass-specific evidence or controlled measurements; otherwise retain UNKNOWN rather than importing violin/vendor parameters.
11. **Future attribution contract:** Endorse the need for target-absent controls, abstention, false-attribution scoring and independent unobservability adjudication. Operational tolerances and masking schedules must be settled before Phases V–VI preregistration, not invented from the pilot's outcomes.
12. **Authorization and ownership:** Approve preregistration preparation only now; separately authorize any future research measurement implementation, calibration, acquisition or experiment. Keep source-instance provenance authority separate from acoustic class evidence and maintain the Observation-before-Interpretation firewall.

Items 1–7, 10 insofar as required for the chosen claims, and 12 block a formal Phase-I pilot preregistration. Items 8–9 require a documented scope/defer decision now and complete operational resolution before the relevant later studies. Item 11's principles should be preserved now; its detailed scoring/adjudication protocol blocks mixture/recovery preregistration. This distinction avoids making an isolated-note pilot wait for an entire future laboratory program.

**INFERRED_HYPOTHESIS — freeze assessment:** **Not scientifically ready to freeze Identity Card v1.0.** The ontology is a defensible working coverage model. Its dimensional sufficiency, redundancies in actual data, perceptual diagnosticity, invariance and mixture attribution are unvalidated. A PASS of DB-MTO-PILOT-01 would justify proceeding to variation studies and revising the representation; it would not close those gaps.

## 14. Source register and access notes

The references below are exact citations or explicitly versioned/undated official documentation. Scientific results remain restricted to their reported conditions. Full-text inspection means relevant text was inspected, not that every equation/figure was independently validated. Primary sources are preferred; adjacent-instrument transfer is labelled H. Bibliographic/access qualifications in the preserved Phase I report remain applicable to reused sources unless updated here.

### Scientific literature

- **S1.** Askenfelt, A. (1982). *Eigenmodes and tone quality of the double bass.* STL-QPSR, 23(4), 149–174. [KTH full text](https://www.speech.kth.se/qpsr/1982/1982_23_4_149-174.pdf). Direct bass measurements; primary technical report, peer-review status not established. Measured instruments are not a population identity template.
- **S2.** Guettler, K., Buen, A., & Askenfelt, A. (2008). *An in-depth analysis of the double bass-stage floor contact.* Proceedings of the Institute of Acoustics, 30, Part 3, 37–44. [Proceedings](https://www.ioa.org.uk/system/files/proceedings/k_guettler_a_buen_a_askenfelt_an_in-depth_analysis_of_the_double_bass-stage_floor_contact.pdf). Full text inspected in Phase I; direct support-coupling evidence, audience audibility qualified.
- **S3.** Ducceschi, M., & Bilbao, S. (2016). *Linear stiff string vibrations in musical acoustics: Assessment and comparison of models.* Journal of the Acoustical Society of America, 140(4), 2445–2454. [DOI](https://doi.org/10.1121/1.4962553); [author-hosted published article](https://www.mdphys.org/PDF/jasa_2016.pdf). Peer-reviewed; full text, Sections II–VII. The Edinburgh manuscript cover says 2445–2456 and omits “stiff” from its title; the published article resolves this bibliographic discrepancy. Wound strings are not modelled explicitly.
- **S4.** Woodhouse, J. (2004). *Plucked guitar transients: Comparison of measurements and synthesis.* Acta Acustica united with Acustica, 90(5), 945–965. [Author full text](https://euphonics.org/wp-content/uploads/2022/03/Guitar_II.pdf). Peer-reviewed measurement/synthesis comparison; relevant string, damping and model-discrepancy sections inspected in Phase I. Guitar-to-bass transfer is H.
- **S5.** Bavu, E., Smith, J., & Wolfe, J. (2005). *Torsional waves in a bowed string.* Acta Acustica united with Acustica, 91, 241–246. [Author full text](https://www.phys.unsw.edu.au/jw/reprints/Bavuetal.pdf). Peer-reviewed; summary, measurements and discussion inspected. Torsion/transverse behavior and limitations of acoustic inference.
- **S6.** Wollman, I., Smith, J., & Wolfe, J. (2010). *The low down on the double bass: Looking for the effects of torsional modes.* Proceedings of the International Symposium on Music Acoustics, Sydney and Katoomba, 25–31 August, six-page contribution. [Author full text](https://www.phys.unsw.edu.au/jw/reprints/WollmanISMA2010.pdf). Direct bass study; conference peer-review process not verified here. Steel/gut and bowed starting behavior, not bass-class recognition.
- **S7.** Woodhouse, J. (2014). *The acoustics of the violin: A review.* Reports on Progress in Physics, 77(11), 115901. [DOI](https://doi.org/10.1088/0034-4885/77/11/115901). Peer-reviewed review; abstract and bibliographic access. No detailed bass-specific claim rests solely on this review.
- **S8.** Issanchou, C., Acary, V., Pérignon, F., Touzé, C., & Le Carrou, J.-L. (2018). *Nonsmooth contact dynamics for the numerical simulation of collisions in musical string instruments.* Journal of the Acoustical Society of America, 143(5), 3195–3205. [DOI](https://doi.org/10.1121/1.5039740); [author text](https://www.lam.jussieu.fr/Membres/LeCarrou/Articles/A24_Issanchou_NonsmoothContactDynamics.pdf). Peer-reviewed; simulation/physical comparison in adjacent instruments, inspected in Phase I.
- **S9.** Woodhouse, J. (2021). *A necessary condition for double-decay envelopes in stringed instruments.* Journal of the Acoustical Society of America, 150(6), 4375–4384. [DOI](https://doi.org/10.1121/10.0009012). Peer-reviewed; abstract and author bibliography verified. Not direct bass-class evidence.
- **S10.** Ackermann, D., Brinkmann, F., & Weinzierl, S. (2024). *Musical instruments as dynamic sound sources.* Journal of the Acoustical Society of America, 155(4), 2302–2313. [DOI](https://doi.org/10.1121/10.0025463). Peer-reviewed; abstract and publisher-indexed text inspected in Phase I. Directivity/motion, not class recognition.
- **S11.** McAdams, S., Winsberg, S., Donnadieu, S., De Soete, G., & Krimphoff, J. (1995). *Perceptual scaling of synthesized musical timbres: Common dimensions, specificities, and latent subject classes.* Psychological Research, 58(3), 177–192. [DOI](https://doi.org/10.1007/BF00419633). Peer-reviewed; abstract and indexed author manuscript. Shared dimensions and listener variation, not a complete bass ontology.
- **S12.** Caclin, A., McAdams, S., Smith, B. K., & Winsberg, S. (2005). *Acoustic correlates of timbre space dimensions: A confirmatory study using synthetic tones.* Journal of the Acoustical Society of America, 118(1), 471–482. [DOI](https://doi.org/10.1121/1.1929229); [author text](https://www.mcgill.ca/mpcl/files/mpcl/caclin_2005_jasa_0.pdf). Peer-reviewed controlled experiments; full text accessed in Phase I.
- **S13.** McAdams, S., Beauchamp, J. W., & Meneguzzi, S. (1999). *Discrimination of musical instrument sounds resynthesized with simplified spectrotemporal parameters.* Journal of the Acoustical Society of America, 105(2, Pt. 1), 882–897. [DOI](https://doi.org/10.1121/1.426277); [author full text](https://www.mcgill.ca/mpcl/files/mpcl/mcadams_1999_jasa.pdf). Peer-reviewed; methods and conclusions inspected. Seven instruments, including violin but not Double Bass; quality/discrimination effects are not class-specific necessity.
- **S14.** Siedenburg, K. (2019). *Specifying the perceptual relevance of onset transients for musical instrument identification.* Journal of the Acoustical Society of America, 145(2), 1078–1087. [DOI](https://doi.org/10.1121/1.5091778). Peer-reviewed; abstract access. No effect-size or timing threshold adopted for JGA.
- **S15.** Iverson, P., & Krumhansl, C. L. (1993). *Isolating the dynamic attributes of musical timbre.* Journal of the Acoustical Society of America, 94(5), 2595–2603. [DOI](https://doi.org/10.1121/1.407371). Peer-reviewed; abstract access. Similarity task, not absolute naming.
- **S16.** Elliott, T. M., Hamilton, L. S., & Theunissen, F. E. (2013). *Acoustic structure of the five perceptual dimensions of timbre in orchestral instrument tones.* Journal of the Acoustical Society of America, 133(1), 389–404. [DOI](https://doi.org/10.1121/1.4770244); [article](https://pmc.ncbi.nlm.nih.gov/articles/PMC3548835/). Peer-reviewed; indexed full article inspected in Phase I, intermittent direct-access challenge.
- **S17.** Siedenburg, K., Jacobsen, S., & Reuter, C. (2021). *Spectral envelope position and shape in sustained musical instrument sounds.* Journal of the Acoustical Society of America, 149(6), 3715–3726. [DOI](https://doi.org/10.1121/10.0005088); [institutional record](https://ucrisportal.univie.ac.at/en/publications/spectral-envelope-position-and-shape-in-sustained-musical-instrum/); [author study repository](https://github.com/Music-Perception-and-Processing/spectral-envelope-study). Peer-reviewed acoustical/computational study; institutional abstract and indexed article text accessible; publisher direct retrieval failed. Its sampled sustained-tone corpus is not an independently crossed bass population or a human constancy experiment.
- **S18.** Steele, K. M., & Williams, A. K. (2006). *Is the bandwidth for timbre invariance only one octave?* Music Perception, 23(3), 215–220. [Institutional record](https://libres.uncg.edu/ir/listing.aspx?id=9224). Peer-reviewed; abstract and citation inspected in Phase I. Instrument/range/expertise conditions do not establish bass invariance.
- **S19.** Siedenburg, K., & McAdams, S. (2018). *Short-term recognition of timbre sequences: Music training, pitch variability, and timbral similarity.* Music Perception, 36(1), 24–39. [DOI](https://doi.org/10.1525/MP.2018.36.1.24); [author text](https://www.mcgill.ca/mpcl/files/mpcl/siedenburg_2018_muspercept.pdf). Peer-reviewed memory/sequence experiments; full text accessible in Phase I.
- **S20.** Glasberg, B. R., & Moore, B. C. J. (1990). *Derivation of auditory filter shapes from notched-noise data.* Hearing Research, 47(1–2), 103–138. [DOI](https://doi.org/10.1016/0378-5955(90)90170-T). Peer-reviewed; abstract access in Phase I. Perceptual masking method, not source-inversion authority.
- **S21.** Darwin, C. J., & Ciocca, V. (1992). *Grouping in pitch perception: Effects of onset asynchrony and ear of presentation of a mistuned component.* Journal of the Acoustical Society of America, 91(6), 3381–3390. [DOI](https://doi.org/10.1121/1.402828). Peer-reviewed; abstract access in Phase I. Complex-tone grouping, not bass recovery.
- **S22.** Culling, J. F., & Darwin, C. J. (1994). *Perceptual and computational separation of simultaneous vowels: Cues arising from low-frequency beating.* Journal of the Acoustical Society of America, 95(3), 1559–1569. [DOI](https://doi.org/10.1121/1.408543). Peer-reviewed; abstract access in Phase I. Adjacent source-segregation evidence only.
- **S23.** Jacobsen, S., Baril, F., Grimm, G., & Siedenburg, K. (2026). *Investigating instrument identification in a virtual orchestral scene.* Music Perception, advance article, 1–17, online July 29. [DOI](https://doi.org/10.1525/mp.2026.2702234). Peer-reviewed; publisher-indexed results verified in Phase I, direct full-text retrieval failed. Earlier [author deposit](https://doi.org/10.5281/zenodo.17208001) is a preprint; final and preprint versions are not silently interchangeable.
- **S24.** Chaigne, A., Touzé, C., & Thomas, O. (2005). *Nonlinear vibrations and chaos in gongs and cymbals.* Acoustical Science and Technology, 26(5), 403–409. [DOI](https://doi.org/10.1250/ast.26.403). Peer-reviewed; publisher-indexed text and author bibliography inspected in Phase I; full PDF retrieval timed out. Used to motivate a later distinct percussion audit.

### Research-system sources

- **R1a–d.** IRCAM, *Modalys documentation*: [bi-directional string, 3.7](https://support.ircam.fr/docs/Modalys/3.7/Objects/ObjectReference/object_string_bi.html); [pluck connection, current](https://support.ircam.fr/docs/Modalys/current/Connections/connection_pluck.html); [finite elements, beta documentation](https://support.ircam.fr/docs/Modalys/beta/Finite-Elements/Finite_Elements.html); [resonance model, 3.3](https://support.ircam.fr/docs/Modalys/3.3/co/object_point_modres.html). Official technical text inspected. Version labels are preserved; old/beta APIs are not asserted to be current. Claims are about explicit model dimensions, not software installation or acoustic validation.
- **R2.** Smith, J. O. III (2010). *Physical Audio Signal Processing.* W3K Publishing. Author's online text via [digital waveguide scheme](https://dsprelated.com/freebooks/pasp/Digital_Waveguide_DW_Scheme.html), [waveguide/FDTD equivalence](https://www.dsprelated.com/freebooks/pasp/Equivalence_Digital_Waveguide_Finite.html), and [commuted synthesis](https://www.dsprelated.com/freebooks/pasp/Commuted_Synthesis.html). Relevant technical sections inspected. Stanford host was robots-blocked; the book mirror was used. This is a technical monograph, not a Double Bass identification experiment.
- **R3.** Desvages, C., & Bilbao, S. (2016). *Two-polarisation physical model of bowed strings with nonlinear contact and friction forces, and application to gesture-based sound synthesis.* Applied Sciences, 6(5), 135. [DOI](https://doi.org/10.3390/app6050135); [institutional record](https://www.research.ed.ac.uk/en/publications/two-polarisation-physical-model-of-bowed-strings-with-nonlinear-c/). Peer-reviewed research model; publisher/institutional indexed abstract inspected. Direct article and institutional PDF retrieval failed; no undocumented algorithm details or quantitative validation result inferred.
- **R4.** Gough, C. (2017). *Influence of the bridge, island area, bass bar and soundpost on the acoustic modes of the violin.* Proceedings of the International Symposium on Musical Acoustics, Montreal, 18–22 June, paper 34. [Proceedings full text](https://isma2017.cirmmt.mcgill.ca/proceedings/pdf/ISMA_2017_paper_34.pdf). Explicitly labelled peer-reviewed paper; finite-element investigation. Bass transfer remains H.
- **R5.** Serra, X., & Smith, J. (1990). *Spectral modeling synthesis: A sound analysis/synthesis system based on a deterministic plus stochastic decomposition.* Computer Music Journal, 14(4), 12–24. [DOI](https://doi.org/10.2307/3680788); [author-group technical description](https://www.upf.edu/web/mtg/sms-tools). Peer-reviewed method; institutional description/reference inspected in Phase I.
- **R6.** FitzGerald, D. (2010). *Harmonic/percussive separation using median filtering.* Proceedings of the 13th International Conference on Digital Audio Effects, Graz, 6–10 September. [Proceedings](https://dafx10.iem.at/proceedings/papers/DerryFitzGerald_DAFx10_P15.pdf). Full text inspected in Phase I, including bass-attack example. Algorithmic component orientation is not source identity.

### Vendor documentation

- **V1.** Vienna Symphonic Library (2007). *Vienna Instruments Upright Bass — Patches, Matrices, Presets.* [Legacy manual](https://odl.vsl.co.at/cms-vsl/legacy-manuals/collections/vi_uprightbass_patch-matrix-preset.pdf). Official nine-page PDF; patch tables inspected. Historical implementation evidence only.
- **V2.** Ample Sound (undated). *Ample Bass Upright*: [product page](https://www.amplesound.net/en/pro-pd.asp?id=21) and [Main Panel Manual](https://www.amplesound.net/en/Main_Panel_Manual-ABU.pdf). Official product text and 13-page legacy PDF inspected; version correspondence unresolved. Generic Ample sample-cycle documentation was located but is not used to assign unverified current ABU-specific internals.
- **V3.** Spectrasonics (undated). [Trilian overview](https://www.spectrasonics.net/products/trilian/overview.php); official Omnisphere integration manual, [Round Robin](https://support.spectrasonics.net/manual/Omnisphere/system/misc/index.html) and [Special Articulations](https://support.spectrasonics.net/manual/Omnisphere/edit_page/oscillator/page07c.html). These sections explicitly discuss Trilian sounds. Technical text inspected; exact acoustic-bass patch counts not generalized.
- **V4.** Audio Modeling (2026-03-16). [*SWAM-S — Pure Physical Modeling Excellence*](https://audiomodeling.com/blog/swam-s-pure-physical-modeling-excellence); [Solo Strings release notes](https://kb.audiomodeling.com/support/solutions/articles/206000050990-swam-solo-strings-release-notes). Manufacturer declarations, not independent solver verification.
- **V5.** Vienna Symphonic Library (2012). [*Solo Strings I+II*, legacy manual](https://odl.vsl.co.at/cms-vsl/legacy-manuals/collections/vi_solostrings_1%2B2_manual_v1.pdf), cello patch tables, especially printed p. 76; and [Synchron Solo Strings documentation](https://www.vsl.co.at/instruments/synchron/solo-strings), undated current page. Indexed official manual/text inspected. Distinct product generations remain distinct.
- **V6.** Modartt (undated, accessed 2026-09-10). [Pianoteq features and modelling overview](https://www.modartt.com/pianoteq_features); [official user manual](https://www.modartt.com/user_manual?product=pianoteq). Technical descriptions/control sections inspected. Descriptive model claims retained; marketing superiority/exclusivity not adopted.

## 15. Review boundary

**Observed Fact:** This deliverable is a literature/design document and static code audit. No model was trained, production code changed, plugin evaluated, experimental audio generated, or pilot executed. The existing Phase I report and accepted scientific evidence are preserved.

**Observed Fact — document checks:** All sixteen domain IDs have ontology and both convergence-panel entries; local Markdown targets resolve and the document has no trailing-whitespace errors. The Phase I SHA-256 and repository HEAD match the baseline above. These are document-integrity checks, not scientific validation. This new report is the only file written for this audit; pre-existing working-tree changes remain outside its scope.

**Decision boundary: STOP FOR PI REVIEW.** Recommended action is preregistration preparation after the identified PI decisions, with the ontology still provisional. Neither the card nor any recovery capability is frozen or accepted by this report.
