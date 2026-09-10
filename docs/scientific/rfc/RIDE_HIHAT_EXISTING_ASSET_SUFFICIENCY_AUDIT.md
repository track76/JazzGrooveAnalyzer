# Ride / Hi-Hat existing-asset sufficiency audit

Identifier: RH-ASSET-AUDIT-01. Date: 2026-09-10. Status: **COMPLETED DOCUMENTARY AUDIT — FOR PI REVIEW**.
Repository starting HEAD: `13f391be8e8ae512c171e79e93f07b7a9ffca37e`, branch `scientific/translation-layer-finalization`.

## 1. Scope and conclusion

Ride is primary; Hi-Hat is secondary/complementary. Other kit channels are considered only as potential contamination/negative controls. No ontology, classifier, feature set or fallback timing logic is designed. No listening, audio decoding/analysis, event annotation, source separation, experiment, timing inference or BPM calculation occurred. Byte hashing establishes integrity, not acoustic properties. Existing metadata was used; missing fields remain unknown.

**Ride: LEVEL C — complementary / real-world material; no established Ride event identity. Hi-Hat: LEVEL B — initial channel-conditioned observability is feasible; event discrimination remains conditional and unvalidated.** These grades are different from proof of identity. Neither source reaches LEVEL A. Ride-vs-Hi-Hat discrimination data are PARTIAL: an intended Hi-Hat channel and same-performance overhead/kit controls exist, but independent Ride-positive labels do not.

Existing material is sufficient to begin research planning and to avoid making live recording a prerequisite. It is not sufficient to claim reliable Ride event recognition or transfer accuracy. **NEW LIVE CAPTURE: NOT_YET_JUSTIFIED for both. EXTERNAL DATASET AUDIT RECOMMENDED before new recording.** No gap has been shown to require newly recorded live material rather than properly documented existing external recordings.

Apply the scientific-minimalism principle: prefer the simpler path when it provides equivalent evidence. Do not confuse postponing a live-capture decision with asserting that these assets can complete all validation stages.

Evidence classes: DOCUMENTED FACT = repository/provider declaration or filesystem/hash observation; INFERENCE = bounded usability assessment; UNKNOWN = insufficient documentary authority. Provider RAW/source names do not certify ADC-original unprocessed samples or event-level identity.

## 2. Locations and authorities inspected

Current state/navigation: `AGENTS.md`; `artifacts/JGA_BOOTSTRAP.md`; `docs/JGA_PROJECT_STATE.md`; `docs/JGA_ROADMAP.md`; `docs/ROADMAP.md`; `docs/project/PROJECT_METADATA.md`; `docs/scientific/README.md`; `docs/scientific/JGA_RIDE_FIRST_TIMING_RESEARCH_DECISION_20260910.md`. These remain unchanged. Current task authorizes only this audit and does not change the Ride-first roadmap.

Repository search covered validation/provider/input/analytical authorities and manifests, scientific dataset records, prior reports, recording/catalog records, and legacy reference-case documentation. Relevant roots:

- `validation/CED-VAL-002-SWING/`, `validation/CED-VAL-003-SWING-3-4/`, `validation/CED-VAL-004-PHYSICAL-ONSET/`;
- `validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/` and `validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/`;
- `validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/`, `validation/CED-VAL-008-VARIABLE-TEMPO-BENCHMARK/`;
- `validation/CED-VAL-010-SPEKTAKULATIUS-IS-YOU-IS/` and `validation/BASS-RECOVERY-EVIDENCE-SYNTHESIS-20260902/` for CED-VAL-009/010 provenance gaps;
- `validation/VAL-001/` accepted EME/map/recurrence and controlled lineage; `docs/scientific/controlled_datasets/`; `recordings/validation/` and legacy recordings;
- `tests/validation/JGA_REFERENCE_CASES.md`: desired Ride examples, not a checksum-bound recorded dataset or completed result.

External discovery covered `/Volumes/SSD Track/JGA/datasets/` families 002–010, `experiments/`, `stems/`, and the remaining storage roots. A read-only filename inventory found 129 dataset audio files, 14 experiment audio files and seven legacy dummy stems; these totals include non-target instruments, duplicates, controls and derived audio. Another 42 audio files under software environments are fixtures, not admitted project source evidence. Cache/temporary/software trees and AppleDouble sidecars are not scientific candidates. Archives are not extra takes; no ZIP was extracted or audio copied. Repository controlled material was inspected through its provenance, not analyzed.

There is no `validation/CED-VAL-009-JESPER-BUHL-TRIO/` directory. Its external raw package/readme exists; the evidence-synthesis authority-gap record is the navigation authority. A missing standalone manifest is retained as a limitation.

No broad internet search or external acquisition was performed. The already documented Cambridge and LEWITT sources are navigation leads only; an external dataset audit is proposed, not completed.

## 3. Counting rule and original candidate inventory

Counts refer to **physical files with documented target-facing original channel intent**, not actual labelled events or independent performances. The primary cohort has five unique files: four overheads (potential Ride and Hi-Hat evidence) and one Hi-Hat spot. Thus **four primary Ride candidates; five primary Hi-Hat candidates; zero original dedicated Ride channels; one original dedicated Hi-Hat channel; four original overhead candidates**. Ride presence in an overhead is not established by its name.

Supplementary material is counted separately: four whole-band room channels; fourteen separated Drum files; two legacy target-named files of unknown origin; controlled/rendered Drum assets and mix references. These must not inflate the primary or independent-session counts. A Hi-Hat spot may contain Ride bleed but is not counted as a Ride-positive candidate. No dedicated Ride channel was documented anywhere in the inspected source populations.

Exact path prefixes:

| Prefix | Absolute directory |
|---|---|
| P5 | `/Volumes/SSD Track/JGA/datasets/CED-VAL-005-REAL-JAZZ-MULTITRACK/raw/MaurizioPagnuttiSextet_AllTheGinIsGone_Full/` |
| P6 | `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw/` |
| P9 | `/Volumes/SSD Track/JGA/datasets/CED-VAL-009-JESPER-BUHL-TRIO/raw/MR0804_JesperBuhlTrio_Full/` |
| P10 | `/Volumes/SSD Track/JGA/datasets/CED-VAL-010-SPEKTAKULATIUS-IS-YOU-IS/Spektakulatius_IsYouIsOrIsYouAint_Full/` |

Full path = prefix + exact filename. Audio formats below are inherited metadata, not newly measured headers.

| ID | Exact file | Primary type | Format / duration | Source and event authority |
|---|---|---|---|---|
| O5 | P5 + `09_Overheads.wav` | C. ORIGINAL OVERHEAD / CYMBAL MIX | Signed 24-bit PCM WAV, 44,100 Hz, stereo; 10,068,072 frames; 119858/525 s | Provider overhead intent; TRACK_LEVEL_ONLY for broad kit, NO_EVENT_IDENTITY for Ride/Hi-Hat |
| H5 | P5 + `05_HiHat.wav` | A. ORIGINAL DEDICATED SPOT CHANNEL | Same scope/rate/encoding as O5; mono | Provider HiHat intent; TRACK_LEVEL_ONLY. Dedicated means intended channel, not isolation. |
| O6 | P6 + `Dums Overheads LCT 640 TS-Dual Output Mode.wav` | C. ORIGINAL OVERHEAD / CYMBAL MIX | Signed 24-bit PCM WAV, 48,000 Hz, two channels; 11,912,868 frames; 248.184750 s | Provider setup corroborates overhead role; no component event labels |
| O9 | P9 + `04_Overheads.wav` | C at provider raw-package declaration level | Readme: 24-bit/44.1 kHz WAV; per-file channels, duration/encoding detail UNKNOWN | Raw multitrack/readme plus name; no standalone recovered admission or component labels |
| O10 | P10 + `03_Overheads.wav` | C. ORIGINAL OVERHEAD / CYMBAL MIX | Provider 24-bit/44.1 kHz WAV; protocol records two channels, 9,119,107 frames; duration represented by 9119107/44100 s | Prior protocol explicitly says provider-labelled Drum material; no component labels |

Do not merge the stereo channels of O6 conceptually into two independent cymbal microphones: the filename documents dual-output mode. Exact geometry still requires independent documentation.

## 4. Provenance matrix — applies to every primary candidate

| Field | O5 / H5 | O6 | O9 | O10 |
|---|---|---|---|---|
| Provider/session | Cambridge Mixing Secrets; Maurizio Pagnutti Sextet, “All The Gin Is Gone” | LEWITT live COSMIX session, Vienna | Cambridge-referenced Jesper Buhl Trio, “What Is This Thing Called Love” | Cambridge-referenced Spektakulatius, “Is You Is Or Is You Ain't” |
| Original/derived | Supplied raw multitrack, not JGA separation | Provider-declared RAW supplied multitrack | Readme declares raw multitrack | Readme and prior protocol declare supplied multitrack |
| Performer identity | Individual drummer not established in inspected authority; band name is not a performer roster | Individual drummer not established | Individual drummer not established | Individual drummer not established |
| Recording environment | Provider transcription says live/direct, musicians in separate rooms; Artesuono contributor credit does not alone establish location | Provider declares COSMIX Studios Vienna, live band | Room/studio/date UNKNOWN | Room/studio/date UNKNOWN |
| Microphone model | O5 and H5 UNKNOWN | LEWITT LCT 640 TS, dual-output overhead | UNKNOWN | UNKNOWN |
| Position | Overhead/HiHat intent only; distances/angles UNKNOWN | Overhead role; provider says video shows initial placement; numeric geometry not established | Overhead intent only | Overhead intent only |
| Chain | PI-preserved provider transcription: Pro Tools / Digi 192; exact preamps/settings/clock topology UNKNOWN | Recorder/preamps/routing/clock topology UNKNOWN | UNKNOWN | UNKNOWN |
| Processing | Beginnings/endings cleaned, no quantization/warp declared; possible small alignments; exhaustive EQ/compression etc UNKNOWN | Provider says no editing/no tuning and RAW; exhaustive processing/transfer history UNKNOWN | UNKNOWN beyond raw-package declaration | UNKNOWN beyond raw-package declaration |
| Rights | Educational use; commercial use requires express permission; supplied copyright holder retained | Supplied rights PDF: attribution for public release, no commercial exploitation, owner rights reserved | Educational only; commercial use needs permission | Educational only; commercial use needs permission |
| Clock / temporal authority | Immutable distributed sample coordinates; later declaration strengthens same-performance capture; exact acquisition/sample-zero mapping still unestablished | Immutable per-file coordinates; same-performance declaration; exact acquisition clock/origin unestablished | File existence; recovered calibrated/session timing authority absent | Exact per-file coordinates for admitted protocol input; no common acquisition clock or event timing GT |
| Ride model/diameter/weight/material | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Hi-Hat model/top-bottom pair | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Stick/brush/mallet, tip/shoulder | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Bow/bell/edge and Hi-Hat zone | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Open/closed/half-open; pedal closure | UNKNOWN, including H5 | UNKNOWN | UNKNOWN | UNKNOWN |
| Articulation/dynamic conditions | No independently labelled conditions | No independently labelled conditions | No independently labelled conditions | No independently labelled conditions |
| Repeated target events | Not established at Ride/Hi-Hat level | Not established at Ride/Hi-Hat level | Not established | Not established |
| Component onset/offset/choke/damping labels | NONE FOUND | NONE FOUND | NONE FOUND | NONE FOUND |

Rights statements are documentary limits, not new legal opinions. Educational availability does not authorize unrestricted redistribution or commercial model/software-development use. A future use must be checked against the actual supplied permissions; no missing permission is invented.

Authorities: families 005/006 `INPUT_AUTHORITY.md`, `ANALYTICAL_INPUT_AUTHORITY.md`, `input_authority_manifest.json`, `analytical_input_authority.json`; 005 `provider_evidence/PE-CEDVAL005-AMERIO-ACQUISITION-DECLARATION-01.md`; P9/P10 `Readme.txt`; 010 `upper_partial_harmonic_replication_20260901_01/protocol.json`. The later Amerio declaration supplements rather than overwrites the earlier simultaneous-capture uncertainty. Its original correspondence/header custody is unavailable; it is a PI-supplied transcription.

## 5. Supplementary original channels and controls

Four P6 room files are present: `ROOM LEFT LCT 640 TS.wav`, `ROOM RIGHT LCT 640 TS.wav` (two channels each), `Room Mono LCT 550.wav`, `Room Mono MTP 550.wav` (mono). All share documented 48 kHz, signed 24-bit PCM and 248.184750-second scope. They are original whole-band room captures, **H. UNKNOWN within the requested kit-specific type taxonomy**, not source-separated and not silently classified as isolated cymbal or full-Drum-only mixes. Their origin is documented; exact target content/dominance is unknown. Supporting microphone models follow filenames/provider manifest; positions/calibration unknown. Event identity: NO_EVENT_IDENTITY. These four are supplementary capture/transfer references, not four extra confirmed target examples.

Potential kit confound channels, primary type A at provider-intended spot-channel level (bleed unestablished), are:

- P5: `01_KickIn.wav`, `02_KickOut.wav`, `03_SnareUp.wav`, `04_SnareDown.wav`, `06_Tom1.wav`, `07_Tom2.wav`, `08_Tom3.wav`.
- P6: `Kick DTP 640 REX Condenser Capsule.wav`, `Kick DTP 640 REX Dynamic Capsule.wav`, `Snare MTP 440.wav`.
- P9: `01_KickInside.wav`, `02_KickBeater.wav`, `03_Snare.wav`.
- P10: `01_Kick.wav`, `02_Snare.wav`, `04_Toms.wav`.

These are 16 intended confound-channel files, not 16 independent negative-example authorities. Ride/Hi-Hat absence is not established; a target may bleed into them. They may help future independent source-dominance qualification in the same session. No Crash spot/isolated confound set was documented. No source subtraction or new mix is authorized.

## 6. Derived, synthetic and unresolved material

Fourteen path-distinct `drums.wav` outputs are listed in Appendix B. All are **F. JGA / DEMUCS / OTHER SOURCE-SEPARATED STEM**, not original GT. Twelve are CED-VAL-006 prior separation experiments and two are its later htdemucs_6s operational runs. Replays are not new performances; algorithm differences are not cymbal variability. Processing provenance remains experiment-specific. These can be complementary robustness/transfer material only after independently labelled originals exist. Source key `drums` is not Ride/Hi-Hat identity. No RX Ride/Hi-Hat output authority was found; inspected RX material concerns Bass and is not counted as cymbal evidence.

The CED-VAL-006 controlled mixdown and CED-VAL-010 controlled mix are JGA-derived multi-source mixes, not provider original Drum-only audio. They are supporting mixture references; the requested kit-only asset taxonomy does not fit them, so type H with documented derived-mix provenance, not a fabricated original D/E classification. Exact mix definitions live in 006 `controlled_mixdown_authority/source_manifest.json` and 010 attack-observability `protocol.json` / external representation authority. They do not supply component labels.

Controlled/rendered **G. SYNTHETIC / RENDERED SOURCE** candidates/control families:

- `recordings/validation/stems/drums.wav` and canonical controlled VAL-001 provenance; component-to-render event authority is not established by the accepted global EME/recurrence result. The MusicXML instrument roster inspected here declares “Drum Set (Jazz)”, not a validated event-to-Ride/Hi-Hat mapping. No notation-based labels were created.
- External 002 `steams/CED-VAL-002-swing_drums.wav`; 003 `steams/CED-VAL-003-SWING-3-4_drums.wav`: score/render/observation records are available, but inspected authority does not establish the needed real component identity. The 003 physical-authority gate explicitly excludes Drum-component identity.
- External 004 `renders/CED-VAL-004-CANONICAL DRUMS.wav`, `CED-VAL-004-RENDER-01 DRUMS.wav`, `CED-VAL-004-CONTROL-DRUMS.wav`: generation authority identifies Ableton Simpler with `00DB_Kick_2.aif`; scheduled events and silent control do not supply cymbal positives. These are kick/silence methodological controls. Collected sample and duplicate imports are not new instruments or sessions.
- External 007 `raw/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK-v0.1 DRUM GT.wav`; 008 `raw/CED-VAL-008-VARIABLE-TEMPO-BENCHMARK-v0.1  DRUM GT.wav` (two spaces): symbolic schedules and preserved Live sets do not establish Ride/Hi-Hat identity or physical strike time. “DRUM GT” does not imply component GT. Future routing/sample-map verification could establish bounded synthetic labels, not real-cymbal class validity. Reference tempo values are not used in this audit.

These eight named rendered Drum files include replays and silence, not eight positive cymbal examples. Other marker/effect returns are not source identity. Earlier controlled variants and synthetic numerical fixtures remain methodological controls, not independent real performances.

`/Volumes/SSD Track/JGA/stems/legacy_dummy_stems/Ride.wav` and `Hi-Hat.wav`: **H. UNKNOWN**, EVENT_GT = NO_EVENT_IDENTITY. No original parent, generating instrument, trustworthy labels, rights, chain or prior admitted measurement was recovered. Do not upgrade them to synthetic or real solely from directory/name. Legacy whole-recording MP3s and software-environment samples similarly have no admissible component-event authority for this task.

## 7. Bleed and event-level GT

No primary asset has independently established bleed-free isolation or quantitative Ride/Hi-Hat source dominance. H5's track intent is useful, but a transient in that channel could be another component. O5/O6/O9/O10 observe a kit/cymbal projection; presence and dominance of Ride are not documented per event. Room separation between musicians does not isolate cymbals within a kit. No existing measurement was found that quantifies contamination specifically for these target channels.

Zero bleed is not required by default. A source-dominant capture could support bounded observations if target identity, dominance limitations, overlap and uncertainty had independent authority. No dominance ratio/threshold is invented here. Estimating the loudest transient or detecting coincidences between channels cannot independently create its own source GT.

| Dataset | Ride event authority | Hi-Hat event authority | Possible documentary route without listening labels |
|---|---|---|---|
| 005 | NO_EVENT_IDENTITY | TRACK_LEVEL_ONLY | Recover provider event/session annotations or independently documented action/isolation records. Spot channel alone insufficient. |
| 006 | NO_EVENT_IDENTITY | NO_EVENT_IDENTITY | Supplied `Cosmix Video.mov` may contain visual action evidence, but view/sync/occlusion and frame uncertainty need a separately approved annotation protocol; no video inspected or labels made here. |
| 009 | NO_EVENT_IDENTITY | NO_EVENT_IDENTITY | Recover missing original metadata/annotations and file authority; package names cannot decide events. |
| 010 | NO_EVENT_IDENTITY | NO_EVENT_IDENTITY | Existing protocols label broad original channels; Bass/Piano anchors are not component GT. |
| Controlled 001/002/003 | NO_EVENT_IDENTITY for these components under inspected authority | Same | Score/device-routing/sample mapping may permit future conditional synthetic event labels, not granted now. |
| Controlled 004 | No target positives; kick source schedule documented | Same | Use only as non-target/control authority within its render scope. |
| Controlled 007/008 | NO_EVENT_IDENTITY for these components | Same | Saved device/routing verification needed before any conditional component claim. |
| Separated / legacy | NO_EVENT_IDENTITY | NO_EVENT_IDENTITY | Separator label or filename cannot independently establish event identity. |

No dataset is assigned EVENT_GT_STRONG or EVENT_GT_CONDITIONAL for actual Ride/Hi-Hat events now. At dataset level 005 supports TRACK_LEVEL_ONLY Hi-Hat intent; other original overheads provide only broad Drum track intent. Pedal/open/closed identity, offsets and physical onset uncertainty remain absent. Preserved global EME are observations, not component-event truth.

## 8. Candidate observability potential — not a frozen ontology

| Candidate phenomenon | Existing support / limitation |
|---|---|
| Ride impact/broadband attack, envelope, centroid/high-frequency evolution | Original O5/O6 waveforms could support future mixed-channel measurements; attribution to Ride is unestablished. PCM bandwidth is not calibrated microphone response or proof of useful signal. |
| Ride inharmonic/modal structure, decay, modulation/beating, noise-like content | Potentially retained in overhead audio, but overlapping excitation, other cymbals and room decay can confound source-specific estimates. No independent mode or damping measurement exists. |
| Ride bell/bow/edge, tip/shoulder, stick contrasts | No independently labelled contrast found. |
| Ride long free decay / choke | No documented isolated onset-to-decay/choke sequence; song duration does not guarantee an unobscured tail. |
| Hi-Hat attack, metallic/noise structure, high-frequency distribution, envelope | H5 provides the best intended-source channel for initial conditional observation; contamination and transfer remain unresolved. |
| Hi-Hat open/closed/half-open contrast; decay/sustain suppression | No state-conditioned labels or isolated contrasts found, even in H5. |
| Hi-Hat pedal closure/opening modulation/top-bottom interaction | Physical cause not identifiable merely from one noisy channel; no pedal/action authority found. |
| Dynamics, articulation and capture dependence | Real performance variation is possible, but not a controlled labelled manipulation in these records. |

This is acoustic observability potential, not established source-specific fidelity. Standard centroid/flux descriptors are not an instrument identity model. No Bass harmonic representation is presumed appropriate for inharmonic cymbals.

## 9. Identity-research value, variability and transfer

| Use | O5/H5 | O6 + rooms | O9/O10 | Derived/rendered/legacy |
|---|---|---|---|---|
| Positive examples | H5: conditional channel intent; Ride positive unknown | Component positives unknown | Component positives unknown | No real target authority |
| Negative/contrast examples | Same-session kick/snare/toms potentially useful, target absence unknown | Same limitation | Same limitation | 004 kick/silence bounded synthetic controls only |
| Ride-vs-Hi-Hat discrimination | Strongest partial pairing: H5 versus O5, not labelled opposite classes | No dedicated Hi-Hat/Ride pair | No dedicated pair | Not a substitute for independent positives |
| Within-class / dynamics / articulation variability | Not established as class-labelled conditions | Not established | Not established | Algorithm/render repetition is not class variability |
| Between-player / instrument variability | Multiple sessions exist across families, but drummer/cymbal identities not bound | Same | Same | No independence from copied input |
| Capture variability | Mono spot versus stereo OH, same session | Documented overhead and room models; geometry unknown | Other overhead files, models unknown | Processing differences documented, confounded with source/chain |
| Real-mix transfer | Strong contextual material after independent labels | Strong live-session contextual material | Useful conditional references; 009 provenance weaker | Separated/controlled mixes complementary, never primary GT |

The four real packages document different named sessions/ensembles, not necessarily independently identified cymbals, players or stick sets. Instrument brand/model/diameter/weight, dynamic labels, articulation, zone, pedal state and repeated target-event counts are unknown. Differences between H5 and O5 cannot be attributed solely to instrument class: microphone transfer and source mixing differ. No invariance is established.

A later transfer validation requires target-present and target-absent/ambiguous passages, overlapping confounds, independent event labels and timing uncertainty, withheld sessions/instruments/capture conditions where claimed, and abstention. Existing music is reusable as test material; it is not already a scored test set. Strongest Ride contextual source is O6 for provider setup/live provenance, with O5 valuable for same-session H5 contrast. O9 is weaker due to missing independent admission details.

## 10. Prior measurement reuse

| Existing authority | Reuse classification | Bounded contribution / exclusion |
|---|---|---|
| 005/006 input and analytical manifests | DIRECTLY_REUSABLE | File identities, prior PCM metadata and documented source/processing/clock limits; no component identity. |
| 005/006 timing/profile and 006 operational acceptance | PARTIALLY_REUSABLE | Source/EME lineage and file-local timing; generic Drum detections do not label Ride/Hi-Hat or validate transient accuracy. |
| VAL-001 accepted complete map and exact-witness audit | CONCEPTUALLY_RELATED | Preserved global timing evidence and lineage can be joined only after independent component identity exists. No component claims or new timing use here. |
| 010 `bass_piano_spectrotemporal_timbre_20260902_01/REPORT.md` | CONCEPTUALLY_RELATED | Known BassDI/Piano/BassMic source-conditioned spectral/temporal methodology; 206 windows per label, 20 endpoints, replay. Not cymbal measurements or transferable harmonic-feature authority. |
| 010 `event_blind_attack_timbre_observability_20260902_01/REPORT.md`, protocol and external representation authority | PARTIALLY_REUSABLE as mixed-channel evidence only | Frozen mixed-input STFT power, 2048-sample Hann frames, 256 hop, FFT4096, 0–8 kHz; four attack observables with availability. No Ride/Hi-Hat attribution; omitted >8 kHz evidence not recoverable from this representation. |
| 010 local-spectral-evolution and upper-partial reports | CONCEPTUALLY_RELATED | Bass-oriented correspondence/harmonic hypotheses; no inharmonic Ride modal authority or Hi-Hat state labels. |
| 004 scheduled kick/marker render authority | PARTIALLY_REUSABLE | Numerical scheduling/render controls; not physical cymbal timing or source identity. |
| 007/008 tracker benchmark scores | NOT_REUSABLE for target identity | Temporal reference/tracker results do not establish component identity; not inspected to supply a timing answer. |
| Legacy Ride “reference cases” / dummy names | NOT_REUSABLE as scientific identity evidence | Aspirational descriptions or unbound filenames, no source-event authority. |

No independently validated Ride-specific or Hi-Hat-specific spectral/temporal measurement population was found. Existing numeric results were not regenerated or applied to new audio. No stored NPZ was analyzed in this task.

## 11. Sufficiency and minimum missing identity evidence

**Ride C:** real overhead material can complement research and later real-world validation, but no independent positive Ride-event authority is established. Some individual assets, particularly O9 and legacy files, have E-level provenance limitations.

**Hi-Hat B:** H5's documented original intended-source channel supports initial bounded observability research without a new session, but does not supply controlled identity training/evaluation or certified open/closed/pedal discrimination. “B” here uses the initial-observability branch of the level definition, not a claim that conditional event discrimination has passed.

The smallest eventual evidence requirement for Ride-conditioned timing is a bounded source/event validity contract: independently identified Ride positives and Hi-Hat/Crash/snare/other dominant confounds; explicitly scoped articulations/capture conditions; held-out identity/event evaluation with false attribution, missed/overlapped events and abstention; and file/event timing authority sufficient for the later timing claim. Source identity uncertainty and event-time uncertainty must both survive. No universal classifier, complete cymbal taxonomy or zero-bleed requirement is necessary initially. No reliability threshold is invented; source name, flux peak or rhythmic regularity cannot serve as its own identity authority.

Hi-Hat remains secondary/complementary, never mandatory BeatReference. Recognition and any future fallback need their own validation; no fallback logic is proposed here.

## 12. Gap resolution and live-capture decision

EXISTING_EXTERNAL_DATASET below means a route to audit, **not** a verified dataset already satisfying the requirement. UNKNOWN is retained where no existing authority was located. New recording is a possible last route, never established necessary by these gaps alone.

| Gap category | Present evidence | Preferred resolution / current certainty |
|---|---|---|
| MISSING_RIDE_POSITIVE_EXAMPLES | Potential OH content, no certified event positives | EXISTING_EXTERNAL_DATASET audit; UNKNOWN whether internal provider/video evidence can close it |
| MISSING_HIHAT_POSITIVE_EXAMPLES | H5 intended-source examples only | EXISTING_INTERNAL_ASSET for channel observability; EXISTING_EXTERNAL_DATASET audit for independent event positives |
| MISSING_NEGATIVE_CONTROLS | 16 original spot-control files, synthetic kick/silence; target absence unproved | EXISTING_INTERNAL_ASSET partial; EXISTING_EXTERNAL_DATASET audit for Crash/other cymbal negatives and absent-target labels |
| MISSING_EVENT_GT | No qualified Ride/Hi-Hat event catalogue | EXISTING_EXTERNAL_DATASET / recover provider annotations; UNKNOWN pending provenance review |
| MISSING_WITHIN_CLASS_VARIATION | Performance streams without target labels | EXISTING_INTERNAL_ASSET if independent labels recovered; otherwise EXISTING_EXTERNAL_DATASET audit |
| MISSING_BETWEEN_INSTRUMENT_VARIATION | Different sessions, cymbal identities unknown | EXISTING_EXTERNAL_DATASET audit; necessary only for declared generalization |
| MISSING_ARTICULATION_VARIATION | No zone, pedal or opening labels | EXISTING_EXTERNAL_DATASET audit; not every articulation required for first bounded scope |
| MISSING_DYNAMIC_VARIATION | No controlled dynamic labels | EXISTING_EXTERNAL_DATASET audit or existing provider metadata; UNKNOWN |
| MISSING_CAPTURE_PROVENANCE | 005/006 partial; 009/010 less complete | EXISTING_INTERNAL_ASSET/provider-record recovery first; external dataset audit if insufficient |
| MISSING_ISOLATION / SOURCE_DOMINANCE | Unknown target contamination | EXISTING_INTERNAL_ASSET may permit future independent qualification; no current measurement. External documented isolated/dominant recordings preferred. |
| MISSING_REAL_MIX_TRANSFER | Existing multitracks/live music | EXISTING_INTERNAL_ASSET provides material; independent labels/rights still required |
| MISSING_INDEPENDENT_AUTHORITY | No target-source event evaluator authority | EXISTING_EXTERNAL_DATASET/provider logs/validated recording annotations; UNKNOWN until inspected |

A NEW CONTROLLED RECORDING becomes warranted only after a specific required source/articulation/provenance condition cannot be filled by existing admitted material. The present evidence does not establish that circumstance for Ride or Hi-Hat.

## 13. External audit requirements and next action

EXTERNAL DATASET AUDIT RECOMMENDED. First inspect existing-source provider documentation/annotation availability, then existing datasets with:

- Real original Ride and Hi-Hat audio, explicit cymbal/component and event labels supplied independently of the proposed JGA measurements; documented onset/offset authority and uncertainty, not merely named stems.
- Isolated or independently characterized source-dominant events, and relevant negatives, with declared overlapping-event handling and absent/uncertain labels.
- For Hi-Hat, separately documented stick/pedal and open/closed state where included in the intended scope; for Ride, zone/excitation labels where the scope requires them.
- Traceable instrument/player/session/capture/processing metadata, lossless original files, integrity records and rights appropriate to the intended research/software-development use.
- Enough independently identified sessions/instruments to test whatever generalization is claimed; controlled samples plus compatible real mixtures if available. No fixed sample count is selected here.

Cambridge Mixing Secrets and LEWITT are already documented source leads, but their current JGA packages do not themselves meet all these conditions. No new external dataset is claimed qualified, and no acquisition occurred.

Exact recommended next action requiring PI authorization: a bounded external-dataset/event-label authority audit before live-capture planning, while the already authorized Ride physical/perceptual research-design preparation remains a separate next task. This audit does not autonomously begin either task or authorize recording, classifiers or timing execution.

RECURRENCE != BEATREFERENCE; source identity != musical role. Global recurrence evidence and all Double-Bass work remain unchanged. STOP FOR PI REVIEW.

## Appendix A. Asset integrity and documentary provenance

The five primary files were byte-hashed during this audit. Four matched existing authorities; O9 obtains only a current byte identity, not retroactive provider authenticity or missing metadata.

- O5: `/Volumes/SSD Track/JGA/datasets/CED-VAL-005-REAL-JAZZ-MULTITRACK/raw/MaurizioPagnuttiSextet_AllTheGinIsGone_Full/09_Overheads.wav`; SHA-256 `0569a396cff95b130042fc71093e8ba3460e3c0fe0034cb86d2158027d585f3a`; existing authority verified.

- H5: `/Volumes/SSD Track/JGA/datasets/CED-VAL-005-REAL-JAZZ-MULTITRACK/raw/MaurizioPagnuttiSextet_AllTheGinIsGone_Full/05_HiHat.wav`; SHA-256 `0e0801cf3d57c06b524aea3e497520f79afe0e7b10401e4cb6f46654ce227253`; existing authority verified.

- O6: `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw/Dums Overheads LCT 640 TS-Dual Output Mode.wav`; SHA-256 `dbfc4c3c59cac2c42cb2bbd33f1e55dbb1ec8c2fe6c6d095e30efc791dd57b8d`; existing authority verified.

- O9: `/Volumes/SSD Track/JGA/datasets/CED-VAL-009-JESPER-BUHL-TRIO/raw/MR0804_JesperBuhlTrio_Full/04_Overheads.wav`; SHA-256 `573ed86d61717c40c32ca71bccb2bba98e99a01602b28d9a0a27ff3d5b97d884`; current byte identity only; no recovered prior checksum.

- O10: `/Volumes/SSD Track/JGA/datasets/CED-VAL-010-SPEKTAKULATIUS-IS-YOU-IS/Spektakulatius_IsYouIsOrIsYouAint_Full/03_Overheads.wav`; SHA-256 `f3f6712be5713fb62336e2ff6a5e573d38934c72a7acace2f63b4d2b1a7ae0c6`; existing authority verified.

Room-file checksums are documented in the CED-VAL-006 manifest; these supplementary files were not newly decoded or rehashed. P9 duration/encoding details remain unknown despite its newly recorded byte identity.

## Appendix B. Separated Drum-file inventory

These are 14 physical paths, not 14 independent source performances. All type F, NO_EVENT_IDENTITY, complementary only. Source-level rights inherit the parent package; no new rights are inferred. Per-file processing, numeric format and hashes must be taken from the named historical separation authorities before later admission; no audio analysis or re-separation is performed here.

1. `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE1-01/B_run_1/htdemucs/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/drums.wav`

2. `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE1-01/B_run_2/htdemucs/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/drums.wav`

3. `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE1-01/C_run_1/htdemucs/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/drums.wav`

4. `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE1-01/C_run_2/htdemucs/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/drums.wav`

5. `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE2-01/M1_run_1/htdemucs_ft/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/drums.wav`

6. `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE2-01/M1_run_2/htdemucs_ft/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/drums.wav`

7. `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE2-01/M2_run_1/htdemucs_6s/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/drums.wav`

8. `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE2-01/M2_run_2/htdemucs_6s/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/drums.wav`

9. `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE2-01/M3_run_1/mdx_extra/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/drums.wav`

10. `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-BASS-PRESERVATION-PHASE2-01/M3_run_2/mdx_extra/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/drums.wav`

11. `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01/separation_run_1/htdemucs/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/drums.wav`

12. `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/derived/EXEC-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01/separation_run_2/htdemucs/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1/drums.wav`

13. `/Volumes/SSD Track/JGA/experiments/CEDVAL006-AD041-HTDEMUCS6S-OPERATIONAL-20260907/run_1/drums.wav`

14. `/Volumes/SSD Track/JGA/experiments/CEDVAL006-AD041-HTDEMUCS6S-OPERATIONAL-20260907/run_2/drums.wav`

Authority navigation: CED-VAL-006 controlled-mixdown/source manifests, Bass-preservation phase 1/2 and controlled-mix-separation records, plus `validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/demucs_operational_reintroduction_20260907/separator_authority.json` and README. Per-run copies preserve replay, not population expansion.

## Appendix C. Documentary checksums and verification boundary

Current documentary byte identities (not new scientific validation):

- `docs/JGA_PROJECT_STATE.md`: `46721acf6cc99cc644fb8588bc279b96255c1dc8ec7bb1cb75e1b10b3dcbee04`.

- `docs/JGA_ROADMAP.md`: `157a4a56c8ffa39a9a8b38b1ec24026ea7ac5ecdb7e473dd7982af70fd9ae67a`.

- `docs/ROADMAP.md`: `df85792bda411b30f5a6454cf2aafce62f071bab9446d3c3a5d2f5dca4b7ec86`.

- `docs/project/PROJECT_METADATA.md`: `3e069ed1b622d4e42541e32fb5243dabb066562ccdc04e5327f8e7a63adbd56c`.

- `docs/scientific/README.md`: `d7175da0e777a4a4e56977a5c241c39755d8e542bef7c20b1cc5e7aa41daaf09`.

- `docs/scientific/JGA_RIDE_FIRST_TIMING_RESEARCH_DECISION_20260910.md`: `610b115b374af839b0e0821101f6c24f3ffdb5d748c8a7038664ae5eb4d8c50c`.

- `validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/input_authority_manifest.json`: `8248368cf1ab4bdb104b5eeff37be0a28a283af68e76e07c8f622a3fbe844b46`.

- `validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/input_authority_manifest.json`: `c96ad3bac2b8dbc9e5a949ae13c5a0a65a47c89bd09f8a9c369551bada12e72b`.

- `validation/CED-VAL-010-SPEKTAKULATIUS-IS-YOU-IS/upper_partial_harmonic_replication_20260901_01/protocol.json`: `19ff7e59eb7f96fdf486b81ba8edd8acf624e8d8a71ebfe6adaa2be41d97ffd4`.

No tracked file differs from its starting state because of this audit. Existing user plot/score modifications and historical deletions were untouched. Only this new report was created; no commit or push. Documentary/hash checks are the only verification performed, not source-observability tests.
