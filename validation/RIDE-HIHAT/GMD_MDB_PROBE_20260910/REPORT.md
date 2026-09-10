# First GMD Ride / Hi-Hat probe and frozen MDB transfer

Date: 2026-09-10. Status: **EXECUTED — NEGATIVE INDEPENDENT TRANSFER RESULT PRESERVED; STOP FOR PI REVIEW.**

## Result and claim boundary

**Observed outcome: GMD_WORKS_MDB_TRANSFER_FAILS.** The prospectively bound short log-mel linear probe discriminates on held-out GMD drummers, but fails the untouched MDB Ride-versus-Hi-Hat transfer gate. No post-result adjustment, new dataset search, additional validation, autonomous event detection or timing work occurred. This does not show that acoustic discrimination is impossible; it shows this frozen rendered-data development pipeline did not transfer adequately under its specified test.

The population is **provider-annotated onset opportunities with no other annotated onset in the 250 ms crop**. Overlapping events are excluded and counted, not silently recovered or classified. Earlier tails can remain. Results do not cover all performance events. GMD is TD-11 rendered sound, not original acoustic cymbal capture; held-out drummers do not establish held-out sound-engine or instrument invariance. A domain difference is a possible explanation of the failed transfer, not a demonstrated cause.

## Prospective authority and input admission

[PROTOCOL.md](PROTOCOL.md) and [probe.py](probe.py) were fixed before GMD feature extraction/training. The task's explicit PI authorization covers the bounded operational parameter choices and conditional one-time MDB execution; no further broad research phase was introduced. The historical simplified design is unchanged (SHA-256 `0e0de13354e60d3f56d54d5542b4550a25f0fd16b2f2f9d179e56cd32904ebf3`).

GMD archive `/Volumes/SSD Track/JGA/downloads/groove-v1.0.0.zip` matched official SHA-256 `21559feb2f1c96ca53988fd4d7060b1f2afe1d854fb2a8dcea5ff95cf3cce7e9` before extraction. Originals remain under `/Volumes/SSD Track/JGA/datasets/RIDE-HIHAT-EXTERNAL/GMD-v1.0.0/groove/`; archive preserved. Admission manifest is in the sibling `authority/` directory. ZIP CRC and member SHA-256 recorded. Source files used by feature extraction were checked against admission hashes. `info.csv`, MIDI and WAV retained; provider page saved with admission provenance. License CC BY 4.0. [Official provider mapping/alignment/license](https://magenta.tensorflow.org/datasets/groove).

Provider authority supplies alignment within 2 ms; no independent physical-contact or new audio-alignment measurement is claimed. Native mapping preserves Ride bow51/edge59/bell53 and HH closed bow42/edge22, open bow46/edge26, pedal44. MIDI timing messages are used only for ticks-to-file-seconds conversion, not as classifier features or BPM inference. Audio pairs exist for 1,090/1,150 rows; no drummer2 audio and 42 missing drummer8 pairs. Missing material is not synthesized.

MDB admission remains `/Volumes/SSD Track/JGA/datasets/RIDE-HIHAT-EXTERNAL/MDB-original-b29e2d63/authority/admission_manifest.json`, SHA-256 `3c66085a119419d21d8268b8aac37f8bc16cb613c399af825d7b248c87d92421`. Original MIDI-free MDB subclass annotations supply scoring authority. Prior admission/aggregate label counts were known; MDB signals, features and model outcomes were unused in development. The MDB execution entry point checked the saved GMD freeze and environment before opening its inventory/audio. No refit or calibration on MDB. MDB remains CC BY-NC-SA 4.0; no commercial-use or redistribution permission inferred.

## Population and development separation

Training: drummers1,3,4,5,6; calibration: drummer7; held-out development: drummers8,9,10. No random event-level split. Training alone caps 250 eligible events per drummer/native subtype by stable hash, a resource limit rather than an evidence threshold. Calibration and evaluation retain all eligible events. Exclusion, selection and source lineage are preserved externally. No zero/incomplete feature crops remained after admission filtering.

GMD: 32,986 selected; exclusions {"BOUNDARY": 1736, "OTHER_ONSET_IN_WINDOW": 291385, "TRAIN_RESOURCE_CAP": 22117}. Before the training resource cap: 55,103 eligible events; Ride 6,190; Hi-Hat 21,276. Counts are dependent events, not independent instruments.

| GMD subtype | Train | Calibration | Held-out development | Total used |
|---|---:|---:|---:|---:|
| HH_CLOSED_BOW | 850 | 3939 | 2000 | 6789 |
| HH_CLOSED_EDGE | 962 | 2134 | 1810 | 4906 |
| HH_OPEN_BOW | 273 | 197 | 18 | 488 |
| HH_OPEN_EDGE | 673 | 217 | 520 | 1410 |
| HH_PEDAL | 555 | 243 | 188 | 986 |
| RIDE_BELL | 463 | 120 | 79 | 662 |
| RIDE_BOW | 1000 | 692 | 1037 | 2729 |
| RIDE_EDGE | 34 | 11 | 27 | 72 |

## Frozen representation, probe and operating rules

250 ms onset-centred mono crop, analysis44.1kHz, RMS-relative scaling, Hann2048/hop441, 32 Slaney mel bands20–20,000Hz, log1p magnitude, 26 frames/832 coordinates. StandardScaler and balanced logistic regression C1 fitted on training only; lbfgs converged in590 iterations without parameter adjustment. No onset spacing, velocity, tempo, grid, meter, style, filename or drummer field enters the classifier. Default0.5 is a diagnostic equal-cost boundary, not calibrated confidence.

Calibration-only selective boundaries: low `1.8731723246104754e-05`, high `0.9999970957595729`. The interval between them abstains. These avoid observed calibration errors by construction; they do not guarantee future precision or supply scientific sufficiency. Full precision–recall curves are preserved, without a test-picked operating threshold.

## Results

| Population | N / Ride | Precision | Recall | AP / prevalence | Balanced accuracy |
|---|---:|---:|---:|---:|---:|
| GMD held-out, all controls | 9954 / 1143 | 0.902008 | 0.982502 | 0.993678 / 0.114828 | 0.984328 |
| GMD held-out, Ride vs HH | 5679 / 1143 | 0.944491 | 0.982502 | 0.996107 / 0.201268 | 0.983976 |
| MDB, all controls | 2507 / 219 | 0.105882 | 0.082192 | 0.195640 / 0.087355 | 0.507879 |
| MDB, Ride vs HH | 1262 / 219 | 0.117647 | 0.082192 | 0.236230 / 0.173534 | 0.476379 |

The predeclared technical gate requires above-reference balanced accuracy and AP, both against all controls and within Ride-vs-HH. It is not statistical significance or high-confidence admission sufficiency. MDB fails the Ride-vs-HH balanced-accuracy gate (below0.5); no criterion changed after results.

| Selective population | Ride admitted (true / false) | Ride recall | Overall decision coverage | Abstentions | False NOT_RIDE |
|---|---:|---:|---:|---:|---:|
| GMD held-out | 751 (751 / 0) | 0.657043 | 0.702331 | 2963 | 0 |
| MDB | 4 (3 / 1) | 0.013699 | 0.755086 | 614 | 81 |

Coverage includes NOT_RIDE decisions; it is not Ride recall. MDB's three correct selective Ride admissions do not offset 81 false NOT_RIDE decisions on Ride, one false Ride admission, and extremely low Ride recall. Finite-sample perfect precision in the GMD selective subset is not a guarantee. No naive event-independent confidence interval is asserted.

### Subtype confusion at the frozen 0.5 diagnostic boundary

For positive Ride rows, TP/FN; for negative HH rows, FP/TN. Complete other-control and per-group metrics remain in result JSON.

| Dataset | Subtype | N | TP | FP | FN | TN |
|---|---|---:|---:|---:|---:|---:|
| GMD held-out | HH_CLOSED_BOW | 2000 | 0 | 36 | 0 | 1964 |
| GMD held-out | HH_CLOSED_EDGE | 1810 | 0 | 17 | 0 | 1793 |
| GMD held-out | HH_OPEN_BOW | 18 | 0 | 0 | 0 | 18 |
| GMD held-out | HH_OPEN_EDGE | 520 | 0 | 0 | 0 | 520 |
| GMD held-out | HH_PEDAL | 188 | 0 | 13 | 0 | 175 |
| GMD held-out | RIDE_BELL | 79 | 79 | 0 | 0 | 0 |
| GMD held-out | RIDE_BOW | 1037 | 1018 | 0 | 19 | 0 |
| GMD held-out | RIDE_EDGE | 27 | 26 | 0 | 1 | 0 |
| MDB | HH_CLOSED | 788 | 0 | 131 | 0 | 657 |
| MDB | HH_OPEN | 99 | 0 | 2 | 0 | 97 |
| MDB | HH_PEDAL | 156 | 0 | 2 | 0 | 154 |
| MDB | RIDE_BELL | 6 | 0 | 0 | 6 | 0 |
| MDB | RIDE_UNSPECIFIED | 213 | 18 | 0 | 195 | 0 |

MDB: 2507 eligible opportunities out of7,994 annotations; 28 boundary and5,459 other-onset exclusions. Eligible Ride219 (213 unspecified,6 bell), Hi-Hat1,043 (788 closed,99 open,156 pedal). No mapping of unspecified Ride to bow. This is a limited real-performance subset, not a full transcription validation.

## Preservation and checks

External result root: `/Volumes/SSD Track/JGA/experiments/RIDE-HIHAT-GMD-MDB-01/`. Each dataset folder preserves inventory/exclusions, feature lineage, features, predictions, full PR curve and result. Model and freeze precede MDB execution. Logs and initial execution/environment binding retained. Only protocol, implementation and this lightweight report enter the repository working tree. No commit/push; previous unrelated dirt preserved.

| Artifact | SHA-256 |
|---|---|
| `PROTOCOL.md` | `70a6a8dcf2845d506febe299318197b6ffe742480a98db8e3165c1a406ca761d` |
| `probe.py` | `094a19784dc267876b858537647a3da2dbbc5bf03989931cabda4a860db3bb69` |
| `execution_binding.json` | `7a56af38bfbcb5ad6a5aae69912cd3fe984e90f41292fdcdb3b393b5b921cbe8` |
| `freeze.json` | `438aaab8438e020b4d22fc39e431365228077dfd9177a4c8d68ff548dd952ab1` |
| `gmd/model.npz` | `efb90babca6f5e18dc267564bc6f225c3aa80ee3b4396cc4b66111b2f49adcb9` |
| `gmd/result.json` | `9005b29e45c0b13e0ed09abc773edda5c134561759eb9c9b2d15a99465eedea7` |
| `mdb/result.json` | `3aceee82c630a2dfb462353ecd1064fb2f9580525dd82907e1d9a8a8da3a8971` |

Environment: Python3.13.14; numpy2.4.6, scipy1.18.0, scikit-learn1.9.0, soundfile0.14.0, librosa0.11.0, mido1.3.3 (installed only in external experiment dependencies); thread limits1. Exact environment stored in freeze. Eight synthetic mapping/eligibility/representation/clock checks passed. Code/protocol/model/result hashes checked after validation. One GMD fit and one MDB validation, no empirical rerun or independent computational checker claimed. Analyst/implementer is the same Codex assistant; external label authority and separate data roles do not imply independent human review.

## Next minimal step

**PI review of the preserved negative MDB transfer result, to decide whether to authorize one bounded acoustic-development substitution.** No substitution, new search, recording, training, threshold change or repeat validation begins in this task. Autonomous event recognition, BeatReference and BPM remain unauthorized.
