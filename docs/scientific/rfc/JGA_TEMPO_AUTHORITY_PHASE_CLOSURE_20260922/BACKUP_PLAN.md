# Established backup plan for this closure

Authority: `/Volumes/HD BackUp/JGA_BACKUP/JGA_BACKUP_POLICY.md` (existing PI-authorized 2026-09-12 policy). Verified available HD BackUp; use existing INTERNAL_MAC/JazzGrooveAnalyzer and SSD_TRACK_JGA/JGA mappings.

After commit/push, synchronize repository working files and .git, including all scientific packages, to the internal mapping. Exclude disposable virtual environments, Python/test caches and OS metadata. Never propagate source deletions. Preserve backup-only files. Copy new or modified files only; verify SHA-256 for every in-scope source/destination. The established policy updates modified copies and does not use versioned snapshots; do not invent a new versioning destination. Frozen scientific mismatches stop; legitimate current-document updates follow the existing policy.

For SSD data, synchronize the eight frozen corpus source files and canonical Exactly Like You source (not the unrelated downloads collection), original top-level PI JSON exports and both preserved Ableton project trees to their existing mapped destinations; preserve external large assets already backed up without relocating them. No raw source changes. Export-content blinding is preserved: backup copies bytes without interpreting JSON mappings or uncompleted responses.

Record exact scope, exclusions, timestamp, commit and per-file hashes in a uniquely named backup receipt under the established JGA_BACKUP root. Verify current documentation against both Git HEAD and backup. Operational receipt is post-commit and outside the pre-commit closure hash to avoid a hash cycle.
