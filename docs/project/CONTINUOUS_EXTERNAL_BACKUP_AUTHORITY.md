# Continuous external backup — permanent PI authority

Effective 2026-09-25. This operational directive supplements Git and immutable
milestone backups; it changes no scientific result or freeze.

Approved external root: `/Volumes/HD BackUp/JGA_BACKUP`.
Current mirror: `/Volumes/HD BackUp/JGA_BACKUP/JazzGrooveAnalyzer_CURRENT/`.
Preserve repository-relative paths. Never delete orphaned mirror files and never
use destructive synchronization or `--delete`. Previous versioned backups are
untouched; major milestones still require separate immutable recovery copies.

## Required synchronous workflow

Before any workflow that may write repository files, run
`python3 tools/continuous_backup.py check`. It requires the external volume to be
mounted, distinct from the working disk, and writable with a flushed write test.
If unavailable, report **CONTINUOUS EXTERNAL BACKUP UNAVAILABLE** and ask the PI
whether to stop or explicitly proceed locally with backup debt. Never decide
this autonomously. Sandbox permission errors require authorized execution, not
silently skipping backup.

After EVERY scientifically or operationally relevant completed artifact:

1. Write the local artifact atomically (temporary sibling, flush/fsync, rename).
2. Immediately run `python3 tools/continuous_backup.py files RELATIVE_PATH`.
3. Require successful local SHA-256, external copy and independently read external
   SHA-256 equality before dependent work continues.

Python producers can call `atomic_write_and_backup(relative_path, bytes)` from
`tools/continuous_backup.py`. Existing producers must finish/close their output
and call the `files` command before dependent work. Multi-file operations must
back up each completed file incrementally; do not defer until session end.
This is a synchronous completion gate, NOT an automatic filesystem watcher:
watchers cannot establish that arbitrary scientific output is complete.
Future Codex workflows are required to invoke this gate.

After a batch run `python3 tools/continuous_backup.py all` for an independent
source/mirror inventory and hash comparison. Before a commit run
`python3 tools/continuous_backup.py staged`; staged bytes must match both the
working file and its verified backup. No commit is authorized by this directive.
Serialize repository-writing/backup operations, especially Git operations.
Safely completed Git metadata is included; in-progress Git lock files are not.

## Coverage and exclusions

Include source/scripts, studies/RFCs, tables, figures/PDFs, reports, model files,
manifests/checksums, configurations, documentation/root bootstrap, repository
scientific audio/data, untracked scientific artifacts, and quiescent Git metadata.
Do not interpret Git ignore rules as permission to omit scientific data.
The helper excludes only named disposable Python environments/caches,
`__pycache__`, pytest/mypy/ruff/notebook caches, `.pyc`/`.pyo`, `.DS_Store`,
AppleDouble `._*`, `.lock` and `.tmp` files. Scientific `output` and data folders
are included. Other disposable build/render paths require explicit inspection,
not a broad exclusion of scientific directories.

Symlinks are preserved and hashed as UTF-8 link text, explicitly logged as
`symlink`; they do not claim to bundle their referents. Externally stored source
data remains covered by the existing milestone backup policy; newly modified
repository audio/data is covered here. The current mirror is not a substitute
for the complete recoverable milestone package.

## Verification, logging and failure

Copies use a temporary sibling on the external disk, flush/fsync and verify
before atomic replacement; then independently hash the installed external file.
Changed source size/mtime/inode causes failure. Never copy an active producer's
partial output. Prior mirror payload remains intact if temporary-copy checking
fails. A hash mismatch reports **BACKUP VERIFICATION FAILURE**; stop dependent
work and notify PI. Other I/O errors also stop the workflow.

`JazzGrooveAnalyzer_CURRENT/BACKUP_LOG.jsonl` is append-only. Every successful
CREATE/UPDATE records UTC/local timestamps, relative path, both hashes, byte size,
PASS status and Git HEAD. Log appends are locked and flushed. Unchanged verified
files need no new copy record. The mirror log and copy temporaries are operational
metadata, not source payload and not recursively mirrored.

## Installation validation

The helper was checked for CREATE, UPDATE, append-only log preservation,
unchanged-file verification, orphan preservation, path traversal rejection and
simulated hash mismatch rejection before installation. Initial population must
finish full inventory/hash verification before installation is reported complete.
