# Vogl 2018 pretrained Ride qualification

Date: 2026-09-10. PI-authorized supplied-model qualification. **Completed: PRETRAINED RIDE RECOGNITION = PROMISING**, within this MDB-exposed benchmark only. No custom training or MDB adaptation occurred.

## Result

All 23 tracks completed with unchanged supplied settings. Primary Ride-cymbal precision is **96.3068%**, recall **40.5988%**, F1 **57.1188%**. This supports further bounded qualification of a selective Ride output, not autonomous JGA admission or independent transfer. No post-hoc operating point was selected.

| Target | GT | Predictions | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Ride cymbal (RDC; model RD) | 835 | 352 | 339 | 13 | 496 | 96.3068% | 40.5988% | 57.1188% |
| Hi-Hat parent | 2,639 | 2,758 | 2,271 | 487 | 368 | 82.3423% | 86.0553% | 84.1579% |

Hi-Hat matched/GT by native subtype: CHH 1,599/1,847; OHH 232/269; PHH 440/523. State-specific precision is not identifiable from a parent-only output.

The broad bell output produced 197 predictions, of which two matched the 16 RDB annotations under the same window. This is **conditional RDB coverage 2/16**, not a pure Ride-bell recognition result. Cowbell/bell output cannot be promoted to Ride identity. Four of the primary RD false positives temporally coincide with RDB annotations; they remain false positives for the prospectively bound RDC-only target.

The 13 primary Ride false-positive temporal coincidences are: RDB 4; SD 3; CRC+KD 2; CHH 1; CHH+KD 1; CHH+SD 1; PHH 1. These are annotation overlaps, not proven acoustic causes. Multiple concurrent labels remain unresolved attribution. No unmatched-within-window case occurred.

### Ride per-track population

| MusicDelta track | GT | Predictions | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| 80sRock | 0 | 0 | 0 | 0 | 0 |
| Beatles | 0 | 0 | 0 | 0 | 0 |
| BebopJazz | 1 | 0 | 0 | 0 | 1 |
| Britpop | 0 | 0 | 0 | 0 | 0 |
| CoolJazz | 0 | 0 | 0 | 0 | 0 |
| Country1 | 0 | 0 | 0 | 0 | 0 |
| Disco | 0 | 0 | 0 | 0 | 0 |
| FreeJazz | 176 | 56 | 49 | 7 | 127 |
| FunkJazz | 0 | 0 | 0 | 0 | 0 |
| FusionJazz | 95 | 15 | 14 | 1 | 81 |
| Gospel | 0 | 2 | 0 | 2 | 0 |
| Grunge | 0 | 0 | 0 | 0 | 0 |
| Hendrix | 0 | 0 | 0 | 0 | 0 |
| LatinJazz | 95 | 21 | 21 | 0 | 74 |
| ModalJazz | 359 | 241 | 238 | 3 | 121 |
| Punk | 0 | 0 | 0 | 0 | 0 |
| Reggae | 0 | 0 | 0 | 0 | 0 |
| Rock | 0 | 0 | 0 | 0 | 0 |
| Rockabilly | 0 | 0 | 0 | 0 | 0 |
| Shadows | 106 | 17 | 17 | 0 | 89 |
| SpeedMetal | 0 | 0 | 0 | 0 | 0 |
| SwingJazz | 3 | 0 | 0 | 0 | 3 |
| Zeppelin | 0 | 0 | 0 | 0 | 0 |

ModalJazz contributes 238 of 339 primary true positives. High aggregate precision does not establish uniform track coverage or adequate recurrence support. Absent predictions do not establish absence of Ride. Per-track Hi-Hat scores and subtype matches are preserved in result.json.

## Capability and execution authority

The [official accompanying materials](https://www.ifs.tuwien.ac.at/~vogl/dafx2018/) provide a downloadable custom madmom package. HTTP 200, 153,667,286 bytes, server Last-Modified 2018-04-24. Downloaded archive SHA-256: `4b3cc9a3a7bd66fa120433a4a70b77af7be4d19d619508f83c7845a2faaaab9d`. This is a locally verified content identity, not an independently published provider SHA-256.

Selected supplied default: **CRNN_8**, custom madmom **0.16.dev0**, executable **DrumTranscriptor.2018**. The website names DrumTranscription, but the actual archive contains `bin/DrumTranscriptor`. All five `drums_crnn1_O8_S0` through `S4` members are retained; no member was selected from MDB performance. Only these pretrained weights were extracted, alongside package code and documentation. The full downloaded archive remains externally preserved.

The [official mappings](https://www.ifs.tuwien.ac.at/~vogl/dafx2018/mappings.py) and package agree: BD, SD, TT, HH, CY, RD, CB/bells, CL. RD is distinct from CY and HH. **Ride bell shares the broad bell/cowbell class**; its output is not clean Ride identity. Primary Ride scoring therefore uses RDC only, without inventing bow identity. HH preserves CHH/OHH/PHH annotation subtypes, although the model predicts their parent. The 18-class alternative is unnecessary for this first RD qualification.

**Important limitation:** the official supplied ensemble includes models trained on MDB. This execution can qualify the supplied recognizer on MDB but cannot establish independent unseen-dataset transfer. It does not repeat the paper's cross-validation. No JGA training, tuning, calibration or adaptation occurred. Previous project-level MDB exposure from the GMD and ENST probes is also preserved.

## Frozen method and technical qualification

See [PROTOCOL.md](PROTOCOL.md) and [qualify.py](qualify.py). Protocol SHA-256: `a9fbf643fd03ef1d692ab626df7840b9b4ced1fb960057a0181a8bd5ea2c3450`; runner SHA-256: `732f37fe533d137d1a1367709b6516145711f01c120668f938dc9cdd22087283`.

External root: `/Volumes/SSD Track/JGA/experiments/RIDE-HIHAT-VOGL-2018/`. Pre-inference `execution/freeze.json` SHA-256: `1e6535e4669bb520882d80b76506d8b1daa3e024f0cd41ae26e62d542ce0d2f4`. It binds each weight, package source/compiled extension, admitted audio, runtime, dependencies, protocol and runner.

Isolated Python 3.11.15; NumPy 1.23.5, SciPy 1.10.1, Cython 0.29.37, setuptools 69.5.1, mido 1.3.3. Main JGA environment unchanged. The shipped stale generated `layers.c` failed compilation against Python 3.11; regenerating it with Cython from unchanged `layers.py` resolved this. A wrapper restores `collections.MutableSequence` from `collections.abc`. No weight, model source, preprocessing or peak rule was changed. Build logs remain external. AppleDouble metadata caused harmless package-discovery warnings.

Six synthetic evaluator checks covered empty inputs, duplicate predictions, duplicate annotations, inclusive 25 ms boundary, just-outside boundary and exact matches. The independent index traversal agreed with the supplied evaluator. The unchanged model processed one second of synthetic silence into finite `(100, 8)` activations; wrapper validation was corrected to accept the supplier's empty peak-array shape before real input.

An initial admission-only attempt stopped because a filename glob included macOS `._` sidecars. No freeze or inference had occurred. The loader was corrected to use exactly the 23 authoritative manifest paths; all admitted file bytes/hashes were verified. Both the aborted admission log and actual execution log are retained. This did not exclude any scientific track or event.

The supplied audio preprocessing and peak picker are used directly. Fixed peak threshold 0.15; smooth 0; pre/post average 0.1/0.01 s; pre/post maximum 0.02/0.01 s; combine 0.02 s; no delay; 100 fps. No explicit timing regularity, tempo, beat or meter input exists in the wrapper. Audio-based recurrent network context is retained as supplied.

**Event matching:** the archived `madmom.evaluation.onsets` default is **±25 ms inclusive**, sorted one-to-one chronological matching. This is the supplied software evaluation convention; it is not claimed as a reconstruction of paper-specific optimized evaluation settings. Predictions are frozen across all tracks before annotation scoring. No oracle crops, overlap exclusions, post-hoc threshold changes or favorable-track selection are permitted. Undefined metrics remain null.

## Input and preservation

Original MDB admission: `/Volumes/SSD Track/JGA/datasets/RIDE-HIHAT-EXTERNAL/MDB-original-b29e2d63/authority/admission_manifest.json`, SHA-256 `3c66085a119419d21d8268b8aac37f8bc16cb613c399af825d7b248c87d92421`. All 23 drum-only WAVs and original subclass annotations are used. Primary Ride GT is 835 RDC events. Sixteen RDB events remain separate because of the model's broad bell class. HH GT is 2,639: 1,847 CHH, 269 OHH, 523 PHH.

Protected reports reverified unchanged:

- GMD→MDB: `a748d39b63a9807e7c5a4408ac4bef6cadacd27e1689c38cf8afe14b9db20ec0`.
- ENST→MDB: `17631ce43a866d741af63cd808b83e2226db45d7cdcd254ad55b51777e1d3387`.

Package software is BSD; model files and MDB are CC BY-NC-SA 4.0. Attribution, noncommercial and share-alike restrictions remain; this research run does not authorize commercial JGA incorporation. No model/audio files are copied into Git.

No fallback was required: the official pretrained package is obtainable and executes. No Riley/Dixon fallback research or execution, custom training, GMD/ENST rerun, periodicity, BeatReference, BPM, Double-Bass work, commit or push occurred.

## Completed output and integrity authority

Under the external experiment root:

- `execution/result.json`: SHA-256 `d4e46ad2e77bc51aaa89ec185c59e8d34c1e515b1117b62315a511877ea103f2` — aggregate and all per-track scores, subtype matching, FP coincidences, training-exposure limit.
- `execution/predictions_frozen.json`: SHA-256 `4c5214ecf3bccbd51f038e672160ffd5ed247406df0c0398f0a5db725a2fea1d` — predictions bound before scoring.
- `execution/SHA256.json`: SHA-256 `39c66ccc90b51e626125820576c68362633b05d9a51661d3d0fea819810a3295` — 98 listed output hashes checked successfully after completion.
- `execution/*.activations.npy` and `*.predictions.json`: all 23 tracks, no selection.
- `execution.log`: preserved aborted admission attempt; `execution_admitted.log`: actual successful inference/evaluation; `build.log` and `build_retry.log`: technical build history.

The broad output glob also bound macOS AppleDouble sidecars: 23 scientific prediction JSON files plus 23 `._` metadata companions in the prediction manifest. They were never scored or counted as tracks. The overall checksum manifest similarly includes sidecars. The first post-run verification's unfiltered 23-entry assertion exposed this overinclusive metadata inventory; subsequent verification distinguished the 23 real predictions and checked **every** listed hash unchanged. No manifest or result was retroactively repaired. Scientific outputs excluding sidecars total 4,465,292 bytes including the checksum inventory itself.

The supplied evaluator and independent index traversal agreed for every scored target/track. The complete output checksum inventory and all prediction bindings passed verification. Protocol and runner hashes match their pre-inference freeze. This is one execution, not a claimed fresh-process replay. OPENBLAS_NUM_THREADS and OMP_NUM_THREADS were both 1; no optional OpenCV backend was installed. Heavy package, environment, audio references and outputs remain external. Only this report, prospective protocol and small runner are repository additions.

## Interpretation and next PI action

Observed fact: the supplied RD output recovered a high-precision, incomplete subset of MDB RDC annotations at its unmodified default operating point. Logical inference: this is **PROMISING** for further selective Ride qualification, with no arbitrary scientific PASS threshold. It neither validates an independent real-audio domain nor establishes that the recovered events suffice for timing. Upstream MDB training exposure, parent/subtype limits and uneven coverage are material limits.

Custom Ride classifier required now: **NOT_YET_JUSTIFIED**. Next minimal PI action: authorize a bounded Ride-admission interface and its evaluation on independently labeled JGA real audio; label authority must be bound before claiming accuracy in that domain. Do not infer identity correctness from periodicity. No autonomous JGA Ride-event recognition, BeatReference or BPM is authorized by this result.

STOP FOR PI REVIEW.
