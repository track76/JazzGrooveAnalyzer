# JGA current-state bootstrap — 2026-09-10 consolidated checkpoint

This is a derived, lightweight repository snapshot, explicitly preserved in Git for session reload. Canonical authority: [current checkpoint](../docs/scientific/JGA_TIMING_CHECKPOINT_20260910.md), [project state](../docs/JGA_PROJECT_STATE.md), [official roadmap](../docs/JGA_ROADMAP.md), [frozen domain rule](../docs/scientific/JGA_HIHAT_2_4_TIMING_RULE_20260910.md), [hash inventory](../docs/project/TIMING_CHECKPOINT_20260910.json). Historical experiment reports remain historical; no stale former frontier is copied here. For exact commit/remote identity use git rev-parse HEAD and upstream; no self-referential commit hash is embedded.

## Purpose, architecture and authority

JGA studies quantitative timing relationships in jazz ensembles and historical performance practice. It is not a universal beat detector. Core observed facts → Translation evidence → Domain musical interpretation. Preserve source UUID, asset hashes, event lineage, native timestamps, uncertainty and observed-versus-inferred status. File labels/model source keys do not establish event GT. Distinct witnesses are not statistically independent. See AGENTS.md, Development Constitution, Scientific Research Constitution/Knowledge Model, AD-015/037/038/040/041 and the source documents for governing boundaries. Do not execute a stale historical authorization.

## Mandatory full-recording workflow

Full audio → approved source separation → relevant native stem → instrument/event recognition → timing analysis → domain interpretation → BPM/behaviour. Recognizer directly on commercial/full mix is an explicitly authorized CONTROL only. Future Double-Bass full-mix analysis follows this rule too.

Approved separator: JGA AuthorizedDemucsRunner / DemucsSeparator.separate_authorized, pinned htdemucs_6s, Demucs4.1.0, offline checked model/environment, six native float32 outputs, AD-041 parent/derived identities. Bind each new source; do not silently reuse another recording's parent UUID. Bulk data and environments stay under `/Volumes/SSD Track/JGA`. Only lightweight records belong in Git.

## Accepted and negative recognition evidence

GMD controlled Ride-vs-HH discrimination worked (94.45% precision,98.25% recall,99.61% AP), but GMD→original MDB transfer failed (11.76% precision,8.22% recall). ENST passed a modest controlled diagnostic gate, but useful selective admission and independent MDB transfer failed. These were small custom probes; do not retrain or reinterpret failures automatically. MDB independence is model-relative; project-level exposure is known.

Vogl2018 official custom madmom0.16.dev0 CRNN_8 is an EXTERNALLY PRETRAINED recognizer, not JGA-trained. RD separate from HH and CY/Crash; broad bell output is not pure Ride-bell identity. HH does not distinguish closed/open/pedal. MDB Ride precision96.31%, recall40.60%, F1 57.12% is NOT independent transfer: supplied ensemble includes MDB-trained networks. Preserve license/noncommercial restrictions recorded in qualification. External Vogl root: `/Volumes/SSD Track/JGA/experiments/RIDE-HIHAT-VOGL-2018/`.

## Jazz timing evidence and current interpretation

CED-VAL-009 Jesper Buhl Trio: first60s overhead,113 Ride candidates,962 recurrent exact relations,2,304 supporting pairs; multiple candidates/no BeatReference. HH from same preserved inference:10 candidates,no repeated exact relation.

CED-VAL-005 fixed28–88s: overhead Ride29 candidates,29.49s prediction gap,22 recurrent relations/46 pairs. HH spot141 candidates,1,649 relations/5,444 pairs; exact0.500s locally supported in6/6 primary and5/5 shifted regions. Source identity remains candidate evidence, no inferred missing strokes. PI observations of ostinato/walking changes, light Ride and HH2&4 function are contextual, not input event timing.

Cross-source005:4,089 labelled pairs,530 recurring signed relations,17 common within-source separations; no unique common reference. Practical original-channel synchronization supported: same Broadcast WAV origin/rate/frame count, observed correlation lag range approximately -4.97 to +3.54ms in eight windows; terminal window ambiguous. No shift applied; physical sample-exact timing not claimed. Synchronization is no longer primary limitation; sparse Ride recognition and unresolved temporal structure remain limiting.

Frozen internal005 decision stays0.500s→120BPM, half/double metric ambiguity unresolved. External approximate246BPM supplied afterward motivated the new PI domain rule; never rewrite that historical result.

## Frozen prospective domain rule

JAZZ_HIHAT_2_4_TIMING_RULE: sufficiently identified, recurrent, locally persistent, covered and reproducible jazz Hi-Hat TIMEKEEPING may be interpreted as2&4 reference anchors. Mere detection is insufficient; isolated fills/accents, irregular/absent/uncertain support requires HIHAT_2_4_REFERENCE_UNAVAILABLE. Missing predictions alone are not proof of no playing, and never authorize invented anchors. First-anchor2-vs4 phase/bar origin is not established automatically.

T_BEAT=T_HH/2; BPM_INTERNAL=120/T_HH only after qualification. Preserve OBSERVED_HIHAT_EVENT, HIHAT_TIMEKEEPING_EVENT, HIHAT_2_4_REFERENCE_ANCHOR and INFERRED_INTERMEDIATE_BEAT separately. The latter is not acoustically observed. No Bass quantization. Visual emphasis may distinguish support/non-support without deleting or calling unsupported events errors.

005 retrospective interpretation under new rule:0.500s→0.250s→240BPM versus approximate246. This is motivation, NOT prospective validation. Generic BeatReference is FALLBACK; Ride remains separate articulation/swing/subdivision/microtiming/historical evidence. No universal historical-jazz claim.

## Chet prospective attempt: recognition failure upstream

Source III_Chet Baker - I fall in love too easily.mp3. Direct-full-mix Vogl control:0HH. Complete approved JGA path full mix→htdemucs_6s/Demucs4.1.0→Drums→unchanged Vogl→qualification:0HH,gate FAIL,noT_HH,noT_BEAT,noBPM. Thus the 2&4 mathematical rule was NOT tested; recognition failed upstream. Likely brush-condition recognition-domain limitation, not proof of absent physical HH or a proven causal explanation. No external Chet tempo used/checked.

Canonical external package `/Volumes/SSD Track/JGA/experiments/CHET-HTDEMUCS6S-HIHAT24-20260910/`, stem `stems/drums.wav`, result `inference/result.json`. Control `/Volumes/SSD Track/JGA/experiments/CHET-HIHAT-24-BLIND-20260910/`. Demucs native decode differed by2,257 samples from prior decode; no trim/shift, exact cross-decoder onset mapping unclaimed. Both remain preserved.

## Earlier ~15GB work: established identity

Complete VAL-001 real-Drum local complex periodicity map, numerical response computation plus streaming validation and independent replay, NOT training/separation. External `/Volumes/SSD Track/JGA/experiments/H-VAL001-COMPLETE-REAL-DRUM-PERIODICITY-01/run_1/production/` and `run_2/production/`. Each wrote15,157,480,854 canonical bytes; two runs roughly30.3GB total. Runtimes10,300.182915416 and10,810.705498833 seconds. Each63centers,1,056periods,3,864scales,4,080,384queries,133,195,392accumulations;126,506,686validator checks,zero failures. Replay1,003byte-identical files including997shards. Lightweight acceptance at `validation/VAL-001/complete_real_drum_periodicity_20260908/README.md`.

Reusable complete bounded map, catalogue/numerical authority and validation/replay, later exact-witness supporting evidence. No metric selection/BPM/physical onset/sufficiency claim. Global exact-witness V1/V2 history preserved; global-null track DEFERRED_PARALLEL with authority gaps. Do not recompute this job for inspection.

## Double-Bass and next authorized boundary

Double-Bass remains active independently: provisional ontology, Identity Card not frozen; DB-MTO design complete but blocked/unexecuted; capture draft0.5,DPA adapter resolved, second-airborne physical availability/mounting and capture-day verification unresolved in authoritative document. No claim of later delivery/readiness without updated authority. Future independently established HH anchors may reference original Bass timestamps/offsets without snapping. No Bass experiment or capture authorized by this checkpoint.

Next available file (existence only verified): `/Volumes/SSD Track/JGA/downloads/Ray Brown Trio - Easy Does It.m4a`. PI hears HH2&4; no PI tempo estimate is stored as input. **NEXT MINIMAL STEP, only after separate PI authorization:** full mix→approved separation→Drums→unchanged VoglHH→recurrence/local persistence→frozen2&4gate→internalBPM or abstention→freeze→external comparison afterward. DO NOT EXECUTE NOW.

No new scientific work is authorized by this consolidation. No automatic model search, classifier tuning, new dataset search, external tempo lookup or fallback experiment. On reload read current source records and wait for PI.

## Integrity and worktree

Current checkpoint source SHA-256: d862c1bb8abd7a17b9c5c6926a1bd1a4e0bdd6d7be7e9d91e54ae5d36e3a0fd7. Exact report hashes and preservation scope: `docs/project/TIMING_CHECKPOINT_20260910.json`. Minimal checks verified reports/citations, unchanged historical records and complete-map lightweight checksums; no new experiment or full code suite. Unrelated plot edits/deletions, score edit, AGENTS.md and VAL-001 visualizations remain deliberately outside this checkpoint. A dirty residual tree is expected and must not be cleaned automatically. Commit/push status is operationally verified after the checkpoint; consult Git rather than stale embedded hashes.
