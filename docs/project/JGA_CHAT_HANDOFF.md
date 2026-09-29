# Handoff — JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-001-20260929

**Status: COMPLETE, awaiting PI review. No commit, no push, no scientific promotion.**

## What was done
Preregistration 0.2 executed exactly as frozen. Identical extractor code was run on the
full mix and the isolated bass stem over the identical interval, followed by temporal
connected-component matching at T0/T1/T2/T4. No pitch-based decision was applied to matching.

## Headline numbers (T1, preregistered primary)
- events: full mix 458 (13.150/s), bass stem 442 (12.690/s)
- T1: 572 components, 328 edges, 71.6% full-mix coverage, 74.2% stem coverage, 0 crossings
- T1 pitch (ALL_F0_BOTH_VALID, n=255): median 0 cents, p75 10, p95 60, max 330;
  139/255 (54.5%) exactly zero cents
- VALIDITY_QUALIFIED low-register pairs at T1: 17 (reporting descriptor only)

## What this evidence is NOT
Not verified notes, not Ground Truth, not independent confirmation, not accuracy,
not STEM_BETTER or FULLMIX_BETTER. No independent replication was performed.

## What the PI needs to decide
1. Accept or reject the six recorded deviations (DEV-1..DEV-6). DEV-3 was a real code defect
   in an export/verification path, caught by cross-check and corrected.
2. Decide whether the descriptive separator numbers warrant any use at all. They are
   deliberately quarantined in SEPARATOR_PROVENANCE.json.
3. Authorize or decline a commit. Nothing has been committed.

## Artifacts
- package: `docs/scientific/rfc/JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-001-20260929/`
- external: `/Volumes/SSD Track/JGA/experiments/JGA_BASS_FULLMIX_VS_STEM_NOTE_EVIDENCE_001_20260929`
- backup:  `/Volumes/HD BackUp/JGA_BACKUP/SSD_TRACK_JGA/JGA/experiments/JGA_BASS_FULLMIX_VS_STEM_NOTE_EVIDENCE_001_20260929`
- manifest: `docs/project/EXTERNAL_ARTIFACT_MANIFEST.json`
