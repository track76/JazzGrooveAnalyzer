# Programmer review — read-only entry

This local review update is PREPARED, not a published release. Start with [scientific limits](SCIENTIFIC_STATUS.md), [architecture reading map](ARCHITECTURE.md) and [Core/Domain boundary](../architecture/CORE_DOMAIN_BOUNDARY.md). The boundary document is Draft; do not treat it as an implemented proof. Existing versioned architecture checkpoints retain their stated scopes.

Inspect src/jga/pipeline/default_analysis_pipeline.py, src/jga/runtime/analysis_context.py and the Core → Translation → Domain boundaries. Review import side effects, dependency direction, deterministic pure computations, temporal support, unknown/missing-event accounting and the distinction between acoustic evidence and semantic claims. Compare current code with the parent branch; no scientific result follows from a successful import.

Core dependency snapshot: [pyproject.toml](../../pyproject.toml) and [requirements.txt](../../requirements.txt). Installation/download commands are not executed by this review. A narrow import smoke test covers package/pipeline/domain imports; full tests and scientific pipeline runs are not claimed. Optional separation backends and data-dependent tests need their own input rights/environment.

The repository is public: a reviewer can view the approved published branch/commit or clone without collaborator rights. On a personal repository an invitation grants collaboration, including push permission; do not invite for read-only review. No credentials, shared token, local workstation access, private audio or browser profile is needed. Copyright remains All Rights Reserved; visibility is not a new license.

Current local review files must be published through the specific V2 publication authorization before they can be read at GitHub. Read-only preparation is not push authority. Do not reproduce internal recovery snapshots, ledgers, approval packets, protected/frozen data, audio/datasets or embargoed contents in a review bundle. Existing public history is not certified by a scoped new-file scan.
