# Ride / Hi-Hat simplified empirical research design

Identifier: RH-SIMPLIFIED-DESIGN-01. Date: 2026-09-10.
Status: **RESEARCH/DESIGN COMPLETE FOR PI REVIEW; NOT AN EXECUTABLE PREREGISTRATION.**
Repository: `scientific/translation-layer-finalization`, HEAD `13f391be8e8ae512c171e79e93f07b7a9ffca37e`.

## 1. Decision, authority and scope

**PI Decision:** Use existing discrimination science and labelled datasets before creating a longer research chain. A comprehensive Ride physical/perceptual Identity Card is not a prerequisite for this initial empirical test. This document does not create a Ride ontology or amend the roadmap, accepted timing evidence, or Double-Bass work.

**Observed Fact:** Both prerequisite audits were read and their SHA-256 values verified:

| Authority | SHA-256 |
|---|---|
| `docs/scientific/rfc/RIDE_HIHAT_EXISTING_ASSET_SUFFICIENCY_AUDIT.md` | `7c1fd3e86a8279183fa2d17ec11f06ee4de4ddd459c0280b355f0e06f0ded15a` |
| `docs/scientific/rfc/RIDE_HIHAT_EXTERNAL_DATASET_EVENT_AUTHORITY_AUDIT.md` | `7fec3be42e9a14b652b80a47aa77eac4b34e25ed0b8fc6b620682f183f833abe` |

Startup authority: `AGENTS.md`, `artifacts/JGA_BOOTSTRAP.md`; governing references include `docs/JGA_DEVELOPMENT_CONSTITUTION.md`, `docs/scientific/foundations/JGA_KNOWLEDGE_MODEL.md`, and `docs/scientific/JGA_RIDE_FIRST_TIMING_RESEARCH_DECISION_20260910.md`. The new PI direction narrows the next research task; it does not contradict an executed identity result. No such result exists. Core → Translation → Domain and observation before musical interpretation remain binding.

Evidence terms: **Observed Fact** means inspected documentation or an attributed published result; **Logical Inference / Proposal** means this design's assessment, not experimental evidence; **UNKNOWN** means unresolved authority. Internal Ride C / Hi-Hat B and absent Ride / track-only Hi-Hat event authority remain unchanged. External documentary sufficiency does not itself admit downloaded inputs.

**Logical Inference:** A small event-local spectral experiment is justified. Literature establishes feasibility, not a universally sufficient individual descriptor or a high-confidence JGA admission operating point. New live capture remains NOT_YET_JUSTIFIED.

## 2. Focused review method and primary references

Reviewed evaluated cymbal classification and multi-class drum transcription, prioritizing studies separating Ride and Hi-Hat. Inspected methods, splits, tables and limitations; did not substitute aggregate transcription scores for per-class discrimination. Only small papers, pages and repository metadata were retrieved; no audio, datasets, features or models were downloaded or executed. Access date: 2026-09-10.

| ID | Exact primary citation / source |
|---|---|
| L1 | Sofia Cavaco and Hugo Almeida (2012), *Automatic Cymbal Classification using Non-Negative Matrix Factorization*, 19th International Conference on Systems, Signals and Image Processing (IWSSIP), pp. 468–471. [Author-uploaded full text](https://www.researchgate.net/publication/234556814_Automatic_Cymbal_Classification_using_Non-Negative_Matrix_Factorization), §§2–3, Table 1. |
| L2 | Perfecto Herrera, Alexandre Yeterian and Fabien Gouyon (2002), *Automatic Classification of Drum Sounds: A Comparison of Feature Selection Methods and Classification Techniques*, Music and Artificial Intelligence, pp. 69–80, DOI 10.1007/3-540-45722-4_8. [Author-uploaded paper](https://www.researchgate.net/publication/221336295_Automatic_Classification_of_Drum_Sounds_A_Comparison_of_Feature_Selection_Methods_and_Classification_Techniques). |
| L3 | Richard Vogl, Gerhard Widmer and Peter Knees (2018), *Towards Multi-Instrument Drum Transcription*, DAFx-18. [Author manuscript, arXiv:1806.06676](https://arxiv.org/pdf/1806.06676), §§3–4, Table 2 and class plots. |
| L4 | Yu Wang, Justin Salamon, Mark Cartwright, Nicholas J. Bryan and Juan Pablo Bello (2020), *Few-Shot Drum Transcription in Polyphonic Music*, ISMIR 2020. [Author manuscript, arXiv:2008.02791](https://arxiv.org/pdf/2008.02791), §§3–4 and class/polyphony analysis. |
| D1 | Olivier Gillet and Gaël Richard (2006), *ENST-Drums: an extensive audio-visual database for drum signals processing*, ISMIR, pp. 156–159. [Proceedings](https://archives.ismir.net/ismir2006/paper/000027.pdf). Release: [Zenodo 21506051](https://zenodo.org/records/21506051). |
| D2 | Carl Southall, Chih-Wei Wu, Alexander Lerch and Jason Hockman (2017), *MDB Drums: An Annotated Subset of MedleyDB for Automatic Drum Transcription*, ISMIR Late-Breaking/Demo contribution. [Institutional paper](https://www.open-access.bcu.ac.uk/6179/1/Southall2017a.pdf); [original repository](https://github.com/CarlSouthall/MDBDrums). |
| D3 | Original MDB [recursive Git tree](https://api.github.com/repos/CarlSouthall/MDBDrums/git/trees/b29e2d63c3a023506f4bf353c5b2e8a558eed135?recursive=1), tree identity `b29e2d63c3a023506f4bf353c5b2e8a558eed135`; untruncated inventory inspected. This is a Git tree identifier, not a release tag or ordinary SHA-256 file checksum. |

## 3. What evaluated studies actually establish

The following are **Observed Facts attributed to the cited study**. “Independent” below distinguishes held-out sounds from independently sourced evaluation; none validates JGA.

| Study / characteristic and rationale | Dataset / task | Ride result | Hi-Hat result | Evaluation independence and limit |
|---|---|---|---|---|
| L1: spectrogram-derived NMF spectral bases and their activation coefficients, classified by 1-nearest neighbour; learned spectral distinctions among similar metallic sounds | Six physical cymbals, selected zones, different loudnesses; combination E compares Ride bow with closed Hi-Hat bow | Six held-out Ride examples correct | Six held-out closed-HH examples correct; combined E: 12/12 | Separate training/test strikes, six per instrument per set; same specimens. No held-out kit/player or open/pedal HH transfer. FFT 2048 at 44.1 kHz, Hann window, 50% overlap. This is small direct feasibility evidence, not universal accuracy. |
| L2: MFCC means/variances, spectral-band energy and temporal/spectral descriptors; feature selection retains distributed spectral information | Drum sample collection, hierarchical/subclass classification including Ride, Crash, open/closed HH | Not separately quantified by the aggregate result used here | Not separately quantified by that aggregate | Ten-fold evaluation; best reported nine-subclass aggregate 90.7% (K*, CDA selection). Not a Ride-vs-HH precision figure. Selected-feature utility is joint/model-dependent; independent dataset transfer and fully nested feature selection are not established here. |
| L3: logarithmically filtered magnitude spectrogram plus positive temporal difference; local spectral changes feed CNN/CRNN | ENST, MDB, RBMA; 8/18-class transcription | Ride and bell evaluated separately in expanded vocabulary; exact per-class values not transcribed from plots | State-specific classes evaluated; closed/pedal confusion discussed | Held-out tracks; 8-class CNN ENST mean/sum F-measure .59/.63 and MDB .68/.65 are aggregate only. 84 log-frequency bins plus differences, 10 ms hop; CNN uses 25 frames. Long-context recurrent variants do not meet this design's no-rhythm-input constraint. No isolated feature ablation proves necessity. |
| L4: 250 ms log-mel patches with learned embeddings/prototypes preserve local spectral evolution | Synthetic training, real ENST/MDB/RBMA evaluation; few-shot transcription | Class-level evaluation exists, but no single transferable Ride accuracy is claimed here | Same qualification for HH states | Five labelled support examples from the evaluated track adapt inference; removing them from scoring does not make the track unadapted validation. Whole-system macro/micro results are not individual-feature evidence. Co-occurring sounds can bias support examples. This protocol cannot be copied while calling MDB untouched independent validation. |

**Logical Inference:** Distributed spectral shape and short-time evolution have stronger direct empirical support than an isolated brightness or decay rule. L1's tiny but explicit comparison is more specific to the present question than a broad transcription score. L3/L4 establish realistic-task relevance with substantial qualifications. None establishes a precision requirement for later timing admission.

## 4. Minimum candidate representation set

These grades concern justification to TEST a representation, not established Ride identity.

| Candidate | Grade | Initial decision |
|---|---|---|
| Event-local filtered magnitude time-frequency patch, logarithmic amplitude | STRONG_EXISTING_EVIDENCE | **One primary representation.** Retains spectral envelope/energy distribution and attack/early evolution jointly; L1/L3/L4 support this representation family through evaluated systems. |
| MFCC-like compact spectral envelope summaries, with temporal variability | USEFUL_SECONDARY_EVIDENCE | L2 justifies an alternative if the primary test fails or is impractically large. Do not simultaneously add it to the first feature vector. |
| Learned NMF bases or neural embeddings of that patch | USEFUL_SECONDARY_EVIDENCE | Supported complete systems, but extra learning choices. A later model-capacity test may use them; not a second mandatory representation now. |
| Spectral centroid, band energy, flux, early envelope/decay as separate scalars | USEFUL_SECONDARY_EVIDENCE | Related to information retained in the patch; individual cross-kit Ride-vs-HH sufficiency not established. Do not infer a universal long-Ride/short-HH rule. |
| Independent MFCC + centroid + rolloff + flux + envelope feature stack alongside the patch | REDUNDANT_FOR_INITIAL_TEST | Increases selection freedom without necessity demonstrated for this bounded question. |
| Inharmonicity estimator, detailed modal identity, modulation/coherence measurements | INSUFFICIENT_EVIDENCE | No inspected evaluated result establishes these as necessary additions to this initial discrimination test. This is not a claim that the phenomena are irrelevant. |
| Long recurrent context, event intervals, regularity and rhythm templates | REDUNDANT_FOR_INITIAL_TEST; EXCLUDED BY SCOPE | Could exploit temporal organization rather than the struck source; prohibited regardless of transcription utility. |

**Proposed starting design, not a copied validated recipe:** a 250 ms onset-centred log-mel magnitude patch; 44.1 kHz analysis, 2048-sample Hann frames, 441-sample hop. Those temporal scales are motivated by L3/L4; the complete combination is a JGA candidate, not their proven optimum. Mathematical form: `X[b,k] = log(1 + sum_f H[b,f] |STFT(x)[f,k]| / s)` for a fixed mel filterbank H and positive scale s. Filterbank count/range, log scale, edge handling, channel combination and amplitude conditioning must be fixed before training in preregistration. They are engineering bindings, not new physical laws. Do not select them on MDB.

One regularized linear Ride-vs-rest probe is the minimum proposed capacity test. Its simplicity limits what a negative result can establish: failure of this probe does not falsify all audio-based discrimination. No architecture tournament, feature search or threshold sweep on the held-out dataset. A pooled-in-time version of the same patch may be a secondary ablation only if preregistered; it is not required to answer whether the primary patch works.

No absolute track time, filename, performer, channel label, annotation class, event spacing or musical metadata enters the model. Centre time only constructs the crop; it is not a numerical feature. Short crops can still contain other attacks/tails: control and report that confound rather than claiming a perfectly isolated event from a short window.

## 5. Targeted ENST acquisition: binding and unresolved member list

**Observed Fact:** D1 release record is Zenodo v2, published 2026-07-23, archive `enst_drums_v1_1.tar.zst`, displayed size approximately **9.6 GB**, MD5 `a134f0a34d12eb5317ff3ddd7d07b6db`. Archive name and release version differ. This is NOT the estimated size of the required subset. No public archive-member manifest was verified during this review; full per-member paths, sizes and hashes are UNKNOWN. Do not invent them or authorize a 9.6 GB transfer to obtain a few hits.

**Proposal — minimum acquisition specification:**

| Required object | Exact selection rule / role | Binding still required |
|---|---|---|
| Release README/license, member inventory, player/kit/implement mapping, label vocabulary and annotations | Small metadata first; all three player–kit groups | Publisher-authoritative member list and selective delivery URL |
| Original `overhead_L` recordings of isolated single-hit sequences from each player | Same microphone role for ALL classes: Ride `rc`, closed `chh`, open `ohh`, and supplied cymbal/membrane negative hits; initially sticks only | Full member filenames, sequence-to-annotation mapping, per-file bytes/checksums and target counts |
| Matching event-annotation files | Preserve native classes, cymbal numbers, original timestamps and full original sequence | Actual schema/version and annotation-to-channel alignment |
| Recording/sequence metadata | Preserve physical specimen/group and original-sequence lineage; flag missing playing-zone/state information | Member-level inventory |

Choose the left overhead consistently before inspecting acoustic quality, not whichever channel yields greater discrimination. This uses an original, common airborne channel and avoids learning “HH spot microphone versus Ride overhead.” It follows the prior audit's preference for original channels. A dry-mix-only delivery is a possible **explicitly approved substitute**, not an assumed equivalent raw channel: it must be rebound as mixed/level-adjusted evidence before acquisition. Do not download overhead_R, all eight channels, video, wet mixes, MIDI-generated material, accompaniment or long performances for this first controlled study. Do not infer that all 108 published hit sequences are relevant stick/target examples.

Acquire source-controlled negative hits, especially Crash/other cymbals and Snare; membranes are controls, not a new full-kit research objective. Preserve original sequences; later derived crops remain traceable. Do not create source separation or synthetic mixtures to fill a gap in this task.

**Acquisition readiness:** scientific scope justified; executable ENST file manifest **INCOMPLETE**. A metadata-only inventory/delivery resolution is the next necessary step. If the authoritative distributor only offers the whole archive, return its actual transfer requirement to PI rather than treating selective extraction after bulk download as targeted acquisition. This access gap is not evidence that live capture is necessary.

## 6. Exact original MDB acquisition manifest

**Proposal:** use all 23 short drum-only performances as the independent test population, not a target-positive or jazz-only cherry-picked subset. This retains negative events and difficult conditions. Do not acquire original MDB beat files, MDB++, multitrack audio or full mixes initially. Whole-kit drum audio is the first real-performance transfer setting; full-music transfer is a later claim.

D3 binds the following path templates and all 23 basenames in Appendix A:

- Audio: `MDB Drums/audio/drum_only/{B}_Drum.wav`
- Annotation: `MDB Drums/annotations/subclass/{B}_subclass.txt`
- Metadata: `MDB Drums/audio/multi-tracks/{B}/{B}_METADATA.yaml`
- Documentation: repository `README.md`, dataset citation/license statement and preserved D3 inventory.

Metadata-only byte totals: audio **115,433,048**; subclass annotations **131,825**; YAML **30,622**. Required 69 members total **115,595,495 bytes (115.60 decimal MB)**, plus small documentation. Optional later full mixes add **230,865,084 bytes**; combined **346,460,579 bytes** plus documentation. No optional full mix is needed to make the first test independent.

Acquire the exact Git objects referenced by the frozen tree, not an unverified future `master`. Appendix A provides audio blob identifiers; the same immutable tree binds matching annotation/YAML blobs. Git blob SHA-1 includes Git object framing; it is not `sha1sum(file)` or SHA-256. Later admission must verify Git-object identity and record ordinary SHA-256 for every downloaded member. A transport mismatch stops admission. File content/header validation is deferred; this task inspected tree metadata, not audio.

## 7. Licensing and storage

Release-specific documented terms remain those audited previously: ENST Zenodo v2 **CC BY-NC-ND 4.0**; original MDB audio/annotations **CC BY-NC-SA 4.0**. Preserve attribution and source terms. NC use scope must be bound by PI; do not presume commercial JGA or redistributed trained-model clearance. ND/SA restrictions concern applicable shared adaptations; this document does not supply a new legal interpretation. The prior audit §15 provides the detailed authority and unresolved-use questions.

Prospective storage: `/Volumes/SSD Track/JGA/datasets/RIDE-HIHAT-EXTERNAL/ENST-zenodo-21506051/` and `/Volumes/SSD Track/JGA/datasets/RIDE-HIHAT-EXTERNAL/MDB-original-b29e2d63/`, each with `original/`, `metadata/`, `authority/`, and separately governed `derived/`. Preserve publisher names, URLs, retrieval time, license, bytes, checksums and original grouping. No directories or heavy data created now; no audio in Git or unnecessary internal-SSD duplication. Combined initial transfer estimate is **115.60 MB + UNKNOWN ENST selected-audio bytes + small documentation**. Do not present the full archive as the minimum total.

## 8. Labels and annotation authority

| Parent / subtype | Native admissible mapping | Role and limit |
|---|---|---|
| RIDE / RIDE_UNSPECIFIED | ENST `rc` with instance suffix retained; MDB `RDC` | Positive parent; neither certifies bow contact |
| RIDE / RIDE_BELL | MDB `RDB` | Retain subtype; training support in selected ENST is UNKNOWN |
| RIDE / RIDE_BOW | Only explicit provider zone authority if subsequently found | Requested vocabulary reserved; never create from `rc` or `RDC` |
| HIHAT / HIHAT_CLOSED | ENST `chh`; MDB `CHH` | Principal contrast |
| HIHAT / HIHAT_OPEN | ENST `ohh`; MDB `OHH` | Preserve state; principal contrast |
| HIHAT / HIHAT_PEDAL | MDB `PHH` | Preserve, evaluate separately; no ENST stick label invented |
| OTHER / native negative subtype | Crash, Splash, China, Snare and other explicitly annotated controls | China is not automatically Ride; keep native identity |
| UNKNOWN / UNRESOLVED | Unmapped label, unresolved concurrence or deficient provenance | No forced positive/negative label |

**Decision proposed:** preserve subtypes under a common Ride parent; train the initial parent decision. Bell/bow aggregation must not erase subtype performance. No separately trained bow/bell classifier is required. Native labels remain immutable and every mapping is reversible.

D2's published subclass counts include 835 RDC, 16 RDB, 1,847 CHH, 269 OHH and 523 PHH. Counts are not independent instruments or verified admission counts. Scarce bell data limits precision claims. ENST provides corrected event annotations; original MDB uses cross-checking and external review. Both are documented human/provider annotation authority, not sample-exact physical-contact truth; neither supplies a validated universal onset-error bound. Do not repurpose MDB's 50 ms annotation heuristic as JGA ground truth.

For simultaneous events preserve multi-label targets. A Ride+HH event is not a negative Ride example. Nearby ongoing Ride energy does not prove that a newly annotated Snare onset is a Ride strike. Define and freeze concurrence/crop-contamination handling from annotation authority before evaluation; mark unresolved cases and retain them in coverage accounting. Absence of a label alone is not sufficient silence/negative truth. No listening-based post-hoc relabelling is authorized.

## 9. Smallest empirical experiment and split

**Question:** Under provider-annotated onset locations, can the chosen short audio representation support Ride-parent discrimination from HH and other controls on held-out player–kit conditions and an untouched independent performance dataset?

This is initially **oracle-onset discrimination**, not autonomous event detection. The annotations locate evaluation opportunities, not features. Positive performance would justify designing a separate high-confidence event-admission stage; it cannot validate that stage already.

1. **Admission first, no learning:** after acquisition authorization, verify payloads, labels, counts, subtype coverage, sequence grouping and rights. Freeze inclusion/exclusion and uncertainty policies before measuring discrimination. If a required class/group is absent, preserve the gap; do not change test data adaptively.
2. **Development:** ENST original isolated-stick-hit sequences, grouped by three player–kit identities. Use leave-one-player–kit-out assessment. Any model/regularization selection occurs within the training groups using whole-sequence partitions; no held-out group information enters it. All microphones/versions/crops of one strike stay together. Three confounded player–kit groups do not establish population invariance or independent player effects.
3. **Representation and probe:** bind the single patch and regularized linear parent classifier described in §4. Freeze preprocessing, model family, a bounded development-only regularization rule, seeds, software/environment and missingness. No features derived from event spacing or class-correlated filenames. Any capacity extension after failure needs a new PI-reviewed design, not MDB-driven tuning.
4. **Freeze before independent validation:** finalize the model on ENST development evidence, freeze code/model/hash and output contract. Evaluation custodian holds MDB labels and joins them only after blind predictions are frozen. Dataset names/annotation order/tempo/genre do not enter predictions. No MDB examples as prototypes or calibration support.
5. **Independent test:** apply the frozen probe to all admitted MDB original drum-only opportunities, preserving concurrence and unsupported-subtype flags. Report parent performance, HH-state/other-cymbal false admissions and Ride subtype results. Do not treat a held-out track with no Ride as undefined overall: it contributes negative exposure; undefined recall is explicitly missing.
6. **Stop:** preserve outputs, errors, abstentions, excluded/unresolved cases and replay. No event detector, timing system, dataset expansion or model repair follows automatically.

An external evaluation custodian may prepare onset-centred crops without supplying labels to the predictor. This is oracle localization and must be disclosed. Frozen sample/crop ordering cannot communicate label order. Full autonomous real-audio recognition later requires independent audio event proposals, missed-event scoring and source attribution under overlap; successful oracle crops are necessary preparatory evidence only.

## 10. Evaluation, abstention and falsifiability

**Proposal:** use Ride precision–recall and selective error/coverage curves, per-recording confusion counts and subtype-stratified false admissions. Report the complete curve, not a validation-picked “best threshold.” Retain denominators, missing positives, overlap strata and each player–kit/recording result. Do not count correlated crops or paired channel versions as independent samples. A prospective uncertainty method must respect grouping; with three ENST groups and uncertain MDB player identities, report limited-group variation rather than fabricating precise population confidence.

Future interface: `RIDE_COMPATIBLE`, `NOT_RIDE_COMPATIBLE`, `UNCERTAIN/ABSTAIN`, with score/evidence, provenance and uncertainty. Score is not automatically calibrated probability. High precision at useful coverage is the intended future criterion, but the acceptable false-admission rate and minimum evidence/coverage require PI scientific authority before a decisive admission claim. No universal threshold is supplied by the reviewed papers.

Prospective bounded outcomes: **DISCRIMINATION_EVIDENCE_OBSERVED** (held-out evidence and complete curves support further development under a subsequently preregistered evaluation rule), **DISCRIMINATION_NOT_SUPPORTED_BY_TESTED_PIPELINE**, **INSUFFICIENT_EVIDENCE** (missing labels/coverage/authority), **INDETERMINATE** (conflicting, uncertain or invalid comparison). This design does not yet supply a numerical success rule; a characterization experiment is preferable to inventing one. Threshold-free reporting can be preregistered without asserting timing-admission reliability.

Falsifiers for this proposed pipeline include failure to separate HH/other-cymbal negatives on held-out conditions, high false admission despite abstention, or performance confined to one capture group. A result explained by microphone or background differences cannot establish source generalization. Report cross-dataset degradation and out-of-support bell/pedal/brush cases; do not silently drop them from apparent reliability.

## 11. Firewalls and maximum claim

No periodicity, expected beat position, BPM, meter, Ride pattern, temporal regularity, human tapping, score/DAW tempo, beat files or tracker outputs enter features, partitions chosen to favor an answer, calibration or inference. No multi-event sequence context. Audio → bounded identity evidence comes before any later Ride-event periodicity work.

Maximum favorable claim: **the frozen event-local audio pipeline demonstrates bounded Ride-versus-confound discrimination at independently supplied onset opportunities under the admitted ENST/MDB conditions, with measured uncertainty and selective-performance evidence sufficient to motivate a separately designed admission test.** It is not universal cymbal identity, high-confidence operational admission, complete event recognition, source separation, Ride recurrence, BeatReference or BPM. Ride absent/uncertain must remain abstain-compatible. Global recurrence and Double-Bass evidence are untouched.

## 12. Remaining bindings and exact next action

| Binding / gap | Resolution needed; does it imply live recording? |
|---|---|
| ENST member paths, selected bytes, checksums and selective delivery | Publisher-authoritative small inventory/delivery check; NO |
| Intended NC research use / release custody | PI confirm applicable use scope before acquisition; NO |
| Actual target/control counts, shared original IDs, tails, channel/annotation alignment | Payload/metadata admission after authorization; NO |
| ENST Ride bell / HH pedal support, actual independent cymbal identities | Preserve absent/unknown subtypes; bounded parent experiment remains possible; not a reason to invent labels or record now |
| Filterbank/amplitude/crop edge conventions, concurrence and annotation uncertainty | Prospective implementation-ready preregistration before learning; no MDB tuning |
| Exact model-selection rule, grouped uncertainty/evaluation rule, meaningful reliability target | Freeze before execution; characterization permitted while decisive admission target remains unsupported |
| Oracle-to-autonomous recognition | Separate later event-admission validation; not solved by this design |

**Recommended next PI action:** authorize targeted acquisition/admission preparation: (a) resolve ENST's small authoritative member inventory and selective access, then present its concrete byte/file manifest before audio transfer; (b) acquire the exact 69 original MDB members plus documentation under the applicable license and external storage policy. Do not authorize the full ENST archive by implication. After input admission, freeze the small empirical preregistration; implementation/training/testing require separate authorization.

Existing literature is sufficient to select a candidate representation family; it does not eliminate empirical validation. Comprehensive Ride Identity Card work is unnecessary at this stage. Targeted acquisition is scientifically justified; indiscriminate bulk acquisition is not. New live Drum recording is NOT_YET_JUSTIFIED. No numerical sufficiency, classifier or feature computation was performed in preparing this document.

## Appendix A. MDB exact basename/audio-object inventory

Use each basename B in ALL THREE templates in §6. Every listed row requires one audio, one subclass annotation and one YAML file. Audio sizes and Git blob identities below come from D3, not decoded audio. The frozen tree binds the corresponding small files without assuming a mutable branch version.

| B | Audio bytes | Git audio blob SHA-1 |
|---|---:|---|
| `MusicDelta_80sRock` | 3,256,364 | `02cdede55df4b8dc966f657e8c677ee88f181ccb` |
| `MusicDelta_Beatles` | 3,208,188 | `16bbec4d7e575bc9dbc48bb6ff665146fd94889f` |
| `MusicDelta_BebopJazz` | 9,081,036 | `f778ac941a1821133809f1dbf6d26e76bdfcff96` |
| `MusicDelta_Britpop` | 3,244,822 | `03410b3078ce3f0727134848119d832ae5d75a42` |
| `MusicDelta_CoolJazz` | 8,957,856 | `e171ffe6b45ee8c6143154b6aa64ef6cf4b9b95e` |
| `MusicDelta_Country1` | 3,064,364 | `80949369121d6e49a5885a4d105779e790e26264` |
| `MusicDelta_Disco` | 11,005,636 | `3ec55a63c3b726b89630d8b9796f5ad2779bb0ed` |
| `MusicDelta_FreeJazz` | 9,201,254 | `6ee6343b9a56a81567f843d356a10cbd29d9568d` |
| `MusicDelta_FunkJazz` | 4,355,918 | `c6997a081222059b5de0870bc04c65264420ae81` |
| `MusicDelta_FusionJazz` | 9,788,974 | `67713fb72a9f8215bb5f923c6dc867530e3d71e4` |
| `MusicDelta_Gospel` | 6,680,074 | `b89503627b59b6097fe9c8272de7ab87c6e88e51` |
| `MusicDelta_Grunge` | 3,691,580 | `485dda89e1a1e940c7ca76b15566eb5de4564d96` |
| `MusicDelta_Hendrix` | 1,750,280 | `d7a7f7edae210da6466586451d1405ac61d15814` |
| `MusicDelta_LatinJazz` | 5,906,428 | `953c1847821bf8e548c0d878fab6118b75ff6019` |
| `MusicDelta_ModalJazz` | 9,153,322 | `52fd211c57960bf89273e3f469f58c3792f73403` |
| `MusicDelta_Punk` | 2,536,900 | `9f86db675f5b46420740cb3154088bde681f4b83` |
| `MusicDelta_Reggae` | 1,540,252 | `12a8fdf5cdfc07e426f9a36af7a348a6b4659317` |
| `MusicDelta_Rock` | 1,154,684 | `b3568e041e5c8926d98ddcea68bb415d9a5c297b` |
| `MusicDelta_Rockabilly` | 2,288,760 | `2bde1efa8de813261374bece025f4f63ab5c9c65` |
| `MusicDelta_Shadows` | 2,953,950 | `7d66a4947b46e034673da77cc23efa5753a3abb8` |
| `MusicDelta_SpeedMetal` | 3,175,980 | `9d62ef64e067c33962f1b37653c3be90ccd5c4e4` |
| `MusicDelta_SwingJazz` | 7,895,084 | `edcb41ab94f5e3b8d0b5551fdfe0dee1a7248dc1` |
| `MusicDelta_Zeppelin` | 1,541,342 | `dba7444516102fcee205854a621b197ed96667ae` |
