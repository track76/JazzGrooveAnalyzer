# Existing governed publication lifecycle — implementation review

PI explicitly authorized minimum tooling support; no new governance subsystem.

`tools/jga_governance.py` now supports publication-stage / publication-verify / publication-commit / publication-push. The lease stores the exact reviewed manifest, initial HEAD/index/worktree, tree identity and transition receipt. Stage checks PI task/agent/paths and reviewed hashes, then advances only the verified index baseline. Commit verifies parent, branch, exact path set/tree/blobs and unchanged worktree before advancing HEAD/index. Push checks the exact remote branch SHA. Wrong/concurrent state fails closed; no generic resync or lease reacquisition.

Append-only historical corrections bind semantic JSON hashes of original immutable ledger records and verify the same task and existing PI decision. Unresolved authorization is explicitly NOT historically authorized. Missing-reference exceptions apply only to the hash-bound historical event, never a current recovery/embargo/current-task reference. Conflicting corrections fail.

Historical external registration requires exact sequential IDs, sorted unique artifact names, valid metadata and opaque SSD size/SHA256 verification. No payload interpretation or old-HD access. Existing review-required status remains unchanged.

Compatibility: original acquire/write/resync behavior remains strict; repository-only tasks remain supported. Global checker returns PASS with explicit historical qualifications only for PI-accepted dispositions. No lowercase-field normalization. Backup-debt publication exception remains separately PI-linked and never means BACKUP_VERIFIED.

Limitations: cooperative single-writer enforcement, not an OS security boundary; after an unexpected hook mutation the lease remains stale for PI inspection. Pattern secret scanning cannot prove absence of every sensitive value. Historical UNKNOWN references and unresolved authorization remain visible. No scientific claim is repaired.
