# DRUM-EXACT-RELATION-WITNESS-AUDIT-01 — implementation freeze

Date: 2026-09-10. **Implementation and synthetic qualification only. No real-input execution.**
Authority: `../preregistrations/H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01.md`
and its sibling `.authorities.json`. Their SHA-256 values remain respectively
`c609cfabdfd31f5122cd0883da861c2b742aa2af7a659cf691dbe0d56161e48a`
and `477cd53b11778091907058ad6157bd0a881b85240d8fd13fa5e9dc3ef676e059`.
This package does not amend their scientific definitions or acceptance boundaries.

## Implemented responsibilities

| File | Responsibility |
|---|---|
| `generator.py` | Independently validates event/time/source authority, traverses the authenticated period catalogue, checks all-pair conservation, rejects authoritative duplicates, writes the complete proposed catalogue and factorized window incidence. |
| `checker.py` | Independently reconstructs producer bits with integer arithmetic, enumerates unordered event pairs, derives exact relation membership and reconstructs window geometry. Checks every canonical generator record against its own derivation. Does not import the generator. |
| `transport.py` | Shared SHA-256, duplicate-key rejecting JSON parsing, canonical serialization and file I/O only. No scientific arithmetic, identities, grouping, membership or outcome functions. |
| `runner.py` | Explicit authorization and hash admission, fresh generator/checker worker processes, immutable run roots and exact replay comparison. No audio/Fourier imports. |
| `fixtures.py` | Small, artificial populations created from literal test values only. No repository or external scientific input reads. |
| `test_witness_audit.py` | Synthetic numerical, identity, conservation, mutation, guard and fresh-process replay checks. |
| `test_results.json` | Recorded non-scientific test outcome and source hashes. No real recurrence result. |
| `implementation_binding.json` | Source, runtime, input closure, external catalogue and resource bindings. Does not grant execution permission. |

Knowledge classification: source/hash checks and test outcomes are **Observed Facts**.
Conformance conclusions are bounded **Logical Inferences** from implementation inspection
and synthetic checks. Real-input conformance and a real recurrence outcome are **NOT ESTABLISHED**.

## Numerical and identity contracts

Generator: binary64 bytes → `struct.unpack` → `as_integer_ratio()` → exact `Fraction`
differences. Checker: binary64 sign/exponent/significand → integer numerator/denominator →
cross-product differences and gcd reduction, using its own `Number` implementation.
Both verify producer bits against preserved ratio, hexadecimal representation and the
original token's binary64 round trip. Neither uses floating-point subtraction, decimal
arithmetic, proximity, epsilon, rounding, bins or clustering to establish equality.
Signed zero metadata is retained. Positive separations alone enter the recurrence catalogue;
coincident distinct-event pairs remain in a separate ledger.

The frozen witness ID is `["EXACT_PAIR_V1", input_freeze_sha256, source_uuid,
lexical_first_EME_ID, lexical_second_EME_ID]`. A relation repeats only if at least two
different such IDs support the identical reduced rational separation. Parent identities,
event timestamps and source lineage are independently checked by both implementations.
Catalogue duplicates are contract errors, including reversed duplicates; they are not repaired.
Window/center reuse is incidence, never another witness. Shared endpoints and temporal
overlap/touch/disjointness are explicit; no statistical independence is inferred.

All singleton and repeated relations survive. Increasing exact-time ordering is deterministic
serialization, not scientific ranking. All unordered pairs of repeated relations receive
neutral exact ratio records. No score, preference, beat label or metric hierarchy is produced.

## Output and replay

Output schema: **JGA-EXACT-RELATION-WITNESS-V1**. The complete prospective files and fields
implement preregistration Section 6: `events.json`, `relations.jsonl`, `witnesses.jsonl`,
`witness_relations.jsonl`, `windows.jsonl`, `reuse_audit.json`, `relation_ratios.jsonl`,
`candidate_population.json`, `result.json`, `checker.json`, `root.json`, and a final
external `replay.json`. No scientific output files exist in this package.

Each proposed candidate retains exact seconds, canonical witness IDs/counts, temporal
distribution, source/input/implementation/environment authority and scope/missingness.
References retain all event/parent/measurement lineage, shared-event dependencies and
complete window geometry/incidence. Zero/one-endpoint membership is factorized by the
complete witness endpoints and immutable membership sets; both-contained and both-positive
incidence is materialized. Unknown physical timing accuracy and independence remain unknown.

Generator membership is **PENDING_INDEPENDENT_ACCEPTANCE**, including the empty-population
case. Checking adds its own report without altering generator bytes. The run root binds
generator files and checker; its fingerprint is SHA-256 of the canonical map of stream
hashes and byte sizes. A separate replay artifact binds both roots and checks every
canonical file byte for byte. Only complete checking and replay can grant admissibility.
The generator does not claim its own proposed outcome is an accepted scientific result.

Serialization: sorted JSON keys; compact ASCII-safe UTF-8; integer quantities as decimal
strings; reduced rational pairs of integer strings; no binary floats or nonfinite values;
one LF per record/file. Ordering follows preregistration Section 9. Original input tokens
remain strings, not new decimal measurements. No wall-clock, process ID or runtime path
enters scientific streams. Operating logs are separate.

Outcome vocabulary remains EXACT_RELATION_RECURRENCE_OBSERVED,
NO_EXACT_RELATION_RECURRENCE_OBSERVED, INSUFFICIENT_EVIDENCE and INDETERMINATE.
Missing/incomplete evidence never becomes a negative result. `failure_report` supplies
withheld-population status; post-start failures retain partial files and a failure record.
Preflight exceptions must be retained in the future operator's invocation/stderr log.
Checker disagreement or replay mismatch withholds admissibility; there is no automatic repair.

## Synthetic qualification

Run from repository root, without real inputs:

```sh
python3 -B -m unittest discover -s validation/VAL-001/exact_relation_witness_audit_20260910 -p 'test_*.py' -v
```

| Requested case | Test evidence |
|---|---|
| A | No recurrence despite multiple windows/centers; coordinate reuse cannot create support. |
| B | `[0,1,1,2]` has one repeated positive separation and two event-disjoint supporting pairs among four retained witnesses; coincident distinct events are explicitly preserved. |
| C | `[0,1,2]` has shared-endpoint support, classified dependent and touching. |
| D–E | The same pair appears in several windows and centers while retaining exactly one witness ID. |
| F–G | Multiple repeated relations and exact neutral ratios; all members preserved. |
| H | A one-ULP perturbation prevents equality even where decimal displays may look similar. |
| I | Reversed catalogue ordering leaves canonical unordered identity unchanged. |
| J | Duplicate pairs and duplicate catalogue/window records are rejected, not inflated. |
| K | Broken source, parent, content hash, numerical authority, missing catalogue, unauthorized input and semantic-field contamination rejected. |
| L | Fresh generator/checker subprocesses produce byte-identical files and roots; independent replay comparison accepts identical synthetic runs and withholds conflicting ones. |

Case B does **not** claim exactly two total witnesses. Four different timestamps with two
event-disjoint pairs of equal separation also imply another repeated cross-pair separation:
`[0,1,4,5]` tests that both are retained. The coincident-event fixture tests the preregistered
generic zero-separation path; it does not relax the real population's 63-distinct-centers
admission requirement. No scientifically required relation was suppressed to construct a fixture.

Additional checks cover normal/subnormal/signed-zero/extreme binary64 encodings, 200 seeded
bit patterns, 16 seeded small populations, opaque-ID renaming, input-order permutation,
boundary incidence, every scientific output stream, malformed JSON and known SHA-256 bytes.
These are implementation integrity tests, not statistical or physical validation.

## Review and independence boundary

Implementation author: **Codex, current `/root` session**. The same session performed a
separate conformance inspection after implementing the two numerical traversals and tests.
This is disclosed as **author review**, not an independent reviewer sign-off.

The checker is computationally independent in the preregistered sense: it derives its
answers from event producer bits, not generator groups/counts, and does not share scientific
helper code. It necessarily shares the frozen hypothesis, input evidence, Python integer
runtime and standard cryptographic/JSON libraries. `runner.authenticate_real` is shared
byte-authority orchestration invoked afresh by both worker processes; event, numeric,
identity, catalogue and window admission is implemented separately in each program.
This shared orchestration remains in the independent review scope. The fixture constructor
is not imported by either scientific implementation.

**Separate independent code review is still required by preregistration Section 8.**
No reviewer identity or approval has been fabricated. Freeze the tested source bytes now;
bind a separate review record to this implementation-binding hash before execution.
The record must identify the reviewer, review scope, exact implementation hash and explicit
completion. A discovered defect requires new source/test/freeze records before real execution;
this package is not retrospectively declared reviewed merely because the checker agrees.

## Input and execution firewall

All preregistration repository entries and the five external root/index/input/period/window
files were checked **by hash only**. The real input freeze, external event/pair/window contents,
canonical timing report and response shards were not loaded into these implementations.
No expected real repeated-relation count, candidate duration or ratio was obtained.

The frozen implementation binding retains the upstream map's input/implementation-source
hash closure. Historical numerical-library environment records remain provenance; this
observer uses no FLINT, Fourier evaluator, audio library, separator or tempo estimator.
The new CPython/runtime file binding is independently specified in the manifest.

Real invocation requires a **new PI authorization record** with experiment, action
`REAL_INPUT_GENERATOR_CHECKER_AND_REPLAY`, `pi_authorized=true`, PI identity, decision
reference, this implementation-binding SHA-256, and the independent-review path/hash.
The reviewer record must bind the same implementation hash. These operational records
do not redefine witness identity or alter preregistration. Neither record is created here.

Future `runner.py real AUTHORIZATION_JSON RUN_DIRECTORY` first verifies that authorization,
review, sources, runtime and all upstream/catalogue hashes match. It admits only the frozen
external root and new `run_1`/`run_2` destinations under
`/Volumes/SSD Track/JGA/experiments/H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01/`.
It launches fresh generator and checker subprocesses. Existing run directories are never
overwritten. After two independently checked runs, the operator calls the bound
`runner.compare_replay(run_1, run_2, replay_path)` once, retaining invocation logs.
No such real invocation or directory creation occurred now.

Synthetic mode requires an explicit fixture tag, a synthetic source/population, at most
16 events and no real source UUID. Direct generator/checker calls also reject a real
source under a synthetic tag and require operational admission for non-synthetic inputs.
These are accidental-execution guards, not a security claim against a user modifying Python.

## Resources and storage

Only events and the compact period catalogue are loaded as collections; windows,
within-relation witness comparisons and exact ratio records stream. The two implementations
run in separate processes. Synthetic fixtures and temporary outputs use the system temporary
directory; no heavy scientific output belongs on the internal SSD.

The bound planning population permits at most P=1,953 unordered witnesses, W=3,864 windows,
R=1,056 positive relations. Capacity planning uses P(P−1)/2 possible within-relation witness
comparisons and R(R−1)/2 ratio records as **worst-case bounds**, not observed counts.
Allow 512 bytes per two-list window/witness incidence, 4,096 per dependency record and
8,192 per ratio record, plus original catalogue bytes, event/provenance duplication and
1 GiB reserve per run. The accepted UUID widths are checked operationally; no long ID is
silently truncated or discarded. Binary64 dyadic arithmetic has bounded integer width.
The conservative rounded disk preflight is **64 GiB before run_1, 32 GiB before run_2**;
this is an operational capacity reserve, never a scientific threshold. Capacity assumptions
and output schema require independent review before release. Actual future free space
must be verified then; availability now is not a reservation.

## Exact remaining boundary

The implementation sources and environment can be frozen after successful synthetic
qualification. **Ready for real-input authorization: NO pending separate independent code
review.** No scientific definition or equality authority is missing or changed. The remaining
review is an implementation-release gate, not permission to inspect the real recurrence result.

Maximum later successful claim remains repeated exact observed temporal relations in this
frozen source/measurement population, with a complete neutral candidate population.
RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED; BeatReference and BPM remain unauthorized.
Double-Bass authorities, accepted map evidence and the preregistration remain unchanged.
No commit or push. Stop for PI review.
