# Historical unreachable Git object archive

The user authorized exact external preservation followed by removal of only
the unreachable retention required to satisfy the no-Git-blob >=100 MiB rule.
This archival action establishes no scientific authority beyond preservation
of historical bytes. It does not reopen the experiments named by historical paths.

[manifest.json](manifest.json) records the three historical blobs, exact byte
sizes, SHA-256 hashes, external relative locations, recoverable path associations,
original Git identities, and the ref/reflog evidence before removal.
[post_prune_verification.json](post_prune_verification.json) records the exact
Git commands and object inventory comparison after removal.

External archive root:
`$JGA_EXTERNAL_ROOT/experiments/GIT-UNREACHABLE-LARGE-BLOB-ARCHIVE-20260907/`

The configured root at execution was `/Volumes/SSD Track/JGA`.
Neutral blob filenames are `<Git object SHA>.blob`. Twelve small commit/tree
objects were also archived under `object-context/`, preserving the exact
historical metadata that referenced these blobs. Original inventory and reflog
records are preserved externally in `inventory_before.json` and `prune_plan.json`.

The six selected reflog entries were removed without rewriting neighboring
entries or updating refs. All Git objects were loose, so a bounded `git prune`
was sufficient; no history filtering, rebasing, broad reflog expiration, or
repository repacking was used. The dry run selected exactly the 15 archived
objects. Explicit prune traversal roots preserved 115 unrelated unreachable
objects. The complete before/after object inventory proved every other object
remained present, including all reachable history.

The prior acceptance preservation-stop record is retained unchanged as history.
This archive verification prospectively clears that blocker. The accepted code,
validation artifacts, canonical report, scientific fingerprint and current branch
ancestry were unchanged by preservation. Scientific acceptance was not rerun.

External objects can be verified by their SHA-256 and by reconstructing Git's
object hash over `<type> <size>\0` followed by the archived bytes. Restoring an
oversized blob into this repository would violate the size gate; any historical
inspection requiring restoration must use a separate external repository.
