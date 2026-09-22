# Single-root bootstrap migration — 2026-09-22

PI authorized infrastructure/recovery migration only. Root JGA_BOOTSTRAP.md is the sole current recovery entry, derived from canonical documents selected by docs/project/BOOTSTRAP_SOURCES.json. Canonical science/project records prevail on conflict. Scientific outcomes and runtime are unchanged.

## Preservation and historical reference resolution

PRESERVATION_FREEZE.json maps both original paths and exact pre-migration hashes to immutable PRE_MIGRATION snapshots. These byte streams preserve every unique section, including old instructions as history only. Their original relative links are preserved literally to preserve hashes: interpret links against the original repository path, not their archive location. Historical manifests are NOT rewritten; references with the matching original path/hash resolve here. Older hashes require the recorded historical Git revision or corresponding preservation package. The preceding Tempo Authority closure's documentation hashes remain historical, not a requirement that mutable recovery documents never evolve.

Artifacts-only history crosswalk: first complete musicological analysis → JGA_FIRST_COMPLETE_MUSICOLOGICAL_PERFORMANCE_ANALYSIS_001_20260922; expanded coverage → JGA_QUARTER_NEAREST_ONSET_COVERAGE_SENSITIVITY_001_20260922; Bass/Drum pilot/recovery → JGA_BASS_DRUM_MICROTIMING_001_EXACTLY_LIKE_YOU_20260920 and observable-groove closure; tempo-attribution correction → JGA_ADAPTIVE_MEASURE_GRID_001_EXACTLY_LIKE_YOU_20260920/PI_BPM_CORRECTION_20260920.md; recognition/Chet/periodicity history → docs/scientific/JGA_TIMING_CHECKPOINT_20260910.md. Exact historical wording is retained in the complete snapshots even where canonical sources summarize differently.

## Contract and compatibility

AGENTS was untracked before migration and is deliberately included in the migration commit. Only its bootstrap startup path/role wording changes. The old artifacts bootstrap is a minimal NON-AUTHORITATIVE redirect because many historical links resolve there. It contains no scientific/project state and the generator never writes it. Historical frozen sync scripts retain old paths; they are not current maintenance tools and must not be executed against current documentation. Their historical checks require historical inputs, not the redirect.

Run python tools/bootstrap.py --recovery-only for authorized root-only regeneration. No tests, scientific algorithms, documentation updaters or archive exporters are invoked by this mode. The legacy full toolchain is not a startup instruction and retains documented side effects. Docs-only context ZIP and committed-HEAD repository ZIP semantics are unchanged. Report tooling names root as the recovery entry and excludes the redirect from generated-artifact reporting.

## Validation

Eight focused tests cover root generation, determinism, required checkpoint fields, current links, AGENTS/redirect role, preservation hashes, fail-before-overwrite on broken links, and recovery-only isolation. Thirteen existing tooling/catalog tests also pass. All 3,523 pre-existing RFC files were hashed before migration and verified unchanged after it. No PLP/Ableton execution, scientific reclassification, runtime change, source-identity experiment, attack refinement or groove recalculation.

Only migration-related files enter the commit. Unrelated dirty-worktree files remain untouched and unstaged. Commit/push identities are reported operationally after the migration freeze, avoiding self-referential hashes.
