# Scientific checkpoint — Hi-Hat 2&4 and complete real-audio pipeline

Date: 2026-09-10. Authority: current PI consolidation instruction. This is the current checkpoint and workflow decision, not a new experiment. Historical reports remain byte-preserved. Report hashes and preservation inventory: [checkpoint manifest](../project/TIMING_CHECKPOINT_20260910.json).

## JGA architecture and workflow decision

JGA studies quantitative timing relationships in jazz ensembles, with source/event lineage and uncertainty. Core observations → Translation evidence → Domain musical interpretation remains the dependency boundary. Labels, separator output names and candidate detections do not automatically establish physical source/event Ground Truth. External models are tools, not JGA-trained scientific identity authority.

**Every primary real/full-mix JGA analysis must use:** full audio → approved source separation → relevant native stem → instrument/event recognition → timing analysis → domain interpretation → BPM/behaviour analysis. Direct recognizer-on-full-mix execution is admissible only as an explicitly authorized control. This workflow applies to future Double-Bass full-mix analysis too; original isolated/multitrack evidence retains its documented authority and is not silently relabelled separated data. No Double-Bass experiment changes here.

Current approved separation: JGA `DemucsSeparator.separate_authorized` / `AuthorizedDemucsRunner`, pinned `htdemucs_6s`, Demucs 4.1.0, offline verified weights/environment, native six-source outputs and AD-041 identities. [Operational binding](../architecture/AD-041_HTDEMUCS6S_OPERATIONAL_BINDING.md). Bind each new parent and separator scope explicitly; preserve all native outputs, but analyze only authorized roles. Never equate separated Drums with event-level GT. Do not introduce another separator configuration silently.

## Accepted development and recognition evidence

- **GMD:** controlled, held-out drummer Ride/Hi-Hat discrimination worked (Ride-vs-HH precision 94.45%, recall 98.25%, AP 99.61%); frozen original-MDB transfer failed (precision 11.76%, recall 8.22%). This was a JGA-trained small log-mel probe on rendered GMD sounds, not proof of acoustic invariance.
- **ENST:** the modest controlled diagnostic gate passed, but useful selective Ride admission was not established even on held-out ENST; ENST→MDB transfer failed. Exact outcome remains `ENST_CONTROLLED_DISCRIMINATION_WORKS_MDB_TRANSFER_FAILS`, not a relabelled success. No failed model was retuned.
- **MDB:** original annotations remain evaluation evidence. Independence is model-relative: new GMD/ENST models froze before their MDB executions, but prior project-level exposure is documented. Do not claim MDB was globally never seen.
- **Vogl 2018:** official pretrained custom madmom 0.16.dev0 / CRNN_8, five supplied ensemble members, made executable in isolated external Python 3.11 environment. RD is distinct from CY/Crash and HH. Broad bell output is not pure Ride-bell identity; HH output has no inferred closed/open/pedal subtypes. Vogl was not trained/fine-tuned by JGA.
- **Vogl MDB qualification:** Ride precision 96.31%, recall 40.60%, F1 57.12%. The supplied ensemble includes MDB-trained members: **not independent MDB transfer validation**. Keep noncommercial/model and dataset license limits from the report; no commercial-use grant is implied by executable availability.

## Jazz timing evidence

**CED-VAL-009 — Jesper Buhl Trio, What Is This Thing Called Love:** first 60 seconds of original overhead audio; 113 frozen Ride candidates, 962 recurrent exact relations, 2,304 supporting pairs; multiple competing separations, no BeatReference. Reused HH outputs supplied only ten candidates and zero exact repeated relations. This is candidate recognition, not verified component-event GT.

**CED-VAL-005 — Maurizio Pagnutti Sextet, All The Gin Is Gone:** PI observations, not algorithm inputs: opening bass ostinato; short walking around 12–16 s; ostinato to approximately 28 s; walking from approximately 28 s to 2:35; Hi-Hat 2&4 role; Ride present but possibly very delicate. No Bass timing was used to recognize events or select relations.

Fixed [28,88) interval: overhead Ride produced 29 candidates and a 29.49-second prediction gap; 22 recurrent exact relations and 46 supporting pairs, insufficient for a reference. Dedicated HH produced 141 candidates, 1,649 recurring exact relations and 5,444 supporting pairs. Exact 0.500 s led local support in six primary and five shifted regions. This supports descriptive local persistence, not guaranteed physical correctness, missing-event robustness or a universal source preference.

Synchronization: both original files declare Broadcast WAV sample zero and equal sample rates/frame counts. PI visual observation and bounded waveform check support practical co-timed file coordinates. Eight preselected windows through 210 s gave raw lag peaks approximately -4.97 to +3.54 ms; the terminal window was ambiguous for precise lag. No shift applied; sample-exact physical origin/latency is not claimed. Synchronization is **not the primary current limitation** of the preserved cross-source test. Sparse Ride/detector uncertainty and unresolved common temporal structure remain the principal limitations. Cross-source test: 4,089 labelled pairs, 530 repeated signed relations, 17 common within-source separations; insufficient to choose a common BeatReference. No pooled event population or inferred missing strokes.

## Internal candidate and prospective domain rule

The frozen CED-VAL-005 internal decision remains **0.500 s → 120 BPM**, operationally promising, half/double metric ambiguity unresolved. External approximately 246 BPM was supplied afterward for the PI's retrospective comparison. Do not rewrite the historical internal selection or present a corrected value as its original output.

The [JAZZ_HIHAT_2_4_TIMING_RULE](JGA_HIHAT_2_4_TIMING_RULE_20260910.md) is PI-adopted and frozen as a **prospective domain hypothesis**, not prospectively validated. Qualified persistent jazz HH timekeeping anchors may be interpreted as alternating 2/4 roles: `T_BEAT=T_HH/2`, `BPM_INTERNAL=120/T_HH`. HH presence alone is insufficient. The gate requires source/time authority, recurrence, successive local persistence, coverage, timekeeping rather than isolated accents, and reproducibility. Insufficient/ambiguous evidence requires `HIHAT_2_4_REFERENCE_UNAVAILABLE`.

Keep observed candidates/events, qualified timekeeping events, actual reference anchors and inferred intermediate beats distinct. Missing predictions do not create anchors. The rule does not establish which first anchor is 2 versus 4 or a bar origin. Unsupported observations remain visible in lineage; emphasize supporting observations without declaring other events erroneous. Bass timestamps must eventually be measured relative to independently established anchors, never snapped to them or used circularly to construct them.

Retrospective motivation only: CED-VAL-005 `T_HH=0.500 s`, `T_BEAT=0.250 s`, rule interpretation **240 BPM**, versus approximately 246 BPM. **No prospective validation** follows. Generic BeatReference is fallback if qualified HH evidence is unavailable, not automatic execution. Ride remains separate timing/articulation evidence for future swing, subdivision, drummer placement, microtiming and historical studies.

## Chet Baker: prospective attempt stopped upstream

Source: `III_Chet Baker - I fall in love too easily.mp3`. Direct full-mix Vogl produced zero HH candidates; preserve this as **CONTROL ONLY**, not complete JGA analysis.

Canonical complete pipeline: original mix → approved htdemucs_6s/Demucs4.1.0 → native Drums stem → unchanged Vogl → frozen qualification. Result again **zero Hi-Hat candidates; gate FAIL; no T_HH, no T_BEAT, no internal BPM**. Brush performance is PI context. Likely recognition-domain limitation under brushes is an interpretation, not demonstrated causation or proof of physical HH absence. **The 2&4 mathematical mapping was not tested because recognition failed upstream.** No external Chet BPM was used or checked.

External package `/Volumes/SSD Track/JGA/experiments/CHET-HTDEMUCS6S-HIHAT24-20260910/`; Drums at `stems/drums.wav`. All six stems, identities, weights/config bindings and result are preserved. Native Demucs output has 8,930,304 frames versus 8,928,047 for the previous decode (2,257-sample difference); no trim/shift was applied and exact decoder-to-stem onset alignment is not claimed.

## The approximately 15 GB earlier job — identified

Accepted complete real-Drum local complex periodicity map: [acceptance](../../validation/VAL-001/complete_real_drum_periodicity_20260908/README.md). External root `/Volumes/SSD Track/JGA/experiments/H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01/`, directories `run_1/production/` and `run_2/production/`.

This was **numerical periodicity-map computation plus streaming validation and fresh-process replay**, not separation, model training or Vogl inference. Each run wrote **15,157,480,854 canonical bytes** (about 15.16 GB), with allocated bytes 15,354,429,440 before metrics. Recorded runtimes: 10,300.182915416 and 10,810.705498833 seconds. Each run: 63 centers, 1,056 periods, 3,864 center-specific scales, 4,080,384 queries, 133,195,392 ordered accumulations; 126,506,686 validator checks, zero failures. Replay preserved 1,003 byte-identical bulk files, including 997 shards.

Reusable evidence: the complete bounded observed response map, exact numerical/query authority, catalogues, validation/replay, and later exact-witness evidence. It does not establish metric preference, recurrence sufficiency, physical onsets or BPM. Both runs remain external; this checkpoint verifies lightweight acceptance checksums and directory presence, not a new full 30+ GB read or recomputation. Global exact-witness V2 results and negative history are also preserved; global-null research remains DEFERRED_PARALLEL.

## Double-Bass and next stop

Double-Bass research remains active independently: provisional ontology, Identity Card not frozen; DB-MTO completed design, blocked/unexecuted. Capture draft0.5 has DPA adapter resolved; authoritative document still leaves second-airborne availability/mounting and capture-day checks unresolved. No delivery/readiness is inferred from later conversational microphone references. No recording, capture or Bass experiment is executed by this checkpoint.

Next available local source: `/Volumes/SSD Track/JGA/downloads/Ray Brown Trio - Easy Does It.m4a` (file existence verified only). PI observation: HH audibly marks 2&4; contextual/domain hypothesis only, not event labels or a tempo input. **Do not execute now.** After separate PI authorization: full mix → approved separation → Drums → unchanged Vogl HH → recurrence/local persistence → frozen rule activation/abstention → internal result freeze → external comparison only afterward. No PI tempo estimate is recorded as input.

Current task is preservation/state/commit/push only. No new experiment, dataset search, tuning, source separation, BPM calculation or Double-Bass work is authorized. The next session must wait for separate Ray Brown execution authorization.

## Report inventory

Each report below is preserved unchanged; its SHA-256 and all associated lightweight scientific files are bound in the checkpoint manifest. Bulk data/models/environments remain external.

- [ADTOF_QUALIFICATION_20260910](../../validation/RIDE-HIHAT/ADTOF_QUALIFICATION_20260910/REPORT.md) — `dce6eedc23b75a90d60dcf218704436665f29aac5b30fb5cdbaa581e8e08632a`
- [CEDVAL005_CROSS_SOURCE_20260910](../../validation/RIDE-HIHAT/CEDVAL005_CROSS_SOURCE_20260910/REPORT.md) — `6a66d7598c5836859d6a8d6e284a1c2837f804a5e44d7a3ebceafe3adc433f9c`
- [CEDVAL005_INTERNAL_PULSE_20260910](../../validation/RIDE-HIHAT/CEDVAL005_INTERNAL_PULSE_20260910/REPORT.md) — `225d014ca2fe2f7dadd9617a87fde48d3f379a7d3825c0e87bc36999c45e9910`
- [CEDVAL005_RIDE_RECURRENCE_20260910](../../validation/RIDE-HIHAT/CEDVAL005_RIDE_RECURRENCE_20260910/REPORT.md) — `9bcc40b9a125892af643de3a86cff2ece6c449306fd80ba64f1b13fb9697baa2`
- [CEDVAL005_SYNC_20260910](../../validation/RIDE-HIHAT/CEDVAL005_SYNC_20260910/REPORT.md) — `dab98518bfc58211834adba08d110f399324d94886d0894e7d8d60c4e1d575bb`
- [CEDVAL009_RIDE_RECURRENCE_20260910](../../validation/RIDE-HIHAT/CEDVAL009_RIDE_RECURRENCE_20260910/REPORT.md) — `b80e59397965e74831679499ecfe68bb11f91fe256eb7f2d0636d4161005015b`
- [CHET_FULL_PIPELINE_20260910](../../validation/RIDE-HIHAT/CHET_FULL_PIPELINE_20260910/REPORT.md) — `1f169d75453deadf94881a865dbc34e33491307c647cb9f716124e1d6f94fa3e`
- [CHET_HIHAT_24_BLIND_20260910](../../validation/RIDE-HIHAT/CHET_HIHAT_24_BLIND_20260910/REPORT.md) — `a0ed99113a07741215cae180877c2ad7f2d73f95974bde96a20e44982647d344`
- [ENST_MDB_PROBE_02_20260910](../../validation/RIDE-HIHAT/ENST_MDB_PROBE_02_20260910/REPORT.md) — `17631ce43a866d741af63cd808b83e2226db45d7cdcd254ad55b51777e1d3387`
- [GMD_MDB_PROBE_20260910](../../validation/RIDE-HIHAT/GMD_MDB_PROBE_20260910/REPORT.md) — `a748d39b63a9807e7c5a4408ac4bef6cadacd27e1689c38cf8afe14b9db20ec0`
- [HIHAT_JAZZ_COMPARISON_20260910](../../validation/RIDE-HIHAT/HIHAT_JAZZ_COMPARISON_20260910/REPORT.md) — `1b7c5d12d081af728aabdb362501e7f11c2e57720aca0cc43b48051c6bf0dbc4`
- [HIHAT_LOCAL_PERSISTENCE_20260910](../../validation/RIDE-HIHAT/HIHAT_LOCAL_PERSISTENCE_20260910/REPORT.md) — `e3fb48286033accf07657d793791c7a6c895df3f130ae1db2998118afcf66ea0`
- [VOGL_2018_QUALIFICATION_20260910](../../validation/RIDE-HIHAT/VOGL_2018_QUALIFICATION_20260910/REPORT.md) — `cd43262c0149ec732eb3613e0bf2486e5e246630df8dd5abd49dc6500c140a07`
- [VOGL_JGA_QUALIFICATION_20260910](../../validation/RIDE-HIHAT/VOGL_JGA_QUALIFICATION_20260910/REPORT.md) — `8f6e00f7f4330de6028ed4d26daf26163c9d07b76836f1f647b744c0e5f3e5c1`
