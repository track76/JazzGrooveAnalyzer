# Pilot002 immutable experimental evidence

Freeze ID: JGA-PILOT-002-CANDIDATE-FREEZE-001-20260928. PI decision: PI-PILOT-002-CANDIDATE-FREEZE-20260928.

The 31-file Pilot002 package is unchanged. FREEZE_RECORD.json binds every file, candidate/cluster inventory, input audio identity, configuration, executed producer and external array by SHA-256. This companion directory is outside the original package so its completed manifest remains valid.

- BASS_COMPATIBLE is not validated Bass identity
- CYMBAL_COMPATIBLE is not validated Cymbal identity
- Frame-derived landmarks are not validated physical attacks
- Candidate density is not note/hit density
- pYIN low-register frame limitation remains
- Adjacent-gap dedup chaining can merge distinct attacks; all members retained
- Source confusers remain unresolved
- No quarter assignments, internal pulse or groove evidence is established

Both future methods must use these exact source hashes. No re-extraction, source addition/deletion, timing/classification/dedup change or agreement-driven selection. A derived subset/weighting needs its own preregistration and preserves source IDs. Global is comparison/index only; Human evaluation only. Initial P/D construction is independent. No downstream task is authorized.

Run `python3 docs/scientific/rfc/JGA_PILOT_002_CANDIDATE_FREEZE_001_20260928/verify_frozen.py` before consuming evidence. Optional `--method-p manifest.json --method-d manifest.json` requires both manifests to identify this freeze_id and identical `source_sha256` dictionaries equal to all candidate_and_cluster_hashes in FREEZE_RECORD.json, plus `external_evidence_sha256` equal to its external array hash. These manifests identify source inputs, not permission for derived transforms.

Hash gating is cooperative, not an OS write lock or proof of scientific identity. Publication HEAD is resolved via Git and the commit-addressed recovery EXPORT_MANIFEST/PUBLICATION_RECEIPT, avoiding a second self-referential commit. Versioned preservation: /Volumes/HD BackUp/JGA_BACKUP/CANDIDATE_FREEZES/JGA-PILOT-002-CANDIDATE-FREEZE-001-20260928. Recovery: /Volumes/SSD Track/JGA/experiments/JGA_FULLMIX_BASS_CYMBAL_EVENT_PILOT_002_20260928/recovery/<publication_HEAD>/PUBLICATION_RECEIPT.json. Prior producer/report no-publication statements describe the completed execution phase; this later PI decision authorizes evidence publication only.
