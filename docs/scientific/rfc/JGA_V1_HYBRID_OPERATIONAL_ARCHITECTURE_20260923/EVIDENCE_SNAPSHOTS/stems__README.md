# Full mix versus separated stems — bounded diagnostic package

Read [RESULT.md](RESULT.md) for the complete comparison and qualified decisions. No canonical adoption is performed.

- Prospective rules: [PROSPECTIVE_RULES.json](PROSPECTIVE_RULES.json), [PROSPECTIVE_FREEZE.json](PROSPECTIVE_FREEZE.json).
- Actual-input preregistration: [PREREGISTRATION.json](PREREGISTRATION.json), [PREREGISTRATION_FREEZE.json](PREREGISTRATION_FREEZE.json).
- Signal lineage: [SOURCE_AUTHORITY.json](SOURCE_AUTHORITY.json), [SEPARATION_RESULT.json](SEPARATION_RESULT.json), [DECODE_EQUIVALENCE.json](DECODE_EQUIVALENCE.json).
- Frozen controls: [CONTROL_LINEAGE.json](CONTROL_LINEAGE.json) and `CONTROL_SNAPSHOTS/`.
- Native stem populations: `BASS_EVENTS.csv`, `DRUMS_EVENTS.csv`; [STEM_EVENT_FREEZE.json](STEM_EVENT_FREEZE.json).
- Selection: `STEM_ASSIGNMENTS.csv`, `STEM_EVENT_ROLES.csv`, `STEM_PAIRS.csv`.
- Matching: `MATCHING_EDGES.csv`, `EVENT_MATCHING.csv`, `UNIQUE_MATCHES.csv`.
- Dual: [DUAL_AUDIT.csv](DUAL_AUDIT.csv).
- Results: [SUMMARY.json](SUMMARY.json), [STATISTICS.csv](STATISTICS.csv), [SECTION_COMPARISON.csv](SECTION_COMPARISON.csv).
- Validation: [FINAL_VALIDATION.json](FINAL_VALIDATION.json), [FIGURE_VALIDATION.json](FIGURE_VALIDATION.json).
- Execution qualification: [METADATA_RECOVERY.md](METADATA_RECOVERY.md).
- Final package integrity: [RESULT_FREEZE.json](RESULT_FREEZE.json).

Scripts are preserved as provenance, not instructions to rerun the study. `prepare.py`, `separate.py`, `detect.py` generate scientific artifacts and must not be executed during recovery. `recover_metadata.py` documents the one metadata-only recovery. `compare.py` derives the comparison; `figures.py` renders the frozen tables. `validate_final.py` independently checks parent hashes, geometry and matching and creates a validation receipt.

External audio is retained at the exact paths recorded in `SEPARATION_RESULT.json`, with all six stem hashes. No large audio is duplicated into this package. New files are additive; previous results, runtime and canonical state remain unchanged. No commit or push.
