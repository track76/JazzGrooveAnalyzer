# Pretrained ADTOF Ride / Hi-Hat qualification

Date: 2026-09-10. Reviewer: Codex /root. Status: **STOPPED AT CAPABILITY / TAXONOMY GATE; NO INFERENCE EXECUTED**.

## Finding and claim boundary

**Observed documentary fact:** the supplied ADTOF-pytorch model has five outputs, including a combined cymbal/Ride class. It has no separate Ride output. Hi-Hat is separate from that combined class, but this is insufficient for the requested Ride-specific qualification.

**Logical inference:** relabeling all combined cymbal predictions as RIDE_COMPATIBLE would change the target and cannot establish Ride identity against other cymbals. Higher activation confidence cannot recover a distinction absent from the supplied output taxonomy. This is a capability mismatch, not an observed empirical transfer failure. Transfer outcome: **INDETERMINATE / NOT EXECUTED**.

**Decision under PI's explicit taxonomy stop condition:** stop before installation, weight acquisition, matching-rule freeze or MDB inference. Do not substitute a generic cymbal experiment or execute a partial Hi-Hat experiment. No custom recognizer is established as necessary by this finding.

## Implementation and source authority

- Port: [xavriley/ADTOF-pytorch](https://github.com/xavriley/ADTOF-pytorch), package version 0.1.0, resolved `main` commit **85c192e78f716ea0b111cc8a5ee4a8f6a3a4f8a9**. GitHub Git-ref API explicitly identifies this SHA as a commit. The recursive inventory was inspected without downloading weights.
- [Pinned post_processing.py](https://github.com/xavriley/ADTOF-pytorch/blob/85c192e78f716ea0b111cc8a5ee4a8f6a3a4f8a9/src/adtof_pytorch/post_processing.py#L7): output codes `[35,38,47,42,49]`; Git blob identity `abdd54521434608859d69bef1ec9146dd093d8fc`.
- [Model factory](https://github.com/xavriley/ADTOF-pytorch/blob/85c192e78f716ea0b111cc8a5ee4a8f6a3a4f8a9/src/adtof_pytorch/model.py#L209): explicitly constructs five output classes. Architecture configurability is not evidence of additional pretrained classes.
- [Original ADTOF configuration](https://github.com/MZehren/ADTOF/blob/master/adtof/config.py#L184) names these outputs BD, SD, TT, HH, CY+RD. The [original mapping](https://github.com/MZehren/ADTOF/blob/master/adtof/ressources/instrumentsMapping.py) supplies the class semantics below. These original-source links were inspected on this date and are moving references, not frozen JGA implementation authority.
- [Original project](https://github.com/MZehren/ADTOF) explicitly links the separate PyTorch port. Its README describes the port as a conversion of the released weights, with approximate rather than exact equivalence.

## Taxonomy gate

| Native distinction | Supplied five-class result | JGA consequence |
|---|---|---|
| Ride MIDI 51, Ride bell 53, second Ride 59 | All become 49 | Ride subtypes cannot be recovered separately |
| Crash 49/57, China 52, Splash 55 | Also become 49 | Combined output cannot distinguish Ride from these confounds |
| Closed Hi-Hat 42, pedal 44, open 46 | All become 42 | Hi-Hat parent is available; state-specific outputs are absent |
| Bass drum / snare / toms | 35 / 38 / 47 | Remaining three output families |

Generic Ride does not establish bow. Original source contains a six-class mapping that separates Ride, but the reviewed supplied port uses five outputs. A mapping constant alone does not establish availability of a compatible six-class trained checkpoint.

MDB retains RDC (Ride), RDB (bell), CHH/OHH/PHH. These native labels must remain unchanged; mapping RDC/RDB plus Crash/China/Splash to one evaluation target would answer a different question.

## Weights, license, and inference conventions

The inventory lists packaged `src/adtof_pytorch/data/adtof_frame_rnn_pytorch_weights.pth`: 3,617,805 bytes, Git blob SHA-1 `773d228e4a4250ed278aecb9fe61e5d0ed611324`. The root `data/` copy has the same blob identity. Availability is documented; weights were not downloaded, SHA-256 verified or loaded.

The original repository states CC BY-NC-SA 4.0. The inspected port inventory has no LICENSE file and its pyproject has no license declaration; a separate explicit port-code grant was not established. This does not grant unrestricted redistribution of the converted weights or port. Licensing and checkpoint training/validation overlap remain unresolved for any later execution; neither required further investigation after the decisive taxonomy stop.

[Port audio implementation](https://github.com/xavriley/ADTOF-pytorch/blob/85c192e78f716ea0b111cc8a5ee4a8f6a3a4f8a9/src/adtof_pytorch/audio.py): documented defaults are mono, 44.1 kHz, 2,048-sample frames, 100 frames/s, 12 bands/octave, 20 Hz–20 kHz, normalization off. These are inspected defaults, not a JGA-executed configuration.

The API can return framewise sigmoid activations. Default peak thresholds are 0.22/0.24/0.32/0.22/0.30 in output order. Peak timestamps use frame index divided by frame rate; exported note lengths and velocity are fixed rendering values. Activations are not independently calibrated Ride probabilities. No event-matching tolerance was selected or applied because no Ride output can be admitted. No precision/coverage curve exists.

## Preserved local evidence

Both protected report hashes were rechecked and match PI authority:

- `validation/RIDE-HIHAT/GMD_MDB_PROBE_20260910/REPORT.md`: `a748d39b63a9807e7c5a4408ac4bef6cadacd27e1689c38cf8afe14b9db20ec0`.
- `validation/RIDE-HIHAT/ENST_MDB_PROBE_02_20260910/REPORT.md`: `17631ce43a866d741af63cd808b83e2226db45d7cdcd254ad55b51777e1d3387`.

Existing MDB admission inspected read-only:
`/Volumes/SSD Track/JGA/datasets/RIDE-HIHAT-EXTERNAL/MDB-original-b29e2d63/authority/admission_manifest.json`;
SHA-256 `3c66085a119419d21d8268b8aac37f8bc16cb613c399af825d7b248c87d92421`.
Its recorded population has 851 Ride annotations (835 RDC, 16 RDB), and 2,639 Hi-Hat annotations (1,847 CHH, 269 OHH, 523 PHH). These are admission counts, not results from an ADTOF run. Audio payloads were not reanalyzed or freshly reverified for execution.

All prediction counts, TP/FP/FN, precision/recall/F1, per-track errors, subtype recovery and false-positive attribution are **NOT EXECUTED**, not zero. Previous MDB project exposure remains acknowledged; checkpoint-level independence has not been established.

No environment installation, model acquisition, audio execution, training, tuning, old-probe rerun, dataset alteration, timing work, Double-Bass modification, commit or push occurred. Only this lightweight report was created.

## Next minimal PI action

Authorize a bounded availability/taxonomy check for one pretrained checkpoint with an explicit Ride output separate from other cymbals, before another MDB test. No broad model search or custom training is justified by this capability finding alone.

STOP FOR PI REVIEW.
