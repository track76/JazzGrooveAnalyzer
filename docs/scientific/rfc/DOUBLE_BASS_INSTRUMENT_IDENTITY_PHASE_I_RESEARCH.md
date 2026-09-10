# Double Bass Instrument Identity — Phase I Research and Design

## 1. Status, authority, and scientific question

**Status: RESEARCH/DESIGN PROPOSAL — STOP FOR PI REVIEW.**

**Decision:** The PI authorized this new literature/design track in the session of 2026-09-10, including creation of a bounded repository document. Authorization covers research and proposals, not adoption of a scientific representation, architecture, implementation, training, or experimental execution. This document records that scope; it does not amend any governing decision.

**Observed Fact:** Repository inspection used HEAD `2856c95952ea078fb01d179c2f94e5cb6bd697e3`, with pre-existing working-tree changes. The certified [bootstrap](../../../artifacts/JGA_BOOTSTRAP.md) distinguishes its prospective continuation lineage from historical metadata. [Project State](../../JGA_PROJECT_STATE.md) preserves the previous Bass-recovery freeze. This report neither resumes that experiment branch nor changes its conclusions. The completed real-Drum work, AD-037/038/040, and accepted periodicity evidence remain outside this proposal.

The [Knowledge Model](../foundations/JGA_KNOWLEDGE_MODEL.md) governs the following labels throughout:

- **Observed Fact (OF):** directly inspected repository content or what an identified external publication actually reports. An external finding is not a JGA experimental result.
- **Logical Inference (LI):** a reasoned consequence of that evidence, with transfer limitations stated.
- **Assumption (A):** an untested hypothesis or proposed design choice. All proposed card fields, measurements, stages, and numerical experimental settings below have this status until PI approval.
- **Decision (D):** only existing approved authority, including this session's research-only scope.
- **Evidence Conflict:** incompatible authoritative project evidence. No new conflict requiring resolution was identified for this bounded document; external evidence gaps are explicitly retained.

The scientific sequence follows the [Research Constitution](../JGA_SCIENTIFIC_RESEARCH_CONSTITUTION.md), [Development Constitution](../../JGA_DEVELOPMENT_CONSTITUTION.md), [Observation Model](../JGA_OBSERVATION_MODEL.md), [Core–Domain boundary](../../architecture/CORE_DOMAIN_BOUNDARY.md), [SVP-001](../JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md), and [F-030](../foundations/F-030_SCIENTIFIC_KNOWLEDGE_RECORD.md).

### Mission alignment gate

| Required statement | Bounded research position |
|---|---|
| Scientific Question | Which physical and perceptual observations support Double Bass identity, and under which conditions do they survive changes of pitch, performance, instrument, and recording? |
| Direct Contribution to JGA Mission | LI: Source-attributable acoustic evidence could eventually improve the defensibility of timing-event attribution. This is a conditional connection, not demonstrated event recovery. |
| Missing Scientific Evidence | Repeatable Double Bass cue trajectories; population-level variability; perceptual diagnosticity; controlled same-pitch discrimination; event-specific evidence under masking. |
| Why Existing Evidence Is Insufficient | Existing onset evidence and coarse spectral summaries do not establish a physical-perceptual identity model. Prior Bass-recovery failure remains informative and unchanged. |
| Smallest Experiment Capable of Obtaining Missing Evidence | Section 13 proposes a one-pitch repeated-pizzicato observability pilot. It addresses only the first measurement gap. |
| Architectural Impact | None in Phase I. Future ownership and representation require separate evidence and approval. |
| Complexity Introduced | One research document; no runtime dependencies or permanent scientific data model. |

## 2. Literature audit and principal conclusions

**OF — audit provenance:** Sources were checked on 2026-09-10 through publisher records, author/institutional manuscripts, PubMed, proceedings, and official product documentation. Search families covered Double Bass bridge admittance/eigenmodes/radiation; plucked and bowed string transients/stiffness/damping/contact; timbre scaling and onset removal; pitch constancy and musician expertise; simultaneous harmonic sources/masking/streaming; sinusoidal-residual and modulation representations; and upright-bass sampling/modelling. Reference-following connected Double Bass work to general string physics and controlled listening studies.

This is a comprehensive topical audit, not an exhaustive systematic review with a reproducible database export or a claim that every eligible study was retrieved. References identify full-text, abstract-only, and bibliographic-only access. Full-text availability does not imply that every figure was independently reanalysed. No numerical result was recomputed. Vendor evidence is segregated in Section 9. Reviews and book chapters supply context; primary experiments carry the narrower empirical claims.

**LI — central conclusion:** A scientifically defensible identity proposal should preserve a *conditional family of spectro-temporal observations*, not a fixed spectrum or weighted identity formula. The current literature supports investigating excitation, resonator behaviour, partial evolution, noise, and perceptual cue combinations. It does not establish a recording-independent, universal Double Bass signature.

**OF/LI — strength of evidence:**

| Question | Evidence located | Defensible boundary |
|---|---|---|
| Does the Double Bass have measurable resonator structure? | Direct bass admittance/modal investigations and specialist synthesis [1–3]. | Yes for measured instruments; no universal resonance-frequency template. |
| Do attack and spectrum affect timbre? | Controlled timbre and recognition studies [7–12]. | Yes; effects depend on task, instrument, stimulus duration, and manipulation. |
| Is a brief transient the entire identity? | Onset-component manipulation [11]. | No: onset-region sinusoidal build-up can be more diagnostic than rapidly varying transient components. |
| Is timbre invariant across pitch? | Pitch-range studies and expert/nonexpert comparison [13–15]. | Constancy is limited and experience-dependent; no universal octave boundary. |
| Is timbre discriminable at controlled pitch? | Equalized-tone dissimilarity experiments [8–10]. | Yes for studied tones; this is not a bass-versus-electric-bass accuracy estimate. |
| Can identity survive overlap? | Harmonic grouping studies; orchestral-mixture identification [18–20, 23]. | Some cues can support segregation; no universal source/event attribution. |
| Does identity recover missed JGA events? | No direct evidence located or generated. | Assumption only; Stage 9 is conditional. |

**Evidence gaps:** The audit did not establish a sufficiently controlled Double Bass population study crossing performer, individual instrument, string, articulation, register, dynamics, and room. Nor did it establish expert Double Bass identification accuracy for matched-pitch bass/piano/electric-bass mixtures with hidden event authority. These are absent supporting evidence in this audit, not assertions that no such work exists anywhere.

## 3. Physical production of Double Bass sound

### 3.1 String, excitation, and coupling

**OF — general string physics:** Bowing is a nonlinear friction-driven interaction coupled to the instrument body and sound radiation. The violin review [4] provides a broad account; Guettler's thesis [5] specifically examines development of Helmholtz motion. Regular stick–slip motion and its establishment are different phenomena. Initial bow acceleration, force, and contact position affect the transient regime. These sources justify examining establishment of periodic motion rather than reducing every arco onset to an amplitude threshold.

**LI — bass transfer:** The physical mechanisms apply to bowed bass strings, but numerical violin attack limits, bridge resonances, and bow-control regions must not be transferred as bass constants. Pizzicato and arco should initially be separate conditions: impulsive release and sustained nonlinear excitation can produce substantially different observations within the same instrument class.

**OF — plucked-string evidence:** Woodhouse's measured guitar study [6] demonstrates frequency-dependent string damping, coupling-dependent decay, and higher-partial sharpening associated with bending stiffness. It also reports limitations of calibrated synthesis, including unexplained differences in some decay rates and polarization-related splitting. Its results concern guitar strings, not measured JGA bass strings.

**LI — pizzicato candidates:** Pluck location and displacement shape the initial modal excitation; finite finger contact and release alter it further. Effective length, tension, mass distribution, winding, stiffness, and termination affect modal frequencies and losses. A stopped note and an open string are not interchangeable boundary conditions. A harmonic comb is therefore a useful reference against which to measure deviations, not a mandatory description of every bass partial.

**A — testable bass hypotheses:** Record excitation position, string construction and age, stopping position, and release technique as controlled factors. Examine whether frequency deviations increase systematically with partial index, but retain departures from any stiffness model. A single fitted inharmonicity coefficient is not instrument identity. Bow-driven harmonic locking and free plucked decay should not be expected to yield identical frequency-deviation patterns.

### 3.2 Bridge, body modes, and radiation

**OF — Double Bass evidence:** Askenfelt measured bass input admittance and compared instruments [1]. Admittance describes velocity response to applied force, not sound pressure at a microphone. Modes differ in radiation efficiency. The measured basses exhibit differing modal/admittance structures; the report discusses low-frequency air/body behaviour and broader bridge-related structure. Its illustrative frequency regions are instrument- and setup-bound, not identity thresholds. The later Double Bass chapter [2] is the specialist reference for this topic, but its full chapter was not accessible from the publisher during this audit.

**OF — environmental coupling:** Guettler, Buen, and Askenfelt [3] measured Double Bass–floor interactions. Mechanical coupling through the endpin can affect bridge mobility and low-frequency transfer. Their report explicitly leaves aspects of audience audibility unresolved. “Room” can therefore include a change in mechanical support, not merely reverberation applied after sound production.

**OF — dynamic radiation:** Ackermann, Brinkmann, and Weinzierl [28] combine note-dependent partial directivities and tracked performer movements across orchestral instruments. Their study reports changing radiated spectra and room excitation, with substantial note-related variation in strings and woodwinds. **LI:** A fixed microphone does not guarantee a fixed source-to-microphone transfer during performance. Instrument orientation and motion should therefore be recorded or bounded before attributing all measured amplitude modulation to string excitation.

**LI — measurement distinction:** A spectral maximum in a note may reflect its excitation, a string partial, a body resonance, microphone response, room response, or a combination. Calling such a maximum a measured body mode is unjustified without additional evidence. Operationally estimating a spectral-envelope region is weaker than identifying a physical resonance; retain that distinction in the card.

### 3.3 Damping, collisions, noise, and modulation

**OF — adjacent physical evidence:** Double-decay behaviour is conditional rather than automatic: Woodhouse [16] investigates a necessary coupling condition across measured string instruments. Issanchou and colleagues [17] model and compare string-contact behaviour in tanpura-like and electric-bass examples; contact introduces nonlinear redistribution and high-frequency components. Neither study supplies a validated acoustic-bass identity signature.

**LI:** Bass slap, fingerboard contact, finger/string friction, bow noise, damping by the hand, and release sounds warrant separate observations. A residual is not necessarily meaningless noise, and a noisy impulse need not be a separate instrument. Conversely, a sound near a bass note could be extraneous handling noise. Attribution requires evidence, not temporal proximity alone.

**A:** Candidate controls include ordinary pizzicato, damped pizzicato, slap, arco, harmonics, and transitions. Vibrato, tremolo, beating, and pitch drift should be recorded without making them required class attributes. Dynamics should mean measured acoustic level and documented playing effort separately: increasing gain is not equivalent to playing harder. Nonlinear contact and changed excitation can alter spectral shape as well as amplitude.

## 4. Temporal identity and human recognition

**OF:** Saldanha and Corso's 1964 paper [7] is the historical recognition reference; its exact citation is verified, but full text was not accessible here, so no numerical claim is drawn from it. Grey [8] motivates multidimensional spectral/transient analysis. McAdams and colleagues [9] distinguish shared perceptual dimensions, sound-specific attributes, and listener weighting; a single common dimension set need not exhaust each source's qualities.

**OF:** Siedenburg [11] trained listeners on ten instruments using 250-ms sounds and tested 64-ms onset or middle segments. The abstract reports a 6% identification impairment when rapidly varying onset transients were omitted, versus 25% when moving the gate to the middle. These are the paper's reported percentage changes, not independently reconstructed percentage-point estimates. The finding supports onset-region tonal build-up as well as transient analysis. It is not a bass-specific effect size or a universal 64-ms observation window.

**OF:** Iverson and Krumhansl [12] found that similarity ratings for whole tones corresponded both to onsets and to onset-removed remainders. Their task was timbre similarity, not absolute instrument naming. Suied and colleagues [24] found very brief category-recognition cues with overlapping pitch ranges, sometimes without an onset advantage. Their strongest short-duration performance concerned voice targets; it supplies no millisecond-scale Double Bass recognition guarantee.

**LI:** These findings do not conflict merely because onset importance differs. Category detection, named-instrument identification, discrimination, similarity, and perceived realism are different tasks. “Remove the attack” also describes different interventions: cutting a time interval, deleting a noisy component, or changing its envelope are not equivalent. JGA should preregister exactly which operation tests which claim.

**A — temporal observations to retain:**

| Region/property | Proposed observable | Interpretation limit |
|---|---|---|
| Attack | Envelope rise interval, slope, overshoot; frequency-band onset distributions | A threshold-based rise duration depends on level, noise floor, and convention. |
| Transient morphology | Short-time waveform and broadband residual evolution | A single derivative peak cannot establish a physical excitation mechanism. |
| Spectral build-up | Relative onset times and growth of resolved partials | Window smearing can manufacture apparent synchrony or asynchrony. |
| Decay | Per-partial and band-envelope decay, curvature, beating | A global decay constant loses nonparallel trajectories; room decay is a confound. |
| Sustain | Partial stability, modulation, tonal/residual balance | Some pizzicato notes have no defensible stationary sustain. |
| Release | Damping transition, residual burst, remaining resonance | Release and onset of a following note may overlap. |
| Modulation | Amplitude/frequency trajectories, rate/depth, coherence | Vibrato is performance evidence, not obligatory bass evidence. |

## 5. Spectral and perceptual dimensions

**OF:** Caclin and colleagues [10] directly manipulated synthetic-tone parameters under controlled pitch, loudness, and perceived duration. Attack time, centroid, and spectrum fine structure influenced dissimilarity; flux was less salient and context-dependent. This supports candidate dimensions and explicitly argues against treating every common MIR statistic as equally perceptually grounded.

**OF:** Elliott, Hamilton, and Theunissen [21] relate a five-dimensional perceptual space for their orchestral-tone set to spectral and temporal modulation structure. That dimensionality is a finding about those stimuli and judgments, not a universal timbre dimension count. Patil and colleagues [22] provide additional modelling evidence that joint spectro-temporal structure can support both instrument discrimination and perceptual-distance prediction. Their learned model is not proposed for JGA implementation.

**A — descriptor/correlate separation:**

| Physical/computational descriptor | Possible perceptual correlate | Required qualification |
|---|---|---|
| Spectral centroid, spectral slope | Brightness; dark/bright judgments | Not synonymous; pitch, bandwidth, level, and weighting influence the relation. |
| Attack rise time and shape | Sharp/soft, impulsive/sustained impression | A scalar cannot describe all transient morphology. |
| Envelope and per-band decay | Ringing, damped, sustained impression | Must distinguish source damping from reverberation. |
| Harmonic envelope and spectral irregularity | Timbre differences, richness or particular colour | Descriptor definitions differ; semantic labels require listener evidence. |
| Tonal/residual balance, spectral flatness | Noisiness | Residual includes modelling error; flatness does not measure source-specific noise directly. |
| Partial-frequency deviations, periodicity evidence | Harmonicity or pitch clarity | Harmonicity is not identical to pleasantness, roughness, or recognizability. |
| AM/FM trajectories and modulation structure | Fluctuation, vibrato, roughness under suitable conditions | Rate, depth, frequency region, and listener matter. |
| Envelope peaks/resonance regions | Possible resonant or vowel-like qualities | “Formant” is descriptive here unless a physical cause is independently established. |

**LI — spectra at equal fundamental:** The fundamental is contextual evidence, not a class label. At equal nominal fundamental, instruments may differ in harmonic amplitudes, spectral envelope, inharmonicity, onset trajectories, damping, and nonharmonic content. Odd/even balance may describe a sound but the audit establishes no Double Bass-specific odd/even rule. Roll-off and spread compress spectral shape; two different envelopes can share those statistics. Spectral fine structure should remain available rather than being replaced by its centroid.

**A — observability rules:** Retain the absolute-frequency envelope and a pitch-relative partial representation together. Pitch normalization alone can erase body regions fixed approximately in hertz; an absolute spectrum alone entangles harmonic spacing with pitch. Measure the presence of the first partial separately from evidence for a fundamental periodicity. Treat a weak or absent fundamental as missing evidence, not absence of the instrument.

## 6. Spectro-temporal representation and variability

**OF — representation precedent:** Serra and Smith's spectral modelling synthesis [25] represents time-varying sinusoidal components with a stochastic residual. This is a useful representation precedent, not proof that a decomposition corresponds uniquely to physical sources. Modulation representations [21,22] offer a complementary account of changes across frequency and time.

**A — candidate representation hierarchy:**

1. Preserve original waveform, channel information, sample rate, and provenance as the recoverable evidence base.
2. Preserve time-frequency observations at explicitly declared resolutions. A long window needed to distinguish nearby bass partials cannot also locate a very brief transient precisely. Zero padding does not resolve that physical tradeoff.
3. Retain candidate partial tracks with frequency, amplitude, time support, uncertainty, and, where recoverable, phase. Tracks may begin, terminate, cross, or be unresolved. Do not fill gaps with asserted observations.
4. Retain residual/noise and resonance-region trajectories with their frequency support. Report decomposition error separately from hypothesized physical noise.
5. Derive scalar summaries and perceptual-model outputs as secondary views with links to the underlying trajectories.

**LI:** A time-averaged modulation-power representation loses temporal localization and modulation phase; it cannot alone identify which event occurred when. A magnitude-only representation also cannot retain interference phase at common partials. These are reasons to preserve supporting waveform/trajectory evidence, not authority to implement every possible representation.

**A — four distinct inference targets:**

| Identity target | Candidate relatively persistent evidence | Major variation/confounding | Future design needed |
|---|---|---|---|
| Instrument class | Distributions of excitation/resonator/decay relationships | Articulation can exceed some between-class differences | Test new physical instruments and performers, including close alternatives. |
| Individual instrument | Body/admittance structure and repeatable radiation characteristics | Setup, strings, support, temperature/humidity, microphone | Cross performers on the same bass and instruments under shared capture conditions. |
| Performance | Pluck/bow control, articulation, modulation, damping patterns | Performer and instrument interact | Crossed performer × instrument design; repeated takes. |
| Recording chain | Channel transfer, room response, compression, noise, separation artefacts | Can imitate source-envelope changes | Paired channels on the same performance, separate rooms/sessions, held-out chains. |

**OF:** Handel and Erickson [13] examine pitch-dependent source matching using wind instruments. Steele and Williams [14] report that musicians retained about 80% accuracy over a 2.5-octave horn/bassoon comparison where nonmusicians' timbre constancy declined more strongly. Siedenburg and McAdams [15] found an expertise advantage for variable-pitch sequence recognition but not constant-pitch sequences. These do not establish expert bass constancy; expertise effects are task-dependent.

**LI — invariance conclusion:** It is more plausible to test predictable transformations and conditional distributions than insist on unchanged feature values. “Invariant” should be a demonstrated result over declared factors, with an uncertainty interval and a failure region. Body geometry is comparatively persistent over a session, but its measured spectral footprint is not automatically invariant to pitch or microphone position. No candidate feature is certified source-invariant by this report.

## 7. Same-pitch discrimination and human expertise

**LI:** Controlled-pitch timbre experiments establish that pitch equality does not remove all discriminative acoustic information [8–10]. They do not prove that any particular pair of bass instruments is separable under every articulation. Nominally identical notes can still differ in intonation and tuning drift; a study claiming pitch control must report those residual differences.

**A — future discrimination design:** Compare naturally played, matched-pitch Double Bass, Piano, and Electric Bass recordings before introducing mixtures. Include fretted and fretless Electric Bass if the intended class boundary includes both. Separate raw-level trials from perceptually loudness-matched trials; equal RMS is not equal loudness. Never use pitch shifting as the only pitch-control method because it may move source resonances and create diagnostic processing artefacts.

Separate four questions: can listeners discriminate two recordings; match them to an instrument class; identify an individual instrument; and locate a source event in a mixture? Use balanced closed-set trials for interpretable confusion matrices and an additional unfamiliar/other-source condition to test rejection. Include uncertainty and confidence responses. Chance level depends on the actual task and response alternatives.

**A — human comparison:** Recruit Double Bass experts, other expert musicians, and nonmusicians as distinct strata in later perceptual work. Record instrument familiarity, training, and hearing-related eligibility rather than treating “musician” as a universal ability. Analyse participant and recording variation, not just pooled trial accuracy. No human-equivalence target or numerical recognition threshold is authorized by this report.

## 8. Simultaneous sources and masking

**OF:** Glasberg and Moore [18] derive auditory-filter characteristics using notched-noise masking, establishing a perceptually relevant frequency-selectivity framework. A spectrogram's bins are not independent auditory channels. Darwin and Ciocca [19] show that onset asynchrony can reduce a mistuned component's contribution to a complex tone's pitch. Their tested offsets and stimuli do not provide a JGA event-separation tolerance.

**OF:** Culling and Darwin [20] distinguish harmonic grouping from useful beating-related spectral fluctuations in simultaneous vowels. Vowels are adjacent evidence, not Double Bass measurements. A recent orchestral-mixture study by Jacobsen and colleagues [23] reports instrument- and voice-dependent identification and no significant room/spatial-condition effects in its tested setting. That bounded result does not establish recording invariance or absence of masking effects generally.

**LI — masking distinctions:** Energetic masking concerns target accessibility within auditory filtering; informational masking concerns uncertainty/confusion even where some target energy remains accessible. Forward/backward temporal interference, onset coincidence, and reverberation can also change access to a target. Source presence, perceptual segregation, waveform separation, and event recovery must be evaluated separately. Human inability to hear a target is not proof of mathematical absence from a recorded waveform; detector failure is not proof of either.

**LI — remaining candidate evidence:** Partials outside strong masker bands, independently evolving amplitudes/frequencies, asynchronous attacks, releases, and residual components may support attribution. These are possibilities conditioned on resolution and signal-to-masker structure. A missing fundamental may leave harmonic relations, but those relations do not uniquely identify the source. Beat-like fluctuation can arise from interference between sources and must not automatically be attributed to one performer's modulation.

**LI — same-frequency limit:** In one channel, exactly coincident components contribute to the same complex spectral quantity. Many different source decompositions can explain their sum. Equal fundamental, coincident onset, common partial support, and similar envelopes can therefore make attribution non-identifiable without additional constraints. A plausible learned or stored template cannot turn nonunique evidence into an observed event.

**OF/LI — harmonic/percussive separation:** FitzGerald [26] separates spectrogram structures using temporal/frequency median filtering. The paper explicitly reports bass attack entering the percussive output. Thus “harmonic” is not equivalent to Double Bass and “percussive” is not equivalent to Drum. A source's attack and tail can be split across both components. Such transforms are future diagnostic manipulations, not independent source authority.

**A:** Later masking experiments should manipulate target-to-masker ratio, band-specific overlap, onset offset, duration overlap, and spatial conditions independently where feasible. Aggregate mixture SNR is insufficient to describe which diagnostic cues remain accessible. Sequential timbral streaming should be tested separately from simultaneous segregation; the former may use memory and continuity unavailable to an isolated masked event.

## 9. Virtual instruments and synthesis: secondary hypothesis sources

**OF — vendor-reported facts only:** No plugin was installed, executed, benchmarked, or accepted as Ground Truth. Product controls demonstrate what a reconstruction system exposes; they do not demonstrate biological cue use or natural-source invariance.

| Representative source | Publicly documented dimensions | Hypothesis suggested; unknowns |
|---|---|---|
| Vienna Instruments Upright Bass, legacy manual [V1] | Pizzicato articulations, velocity layers, alternations, vibrato choices, release samples, noises and performance transitions. The staccato patch lists three velocity layers and two alternations. | Repeated nominal notes and releases merit separate observations. Alternation counts are patch-specific; scheduling and all processing details are not established. |
| Ample Bass Upright [V2] | Product page lists multiple articulations and neck/body/room microphones plus DI; manual exposes release gain, string/position selection, buzz, finger sounds, and modulation. | Separate acquisition channel, articulation, position, and residual events. The older manual must not be treated as a complete current-version implementation specification. Exact round-robin/velocity mapping and internal noise synthesis are unknown here. |
| SWAM-S / Solo Strings [V3] | Manufacturer describes physical modelling without prerecorded samples, digital-waveguide work, and bow speed/pressure/position, vibrato and pizzicato controls. | Excitation controls and resonator variation are candidate factors. Exact equations, parameter identification, solver, and fidelity of Double Bass-specific physics remain proprietary/unknown. |
| Vir2 MOJO: Upright Bass [V4] | Sampling of one named performer/instrument, legato, vibrato, articulations, and an analog recording chain. | A realistic library can conflate performer, individual instrument, and chain; library diversity is not population diversity. Exact processing and sample selection remain unknown. |

**LI — synthesis approaches and scientific use:** Multisampling motivates coverage of pitch and articulation; velocity layers motivate changes beyond gain; round robins/alternations motivate within-condition variability. Release samples and transition models motivate boundaries that an ADSR summary can miss. None proves these dimensions are necessary for human recognition.

**A:** Sympathetic resonance deserves a controlled damped-versus-undamped string comparison, but explicit sympathetic-resonance implementation was not verified for the listed products. Modal synthesis and waveguides offer mechanisms to formulate falsifiable manipulations. Convolution can approximate a fixed linear resonator or room response; it cannot by itself represent changing nonlinear excitation or contact. A product's convolution *reverb* is not evidence of body-resonance modelling. Hybrid sampling/modelling could isolate selected dimensions for perception studies, subject to checking resynthesis artefacts and external validity.

**LI:** Synthesis becomes scientifically useful when a manipulation has documented acoustic effects and a listening comparison tests its consequences. Perceived realism, source naming, and event detectability are separate endpoints. Plugin MIDI timing cannot silently become acoustic event timing authority.

## 10. Proposed Double Bass Identity Card

**Assumption — conceptual proposal, not schema or identity formula.** Revise the suggested A–P categories into four groups: observed signal structure; conditioning factors; tested identity claims; and evidence quality/provenance. Excitation labels remain hypotheses unless independently documented. Source-invariant evidence becomes a *validation result field*, not an assumed measurement domain. Register/dynamics/articulation belong to conditioning, avoiding duplicate “identity features.”

Every measurement would carry time support, channel/source lineage, units, method and resolution, uncertainty, and an evidence-status flag. Alternative explanations should accompany attributed mechanisms. The following candidate names confer no runtime authority.

| Domain | Candidate measurable observables | Physical/perceptual reason | Principal limit and test |
|---|---|---|---|
| Signal and acquisition | Waveform/channel references, sample rate, usable band, clipping/noise estimates | Preserve evidence before interpretation | Derived stems can contain leakage; compare original and derived evidence. |
| Excitation evidence | Rise morphology, impulse/residual timing, periodic build-up | Pluck, bow, contact mechanisms [4–6,17] | Do not infer gesture from one peak; controlled articulation comparison. |
| Fundamental context | Candidate F0 trajectory, harmonic-spacing support, first-partial visibility | Separate pitch from timbre and missing fundamental | Multiple F0 candidates and unresolved states must be permitted. |
| Partial structure | Resolved frequencies, amplitudes and phase where estimable; deviations from candidate harmonics | Preserve harmonic envelope and inharmonicity | Missing, merged, split and spurious tracks; frequency-resolution audit. |
| Spectral envelope | Envelope versus hertz and time; centroid/spread/slope/roll-off as derived summaries | Spectral shape and perceptual correlates [8–10] | State magnitude/power weighting, smoothing and bands; compare pitch and chain changes. |
| Resonator evidence | Persistent envelope regions; modal frequency/damping/admittance only with suitable physical measurements | Body/bridge coupling [1,3] | A note spectrum alone does not identify body modes. |
| Attack and release | Rise/settling/damping intervals; band and partial onset/offset distributions | Temporal identity [11,12] | Window leakage, noise, and following events bias boundaries. |
| Envelope evolution | Broadband, band-specific and partial-specific curves; decay slopes/curvature | Distinguish changes hidden by a single envelope [6,16] | No compulsory exponential or ADSR form. |
| Residual/nonharmonic structure | Residual time-frequency support, flatness, burst statistics, tonal/residual ratio | Noise, contact and unmodelled evidence [17,25] | Residual is algorithm-dependent; inspect reconstruction error. |
| Modulation/coherence | AM/FM rate and depth; cross-partial covariance; localized modulation views | Joint spectro-temporal cues [21,22] | Beating and room interference may imitate source modulation. |
| Conditioning factors | Pitch/register, dynamic effort/level, articulation, string/position, performer/instrument/session | Distinguish class from performance and chain | Hidden authority belongs only to post-blind evaluation; unknown during inference stays unknown. |
| Identity evidence claims | Candidate source hypotheses, supporting/contradicting observations, tested scope, abstention | Observation before musical interpretation | No unsupported certainty or automatic musical-role assignment. |
| Invariance assessment | Within/between-condition variation and held-out performance, with uncertainty | Invariance is an empirical conclusion | Requires crossed factors, adequate independent units and failed-case reporting. |
| Missingness and provenance | Unmeasured/unresolved/masked/not-applicable states; hashes, transformations, calibration and citation links | SVP-001/F-030 traceability | Zero is not missing; source-instance provenance is not acoustic identity proof. |

**A — minimum measurement discipline:** Define each descriptor before comparing values. Examples include magnitude versus power centroid, roll-off percentage, logarithmic versus linear slope, envelope smoothing, attack thresholds, partial-resolution criterion, spectral-irregularity definition, and residual model. Report sensitivity to scientifically plausible analysis resolutions. Preserve physical time as well as any normalized time axis; normalized attack shape must not erase attack duration.

**LI — architectural firewall:** `SOURCE_IDENTITY_EVIDENCE` is useful conceptual language for a future evidence product, not an adopted type. Physical source compatibility must not imply timekeeping role, bass-line function, beat, meter, or other musical semantics. Existing provenance identity and role authority remain separate. Architecture ownership and any proposed boundary crossing require later PI decisions.

## 11. What JGA currently measures and what is missing

**Observed Fact — static code inspection, not execution:**

| Inspected repository evidence | Present capability | Scientific limit for this track |
|---|---|---|
| [BasicFeatureExtractor](../../../src/jga/source_understanding/basic_feature_extractor.py) | Whole-stem duration, RMS, zero-crossing rate; one whole-signal real FFT; magnitude-weighted centroid, bandwidth, and 95% magnitude roll-off | No partial/time matrix; duration is stem duration, not acoustic note duration; RMS is not perceptual loudness. Variable naming does not turn magnitude weighting into power weighting. |
| [BassClassifier](../../../src/jga/source_understanding/classifiers/bass_classifier.py) | Rules using centroid below 300 Hz and roll-off below 400 Hz; returns BASS family, instrument `None`, and decision confidence | Existing coarse heuristic, not Double Bass class recognition, calibrated uncertainty, or physical identity. No changes proposed here. |
| [BasicOnsetDetector](../../../src/jga/dsp/onset_detector.py) | Librosa-derived onset times | No identity-specific attack morphology or source attribution. |
| [BasicTransientDetector](../../../src/jga/dsp/transient_detector.py) | Thresholds absolute first sample difference and returns times | No transient duration, band structure, noise decomposition, or physical-event validation. |
| [SourcePulseCandidateBuilder](../../../src/jga/engines/source_pulse_candidate_builder.py) | Onset frames/times and onset-strength values for input stems | Onset strength is not the full spectral evolution; this file's existence does not establish its use in every current workflow. |
| [SignalRepresentation](../../../src/jga/observation/signal_representation.py), [AudioStem](../../../src/jga/core/audio_stem.py) | Samples and sample rate; AudioStem also includes asset/transformation provenance fields and explicit identity-authority status | Raw evidence can support future analyses, but retained samples are not already measured identity observables. |
| [Project State](../../JGA_PROJECT_STATE.md) and [AD-041 operational binding](../../architecture/AD-041_HTDEMUCS6S_OPERATIONAL_BINDING.md) | Documented source provenance and bounded canonical timing workflow | Separation labels and source-instance identities are not acoustic proof of instrument identity. |

**LI — genuinely missing in the inspected production representations:** event-supported partial trajectories with uncertainty; pitch-relative plus absolute-frequency envelope evolution; residual/transient trajectories; independently supported body-mode attribution; modulation/coherence evidence; crossed-factor variability/invariance results; and a calibrated, abstaining source-evidence assessment. This is a scoped audit of `src/jga` and its relevant contracts, not a claim that no historical research artifact contains any spectral analysis.

**LI:** Existing scalar features remain useful controls. Their presence does not answer whether richer representations improve measurement or perception. Raw waveform and provenance should be reused as evidence where suitable. A new production abstraction is premature until a smaller experiment establishes a missing scientific capability.

## 12. Staged validation roadmap

**Assumption — design only.** Each stage requires a preregistered question, independent units, acquisition/annotation authority, analysis freeze, failure criteria, and a PI continuation decision. Later stages are conditional, not an instruction to execute a large factorial study immediately. Independence is governed by SVP-001: hidden instrument/event metadata must not guide blind analysis or selection of favourable windows.

| Stage | Design and factors | Evidence sought and continuation limit |
|---|---|---|
| 1. Isolated notes | Repeated natural pizzicato at one pitch; fixed bass, performer, string and chain | Establish observable partial/envelope structure and measurement repeatability. No class-identity claim. |
| 2. Pitch/register | Natural notes across usable range; repeated pitch on alternative strings where feasible | Separate pitch-relative excitation from absolute-frequency envelope behaviour; do not infer invariance from transposed copies. |
| 3. Dynamics | Repeated soft/medium/strong effort at fixed notes; retain acoustic level, plus separate level-matched analysis | Test changes of shape versus mere gain. Resolve acquisition noise/compression before interpreting differences. |
| 4. Articulation | Pizzicato variants, arco, damping, harmonics, slap and transitions in bounded subsets | Determine whether conditional models are necessary; allow no stationary sustain. |
| 5. Instruments/performers | Crossed performers × physical basses with repeated sessions; then strings/setups and recording factors | Distinguish class, instrument, performer and chain variance. Hold out whole instruments/performers/sessions. |
| 6. Same pitch | Double Bass versus Piano/Electric Bass and selected alternatives; natural matched notes, loudness controls and unfamiliar alternatives | Demonstrate source-class information beyond pitch and level. Evaluate confusion and abstention. |
| 7. Simultaneous overlap | Independently recorded sources mixed under known timing/gain; exact/small pitch offsets, synchronous/asynchronous onset | Determine which observed components remain attributable. Solo stems are held out from mixture inference. |
| 8. Masking severity | Vary target-to-masker level and diagnostic-band overlap; masked attack versus masked tail; room/channel conditions | Estimate condition-specific limits, false attribution and unresolved rates. No universal SNR boundary. |
| 9. Identity-aided event recovery | Frozen current event path compared against an approved identity-assisted path on unseen mixtures | Test incremental correct source events at controlled false attribution. Hidden independent event authority; no forced recovery. |

**A — statistical and reproducibility plan:** Count independently recorded takes/instruments/performers as experimental units; thousands of frames from one note are not thousands of independent examples. Use paired comparisons where the same original recording is transformed, with uncertainty clustered at the recording and participant level. Quantify repeatability, missingness, between-condition effects, and confidence intervals before proposing acceptance thresholds. Later confirmation requires fresh held-out recordings; exploratory thresholds must not be evaluated on the data that selected them.

**A — controls:** Include repeated exports of identical audio to isolate computational reproducibility from repeated performances; silent/room-noise files; equal-gain transformations; genuinely new notes; and same-performance paired microphones for chain sensitivity. Preserve unprocessed references. A factorial design must not bind every instrument to one unique room or performer. Sample counts beyond the pilot require a prospective precision/power rationale, not an arbitrary catalogue size.

## 13. Exact smallest next scientific experiment

**Assumption — proposed experiment `DB-ID-PILOT-01`, not registered or executed.**

**Question:** At one fixed pitch and ordinary pizzicato condition, do repeated real Double Bass notes contain measurable, repeatable changes in *relative amplitudes of resolved partials* that a whole-note spectral summary cannot express?

**Scope:** One physical Double Bass, one performer, one recording session, one fixed microphone position and gain. Use open A1, nominally 55 Hz, ordinary finger pizzicato without vibrato, with the other strings damped and an unchanged marked plucking region. This deliberately avoids a stopping-finger factor. It tests a condition, not the whole bass class.

**Acquisition proposal:** Twenty independent takes, mono 48-kHz/24-bit PCM, each with 1 second of pre-onset room signal, a note allowed to decay for 4 seconds, then damping and 1 second of post-damping capture. Record five matched-duration room-only controls. Retain the raw files, actual gain, microphone/distance/orientation, room/support, string specifications, tuning and performer/instrument identifiers in separate authority. These settings are pragmatic pilot choices, not literature-derived requirements.

**Independent authority:** A custodian records the physical onset/release reference and its uncertainty using synchronized acquisition/video or an independently justified measurement. Seal that information, source labels, and acquisition logs before blind acoustic analysis. Provide anonymized whole captures and controls, not Ground-Truth-centred crops. Analyst-determined acoustic support is frozen before evaluation; annotator disagreements remain intervals. If independent synchronization is unavailable, event-timing validation is blocked rather than inferred from a score or the current detector.

**Proposed analysis, only after approval:** Independently inspect and document waveform support and two time-frequency views: a 20-ms transient view and a 200-ms partial-resolution view, each with a 5-ms hop and declared window convention. The short view cannot resolve 55-Hz harmonic spacing reliably; its purpose is temporal morphology. Retain these resolution limitations rather than selecting whichever plot looks convincing. A second 160-ms partial view is a predefined sensitivity check, not another hypothesis search.

Track candidate partials 1–8 when individually resolvable above the measured room-noise background. First estimate frequency structure from audio; the nominal pitch remains hidden during blind analysis. Preserve actual hertz and amplitude trajectories. Do not require all eight partials; explicitly record unresolved, masked-by-noise, merged or unobserved components. Include early build-up and decay, with edge support declared. No classifier, learned template, or identity score is needed.

**Endpoint:** For each resolvable pair, describe its relative-amplitude change through time, uncertainty and variation across takes. Compare the time-varying account with a fixed relative-amplitude profile multiplied by a common time envelope. The latter is a null description of spectral shape, not an identity formula. Report whether reproducible nonparallel partial evolution exceeds noise/analysis-resolution sensitivity. Preserve all takes, including weak or contradictory ones; do not select a “representative” successful note as evidence.

**Possible outcomes:** Observable repeatable evolution supports only a next measurement study at another pitch. Evolution that is measurable but inconsistent across takes supports performance variability and an investigation of controls. No resolvable structure, or sensitivity comparable to the purported effect, means insufficient evidence and no richer identity representation is justified yet. This pilot has no population-level significance claim or arbitrary pass percentage; it estimates measurement uncertainty for a subsequent preregistration.

**Why this is smallest:** It tests the need for partial × amplitude × time with one source condition, before instrument discrimination, musicians, mixtures, or learned decisions. It does not establish perceptual diagnosticity. The next distinct experiment, if justified, would be a cue-manipulation listening comparison with resynthesis/sham controls; matched-pitch competing instruments enter at Stage 6.

## 14. Masked-event-recovery hypothesis and scoring limits

**Assumption — future hypothesis:** Given an identity representation validated independently on isolated and controlled-mixture data, source-specific spectro-temporal evidence might support some events that the frozen onset path misses or cannot attribute. The claim concerns incremental evidence for a real event, not interpolation of an expected performance pattern.

**A — mandatory comparison design:** Freeze the baseline event path, assisted path, cue ablations, tolerance and one-to-one event matching before opening hidden event authority. Use independent performed-event records and isolated-source evidence held by a custodian. Analyse only mixtures during the blind phase. Evaluate events absent from the frozen baseline separately from events merely relabelled or shifted. Include target-absent mixtures, noises, non-bass plucked sources, and earlier-note tails to expose false attribution.

| Outcome | Future operational meaning |
|---|---|
| Correctly recovered source event | A new assisted detection matches a hidden independent event of the correct source within the approved uncertainty/tolerance contract, without duplicate credit. |
| False source attribution | A candidate is assigned to the wrong source or has no independently supported target event; report both cases separately. |
| Unresolved evidence | The system abstains, or available evidence supports competing explanations. Distinguish missed visible events from unscorable authority. |
| Genuinely unobservable event | A separate, condition-bound adjudication, supported by the acquisition/mixing record or a declared identifiability argument; never inferred merely from a miss. |

**LI:** “Unobservable” is not an omniscient annotation available from a waveform. A target intentionally removed from the delivered signal is a defensible structural case. Complete masking for a tested listener is a perceptual limit, not necessarily an information-theoretic limit. For natural mixtures, genuinely unobservable may remain undecidable; label that uncertainty rather than forcing this category.

**A:** Report correct recovery counts/rates, precision, false attributions per unit time and per candidate, missed independently observable events, abstention, duplicate detections, and timing-error distributions. Report denominators for all authorized events and for any independently established observable subset, so excluding difficult cases cannot inflate success. Compare systems at matched false-attribution operating points. Confidence calibration, if later available, requires held-out events and explicit rejection behaviour.

**LI — hard limit:** An event consistent with a bass template but not identifiable in the observed mixture remains a hypothesis. Shared partials, cancellation, severe masking and separator artefacts can destroy attribution. No timing grid, musical role, expected bass pattern or BeatReference may supply missing event authority in this study.

## 15. Future Drum adaptation

**Decision:** Priority remains Ride, Hi-Hat, Snare, Kick, Toms, other Cymbals, after Double Bass methodology validation. No periodicity or timekeeping study begins here.

**OF:** Chaigne, Touzé, and Thomas [27] treat nonlinear vibrations of gongs and cymbals, including regimes beyond a simple linear harmonic description. This motivates a new physical audit for percussion rather than reuse of a string harmonic template.

**A:** Retain the methodology—physical mechanism, acoustic observation, perceptual manipulation, crossed variability and uncertainty—but reconsider the actual coordinates. Ride studies should control bell/bow/edge strike region, implement, force, sustain and damping. Hi-Hat additionally requires openness, pedal force, stick versus foot excitation, and inter-cymbal contact. Treat these as proposed factors, not already demonstrated discriminators.

For Snare, investigate membrane/wire/cavity coupling and contact; for Kick and Toms, membrane modes, shell/cavity interactions and damping; for other cymbals, geometry, striking condition, decay and nonlinear spectral evolution. Do not force a fundamental or integer partial index when unsupported. Noise, modal density and energy transfer may be more useful than harmonic ratios. Class, individual instrument, performance and recording variation remain separate questions.

**LI:** Recognized Ride/Hi-Hat evidence would not itself establish a temporal reference or musical function. Any later identity → periodicity → candidate reference → BeatReference/BPM investigation needs its own scientific authority.

## 16. PI decisions and unresolved blockers

**Assumption — recommendations for PI review:**

1. Approve or revise the conditional, evidence-based direction and confirm that its timing-attribution purpose satisfies the mission gate. Do not adopt the proposed card as a permanent representation yet.
2. Decide whether the initial scope is ordinary acoustic pizzicato, with arco/slap held as separate later conditions, and define boundaries for electric upright, acoustic bass guitar, and processed bass sounds.
3. Approve or revise `DB-ID-PILOT-01`, its acquisition resources and independent authority. No experiment is authorized by this report.
4. Identify available real instruments/performers, recording rights, and eventual shared capture conditions for comparison instruments. A single plugin library cannot substitute for these population factors.
5. Resolve how physical modes could be independently measured if claims about body-mode identity are later needed. Audio-only envelope observations cannot resolve that ownership of physical cause.
6. Approve a later perceptual protocol and participant strata before claiming diagnostic cues or expert performance. Decide practical effect/precision goals after pilot measurement uncertainty is known.
7. Define the independent event-authority, uncertainty, rejection and unobservability adjudication contracts before any Stage 9 work. Source-level labels alone are insufficient.
8. Obtain inaccessible key full texts if detailed historical-method comparison is required. Bibliographic or abstract access is insufficient to reconstruct their controls, full participant populations or source-specific effect sizes.

**OF — deliverable validation:** This record contains literature provenance, a scoped static implementation audit, conceptual observables, a staged design and a bounded next experiment. No test suite, classifier training, plugin execution, audio experiment or scientific validation run was performed. No claim of experimental success is made. Local repository links resolve, all 17 numbered sections are present, and the document has no trailing-whitespace errors. Accepted evidence is referenced, not rewritten. This document is the only file created or modified for this task; pre-existing working-tree changes were left untouched.

**Decision boundary:** STOP FOR PI REVIEW. The report does not authorize the pilot, a new schema, a source classifier, masked-event recovery, or Drum periodicity research.

## 17. Sources and access qualifications

The numbered references below also serve as source notes for the bracketed citations in the text. Bibliographic-only entries identify important literature without importing unverified detailed results. Dates below are publication dates, not search-engine crawl dates. External findings remain bounded by their original populations and conditions.

### Scientific references

1. Askenfelt, A. (1982). **Eigenmodes and tone quality of the double bass.** *STL-QPSR*, 23(4), 149–174. [Institutional full text](https://www.speech.kth.se/qpsr/1982/1982_23_4_149-174.pdf). Primary technical report; peer-review status not established here. Direct bass measurements; admittance, modal comparison and radiation distinction. Relevant sections: “Input admittance and eigenmodes” and comparisons among basses.

2. Askenfelt, A. (2010). **Double Bass.** In T. D. Rossing (Ed.), *The Science of String Instruments*, 259–277. Springer. [doi:10.1007/978-1-4419-7110-4_15](https://doi.org/10.1007/978-1-4419-7110-4_15). Specialist refereed chapter; publisher abstract, bibliography and citation inspected, full chapter inaccessible there. No detailed result depends solely on its preview.

3. Guettler, K., Buen, A., & Askenfelt, A. (2008). **An in-depth analysis of the double bass-stage floor contact.** *Proceedings of the Institute of Acoustics*, 30, Part 3, 37–44. [Proceedings full text](https://www.ioa.org.uk/system/files/proceedings/k_guettler_a_buen_a_askenfelt_an_in-depth_analysis_of_the_double_bass-stage_floor_contact.pdf). Primary conference report; Sections 3–4 and conclusion. Mechanical support and radiation; not a universal audibility result.

4. Woodhouse, J. (2014). **The acoustics of the violin: a review.** *Reports on Progress in Physics*, 77(11), 115901. [doi:10.1088/0034-4885/77/11/115901](https://doi.org/10.1088/0034-4885/77/11/115901). [Abstract](https://pubmed.ncbi.nlm.nih.gov/25345563/). Peer-reviewed review; broad physical context, not bass-specific numerical evidence.

5. Guettler, K. (2002). **The Bowed String: On the Development of Helmholtz Motion and On the Creation of Anomalous Low Frequencies.** Doctoral thesis, KTH, Stockholm. [Institutional manuscript](https://kth.diva-portal.org/smash/get/diva2%3A9153/FULLTEXT01.pdf). Thesis and collected research; accessible text on onset development, not treated as a new Double Bass recognition experiment.

6. Woodhouse, J. (2004). **Plucked guitar transients: Comparison of measurements and synthesis.** *Acta Acustica united with Acustica*, 90(5), 945–965. [Author-hosted full text](https://euphonics.org/wp-content/uploads/2022/03/Guitar_II.pdf). Peer-reviewed primary research; string properties and comparison sections, especially pp. 955–956. Guitar-to-bass transfer is explicitly inferential.

7. Saldanha, E. L., & Corso, J. F. (1964). **Timbre cues and the identification of musical instruments.** *Journal of the Acoustical Society of America*, 36(11), 2021–2026. [doi:10.1121/1.1919317](https://doi.org/10.1121/1.1919317). Bibliographic verification through scientific reference lists; full text inaccessible in this audit. Do not confuse with the 1962 meeting abstract of the same title, DOI 10.1121/1.1937169.

8. Grey, J. M. (1977). **Multidimensional perceptual scaling of musical timbres.** *Journal of the Acoustical Society of America*, 61(5), 1270–1277. [doi:10.1121/1.381428](https://doi.org/10.1121/1.381428). [Publication record](https://pubmed.ncbi.nlm.nih.gov/560400/). Peer-reviewed primary study; citation verified and abstract indexed elsewhere, no raw data reanalysis.

9. McAdams, S., Winsberg, S., Donnadieu, S., De Soete, G., & Krimphoff, J. (1995). **Perceptual scaling of synthesized musical timbres: Common dimensions, specificities, and latent subject classes.** *Psychological Research*, 58(3), 177–192. [doi:10.1007/BF00419633](https://doi.org/10.1007/BF00419633). [Abstract](https://pubmed.ncbi.nlm.nih.gov/8570786/). Peer-reviewed primary study; abstract inspected; author PDF retrieval failed.

10. Caclin, A., McAdams, S., Smith, B. K., & Winsberg, S. (2005). **Acoustic correlates of timbre space dimensions: A confirmatory study using synthetic tones.** *Journal of the Acoustical Society of America*, 118(1), 471–482. [doi:10.1121/1.1929229](https://doi.org/10.1121/1.1929229). [Author full text](https://www.mcgill.ca/mpcl/files/mpcl/caclin_2005_jasa_0.pdf). Primary controlled perceptual experiments; abstract, introduction and experimental parameter rationale inspected.

11. Siedenburg, K. (2019). **Specifying the perceptual relevance of onset transients for musical instrument identification.** *Journal of the Acoustical Society of America*, 145(2), 1078–1087. [doi:10.1121/1.5091778](https://doi.org/10.1121/1.5091778). [Abstract](https://pubmed.ncbi.nlm.nih.gov/30823780/). Primary perceptual study; quantitative statements restricted to abstract-reported conditions/results.

12. Iverson, P., & Krumhansl, C. L. (1993). **Isolating the dynamic attributes of musical timbre.** *Journal of the Acoustical Society of America*, 94(5), 2595–2603. [doi:10.1121/1.407371](https://doi.org/10.1121/1.407371). [Abstract](https://pubmed.ncbi.nlm.nih.gov/8270737/). Primary similarity experiments; abstract inspected.

13. Handel, S., & Erickson, M. L. (2004). **Sound source identification: The possible role of timbre transformations.** *Music Perception*, 21(4), 587–610. [Publisher abstract](https://online.ucpress.edu/mp/article-abstract/21/4/587/62157/Sound-Source-Identification-The-Possible-Role-of). Primary wind-instrument pitch-range study; abstract access. Not a Double Bass population study.

14. Steele, K. M., & Williams, A. K. (2006). **Is the bandwidth for timbre invariance only one octave?** *Music Perception*, 23(3), 215–220. [Institutional record and abstract](https://libres.uncg.edu/ir/listing.aspx?id=9224). Primary expert/nonexpert comparison; abstract and citation inspected.

15. Siedenburg, K., & McAdams, S. (2018). **Short-term recognition of timbre sequences: Music training, pitch variability, and timbral similarity.** *Music Perception*, 36(1), 24–39. [doi:10.1525/MP.2018.36.1.24](https://doi.org/10.1525/MP.2018.36.1.24). [Author full text](https://www.mcgill.ca/mpcl/files/mpcl/siedenburg_2018_muspercept.pdf). Primary memory experiments; abstract and task/background inspected.

16. Woodhouse, J. (2021). **A necessary condition for double-decay envelopes in stringed instruments.** *Journal of the Acoustical Society of America*, 150(6), 4375–4384. [doi:10.1121/10.0009012](https://doi.org/10.1121/10.0009012). [Abstract](https://pubmed.ncbi.nlm.nih.gov/34972269/). Primary physical study; abstract access; pagination corroborated by the author's publication site. No bass-specific effect size inferred.

17. Issanchou, C., Acary, V., Pérignon, F., Touzé, C., & Le Carrou, J.-L. (2018). **Nonsmooth contact dynamics for the numerical simulation of collisions in musical string instruments.** *Journal of the Acoustical Society of America*, 143(5), 3195–3205. [doi:10.1121/1.5039740](https://doi.org/10.1121/1.5039740). [Author full text](https://www.lam.jussieu.fr/Membres/LeCarrou/Articles/A24_Issanchou_NonsmoothContactDynamics.pdf). Primary simulation/physical comparison; abstract and model scope inspected; acoustic-bass transfer remains hypothetical.

18. Glasberg, B. R., & Moore, B. C. J. (1990). **Derivation of auditory filter shapes from notched-noise data.** *Hearing Research*, 47(1–2), 103–138. [doi:10.1016/0378-5955(90)90170-T](https://doi.org/10.1016/0378-5955(90)90170-T). [Abstract](https://pubmed.ncbi.nlm.nih.gov/2228789/). Primary psychoacoustic methods/evidence; abstract inspected.

19. Darwin, C. J., & Ciocca, V. (1992). **Grouping in pitch perception: Effects of onset asynchrony and ear of presentation of a mistuned component.** *Journal of the Acoustical Society of America*, 91(6), 3381–3390. [doi:10.1121/1.402828](https://doi.org/10.1121/1.402828). [Abstract](https://pubmed.ncbi.nlm.nih.gov/1619115/). Primary complex-tone experiments; not a bass event-recovery study.

20. Culling, J. F., & Darwin, C. J. (1994). **Perceptual and computational separation of simultaneous vowels: Cues arising from low-frequency beating.** *Journal of the Acoustical Society of America*, 95(3), 1559–1569. [doi:10.1121/1.408543](https://doi.org/10.1121/1.408543). [Abstract](https://pubmed.ncbi.nlm.nih.gov/8176059/). Primary simultaneous-vowel experiments; abstract inspected.

21. Elliott, T. M., Hamilton, L. S., & Theunissen, F. E. (2013). **Acoustic structure of the five perceptual dimensions of timbre in orchestral instrument tones.** *Journal of the Acoustical Society of America*, 133(1), 389–404. [doi:10.1121/1.4770244](https://doi.org/10.1121/1.4770244). [Article](https://pmc.ncbi.nlm.nih.gov/articles/PMC3548835/). Primary perceptual/acoustic study; indexed article text inspected; direct retrieval intermittently challenged.

22. Patil, K., Pressnitzer, D., Shamma, S., & Elhilali, M. (2012). **Music in our ears: The biological bases of musical timbre perception.** *PLOS Computational Biology*, 8(11), e1002759. [Full text](https://doi.org/10.1371/journal.pcbi.1002759). Primary computational/perceptual modelling. The [2013 correction](https://doi.org/10.1371/annotation/d8b290d3-32b7-4ded-b315-d1e699bb34da) concerns switched graphics for Figures 5 and 7; correction text inspected. No benchmark accuracy is adopted as JGA authority.

23. Jacobsen, S., Baril, F., Grimm, G., & Siedenburg, K. (2026). **Investigating instrument identification in a virtual orchestral scene.** *Music Perception*, advance article, 1–17, published online July 29. [doi:10.1525/mp.2026.2702234](https://doi.org/10.1525/mp.2026.2702234). Publisher-indexed results and pagination inspected; full article retrieval failed. The [2025 author deposit, version 2](https://doi.org/10.5281/zenodo.17208001) is explicitly a preprint with supplementary material/data, not interchangeable with the final article.

24. Suied, C., Agus, T. R., Thorpe, S. J., Mesgarani, N., & Pressnitzer, D. (2014). **Auditory gist: Recognition of very short sounds from timbre cues.** *Journal of the Acoustical Society of America*, 135(3), 1380–1391. [doi:10.1121/1.4863659](https://doi.org/10.1121/1.4863659). [Abstract](https://pubmed.ncbi.nlm.nih.gov/24606276/). Primary category-recognition study; abstract inspected.

25. Serra, X., & Smith, J. (1990). **Spectral modeling synthesis: A sound analysis/synthesis system based on a deterministic plus stochastic decomposition.** *Computer Music Journal*, 14(4), 12–24. [doi:10.2307/3680788](https://doi.org/10.2307/3680788). [Author group's description and reference](https://www.upf.edu/web/mtg/sms-tools). Primary representation method; institutional technical description inspected, not a bass validation study.

26. FitzGerald, D. (2010). **Harmonic/percussive separation using median filtering.** *Proceedings of the 13th International Conference on Digital Audio Effects (DAFx-10)*, Graz, 6–10 September. [Proceedings full text](https://dafx10.iem.at/proceedings/papers/DerryFitzGerald_DAFx10_P15.pdf). Primary method report; abstract and examples, especially PDF p. 3 on bass attack leakage.

27. Chaigne, A., Touzé, C., & Thomas, O. (2005). **Nonlinear vibrations and chaos in gongs and cymbals.** *Acoustical Science and Technology*, 26(5), 403–409. [doi:10.1250/ast.26.403](https://doi.org/10.1250/ast.26.403). [Publisher PDF](https://www.jstage.jst.go.jp/article/ast/26/5/26_5_403/_pdf). Scientific physical overview/research; indexed publisher text and author bibliography inspected, PDF retrieval timed out. Used only to motivate a separate percussion audit.

28. Ackermann, D., Brinkmann, F., & Weinzierl, S. (2024). **Musical instruments as dynamic sound sources.** *Journal of the Acoustical Society of America*, 155(4), 2302–2313. [doi:10.1121/10.0025463](https://doi.org/10.1121/10.0025463). [Abstract](https://pubmed.ncbi.nlm.nih.gov/38557737/). Primary directivity/movement study; publisher-indexed text and abstract inspected. Dynamic radiation evidence, not instrument-class recognition validation.

### Vendor documentation: hypothesis provenance only

- **V1.** Vienna Symphonic Library (2007). *Vienna Instruments Upright Bass — Patches, Matrices, Presets*. [Official legacy manual](https://odl.vsl.co.at/cms-vsl/legacy-manuals/collections/vi_uprightbass_patch-matrix-preset.pdf), pp. 2–7. Full text inspected. Historical product, not a current purchase recommendation.
- **V2.** Ample Sound (undated). *Ample Bass Upright*, [official product page](https://www.amplesound.net/en/pro-pd.asp?id=21), and *Ample Bass Upright Main Panel Manual*, [official PDF](https://www.amplesound.net/en/Main_Panel_Manual-ABU.pdf), printed pp. 2–9. Product page and manual inspected; version correspondence not established for every listed control.
- **V3.** Audio Modeling (2026-03-16). *SWAM-S — Pure Physical Modeling Excellence*. [Manufacturer article](https://audiomodeling.com/blog/swam-s-pure-physical-modeling-excellence); [Solo Strings release notes](https://kb.audiomodeling.com/support/solutions/articles/206000050990-swam-solo-strings-release-notes). Manufacturer declarations and controls, not independently verified implementation.
- **V4.** Vir2 Instruments (undated). *MOJO: Upright Bass*. [Official product page](https://www.vir2.com/instruments/mojo-upright-bass/). Product description inspected; no independent realism or classification benchmark.
