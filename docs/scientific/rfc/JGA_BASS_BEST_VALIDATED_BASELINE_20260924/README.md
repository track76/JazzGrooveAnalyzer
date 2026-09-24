# Best validated Bass baseline — definitive closure package

Current PI authority: ../JGA_BASS_BEST_VALIDATED_BASELINE_20260924.md.

Verification order: verify every MANIFEST.json entry using its declared root, then SHA256SUMS.txt, then compare SHA256(MANIFEST.json) with FINAL_FREEZE.json. The latter is the definitive baseline freeze hash. Recovery files and the former partial payload digest are not final authority. All controlled35/40results remain unchanged; historical Bass timing is not finalized.

Audio/raw arrays are referenced rather than unnecessarily duplicated or pushed as large Git blobs. The independently verified versioned external backup contains both the complete working repository and SSD_TRACK_JGA data root, including untracked scientific artifacts. Python virtual environments/caches can be rebuilt from preserved configuration/environment metadata; they are not scientific audio.

Do not execute historical experiment scripts as part of recovery. No training/inference/recalculation is needed to verify these hashes. build_package.py records the interrupted preparation and must not be rerun; complete_manifest.py records this successful resume sequence and is not idempotent by design. backup_versioned.py creates a fresh non-destructive complete backup after verified commit/push.
