# Vogl Ride qualification on independent JGA audio

2026-09-10. **STOPPED BEFORE INFERENCE: independent Ride-event Ground Truth unavailable in the minimal candidate set.** Result: **INDETERMINATE**, not a recognizer failure. One report only; no scientific execution occurred.

## Preserved authority

The accepted Vogl/MDB report remains unchanged: `validation/RIDE-HIHAT/VOGL_2018_QUALIFICATION_20260910/REPORT.md`, verified SHA-256 `cd43262c0149ec732eb3613e0bf2486e5e246630df8dd5abd49dc6500c140a07`. Its MDB training-exposure limitation remains binding. The supplied model package and five weights were checked against `/Volumes/SSD Track/JGA/experiments/RIDE-HIHAT-VOGL-2018/execution/freeze.json`; all bound package files match. No weights, taxonomy, preprocessing or threshold changed.

Repository authority, rather than a fresh provider-web or model search, was used. The existing internal asset audit was verified at SHA-256 `7c1fd3e86a8279183fa2d17ec11f06ee4de4ddd459c0280b355f0e06f0ded15a`: `docs/scientific/rfc/RIDE_HIHAT_EXISTING_ASSET_SUFFICIENCY_AUDIT.md`.

## Minimal candidate comparison

| Candidate | Existing evidence inspected | Independent Ride-event authority | Decision |
|---|---|---|---|
| CED-VAL-006 LEWITT COSMIX | INPUT_AUTHORITY.md, ANALYTICAL_INPUT_AUTHORITY.md, input_authority_manifest.json, current external file inventory | No Ride spot or event annotations. Provider live/RAW overhead provenance; supporting video has no qualified synchronization or event labels. | Primary candidate for later label qualification; strongest documented live provenance. |
| CED-VAL-005 Maurizio Pagnutti Sextet | INPUT_AUTHORITY.md, input_authority_manifest.json, existing audit and current external inventory | Hi-Hat spot and overheads, but no independent Ride-event catalogue or established Ride source dominance. | Hi-Hat track intent does not improve Ride-event truth sufficiently to displace 006. |
| CED-VAL-007 controlled benchmark | INPUT_AUTHORITY.md, input_authority_manifest.json, current external inventory | Authored/rendered symbolic schedule; not independent live acoustic Ride events or a qualified component mapping. | Does not meet the present real-performance identity objective. No symbolic timing values were used for identity. |
| Adjacent 009/010 | Existing internal audit, sections 3–7 and prior-measurement summary only | Original overhead evidence without component-event labels. | No documented stronger alternative; no expanded search undertaken. |

Read-only filename discovery under the three primary external dataset roots found no new Ride annotation/label file supplying the missing authority. Existing detector/EME records and separated Drum stems do not establish component identity. No listening, video annotation, new feature measurement or source separation was performed.

## Selected prospective input

**CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK**, original stereo overhead:

`/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw/Dums Overheads LCT 640 TS-Dual Output Mode.wav`

Reverified SHA-256: `dbfc4c3c59cac2c42cb2bbd33f1e55dbb1ec8c2fe6c6d095e30efc791dd57b8d`. Existing metadata: signed PCM24, 48 kHz, stereo, 11,912,868 frames, 248.184750 seconds. This is the candidate input, **not an executed or newly validated Ride input**. It preserves the existing direct original Drum-input route without a new mix or separated-stem confound. No secondary input is selected.

006 INPUT_AUTHORITY.md SHA-256: `55da89d2b74576f68aef77037703467e933b535821a4a3e579e935d3a4bfecdb`; ANALYTICAL_INPUT_AUTHORITY.md: `3eeee69dc9a7a27a156eaab3b820e085ec518cf8ad0e9b0930b79aed205b01f1`. Their historical temporal-reference role is not reused as Ride identity or beat authority.

## Why precision cannot yet be scored

**Observed documentary fact:** 006 establishes a live Drum overhead channel, not which event is Ride. Exact per-file sample coordinates are available; Ride-event identity and annotation-time uncertainty are not. Authority for the requested Ride GT is therefore **INSUFFICIENT**. Broad Drum provenance is track-level only and must not be promoted even to a conditional Ride-event label.

**Logical inference:** incomplete Ride labels could support a bounded precision study only if an independently defined evaluation region or prediction-blind reference assessment could adjudicate the emitted events, including non-Ride and unresolved cases. No such authority currently exists. Matching overhead transients to kick/snare channels or trusting a Hi-Hat channel cannot identify the remaining transients as Ride; other cymbals, bleed and simultaneous hits remain possible. A 25 ms window cannot repair missing class labels.

The supplied `Cosmix Video.mov` is a possible route to independent physical-action evidence. Existing authority binds its provenance and container but explicitly assigns no synchronization or annotation authority. Visibility, occlusion, cymbal identification, audio/video offset and timing uncertainty would need a bounded, prediction-blind qualification before labels could be used. This report does **not** establish that video annotation is impossible or that it will succeed. No Vogl predictions were generated to guide such assessment.

The recording is distinct from the MDB package, but absence from every upstream training source has not been independently certified. That check would remain part of any later transfer claim. No new independent-validation claim is made here.

## Outcome and exact next action

Ride GT count, TP/FP/FN, precision/recall/F1 and correct-event temporal span: **unavailable**. Vogl predictions: **NOT EXECUTED**, not zero. Hi-Hat scoring was not expanded. JGA Ride admission: **INDETERMINATE**. Ride-conditioned periodicity test justified by this task: **NO**. Custom classifier required now: **NOT_YET_JUSTIFIED**; the immediate gap is independent reference evidence, not a demonstrated model failure.

Next minimal PI action: **authorize a prediction-blind feasibility qualification of the existing COSMIX video/audio for independent Ride-event annotation**. Keep model predictions inaccessible; bind observable labels, unresolved cases and synchronization uncertainty before any scoring. No new recording is established as necessary.

No inference, periodicity, BeatReference, BPM, model tuning, Double-Bass change, commit or push occurred. Existing audio, scientific reports and model authority remain unchanged. No external result package was created because execution was not reached.

STOP FOR PI REVIEW.
