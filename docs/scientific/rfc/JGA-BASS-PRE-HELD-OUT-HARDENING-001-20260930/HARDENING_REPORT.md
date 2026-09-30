# JGA-BASS-PRE-HELD-OUT-HARDENING-001-20260930 — HARDENING REPORT

PI authorization: `PI-BASS-PRE-HELD-OUT-HARDENING-20260930`
Scope: evidentiary / reproducibility firewall only. **This task does not authorize the
held-out experiment, any held-out prediction, or any label reveal.**

---

## 1. Pre-held-out freeze anchor (item 1)

Canonical anchor: `docs/project/BASS_FREEZE_ANCHOR_20260930.json`

It is persisted **outside** the package it authenticates, and enumerates all
**12** package files with size and SHA-256, plus Git HEAD, branch, package path, a
deterministic package fingerprint and a separate frozen-scientific fingerprint.

- `package_fingerprint_sha256` = `0d151561a8ce144a11ef47142e80021eb7f96ce5a6de08c2b2648b2d554da906`
- fingerprint definition: sha256 over, in ascending path order,
  `<path>\0<size_bytes>\0<sha256>\n` for every package file.
- The anchor itself is covered by neither `SHA256SUMS` nor any commit.

### Honest strength statement

The anchor provides **tamper EVIDENCE** — divergence is detectable by recomputation.
It does **not** provide tamper **prevention**, and it is not cryptographic immutability:

- both the working repository and the HD mirror are ordinary writable filesystems;
- an actor able to write to both could rewrite package + anchor + mirror coherently;
- no WORM store, no signature, no notarized third-party timestamp is in use.

**The first anchor was computed before a final edit, and rehearsal step A detected the
drift by itself.** That is recorded as `supersedes_fingerprint` in the anchor. The
detection machinery is demonstrably live, not theoretical.

---

## 2. Untracked package decision (item 2)

### `COMMIT_BEFORE_HELD_OUT: RECOMMENDED`

Evidence gathered:

| Fact | Value |
|---|---|
| Git remotes | 1 — `https://github.com/track76/JazzGrooveAnalyzer.git` |
| Commits in history | 614 |
| Tracked files under `docs/scientific/rfc` | 723 |
| Untracked rfc packages | ~150 |
| BASS classifier package tracked | no (9 → now 12 files) |
| Phase A package tracked | no (23 files) |
| Freeze anchor tracked | no |

Rationale:

1. **The untracked state is an anomaly, not the project norm.** The majority of
   scientific rfc packages are tracked; the entire BASS evidence chain is not. A
   freeze that sits outside version control is inconsistent with how the rest of the
   scientific record is maintained.
2. **A local-only commit adds little.** The anchor and a local commit are both inside
   the same trust domain (this machine). The meaningful unit is commit **and push**.
3. **Push is the only available independent copy.** Once pushed, rewriting local
   history does not remove the object from the remote. This is the one asymmetry that
   defeats the coordinated local rewrite that defeats anchor + mirror.
4. **It is not REQUIRED** in the strict sense: JGA governance mandates continuous
   external backup, not commit, and no scientific value of the evaluation depends on
   Git specifically. The anchor + external backup already satisfies the letter of the
   governance requirement and makes drift detectable.

**Escalation condition.** If the PI requires the freeze evidence to be independent of
this machine's control — that is, to defeat a post-hoc coordinated rewrite by a
local agent — then commit **and push** must be treated as a **precondition** for
reveal authorization, not a recommendation. The PI's decision.

No commit and no push were performed in this task.

---

## 3. Held-out plaintext on HD (item 3)

Recorded truthfully: **held-out human labels exist in plaintext on the canonical HD
archive and are not physically inaccessible.** Nothing was deleted or moved to
manufacture an appearance of blindness; doing so would fabricate the evidentiary
condition the report is meant to establish.

Blindness is therefore enforced by **process**, in seven layers:

1. explicit prohibited-path list bound to real on-disk artifacts;
2. runtime audit-hook test that fails if pre-reveal scoring opens any prohibited path;
3. anti-vacuity test that fails if the prohibited list stops matching disk;
4. static AST check that no answer-bearing filename appears in executable code;
5. prediction artifact must carry no label field — scoring rejects it otherwise;
6. prediction artifact hashed and externally backed **before** reveal authorization;
7. reveal and scoring are separate, individually authorized, ordered gates.

Presence of every listed artifact was established with `stat` only. **No answer-bearing
file content was opened, read, parsed or inferred.**

---

## 4. Partial unstable-membership leak (item 4)

`HELD_OUT_UNSTABLE_MEMBERSHIP_BLINDNESS: PARTIALLY_COMPROMISED`

The global set of 10 human-unstable item numbers is public, and the 8
development-unstable identities are readable. The two held-out-unstable identities
are therefore logically derivable by set difference.

**The derivation was not performed. The two item numbers were not identified and are
not recorded anywhere in this task's output.**

This does **not** reveal the stable held-out YES/NO answers, and it does **not** affect
binary scoring: human-unstable held-out cases are already excluded from binary scoring
by the preregistered methodology. The split was **not** redesigned; it was sealed
before the classifier existed.

---

## 5. Firewall tests (item 5)

The previous guard listed three filenames that **do not exist** at the SSD path the
predictor reads. It certified a firewall it never tested.

Repaired to guard the real artifacts on both volumes, and to fail if that list ever
drifts away from disk again. The runtime check uses `sys.addaudithook`, which traps
`io`/`pathlib` mechanisms that bypass `builtins.open`.

**Negative control:** the detector was proven to fire by opening decoy files with the
same basenames in a temporary directory. The genuine answer files were never opened.
The guard is therefore demonstrably not vacuous.

---

## 6. Predictor file-access audit (item 6)

`PREDICTOR FILE-ACCESS AUDIT: PASS`

Inputs were synthetic feature records plus one **confirmed development** item. No
held-out identifier was used.

Complete observed access set — exactly three files:

1. `.../JGA-BASS-SOURCE-PRESENCE-CLASSIFIER-DEV-001-20260930/FROZEN_PIPELINE.json`
2. `.../JGA-FULLMIX-INSTRUMENT-IDENTITY-001-20260929/PHASE_A/SOURCE_EVIDENCE_TABLE.json`
3. `/Volumes/SSD Track/.../SEALED_ITEM_EVENT_MAP.json` (membership only)

Answer-bearing artifacts opened: **NONE**. `score()` performs no file access at all
once the spec is in memory. Scoring is deterministic across repeats.

---

## 7. Frozen overwrite protection (item 7)

`FROZEN OVERWRITE PROTECTION: PASS`

`train_bass_classifier.py` now refuses by default to overwrite an existing
`FROZEN_PIPELINE.json` / `VALIDATION.json`, failing fast *before* any fitting. Escape
hatches require a new namespace, or `--allow-regeneration` **plus** a PI override token
in the environment for an in-place write.

No scientific logic was changed. **No retraining was executed** while testing this —
the refusal was proven against the live frozen package, which remained byte-identical.

---

## 8–9. Held-out scoring preregistration and post-reveal prohibitions

`HELD-OUT SCORING PREREGISTRATION: PASS` — see `HELD_OUT_SCORING_PREREGISTRATION.json`.

Agent A's methodology adopted formally. Metrics: balanced accuracy, BASS_PRESENT
sensitivity, BASS_ABSENT specificity, precision, F1, confusion matrix, plus counts of
stable PRESENT / stable ABSENT / human-unstable. Human-unstable cases are excluded
from binary scoring, never counted as binary errors, never relabelled, reported as an
aggregate count only.

**No categorical strong / partial / failure boundary is authorized.** The report must
state that n is too small for a defensible categorical performance boundary. Exact
Clopper-Pearson intervals are reported for single proportions; no interval for
balanced accuracy; no significance test and no p-value.

Post-reveal prohibitions recorded: no threshold adjustment, no feature replacement, no
model selection, no relabelling, no deletion of stable cases, no second attempt. Any
improvement must be a new development cycle, with this held-out result retained as
historical evidence.

---

## 10. Prediction freeze sequence (item 10)

See `PREDICTION_FREEZE_SEQUENCE.json`. Steps A–K are defined and **rehearsed on dummy
data only**: dummy identifiers `DUMMY_ITEM_01..20` and synthetic features. Steps J
(reveal) and K (scoring) execute as **refused gates** and were not run.

Rehearsal result: order `ABCDEFGHIJK` verified, step A anchor verification passed over
all 12 files, step F hashed the artifact, step G wrote a freeze record containing
prediction hash, model-anchor hash, timestamp, HEAD, branch and the exact item IDs,
step I independently confirmed the artifact unchanged, steps J and K blocked.

---

## 11. Scoring code freeze (item 11)

`SCORING CODE: FROZEN` — `REPRODUCTION/score_bass_heldout.py`

Written before any result is known and tested **only on synthetic fixtures**. It
separates unstable cases, computes only the preregistered metric set, never mutates
predictions or labels, is deterministic, and rejects any prediction artifact carrying a
label field. It is covered by the freeze anchor, so its hash is anchored before reveal.

---

## Residual risks carried forward

| Risk | Status |
|---|---|
| Anchor and package share one trust domain; coordinated local rewrite defeats both | **OPEN** — needs commit+push or a notary |
| `tools/continuous_backup.py` has no label/sealed exclusion | **OPEN** — out of scope; mirror is not a secrecy boundary |
| Anchor itself untracked and uncommitted | **OPEN** — same remedy as item 2 |
| Phase A package (23 files) untracked and not covered by the BASS anchor | **OPEN** — its hashes are recorded in `INPUT_PROVENANCE.json` |
| Held-out unstable identities derivable | **ACCEPTED AND QUALIFIED** — recorded, not mitigated |
| `FROZEN_PIPELINE.json` imputation wording vs predictor's non-finite rejection | **PRE-EXISTING** — unaffected by this task; all eligible rows are complete |
