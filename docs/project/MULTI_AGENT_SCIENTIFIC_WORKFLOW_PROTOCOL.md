# Multi-agent scientific workflow protocol

Status: PI-authorized project governance, effective2026-09-27. Applies equally to Codex, GitHub Copilot, Qwen and any later agent. This protocol coordinates work; it does not replace the scientific knowledge hierarchy or promote experimental results.

## Entry point and authority synchronization

Start with the single root [JGA_BOOTSTRAP.md](../../JGA_BOOTSTRAP.md). Before following scientific links, searching repository contents or loading another agent's context, read the [coordination state and active embargo register](MULTI_AGENT_COORDINATION_STATE.md). It contains safe metadata only. Follow [AGENTS.md](../../AGENTS.md) and the [single-root contract](../architecture/BOOTSTRAP_SINGLE_ROOT_DECISION_20260922.md); do not create another bootstrap root.

Before ANY new scientific, research or engineering task:

1. Read the root bootstrap; determine current branch, HEAD, worktree and staged state (`git branch --show-current`, `git rev-parse HEAD`, `git status --short`). Preserve unrelated changes. Use filenames/metadata first so status discovery does not expose embargoed contents.
2. Identify the task's explicit PI authorization, constraints and relevant PI decisions. A recommendation, another agent's completion or this protocol is not task authorization.
3. Follow the bootstrap's canonical authority references relevant to the task, subject to embargo. Check relevant artifacts created since the last completed authorized task, including untracked work and external manifests; Git commit history alone is insufficient. Use prior handoff/manifests as the baseline. If no baseline exists, say UNKNOWN and inventory relevant safe metadata instead of claiming none exist.
4. Classify relevant artifacts from explicit provenance/PI decisions: CANONICAL AUTHORITY, FROZEN HISTORICAL RESULT, EXPERIMENTAL, PI REVIEW REQUIRED, SUPERSEDED, or EMBARGOED FROM THIS AGENT. These labels can coexist (e.g. EXPERIMENTAL plus embargo). Unknown status remains UNRESOLVED. Newest timestamp/file/commit never implies authority, promotion or supersession.
5. Identify conflicts or missing authorization; report an Evidence Conflict and stop only dependent work for PI clarification. Do not silently choose the latest result, rewrite another agent's evidence or reinterpret an old task's permissions.
6. Establish storage and backup preflight before substantive work. Report the following, compactly for small read-only tasks:

```text
AUTHORITY SYNC: PASS/FAIL
CURRENT BRANCH:
CURRENT SCIENTIFIC AUTHORITY:
NEW RELEVANT ARTIFACTS:
PI DECISION:
INDEPENDENCE EMBARGO:
STORAGE PREFLIGHT:
BACKUP PREFLIGHT:
```

## PI authority and task boundaries

Only the PI may authorize new scientific directions or methodological decisions; experimental-to-authority promotion; frozen-result changes; canonical-method replacement; lifting an embargo; diagnosis-to-optimization transition; detector/selector deployment; and final scientific interpretation. An agent may recommend, never self-promote a finding.

Complete only the authorized task. Completion does not authorize the next experiment, a cross-review, a new download, or a deployment. STOP FOR PI REVIEW unless the PI explicitly authorized a bounded chained sequence in advance. Such authorization does not implicitly lift an embargo or expand scientific scope. The PI may explicitly authorize a task despite an older milestone stop; record that authorization without rewriting historical freezes.

## Independence and embargo

The generic marker is `INDEPENDENT_REVIEW_EMBARGO`; the embargo registry specifies audience, protected path/derivatives, owner, task status, PI decision and release condition. A restricted agent may know that the independent task and newer experimental artifacts exist, but must not read their results, feature findings, conclusions, proposed solution/next step, or use their derived features. Apply embargo checks BEFORE broad searches, diffs, context/export loading, retrieval/indexing or another agent's handoff.

Scope protection includes copies, summaries, generated exports, shared chat/context, tool outputs and agent messages that convey the protected findings. Do not bypass it through a renamed file or a shared sub-agent. Allowed prior evidence remains allowed even where it independently contains related concepts; embargo is not a blanket block on the research topic.

Independent work uses a separate context and separate output package. Do not inject the other agent's reasoning through delegation, shared notes or prompts. This document is a behavioral protocol, not an OS access-control guarantee. Configure retrieval/context exclusions when available. If a tool cannot respect the boundary, stop the affected work. If accidental exposure occurs, stop the independent interpretation, report what was exposed without redistributing the finding, and let PI decide whether a fresh context or other remedy is required. Do not claim blindness after exposure.

Both independent investigations must be finalized before the PI may lift the embargo and authorize CROSS-REVIEW. Finalization alone does not lift it. Record the explicit PI release decision in the PI decision log and scope in the embargo registry; elapsed time, shared Git visibility, common employer/model or task completion is not release.

## Authorized cross-review

Only after PI authorization may AgentA inspect AgentB's finalized experimental report. Write a separate review, cite exact artifact versions/hashes and classify findings individually:

- AGREEMENT
- DISAGREEMENT
- UNSUPPORTED CLAIM
- METHODOLOGICAL RISK
- REPLICATION FAILURE
- UNRESOLVED

A read-only disagreement is not a replication failure without an authorized attempted replication. No silent edits to the reviewed agent's artifacts. Recommendations and corrections require PI authorization through their own task; cross-review does not grant scientific promotion or detector execution.

## Shared workspace and handoff discipline

The [infrastructure ownership/operating contract](INFRASTRUCTURE_ARCHITECTURE.md) defines the mandatory single-writer lease, lifecycle, registries, routing, consistency and Git guards for ALL agents. Read the [agent registry](AGENT_REGISTRY.json), [work ledger](AGENT_WORK_LEDGER.jsonl), [PI decisions](PI_DECISION_LOG.jsonl), [embargo registry](EMBARGO_REGISTRY.json) and [external artifact index](EXTERNAL_ARTIFACT_MANIFEST.json). Current coordination is a view; these typed records own their respective state. Concurrent work permits at most ONE writer; every other agent is read-only. Mode and writer authority must be explicitly assigned for the task.

State task ownership and intended output paths before writing. Do not overwrite another agent's in-progress output, clean unrelated worktree changes, or stage unrelated files. Prefer distinct task packages/branches where appropriate; branch isolation does not provide epistemic independence. Serialize shared canonical mutations, backup and Git operations. If ownership conflicts, stop the conflicting write and ask PI. This protocol does not itself authorize spawning agents, delegating research or assigning Copilot its pending task.

## Storage preflight — external SSD

Follow [External Storage for Heavy Operational Artifacts](../TOOLCHAIN/EXTERNAL_STORAGE.md). Resolve the existing authorized `JGA_EXTERNAL_ROOT` and destination, not a new convenient internal location. The established local SSD JGA architecture is `/Volumes/SSD Track/JGA`; verify actual configuration, volume availability, space and destination authorization before use. A known root does not automatically authorize every new workload/destination.

Before a NEW large download/generation, report expected artifact, estimated size (or explicitly unknown), intended SSD path and the authorizing PI decision. Audio, stems, datasets, weights, checkpoints, large caches/intermediate arrays and large external repositories must not be placed in the Git repository or duplicated on the Mac internal disk for convenience, including internal temporary/cache paths. STOP FOR PI APPROVAL when destination/authority is not already explicitly authorized. Missing external storage never permits internal fallback.

Small governance/code/manifest records stay in the repository under its storage rules. Do not move, delete or replace existing authoritative heavy assets (including grandfathered repository assets) without PI approval. No migration or GUI implementation is authorized by this protocol.

## Continuous backup and version control

The [continuous external backup authority](CONTINUOUS_EXTERNAL_BACKUP_AUTHORITY.md) governs all required writes, including scientific outputs and governance artifacts. Run its preflight; atomically complete each file, immediately external-copy/SHA-256 verify, and perform the required final inventory. Backup copy/verification is not permission to inspect or summarize embargoed content. Restricted agents should not load such payloads into their reasoning context when running approved integrity utilities.

Before declaring completion explicitly report BACKUP. If required backup fails, report `BACKUP: FAIL` and STOP FOR PI REVIEW; do not declare the scientific operation safely completed. Existing policy governs any PI-authorized backup debt and never allows silently claiming PASS. Use NOT APPLICABLE only when no required writes/backups occurred.

Follow existing Git policy and current PI scope. Before commit show the concrete changed files/reasons when repository policy requires approval; do not infer commit/push or a scientific freeze from experiment completion. Use focused staging and required staged-byte backup verification. An authorized governance commit is not promotion of scientific results.

## Persistent external-chat recovery manifest

Maintain [JGA_CHAT_HANDOFF.md](JGA_CHAT_HANDOFF.md) as the lightweight PERSISTENT EXTERNAL-CHAT RECOVERY MANIFEST. It supplements attached root bootstrap for ChatGPT without filesystem access. It is NOT a second bootstrap, scientific authority, replacement scientific record or replacement experimental report. Every substantive scientific statement must cite its repository authority/artifact, classification and important SHA-256 where applicable.

Synchronize it whenever an authorized completed block changes scientific/project state, authority status, a PI decision, agent roles/status, embargoes, an open PI-review gate, authorized/deferred work, recovery-relevant branch/HEAD, storage or required backup state. This is mandatory post-task maintenance, not permission for another scientific task. Include current Git/worktree state and distinguish frozen results from experiments; embargoed work receives safe existence/path/status metadata only. Never leak protected results via a chat attachment.

Before declaring a block fully handed off: (1) synchronize the manifest; (2) verify factual content against repository authorities; (3) verify paths; (4) check embargo safety; (5) record observed HEAD/branch and update time; (6) record verified backup status and scope. If any cannot be completed, report `HANDOFF STATUS: STALE` and STOP FOR PI REVIEW. Do not silently present stale facts as current.

Record HEAD as an observed snapshot, not the hash of the commit containing this file; avoid self-referential hashes/endless amend cycles. After an authorized Git operation changes recovery state, refresh the working-tree handoff and back it up, clearly distinguishing it from an older committed copy. Commit/push remains separately scoped by PI authorization. The PI explicitly approved the infrastructure closure, including focused commit/push; this grants no scientific task.

Keep the file small: brief permitted summaries, status, paths and hashes; no audio, datasets, weights, binary artifacts, full reports, large CSVs or logs. Use [coordination state](MULTI_AGENT_COORDINATION_STATE.md) for PI role/embargo decisions, not a competing authority in the handoff. On mismatch, report the conflict and stop dependent work.

For a new external ChatGPT conversation, the PI supplies root `JGA_BOOTSTRAP.md` and `docs/project/JGA_CHAT_HANDOFF.md`. Instruct ChatGPT to read both completely, assume NO direct filesystem access unless explicitly supplied, distinguish reported repository references from files personally inspected, preserve team roles/embargoes/storage/backup/PI gates, and complete recovery before any scientific work. Additional scientific execution still needs PI authorization.

## Mandatory post-task handoff

Provide this handoff in the task's authorized result package or final response; do not create a parallel scientific authority. Put only safe status/path metadata in shared coordination records when findings are embargoed. Record PI decisions and artifact classification, not just a wall-clock 'latest' marker.

```text
TASK STATUS:
HANDOFF STATUS: CURRENT/STALE
CHAT HANDOFF PATH:
RESULT:
ARTIFACTS CREATED:
ARTIFACTS MODIFIED:
INPUT SHA-256:
OUTPUT SHA-256 where applicable:
SCIENTIFIC STATUS:
AUTHORITY CHANGED: YES/NO
FROZEN RESULT CHANGED: YES/NO
STORAGE STATUS:
BACKUP: PASS/FAIL/NOT APPLICABLE
COMMIT:
PUSH:
NEXT STEP RECOMMENDATION:
STOP FOR PI REVIEW
```

Input/output hashes identify exact bytes, not claims of validation. Update task status/embargo metadata only to reflect authorized decisions and actual completion; never copy restricted conclusions into shared handoff channels. A next-step recommendation is not authorization to execute it.

## Publication and exact-HEAD external chat recovery

A committed document cannot literally contain the hash of its own containing commit. The persistent handoff therefore declares `Publication HEAD: $Format:%H$` with Git `export-subst`. Its numeric preparation/content-snapshot HEAD is explicitly historical. The CURRENT check requires a clean committed handoff, export-subst enabled and its last-touch commit equal to HEAD; later unsynchronized commits are STALE.

After an authorized push, run `tools/export_chat_recovery.py --destination <authorized-SSD-recovery-path>/<final-HEAD>`; it verifies remote HEAD, exports ONLY root bootstrap and handoff through Git, substitutes the exact final HEAD, and hash-verifies the immutable package and its mapped backup. Give these exported files to external ChatGPT. Raw Git template tokens are not an inspected commit hash. Publication receipts reference the verified content commit; the final carrying commit is resolved through Git/export, avoiding recursive commits. No intentional tracked handoff changes may remain uncommitted.

A full repository mirror and a versioned GOVERNANCE-ONLY freeze archive preserve this closure. Historical SSD inventory remains NOT FULLY CERTIFIED. Unrelated existing scientific work must never be staged, reverted or hidden just to make a governance working tree appear clean. Report its actual status.

## PI-controlled restricted blind-worker startup — 2026-10-06

Root JGA_BOOTSTRAP.md remains the single recovery root. A coordinator/recovery
context performs complete canonical recovery. Only explicit PI authorization may
permit a scientifically blind worker to start from a restricted authority/input
view when complete recovery would expose protected validation targets. This is an
execution view of canonical authority, never MACHINE_BOOTSTRAP/BLIND_BOOTSTRAP or
another recovery root. A worker cannot silently select skipped documents.

Record task ID, agent, PI decision, hash-bound coordinator recovery record,
permitted authority file identities/hashes, absolute allowed paths, denied and
embargoed paths, and release condition. `validate_blind_view` / `blind_access` in
the existing governance tool validate those bindings; callers must route opens
through the permitted view and retain file-open audit evidence. Cooperative
checks do not intercept arbitrary file access. Denied paths remain denied in the
pre-unseal view: use a separately PI-bound post-release access view only after
verified release gates. The existing embargo registry and independent Agent A/B/C
roles continue to apply; no new universal role roster is imposed.

Generic or PI-permitted Human-derived summaries alone do not automatically
invalidate independence. Exposure to protected CURRENT validation-target
coordinates before output freeze compromises claimed blind execution. Using
protected target information to change method, parameters, population or machine
selection invalidates independent qualification. Output freeze before reveal is
necessary but insufficient: method, parameters, population and evaluation rules
must also be independently fixed. Existing stricter task-specific freezes prevail.
No already-blocked qualification is retroactively rehabilitated by this rule.

One admitted bounded task may contain multiple gated phases. Required transitions
are recorded in its ledger under the same task ID; phase IDs are optional. A
new scientific scope still requires PI admission. A phase gate cannot confer
another task, change a frozen criterion, or release Human data automatically.

The coordinator validates canonical PI linkage. Restricted workers receive only
the permitted, coordinator-verified PI decision record, with its source provenance
and hash in their access audit. `blind_access` requires that record explicitly; it
never implicitly reloads full canonical PI logs. Its optional coordinator validator
may use full recovery only in the unrestricted coordinator context.

## PI-authorized historical consistency and governed publication — 2026-10-06

PI-PRE-DC3-GOVERNANCE-RECONCILIATION-PUBLICATION-20261006 authorizes the existing
lifecycle tooling alignment and scoped pre-DC3 checkpoint publication only.
Historical ledger events remain immutable. Append-only corrections identify the
original record number plus canonical JSON SHA-256, task/event, correction PI
decision and preservation/provenance. Verified same-task decision linkage may
resolve historical malformed fields; unresolved consent remains visibly
HISTORICAL_AUTHORIZATION_UNRESOLVED, never retroactively authorized. PI-accepted
missing intended historical references remain UNKNOWN qualifications without
fabrication. Current references and task admission remain strict. Corrections
cannot resolve current recovery or embargo references; conflicts fail closed.

The existing governance adapter supports REVIEWED_WORKTREE → GOVERNED_STAGE →
VERIFY_STAGED_SCOPE → GOVERNED_COMMIT → VERIFY_COMMIT → GOVERNED_PUSH →
VERIFY_REMOTE_HEAD. Its owner lease remains held throughout. Exact reviewed
path/operation/blob hashes, parent/branch/tree and unchanged unrelated worktree
are verified before advancing only expected index/HEAD transitions. Unexpected
changes are not absorbed by generic resync. Publication guards and a reviewed
passing test receipt remain required. No automatic task chaining or promotion.

This checkpoint has an explicit PI-linked publication-under-backup-debt exception.
It remains BACKUP_DEBT_PI_AUTHORIZED — OPEN, never backup PASS. Old HD access is
prohibited. Final Git export-subst recovery resolves the actual carrying commit;
a post-publication receipt may reference the verified content commit and be
carried by one explicit final closure commit, without a recursive amend loop.
