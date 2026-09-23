# JGA v1 hybrid historical-recording analysis architecture — final operational adoption

**PI decision: ADOPTED / USABLE_WITH_QUALIFICATION. Methodological development CLOSED for bounded v1 operational historical analysis.** Next phase: HISTORICAL JAZZ CORPUS ANALYSIS / REPORT PRODUCTION.

- [Authoritative PI decision, architecture, provenance/timestamp rules and limits](PI_OPERATIONAL_DECISION.md).
- [Historical-report workflow](HISTORICAL_REPORT_WORKFLOW.md).
- [Canonical evidence paths, SHA-256 and storage status](AUTHORITY_REFERENCES.json).
- [Historical evidence preservation inventory](HISTORICAL_PRESERVATION.json).
- [Focused validation](VALIDATION.json).
- [Decision/result freeze](DECISION_FREEZE.json).

`EVIDENCE_SNAPSHOTS/` contains byte-preserved compact provenance records, not independently maintained authorities. Several original study trees remain untracked local scientific holdings; their complete data/audio/figures are not newly committed or backed up by this decision. Snapshot manifests preserve original relative-path semantics and hashes; resolve their members at the original canonical package path given in the authority inventory, not relative to the flattened snapshot filename. Historical README/report links retain original location semantics. This package makes the decision and its basis recoverable across clones, but does not claim to supply every raw experimental artifact in a fresh clone.

No frozen scientific result, original PI response, source audio, runtime algorithm or historical analysis is changed. The independent PLP FAIL remains separate from operational adoption. No analysis or methodological experiment is run. Root `JGA_BOOTSTRAP.md` is generated from the updated canonical project checkpoint; the artifacts bootstrap stays a non-authoritative redirect.
