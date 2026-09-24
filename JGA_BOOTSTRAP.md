# Jazz Groove Analyzer — single current bootstrap

This ROOT file is the sole current session recovery entry point.
Canonical repository scientific/project records remain the source of truth.
If this bootstrap conflicts with them, canonical records prevail: report the
conflict and stop dependent work. Historical bootstrap snapshots are provenance
records, not competing current authorities.

Generated from [canonical recovery sources](docs/project/BOOTSTRAP_SOURCES.json).
Do not edit or prepend state here. Update canonical sources, then run
`python tools/bootstrap.py --recovery-only` when generation is authorized.
Startup requires reading this file, not running generators or experiments.
The next scientific action requires separate PI authorization; recovery grants none.
Consult Git for current branch/commit; no commit identity is embedded here.


# Current authoritative checkpoint — best validated Bass baseline · 2026-09-25

**BEST VALIDATED BASS BASELINE — CURRENT BEST VALIDATED BASS ATTACK BASELINE.** PI-selected [baseline authority](docs/scientific/rfc/JGA_BASS_BEST_VALIDATED_BASELINE_20260924.md). Audio → Spotify Basic Pitch → native note identity and approximate onset → fixed ±150 ms local window → acoustic candidates → frozen JGA Learned Local Attack Selector → selected attack / abstain.

**Controlled Gallegati/Fishman holdout: 35/40 = 87.5%; median absolute error 5.213 ms; P95 absolute error 5.621 ms; 100% of selected within ±10 ms.** This validates recognized-note-conditioned local selection, not autonomous Bass identity or cross-domain generalization. [Contained fallback](docs/scientific/rfc/JGA_CONTAINED_BP_FALLBACK_20260924/RESULT.md) is secondary validation: independent windows only; distinct attacks trigger abstention. Do not pool its statistics with the primary35/40baseline.

**Definitive baseline freeze SHA-256:** `31d865a6d8b48f41cab7e147b01c336bde0bc2c4ceb211a101399994bf9772d4`. [Final manifest](docs/scientific/rfc/JGA_BASS_BEST_VALIDATED_BASELINE_20260924/MANIFEST.json) · [verified digest receipt](docs/scientific/rfc/JGA_BASS_BEST_VALIDATED_BASELINE_20260924/FINAL_FREEZE.json). The older fd768ec83bc77a5e32938bed743edef10d1355d0c1a961c623be5ea4728b850d hash is an incomplete payload, NOT this milestone.

**Historical Bass microtiming NOT finalized.** [Direct Exactly Like You transfer](docs/scientific/rfc/JGA_BASS_V1_HISTORICAL_TRANSFER_20260924/JGA_BASS_V1_HISTORICAL_REPORT.md) recovered only17/63episodes with46abstentions; its walking structure is insufficiently recovered. Fishman→historical/Demucs domain shift remains important. [Targeted-pitch full-mix diagnostic](docs/scientific/rfc/JGA_TARGETED_PITCH_ONSET_20260924/RESULT.md) reached37/63CLEAR=58.73%, explicitly NOT GT validated. These are research evidence, not replacement authorities. Bass-v1 historical milestone is NOT complete; prior Report001 stays unchanged within its historical operational scope.

**Do not restart Bass development from scratch.** Preserve the frozen Learned Local Attack Selector as the mandatory comparison baseline. Future methods are extensions/improvements and must report baseline modification, controlled coverage, median/P95 absolute error,±10ms, abstention, cross-domain/historical coverage and any timing-precision cost. Visual plausibility cannot supersede independent controlled validation. **Next scientific goal: improve cross-domain/historical coverage while preserving the frozen controlled baseline.** New scientific execution requires separate PI authorization.

RAW PLP remains temporal authority for quarter reference; PLP must not guide acoustic attack selection. Historical attack timestamps must be frozen before PLP evaluation. Full mix remains original audio authority; stems are complementary source/identity evidence. This closure changes documentary authority/preservation only; no scientific rerun, model update or timestamp correction.

## Recovery references

- [AGENTS.md](AGENTS.md)
- [docs/JGA_PROJECT_STATE.md](docs/JGA_PROJECT_STATE.md)
- [docs/JGA_ROADMAP.md](docs/JGA_ROADMAP.md)
- [docs/JGA_SCIENTIFIC_STATE.md](docs/JGA_SCIENTIFIC_STATE.md)
- [docs/JGA_ARCHITECTURE.md](docs/JGA_ARCHITECTURE.md)
- [docs/JGA_DECISIONS.md](docs/JGA_DECISIONS.md)
- [docs/project/PROJECT_METADATA.md](docs/project/PROJECT_METADATA.md)
- [docs/architecture/BOOTSTRAP_SINGLE_ROOT_DECISION_20260922.md](docs/architecture/BOOTSTRAP_SINGLE_ROOT_DECISION_20260922.md)
- [docs/scientific/rfc/JGA_TEMPO_AUTHORITY_PHASE_CLOSURE_20260922/AUTHORITY_REFERENCES.json](docs/scientific/rfc/JGA_TEMPO_AUTHORITY_PHASE_CLOSURE_20260922/AUTHORITY_REFERENCES.json)
- [docs/scientific/rfc/JGA_SINGLE_ROOT_BOOTSTRAP_MIGRATION_20260922/PRESERVATION_FREEZE.json](docs/scientific/rfc/JGA_SINGLE_ROOT_BOOTSTRAP_MIGRATION_20260922/PRESERVATION_FREEZE.json)
- [docs/scientific/rfc/JGA_V1_HYBRID_OPERATIONAL_ARCHITECTURE_20260923/README.md](docs/scientific/rfc/JGA_V1_HYBRID_OPERATIONAL_ARCHITECTURE_20260923/README.md)
- [docs/scientific/rfc/JGA_V1_HYBRID_OPERATIONAL_ARCHITECTURE_20260923/PI_OPERATIONAL_DECISION.md](docs/scientific/rfc/JGA_V1_HYBRID_OPERATIONAL_ARCHITECTURE_20260923/PI_OPERATIONAL_DECISION.md)
- [docs/scientific/rfc/JGA_V1_HYBRID_OPERATIONAL_ARCHITECTURE_20260923/AUTHORITY_REFERENCES.json](docs/scientific/rfc/JGA_V1_HYBRID_OPERATIONAL_ARCHITECTURE_20260923/AUTHORITY_REFERENCES.json)
