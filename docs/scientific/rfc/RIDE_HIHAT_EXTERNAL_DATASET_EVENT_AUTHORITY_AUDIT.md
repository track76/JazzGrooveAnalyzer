# Ride / Hi-Hat external dataset and event-authority audit

Identifier: RH-EXTERNAL-AUTHORITY-AUDIT-01. Date: 2026-09-10.
Status: **COMPLETED DOCUMENTARY RESEARCH AUDIT — FOR PI REVIEW; NO DATASET ADMISSION OR EXPERIMENT EXECUTED.**
Repository HEAD: `13f391be8e8ae512c171e79e93f07b7a9ffca37e`; branch: `scientific/translation-layer-finalization`.

## 1. Scope, authority and decision brief

**Logical Inference:** Existing external evidence is sufficient for the next Ride physical/perceptual research and validation-design phase. New live Ride or Hi-Hat capture is **NOT_YET_JUSTIFIED**. Prefer ENST's controlled material plus original MDB's performance annotations as the smallest initial evidence chain. This is documentary suitability, not a claim that downloaded files have been admitted, a model works, or all future validation requirements are satisfied.

The internal audit was read and its SHA-256 verified before dependent work:

`docs/scientific/rfc/RIDE_HIHAT_EXISTING_ASSET_SUFFICIENCY_AUDIT.md`

`7c1fd3e86a8279183fa2d17ec11f06ee4de4ddd459c0280b355f0e06f0ded15a`.

Its Ride C / Hi-Hat B, absent Ride event GT, Hi-Hat track-only authority and partial discrimination findings remain unchanged. External labels supply a different evidence source; they do not retrospectively label JGA audio.

Governing navigation: `AGENTS.md`, `artifacts/JGA_BOOTSTRAP.md`, `docs/scientific/README.md`, `docs/JGA_DEVELOPMENT_CONSTITUTION.md`, `docs/scientific/foundations/JGA_KNOWLEDGE_MODEL.md`, and `docs/scientific/JGA_RIDE_FIRST_TIMING_RESEARCH_DECISION_20260910.md`. Repository/bootstrap frontier agrees: Ride-first research; global recurrence preserved with sufficiency validation deferred/parallel; Double-Bass independent. No architectural change is needed by this audit. Core → Translation → Domain and observation before musical interpretation remain binding.

Evidence classification throughout: **Observed Fact** means a directly inspected repository record or attributed external declaration, not independently measured acoustic truth. **Logical Inference** covers usability grades, recommendations and limitations derived from those declarations. **UNKNOWN** marks absent or unverified authority; no assumption fills it. Existing PI direction is a **Decision**; recommendations here await PI review.

## 2. Search method and access boundary

Inspected the four requested dataset releases, original papers and author/institution documentation; followed annotation and licensing references. Additional screening was limited to E-GMD and STAR Drums because their apparent label strength could otherwise be confused with original acoustic authority. Search engines were navigation aids; findings below rely on primary sources.

Read small public README, metadata and GitHub tree records. No audio/video was downloaded, decoded, listened to, normalized or measured. No model, feature extractor, onset detector, annotation correction, surrogate, separation or timing computation ran. Git tree byte totals are metadata arithmetic only. No bulk archives were downloaded. Archive member inventories, audio headers, annotation populations and payload checksums remain subject to later separately authorized admission.

Some legacy links and Zenodo API requests failed. Successful replacement sources are identified below. A missing license field in a rendered webpage was not interpreted as permission. For 29k, DOI registration metadata supplied the license. GitHub branch heads are mutable; tree identities observed here are navigation snapshots, not JGA input freezes.

## 3. Authoritative source register

All sources accessed 2026-09-10. Dataset licenses are distinct from paper licenses.

| ID | Primary source / exact citation and scope |
|---|---|
| E1 | Olivier Gillet and Gaël Richard (2006), *ENST-Drums: an extensive audio-visual database for drum signals processing*, ISMIR, pp. 156–159, especially §§2.1–3.5 and Table 2. [Proceedings PDF](https://archives.ismir.net/ismir2006/paper/000027.pdf). |
| E2 | Gillet and Richard, *ENST-Drums*, Zenodo release v2, published 2026-07-23; DOI [10.5281/zenodo.21506051](https://zenodo.org/records/21506051). |
| E3 | Author's [dataset page](https://perso.telecom-paristech.fr/grichard/ENST-drums/) and [legacy user license](https://perso.telecom-paristech.fr/~grichard/ENST-drums/ENST_Drums_License.pdf). |
| M1 | Carl Southall, Chih-Wei Wu, Alexander Lerch and Jason Hockman (2017), *MDB Drums: An Annotated Subset of MedleyDB for Automatic Drum Transcription*, ISMIR Late-Breaking/Demo extended abstract, §§2.2–2.3 and Table 1. [Author institution PDF](https://www.open-access.bcu.ac.uk/6179/1/Southall2017a.pdf). This is a late-breaking/demo contribution, not silently treated as a full proceedings article. |
| M2 | Original [CarlSouthall/MDBDrums](https://github.com/CarlSouthall/MDBDrums), [README](https://raw.githubusercontent.com/CarlSouthall/MDBDrums/master/README.md), [tree metadata](https://api.github.com/repos/CarlSouthall/MDBDrums/git/trees/master?recursive=1). Observed tree `b29e2d63c3a023506f4bf353c5b2e8a558eed135`. |
| M3 | Original [BebopJazz recording metadata](https://raw.githubusercontent.com/CarlSouthall/MDBDrums/master/MDB%20Drums/audio/multi-tracks/MusicDelta_BebopJazz/MusicDelta_BebopJazz_METADATA.yaml). One example inspected, not a complete personnel audit. |
| P1 | Xavier Riley, *Transcribing the Jazz Ensemble*, doctoral thesis, Queen Mary University of London, §§7.4.1–7.5.1, printed pp.100–102. [Author university PDF](https://webspace.eecs.qmul.ac.uk/s.e.dixon/phd/XavierRiley-PhD-Thesis.pdf). Repository revision is separately bound below; thesis publication year not inferred from search crawl dates. |
| P2 | Author [MDBDrumsPlusPlus repository](https://github.com/xavriley/MDBDrumsPlusPlus), [metadata CSV](https://raw.githubusercontent.com/xavriley/MDBDrumsPlusPlus/main/metadata.csv), [tree](https://api.github.com/repos/xavriley/MDBDrumsPlusPlus/git/trees/main?recursive=1). Observed tree `13aa81750e74810aec7ca17a75fe438961613d82`. |
| P3 | Author [Hugging Face dataset card](https://huggingface.co/datasets/xavriley/MDBDrumsPlusPlus), inspected specifically for release/license consistency. |
| K1 | Macià Amorós i Cortiella (2021), *29kSamplesDrumsDataset*, DOI [10.5281/zenodo.4958592](https://zenodo.org/records/4958592); [DOI registration metadata](https://api.datacite.org/dois/10.5281/zenodo.4958592). |
| K2 | Creator's linked sample documentation: [Ride + Snare, Sennheiser e945](https://freesound.org/people/MaciaAC/sounds/576683/), [Hi-Hat + Kick + Snare, Samson C03](https://freesound.org/people/MaciaAC/sounds/576769/). Pages only; no listening/download. |
| I1 | Feliks Weber, Manuel Winges, Christian Dittmar and Daniel Gärtner, *IDMT-SMT-Drums Dataset*, [Fraunhofer documentation](https://www.idmt.fraunhofer.de/en/publications/datasets/drums.html); [Zenodo release 7544164](https://zenodo.org/records/7544164), 2023-01-17, record version 1.0.0, archive named `IDMT-SMT-DRUMS-V2.zip`. Associated citation: Dittmar and Gärtner (2014), *Real-time transcription and separation of drum recordings based on NMF decomposition*, DAFx-14. Dataset findings use provider/release documentation, not an uninspected method implementation. |
| X1 | Lee Callender, Curtis Hawthorne and Jesse Engel (2020), *Improving Perceptual Quality of Drum Transcription with the Expanded Groove MIDI Dataset*, [arXiv:2004.00188](https://arxiv.org/abs/2004.00188); [official E-GMD release](https://magenta.tensorflow.org/datasets/e-gmd). |
| X2 | Philipp Weber, Christian Uhle, Meinard Müller and Matthias Lang (2025), *STAR Drums: A Dataset for Automatic Drum Transcription*, TISMIR, DOI 10.5334/tismir.244. [Fraunhofer publication record](https://publica.fraunhofer.de/entities/publication/1c90a7b6-7722-472c-8ac8-482b99c328d2). |
| L1 | Creative Commons [BY 4.0](https://creativecommons.org/licenses/by/4.0/), [BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), [BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/), and [ND legal code, §2(a)(1)](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.en). |

## 4. ENST-Drums audit

**Observed Fact — E2/E3:** Three professional players, Louis Cavé, Bertrand Clouard and Frédéric Rottier, each used their own acoustic kit. Approximately 75 minutes per player describes recorded material, not a verified public-download duration. Sticks, rods, brushes and mallets; eight audio channels and two video views are documented. Release v2 adds missing video. Its archive name still contains `v1_1`; preserve both identifiers rather than equating their version strings.

**Observed Fact — E1, compact technical record:** Individual-stroke sequences include intervening silence. Audio: 44.1 kHz/16-bit; mono microphones plus stereo mixes. Hi-Hat: Schoeps CMC/cardioid; overheads: two AT4040; MIC2200 preamps → Tascam MX2424. Edited/segmented masters remove bad takes/gaps. Dry mix changes level/pan; wet mix adds EQ, compression, reverb and L3 processing. Video: 25 fps, manually aligned, no time-stretch reported. Annotations: onset-detector proposals, audio/video correction by Gillet, rechecked by the same annotator. Hi-Hat has Snare contamination; cymbals use overheads. Missed strokes and some quiet timekeeping actions/strokes are omitted; ghost notes included. Format: time/event pairs, numbered cymbal identity within player. Taxonomy: `rc` Ride, `ch` Chinese ride, `cr` Crash, `spl` Splash, `c` other; `chh` closed and `ohh` open Hi-Hat. No separate Ride-zone or pedal/half-open label established.

**Logical Inference:** Strongest controlled acoustic starting resource among the audited priorities, with a path to performance testing. GT-B for positive annotated identities; conditional completeness for timing. Never use every unlabeled instant as a target-absent negative. Video assists attribution but cannot establish sample-exact stick contact. Do not import the annotation policy's musical distinctions into JGA recognition or timing discovery. Actual release-level Ride/Hi-Hat hit counts and tail availability need admission, not a new recording by default.

## 5. Original MDB Drums audit

**Observed Fact — M2:** 23 tracks; drum-only, full mixes and multitracks; 7,994 annotations in six broad classes and 21 subclasses. Audio/annotations: CC BY-NC-SA 4.0. Broad `CY` is not Ride authority. The repository also lists beat-annotation files; their contents were not read and must remain excluded from identity discovery and later blind timing inputs.

**Observed Fact — M1:** MusicDelta real musician recordings; average track length 54 seconds. madmom onset proposals were corrected/classified in Sonic Visualiser, including missing hits. Two annotators cross-checked each other, followed by an external reviewer. Heuristic checks flagged invalid labels, duplicate labels within 50 ms, and three-or-more labels within that window. Table 1: `RDC` 835, `RDB` 16, `CHH` 1,847, `OHH` 269, `PHH` 523; contrasts `CRC`, `CHC`, `SPC`. Annotator-specific timing uncertainty and exhaustive ambiguity adjudication are not quantified. The paper acknowledges Maciek Tomczak's review contribution.

**Observed Fact — M3:** The inspected example credits Music Delta / producer Mike Tierney, declares `has_bleed: no`, and maps its Drum stem to a whole-`drum set` raw file. It does not provide individually isolated Ride/Hi-Hat channels. A dataset-level no-bleed flag cannot establish separation among kit components.

**Logical Inference:** Strongest reviewed real-performance event authority in this audit; GT-B, not physical GT-A. Preserve the subclass vocabulary, including scarce bell examples. The 50 ms rule is a quality-control heuristic, neither a JGA tolerance nor a physical timing bound. Twenty-three songs do not establish 23 players/kits/cymbals. Matched mix/stem versions must stay in the same future data partition. No claim of unprocessed acoustic transfer follows from `RAW` naming.

## 6. MDB Drums++ audit — separate authority

**Observed Fact — P1:** Re-annotation was motivated by suspected missing brush events. Logic Pro X onset extraction at −40 dB was followed by manual component assignment; judged simultaneous hits received copied onset times. Reported totals are 8,448 versus 7,994, with roughly 94% annotation agreement. The author explicitly does not treat estimated velocities as ground truth. These are published results, not computations rerun here.

**Observed Fact — P2:** MIDI annotations, drum-only WAVs, Logic sessions and per-track metadata are supplied; original mixes remain in MDB. CSV rows document 44.1 kHz mono. No calibrated physical velocity follows. **External license inconsistency — P3:** card metadata says BY-SA while prose says BY-NC-SA, consistent with P2/original MDB. No permission is inferred from the less restrictive tag.

**Logical Inference:** GT-C supplementary annotation sensitivity evidence; Tier B complementary, not a replacement benchmark admitted as superior. Increased counts do not prove correctness. Same performances are not an independent test dataset. Independent second review, uncertainty estimates and a validated Ride/Hi-Hat MIDI mapping for this revision remain UNKNOWN. Do not assume General MIDI alone certifies the actual mapping. Resolve the mirror license inconsistency before relying on that distribution; it does not prevent this documentary audit or authorize acquisition.

## 7. 29kSamples audit

**Observed Fact — K1:** Approximately 29k samples, 22 classes including combinations; one kit, two cymbal sets; eight microphones positioned one metre in front. `cy` denotes Ride, `cr` Crash, `hh` Hi-Hat; other codes cover membranes. A supplied Essentia MusicExtractor CSV is derived evidence. DOI registration explicitly specifies **CC BY 4.0**. Zenodo page creation/modification is June 16, 2021; DOI metadata issued date is June 10. Bind the DOI, not an assumed date-based version.

**Observed Fact — K2:** Selected creator examples are 1 s, mono, 44.1 kHz/16-bit. Creator warns of time-shifted examples and retained cymbal tails. These pages identify specific microphones; they do not establish the format or processing of every archive member. Their CC0 notices cover those posted examples, not a relicensing of the full archive.

**Logical Inference:** Tier B conditional sample resource, GT-D file class for both targets; not strong onset GT. Best compact supplementary sample collection, but weaker primary physical authority than ENST. Do not call all 29k files independent isolated strikes or count eight microphone renditions as eight performances. Archive-level augmentation lineage, sample boundaries, original-hit IDs, long decays and target-only purity remain unverified. No independent annotator/cross-check or HH state/Ride zone authority was found. Essentia features neither define Ride identity nor substitute for JGA observability validation.

## 8. IDMT-SMT-Drums audit

**Observed Fact — I1:** 608 WAVs, mono 44.1 kHz/16-bit, about 2 h 10 min; 104 kick/Snare/Hi-Hat loops and 312 instrument-training files. RealDrum is acoustic; WaveDrum library-based; TechnoDrum synthesized. Manual onset annotations are supplied in XML/SVL with filename correspondence. The 192 isolated reference tracks belong to the 64 TechnoDrum02/WaveDrum02 loops; they are not documented acoustic isolated stems. Provider names Weber/Winges as recording/annotation contributors. License: BY-NC-ND 4.0, evaluation purpose. No Ride class is documented.

**Logical Inference:** Tier B for complementary Hi-Hat evaluation; Tier E for Ride positives. Hi-Hat GT-B within documented broad-class annotation scope, with UNKNOWN cross-review, state taxonomy and timing error. Acoustic versus synthetic subsets must remain separate. Do not infer closed/open/pedal labels from another library's loader. Excellent source-reference isolation in rendered subsets cannot prove original cymbal physics. Performer/kit/cymbal counts, microphone geometry and full processing history are not established by the inspected provider record.

## 9. Additional dataset screening

**Observed Fact — X1:** E-GMD v1.0.0 re-records MIDI performances through a Roland TD-17: 43 sound kits, 44.1 kHz/24-bit, declared alignment within 2 ms; 90 GB compressed/132 GB unpacked; BY 4.0. All sound kits occur across its supplied partitions. **Logical Inference:** Tier D for this acoustic-source objective; useful future rendered-control authority, not 43 physical cymbal sets. MIDI scheduling is not acoustic contact truth. Not recommended for initial acquisition; it does not close the original-acoustic gap more directly than ENST/MDB.

**Observed Fact — X2:** STAR Drums separates, automatically annotates, then re-synthesizes the Drum stem and combines it with recorded non-Drum material. **Logical Inference:** Tier D here; resynthesis provides controlled rendered labels, not independent truth about the original Ride events. No full license/storage admission audit was pursued because it is not needed for the minimum acoustic chain. Do not equate the paper's license with dataset licensing. No additional bulk dataset is recommended.

## 10. Event-label authority matrix

Grades classify evidence role, not measured accuracy: GT-A strong independent event authority; GT-B documented human/provider event annotation; GT-C conditional; GT-D file/track class; GT-E inferred/weak; GT-F none. None of the recommended acoustic datasets establishes sensor-independent, sample-exact physical-contact GT-A.

| Dataset | Ride | Hi-Hat | Temporal / simultaneous / uncertainty admission limit |
|---|---|---|---|
| ENST | GT-B positives | GT-B positives | E1 correction/omission policy; timestamp numeric precision and error bound UNKNOWN; video frame spacing is not onset uncertainty; component events can coexist, not mutually exclusive labels |
| MDB original | GT-B | GT-B | M1 external review; concurrent-label heuristics do not prove impossible combinations; no published per-event error intervals established |
| MDB++ | GT-C | GT-C | P1 copied simultaneous times; estimated velocities; MIDI-to-seconds binding and revision-specific mapping require verification; no silent replacement of original |
| 29k | GT-D | GT-D | File class only; no verified within-file contact/onset/offset authority; combinations and previous tails matter |
| IDMT | GT-F | GT-B broad HH | I1 manual annotation; exact encoding/resolution/error and state labels require member-level inspection |

For all five, formal confidence values, annotation disagreement ledgers, offset/choke authority and calibrated physical contact times remain UNKNOWN unless the later admitted package supplies them. No classifier-derived labels may be used to validate that same classifier. External annotations are independent of future JGA outputs, but may share detector biases across their original generation methods.

## 11. Ride taxonomy matrix

| Dataset | Admissible native distinction | Not established / prohibited mapping |
|---|---|---|
| ENST | E1 `rc` plus cymbal instance; other native cymbal classes retained | `rc` does not certify bow; `ch` must not silently merge with conventional Ride; no bell/edge or crash-ride coverage claimed |
| MDB | M1 `RDC` versus `RDB`; contrast subclasses | Broad `CY` cannot replace subclass GT; no explicit edge/bow/crash-ride or Chinese-*Ride* identity inferred from China label |
| MDB++ | Parent audio reusable; revised MIDI taxonomy unadmitted | No inferred equivalence from original names or standard MIDI convention |
| 29k | K1 file-class distinction | No within-Ride zone or manufacturer identity inferred |
| IDMT | None | No Ride positive or broad-cymbal-to-Ride conversion |

## 12. Hi-Hat taxonomy matrix

| Dataset | Admissible native distinction | Not established |
|---|---|---|
| ENST | E1 open/closed | Half-open, explicit pedal versus stick, top/bottom contact and zone labels |
| MDB | M1 open/closed/pedal | Half-open aperture, precise stick contact zone; pedal onset does not certify opening trajectory |
| MDB++ | Re-annotated events subject to mapping admission | No inherited guarantee of original subclass preservation |
| 29k | Broad HH file class | States, pedal/strike, zone |
| IDMT | Broad HH event class | States, pedal/strike, zone |

Do not homogenize all HH states or collapse cymbal taxonomies during admission. A future common vocabulary must retain native labels and unresolved mappings; it is not designed here.

## 13. Audio and provenance admission matrix

| Dataset | Original / derived distinction | Remaining capture metadata UNKNOWN |
|---|---|---|
| ENST | E1 individual microphones versus dry/wet mixes; use the former first for physical observability | Individual cymbal brand/model/diameter/weight/serial; numerical microphone geometry, room characterization, gains, calibrated SPL; per-file normalization/lossy-history verification |
| MDB | M2 distributed multitracks, stems and mixes are different representations of a performance, not newly separated JGA stems | Exact players/kits/cymbals; microphone models/positions; gain/EQ/compression history; room/chain; each original file's rate/bit depth/channel format must be read from admitted metadata |
| MDB++ | Same underlying performances, updated annotations, P2 declared format | Byte equivalence to original audio, complete audio transformation and MIDI export provenance |
| 29k | K1 acoustic sample collection; K2 warns of temporal alteration/contamination | Full per-member format, normalization, augmentation recipes, source-hit grouping, clipping, decay truncation, performer and cymbal models |
| IDMT | I1 acoustic/library/synth classes; isolated rendered references separately identified | RealDrum physical provenance and full channel/processing history beyond I1 |

UNKNOWN applies individually to unlisted preamp settings, resampling, lossy compression, normalization, source separation, microphone calibration and onset-clock alignment. Absence of an effect in a short description is not evidence it never occurred. An original multitrack channel need not be acoustically isolated. Preserve supplied filenames and representations; do not substitute commercial mixes, wet mixes or synthetic references as physical ground truth.

## 14. Variability and confound coverage

**Logical Inference from §§4–8:**

| Variation / contrast | Evidence available for later testing | Limit |
|---|---|---|
| Within-class repetition | ENST controlled hits and performances; MDB target annotations; conditional 29k samples | Counts are not independent player/instrument replication |
| Between player / kit | ENST documented three player–kit combinations | Player and kit are confounded; no crossed design or universal invariance claim |
| Between cymbals | ENST local instance identity; 29k two-set declaration | Target-specific inventory/count of unique physical Rides/HHs not audited; multiple kits do not by themselves certify distinct cymbal specimens |
| Dynamics | Natural performance/sample variation potentially available | No calibrated force/SPL or prospectively balanced dynamic levels established |
| Articulation / implement | ENST implements; MDB state/bell distinctions | Rare subclasses and incomplete target × implement coverage; no balanced bow/bell/edge factorial design |
| Microphone / capture | ENST multi-channel observations; 29k microphone variation; JGA separate sessions | Same-hit channels are dependent; room/player/instrument effects can remain confounded |
| Musical contexts | ENST performances, MDB real tracks, existing JGA jazz | Style labels cannot become source identity or beat priors |
| Ride vs HH / Crash / other cymbals | ENST and MDB native taxonomies; 29k conditional combinations | Exact negative truth requires annotation completeness, not lack of a target label alone |
| HH vs Snare / membrane transients | Existing original channels and external co-occurrence labels | Bleed and simultaneous hits require multi-label evaluation or abstention, not forced exclusive classification |

There is enough documented variation to plan bounded held-out player–kit and cross-dataset tests. Isolating a *causal* player effect from an instrument effect is not yet supported. Future partitions must group an original performance and all microphones, mixes, crops, shifted copies and revised annotations together. A file-random split would risk recording-chain/session recognition instead of identity. No partitions or classifier are implemented here.

## 15. Licensing / JGA use

These are documented terms and unresolved applicability questions, not new legal conclusions.

| Release | Documented license | Research / commercial / redistribution implication |
|---|---|---|
| ENST Zenodo v2 | E2 BY-NC-ND 4.0; research only | NC applies; preserve attribution/citation; ND restricts sharing adapted material |
| ENST legacy portal | E3 separate personal scientific-use agreement | Signed-return procedure and stronger access/derivative restrictions are documented; do not silently substitute Zenodo terms for a previously acquired legacy package |
| MDB original | M2 BY-NC-SA 4.0 audio and annotations | NC; attribution; distributed adaptations subject to SA. M1 paper's BY license does not relicense audio |
| MDB++ GitHub | P2 BY-NC-SA 4.0 | Same restrictions; P3 mirror tag discrepancy unresolved, so no mirror-based broader permission |
| 29k DOI release | K1 DOI registration BY 4.0 | Attribution, license/changes notice; no NC/ND/SA declared in that registration. Confirm included license on later admission; selected K2 CC0 files do not relicense archive |
| IDMT specified release | I1 BY-NC-ND 4.0; evaluation purpose | NC/ND; preserve provider conditions and attribution; do not import terms from historical mirrors |

L1: BY permits sharing/adaptation including commercial uses under its terms. NC limits commercial use; SA governs shared adaptations. Under ND §2(a)(1), noncommercial adapted material may be produced/reproduced but not shared. **ND is not a blanket ban on private signal analysis.** Whether particular features, models or software deliverables constitute adaptations or permitted uses is not specified by these dataset records; do not presume trained-model redistribution or commercial JGA clearance. Features/models are not produced in this task.

Download and external-SSD custody do not erase restrictions. PI must bind the intended noncommercial research/evaluation use before NC acquisition/use, and resolve permissions separately if commercial software-development use is intended. Publication should cite datasets and report bounded findings; publishing audio excerpts, modified annotations, feature corpora or model weights requires the applicable release-level rights check. No dataset audio belongs in Git regardless of license; Git may preserve JGA-authored reports, references and lightweight authorities, with licensing checked before copying annotation content.

**External ambiguity handling:** ENST legacy/v2 terms are release-specific; applicable terms must be bound before acquisition, not selected opportunistically. MDB++ mirror discrepancy blocks reliance on that mirror's rights claim. Neither ambiguity changes protected JGA state or prevents the minimum non-acquisition research conclusion.

## 16. Storage and reproducible acquisition boundary

| Resource | Observed download / payload size | Published integrity / version |
|---|---|---|
| ENST v2 | 9.6 GB archive; unpacked size UNKNOWN | `enst_drums_v1_1.tar.zst`; MD5 `a134f0a34d12eb5317ff3ddd7d07b6db`; E2 DOI |
| MDB original | Git tree sums: 2,010,349,446 bytes across 362 files (~2.01 GB payload); archive/history overhead UNKNOWN | M2 tree above; not a SHA-256 audio freeze |
| 29k | 941.6 MB ZIP; unpacked size UNKNOWN | MD5 `75784e5bdbd069af66bee91d25b3e984`; K1 DOI |
| IDMT | 287.1 MB ZIP; unpacked size UNKNOWN | MD5 `d2664b4c2aaa34b90ba2f57b389c5663`; I1 version/archive distinction |
| MDB++ optional | 166,078,309 bytes in Git tree; audio portion 116,253,368 bytes | P2 tree above; excludes Git history; do not duplicate parent audio unnecessarily |

**Planning estimate, not measured disk requirement:** minimal ENST + original MDB payload/download budget ~11.61 GB. Including optional 29k and IDMT gives ~12.84 GB, excluding unpacking, backups, archive duplication and future derived files. No defensible exact total installed footprint is available without archive inventory. Do not declare a fixed free-space amount sufficient on these compressed totals. MDB++ and E-GMD are excluded from the minimum budget.

If later authorized, use `/Volumes/SSD Track/JGA/datasets/<dataset>/<release>/` with separate `original/`, `provenance/`, `manifests/`, and later-authorized `derived/`. Preserve downloaded bytes, release/license text, retrieval URL/date, DOI or commit and tree, file size, provider checksum and locally computed SHA-256. Keep annotations and original audio aligned by immutable identities; quarantine musical metadata from discovery inputs. Verify available external space and archive expansion before extraction. Do not duplicate heavy assets onto the internal SSD or into this repository. No such acquisition or directory population occurred here.

## 17. Scientific tier and role matrix

All grades below are **Logical Inferences**, conditional on later byte/rights admission and on the bounded annotation policies above.

| Dataset | Tier | Role 1: controlled physical/timbral evidence | Role 2: real-performance recognition |
|---|---|---|---|
| ENST | A — primary | Best documented candidate for both targets | Strong positives; incomplete-event policy limits exhaustive recall/timing claims |
| MDB original | A — primary event authority | Performance examples, not isolated physical controls | Best reviewed complementary benchmark for both targets |
| 29k | B — complementary | Useful after original-hit/processing qualification; not automatically pristine | No independently annotated continuous-performance role |
| IDMT | B for HH; E for Ride positives | Selected acoustic HH references conditionally useful | Independent HH-only complementary benchmark within its subset scope |
| MDB++ | B — annotation sensitivity | No additional original capture | Conditional alternative labels, not independent performances |
| E-GMD / STAR | D for original-acoustic objective | Rendered controls only, if later justified | Cannot establish original acoustic-event truth |

## 18. Minimum combined evidence chain

**Recommendation, not an adopted classifier design:**

1. Ride physical/acoustic/perceptual literature and observability design remains first. Data availability must not decide the ontology or feature set.
2. Prospectively admit ENST controlled target/contrast material and its original channels; bind native class and instance identity, uncertainty and source lineage. Verify which relevant members are in the public release.
3. Use disjoint ENST performance/player–kit groups and original MDB performance annotations for future independently authorized recognition evaluation. Reserve MDB labels from measurement generation. Keep all target subtypes/contrasts and unresolved cases.
4. Add 29k only if its additional capture contrasts fill an identified requirement after qualification. Add IDMT if independent HH validation materially helps. Do not acquire every dataset merely because it exists.
5. Use existing JGA CED-VAL-005/006 as later domain-transfer material; add 009/010 only where their existing authority permits. External performance recognition does not generate independent JGA event GT.

This combination offers documented multi-condition evidence unavailable from a single unspecified new session. It is not demonstrated statistically stronger than every possible new capture. No residual gap has yet been shown to require a live session rather than existing data, additional metadata or independent annotation authority.

## 19. Internal JGA transfer and minimum identity evidence

The unchanged internal audit provides exact paths/checksums. In CED-VAL-005, `05_HiHat.wav` and `09_Overheads.wav` are useful paired context; CED-VAL-006 has the original dual-output overhead channel `Dums Overheads LCT 640 TS-Dual Output Mode.wav`. They are not independently labelled Ride/HH events. Derived Demucs/RX material remains a separate processed condition. No listening labels are created here.

The minimum future identity evidence is target-positive and principal-confound coverage under declared capture/performer conditions, independent event labels for a held-out test, observable uncertainty, and a way to abstain on ambiguous/multiple-source events. Reliability and adequate sample size must be justified prospectively; none is inferred from a dataset's reputation. Recognition must survive held-out original-source groups before its events can be admitted to source-conditioned timing research.

A future JGA transfer test requiring quantified accuracy needs independently authorized labels or adjudication for the actual JGA files. External labels cannot certify those events. Initially, unlabelled JGA material can support only bounded observational transfer inspection after separate authorization. No Ride score, feature selection, fallback or timing rule is designed here.

## 20. Residual evidence gaps and resolution matrix

| Gap | Existing route before new recording | Present status / impact |
|---|---|---|
| Ride and HH positive authority | ENST; MDB | Documentary gap closed for initial research; file-level admission pending |
| Confound and simultaneous-event examples | ENST/MDB; conditional 29k | Available in principle; exact target/contrast balance and trustworthy negatives need inventory |
| Exhaustive quiet-event labels / timing eligibility | Independently audited existing performance labels, potentially video-assisted authority | Not established; ENST omission policy is material; no automatic transition to timing |
| Calibrated physical onset / annotation uncertainty | Existing clock/annotation documentation or future independent validation authority | UNKNOWN; do not substitute waveform sample precision or evaluation windows |
| Between-player/kit holdout | ENST grouped player–kit data | Supports joint held-out variation; does not isolate causal effects |
| Named individual Ride/HH specimens and crossed factors | Existing provider records/metadata first | Target specimen inventory and independent factor separation remain incomplete |
| Bell/bow/edge, half-open/pedal, dynamics | Native external subclasses plus additional documentation if needed | Partial; full factorial coverage not required to begin bounded research |
| Long decay, noise floor, authentic excitation | Qualify original ENST hit sequences first | Required support depends on future physics-based model; 29k crops cannot be presumed adequate |
| Rights and package integrity | Release-specific admission and permissions | Must bind before download/use; no scientific need for new recording follows merely from unperformed admission |
| Real JGA accuracy labels | Existing JGA source records plus independently authorized annotation procedure | Still missing; no current label generation authorization |
| Commercial deployment rights | Provider permission or independently cleared material | Not granted by this audit; current conclusion concerns research evidence |

If these routes later fail for a specific required phenomenon, the PI can reconsider new controlled recording with that exact gap. This report does not design or authorize such recording.

## 21. Live-capture avoidance decision

**Logical Inference, scoped to the next research phase:**

| PI question | Answer |
|---|---|
| Initial Ride identity research | YES — external documented source/event examples remove the internal positive-authority obstacle |
| Initial HH identity research | YES — adds event labels beyond internal track intent |
| Ride-vs-HH discrimination study preparation | YES — native target/contrast labels exist; no discrimination capability demonstrated |
| Real-performance event-recognition validation data | YES for bounded external annotation-based evaluation; NOT complete original-event truth or JGA-specific scored transfer |
| Between-player/instrument variability testing | YES for joint player–kit holdout planning; PARTIAL for independently controlled cymbal/player effects |
| Avoid new live recording now | YES — acquisition and research preparation can proceed without making live capture a prerequisite |

Here **SUFFICIENT** means enough documented evidence to prepare a bounded next research study, subject to admission, not enough to freeze an identity model, guarantee statistical power, or complete the entire Ride-to-BPM path. Under that definition controlled and performance data are sufficient for both initial target studies; exhaustive articulation/physical authority remains partial. The strongest external event grade is GT-B, described as STRONG dataset annotation, not GT-A contact authority.

## 22. Next PI action and preservation

Recommended next PI decision: accept the bounded reuse conclusion and authorize **Ride physical/perceptual identity research and observability-design preparation**, using this dataset map. Separately authorize limited ENST/MDB acquisition and input/label admission once release-specific use and external space are bound; 29k/IDMT remain optional supplements. No experiment authorization is implied by either action. No need to schedule a new Drum session now.

Only this report is created. Internal audit, roadmap, bootstrap, protected timing evidence, Double-Bass records, source code and tests remain unchanged. No commit or push. No recognition, invariance, recurrence, BeatReference or BPM result is established.

EXTERNAL RIDE EVENT AUTHORITY: STRONG (GT-B, bounded annotation scope)

EXTERNAL HIHAT EVENT AUTHORITY: STRONG (GT-B, bounded annotation scope)

CONTROLLED RIDE IDENTITY EVIDENCE: SUFFICIENT (next research phase only)

CONTROLLED HIHAT IDENTITY EVIDENCE: SUFFICIENT (next research phase only)

REAL-PERFORMANCE RIDE VALIDATION DATA: SUFFICIENT (bounded external annotation-based evaluation)

REAL-PERFORMANCE HIHAT VALIDATION DATA: SUFFICIENT (bounded external annotation-based evaluation)

RIDE-vs-HIHAT DISCRIMINATION DATA: SUFFICIENT (study preparation, not validated discrimination)

EXTERNAL + INTERNAL EVIDENCE CHAIN: SUFFICIENT_FOR_NEXT_RIDE_RESEARCH_PHASE

NEW LIVE RIDE CAPTURE REQUIRED: NOT_YET_JUSTIFIED

NEW LIVE HIHAT CAPTURE REQUIRED: NOT_YET_JUSTIFIED

BEATREFERENCE AUTHORIZED: NO

BPM AUTHORIZED: NO

NEXT STEP REQUIRES PI AUTHORIZATION: YES
