# Vogl 2018 supplied-model MDB qualification

Prospective binding, 2026-09-10; PI authorizes execution. No MDB inference has occurred when this record is created.

Use official `madmom-drums-dafx18.tar.gz`, custom madmom 0.16.dev0, `DrumTranscriptor.2018`, default CRNN_8 ensemble (all five supplied O8 CRNN weights). The accompanying materials explicitly include MDB-trained networks: this is a supplied-model benchmark qualification with upstream training exposure, **not independent unseen-dataset transfer**. No JGA training, calibration, member selection or threshold optimization occurs.

Sources: https://www.ifs.tuwien.ac.at/~vogl/dafx2018/ and its mappings.py; package at https://ifs.tuwien.ac.at/~vogl/models/madmom-drums-dafx18.tar.gz. Software license BSD; models CC BY-NC-SA 4.0 as packaged. No commercial admission is implied.

Taxonomy: BD, SD, TT, HH, CY, RD, CB/bells, CL. RD output MIDI 51 is separate from CY 49 and HH 42. Primary Ride target is native MDB RDC only (835 recorded admission events). RDB is not pooled: the 8-class bell output combines Ride bell and cowbell. Report RDB timing coincidence with that broad bell output separately as conditional coverage, not Ride identity precision. HH target is union CHH/OHH/PHH, retaining subtype match counts. No generic label is inferred as bow.

Use all 23 admitted original MDB drum-only tracks, unchanged, with original subclass annotations. Root `/Volumes/SSD Track/JGA/datasets/RIDE-HIHAT-EXTERNAL/MDB-original-b29e2d63`; admission SHA-256 `3c66085a119419d21d8268b8aac37f8bc16cb613c399af825d7b248c87d92421`. Verify every admitted file before inference. No event-isolation exclusions or oracle onset crops. No prior GMD/ENST probe rerun. Existing project-level MDB exposure is acknowledged.

Use original CRNNDrumProcessor audio preprocessing and DrumPeakPickingProcessor, with command-line defaults: model CRNN_8, threshold 0.15, smooth 0, pre_avg 0.1 s, post_avg 0.01 s, pre_max 0.02 s, post_max 0.01 s, combine 0.02 s, delay 0, offline, 100 fps. No supplied setting is chosen from MDB. Python 3.11 compatibility may restore the moved `collections.MutableSequence` name without changing computation; any other technical change must be documented before scientific execution.

Scoring: supplied `madmom.evaluation.onsets.onset_evaluation` default window 0.025 s, inclusive absolute difference, sorted one-to-one chronological matching. This binds the package evaluation convention, not a claim that paper-specific validation tuning is reproduced. One prediction cannot match multiple annotations. Save all predictions before evaluating labels; freeze package source/weights, runner, protocol, dependencies and compiled extensions before inference. Preserve every track and original result, including failure.

Report aggregate counts and micro precision/recall/F1 for Ride and HH; per-track counts; HH subtype recovery; broad-bell RDB coincidence. Undefined ratios remain null. FP coincidence categories are descriptive temporal overlaps within the same 25 ms window, not causal source attribution; multiple possible classes remain unresolved. No numerical scientific PASS threshold is invented. A positive benchmark result remains limited by upstream MDB training exposure and cannot establish autonomous recognition or timing admission.

No fallback unless Vogl is technically unavailable/incompatible. No adaptation after results. No training, periodicity, BeatReference, BPM, Double-Bass changes, commit or push.
