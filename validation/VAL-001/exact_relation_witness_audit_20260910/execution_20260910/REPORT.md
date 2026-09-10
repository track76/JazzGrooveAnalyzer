# DRUM-EXACT-RELATION-WITNESS-AUDIT-01 — real-input execution report

Date: 2026-09-10. Status: EXECUTED; independently computationally checked; fresh-process replay verified; awaiting PI review of the scientific result.

**Scientific outcome: EXACT_RELATION_RECURRENCE_OBSERVED.**

## 1. Authority and admission

DOCUMENTED AUTHORITY: The current PI authorization permits exactly two real-input executions under reviewed replacement freeze V2, independent checking, custody binding, replay and preservation. The preregistration and freeze remain historical immutable records; their pre-execution status fields are not rewritten. V1 remains superseded.

- `validation/VAL-001/preregistrations/H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01.md` — SHA-256 `c609cfabdfd31f5122cd0883da861c2b742aa2af7a659cf691dbe0d56161e48a`.
- `validation/VAL-001/preregistrations/H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01.authorities.json` — SHA-256 `477cd53b11778091907058ad6157bd0a881b85240d8fd13fa5e9dc3ef676e059`.
- `validation/VAL-001/exact_relation_witness_audit_20260910/implementation_binding_v2.json` — SHA-256 `418d6f71f855414a0aed06d02e6906ede42efba3bab1a7f2044fac3b4df29dfe`.
- `validation/VAL-001/exact_relation_witness_audit_20260910/INDEPENDENT_CODE_REVIEW_V2.md` — SHA-256 `87564d731c940ec5fa255a550bfc82b56a6551f78058c61ee2870c8a4bb0008b`.
- `validation/VAL-001/exact_relation_witness_audit_20260910/execution_20260910/pi_execution_authorization.json` — SHA-256 `efd76f0c53081f5962479b2a034fde0df044c678af337936c52038b6c79169d9`.
- `validation/VAL-001/exact_relation_witness_audit_20260910/execution_20260910/review_authority.json` — SHA-256 `cd9f08c80828ed21f08b151fd23ab6e83b7f933f3853108c8f229ae4186e959d`.
- `validation/VAL-001/exact_relation_witness_audit_20260910/execution_20260910/preflight.json` — SHA-256 `30c754937cdf954ae6c91d4d6e66c0d4201da808ec52d683a9f61b597a4f51ec`.

OBSERVED VERIFICATION: all frozen hashes and population metadata matched before execution. The admitted population contains 63 EME, 63 unique PulseCandidate parents, one source UUID, 1,953 unordered pairs, 1,056 positive exact separations and 3,864 windows. Source UUID: `c46d6cb9-b99c-5bd6-8d81-656dc1ad48ec`; input-freeze hash: `ba21b73d7fe122b29b522f442a3724a89b8fec96549a34b39db62bb7830b29e7`. No original report musical fields, audio or periodicity response shards were used for discovery.

Runtime: CPython 3.13.14, frozen environment fingerprint `13bd11b30796d461ef2cfd73053bb725e26bdd7a9c093226da0a21999911ca2c`. All 690 bound implementation, upstream, external-input and runtime file hashes were rechecked unchanged after execution; see `post_execution_authority_verification.json`. No implementation or scientific authority changed.

## 2. Execution, checking and replay

External result root: `/Volumes/SSD Track/JGA/experiments/H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01`.

### Run 1

- Directory: `/Volumes/SSD Track/JGA/experiments/H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01/run_1`.
- Execution ID: `20bb9467d24339bd9a13c6a2239fcd00`.
- Receipt: `run_1/execution.json`; SHA-256 `72b5d1aaf3f9aa32321bc206f3e64cbc4ca7632f0ab6b4494fe35ce08c26ff6f`.
- Custody authority: `custody_ledger/20bb9467d24339bd9a13c6a2239fcd00.json`.
- generator: launch `90710b5709c261a89164f26d8e88135c`, PID `62781`, exit code `0`.
- checker: launch `c772b71a41c22e2b173c097398ccdf5a`, PID `62804`, exit code `0`.

### Run 2

- Directory: `/Volumes/SSD Track/JGA/experiments/H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01/run_2`.
- Execution ID: `80b822136a75a5e9950bc9882e095d7a`.
- Receipt: `run_2/execution.json`; SHA-256 `72bc611e56ad53a8a6878220f88c0a9152eb5c8dab1d44744666c01d7af085a4`.
- Custody authority: `custody_ledger/80b822136a75a5e9950bc9882e095d7a.json`.
- generator: launch `4bac55dd9b1f000b0edb59d4a2c00596`, PID `62897`, exit code `0`.
- checker: launch `bbe62e3b83e7d28a3cf45943cf74c36a`, PID `62919`, exit code `0`.

OBSERVED: both independent checker traversals returned CONTRACT_VALID, without discrepancies. Both fresh executions preserved the same scientific authority, software and environment. Distinct directories, execution IDs and worker launch IDs were verified against the explicitly selected orchestrator custody ledger before comparison. Eleven canonical files per run, including checker and root, were byte-identical.

Final admission authority: `/Volumes/SSD Track/JGA/experiments/H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01/replay.json`, SHA-256 `f313975acdc4dda71a37bdc40e2134e3e4fcb26d5245d5563ddab690a3bc9d86`. Integrity: CONTRACT_VALID. Candidate acceptance: ADMISSIBLE_COMPLETE_POPULATION. Both roots have SHA-256 `d658d8082612e4e88a41b7a985f735bd7301036524e24e6324a803a1441139ab`.

Checker independence is computational: generator catalogue traversal versus checker enumeration from producer-bit-reconstructed events. It is not a second physical dataset. The renewed review was performed by Codex /root, the same assistant identity as author; the limitation was disclosed and accepted by PI. Custody relies on the trusted ledger and does not claim protection against deliberate forgery of the complete ledger.

## 3. Bounded observed result

Exact equality uses binary64-derived reduced rational seconds. One witness is the full canonical unordered EME-pair identity bound to input-freeze hash and source UUID. Repetition requires at least two distinct witnesses. No tolerance, rounding, bins, clustering, ranking or metric labels were introduced.

| Quantity | Observed value |
|---|---:|
| All positive exact relations | 1,056 |
| Repeated exact relations | 368 |
| Singleton relations retained | 688 |
| All distinct positive pair witnesses | 1,953 |
| Distinct witnesses belonging to repeated relations | 1,265 |
| Windows preserved | 3,864 |

Witness-count distribution (descriptive frequencies, not a ranking of relations):

| Witnesses per repeated relation | Number of relations |
|---:|---:|
| 10 | 4 |
| 11 | 1 |
| 13 | 4 |
| 14 | 2 |
| 18 | 1 |
| 19 | 1 |
| 2 | 182 |
| 20 | 1 |
| 3 | 80 |
| 4 | 45 |
| 5 | 22 |
| 6 | 8 |
| 7 | 5 |
| 8 | 8 |
| 9 | 4 |

Minimum recurring separation: **98037542908745/281474976710656 seconds**, approximately 0.3482993197278894115243 seconds.

Maximum recurring separation: **159160682994251343/4503599627370496 seconds**, approximately 35.34077097505668851873 seconds.

Decimal durations are display-only renderings; exact fractions are authoritative. Nearly equal durations remain separate where their exact rationals differ.

## 4. Dependency, coverage and ratio preservation

Within the same exact relation, 2,748 unordered comparisons of distinct witnesses are preserved: 42 share an endpoint (42/2748), while 2,706 are event-disjoint. There are 80 individual recurrent witnesses involved in shared-endpoint support (80/1265) and 20 relations containing such support (20/368). These denominators describe different objects. No event-disjoint pair is declared statistically independent. Interval relationships: 1,353 disjoint, 42 touching, 1,353 overlapping. Cross-relation reuse remains recoverable through the complete event IDs; these statistics concern same-relation support.

Recurrent witnesses involve 62 of the 63 frozen EME. Endpoint extent is 5437815713338417/4503599627370496 through 2598811866605995/70368744177664 seconds (approximately 1.2074376417233561–36.931337868480725 seconds). The frozen observation scope is [0, 5954146772657809/140737488355328] seconds, approximately [0,42.30675736961451]. Endpoint extent does not establish continuous recurrence, persistence sufficiency or complete physical-event coverage. Every individual temporal location and interval remains preserved.

All 67,528 unordered pairs of repeated relations have an exact neutral ratio record. Integer-ratio occurrence counts: ratio 2: 25; 3: 10; 4: 6; 5: 3; 6: 3; 7: 1. The remaining records also remain preserved; there is no low-denominator filtering, root selection or interpretation as a hierarchy. Every rational pair has a rational ratio; this alone is not structural or metric evidence.

Representation reuse: 1,953 original positive catalogue pair occurrences produce exactly 1,953 unique pairs; no duplicate violations or coincident distinct events. The 2,615,184 both-contained and 2,492,145 both-positive window incidences are preserved as reuse, never additional recurrence witnesses. Coordinate repetition does not count as a witness.

## 5. Complete admissible population and preservation

Candidate file: `/Volumes/SSD Track/JGA/experiments/H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01/run_1/candidate_population.json`.
SHA-256: `b933c5ab50b18b4732f49ea33e3b60d7bfc183f1ae845771d981f704bdd6ca5e`. Run 2 has identical bytes.

**Admission requires candidate file + run root + final replay authority.** The generator file retains PENDING_INDEPENDENT_ACCEPTANCE and proposed-membership flags by design; final replay grants ADMISSIBLE_COMPLETE_POPULATION without modifying frozen generator output. Consumers must not treat the generator file alone as final admission.

All 368 repeated relations are included, with all and only their distinct witnesses, exact locations, source/EME/parent lineage, dependency references, window incidence, uncertainty/missingness and exact neutral ratio references. All 688 singleton relations remain in the full catalogue. No member has priority or beat status.

Preserved in each run: events.json, relations.jsonl, witnesses.jsonl, witness_relations.jsonl, windows.jsonl, reuse_audit.json, relation_ratios.jsonl, candidate_population.json, result.json, checker.json, root.json, execution.json. Custody receipts and replay.json are separate final authorities. Small operational records, descriptive_summary.json and this report are in the repository execution directory and mirrored under the external `operational/` directory. `SHA256SUMS` indexes repository operational files; external `SHA256SUMS` indexes the full new package excluding itself. Mirrors are custody copies, never new executions. Heavy data remains external.

## 6. Maximum claim and limits

OBSERVED, maximum authorized claim: Repeated exact temporal relations are recoverable from distinct event-pair witnesses within the frozen authorized real-Drum observation population, with deterministic independent checking and replay.

UNKNOWN / NOT ESTABLISHED: physical timing uncertainty, physical-event independence, statistical independence, recurrence above chance, statistical significance, recurrence sufficiency, timing invariance, preferred temporal scale, component identity and complete musical-event coverage. Numerical missingness is empty and checking/replay discrepancies are empty; this does not remove physical uncertainty. No BeatReference, tactus, meter, BPM, groove or swing is established.

The observed candidate population is admissible neutral input for future separately authorized research. RECURRENCE != BEATREFERENCE; BEATREFERENCE != BPM. No accepted-map recomputation, audio acquisition, Double-Bass modification, source modification, commit or push occurred. No scientific work outside this experiment was executed.

## 7. PI review boundary

Current boundary: exact relation recurrence observed; RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED. Scientific-result PI acceptance remains pending.

Next scientific question: What additional independently justified evidence is needed to establish recurrence sufficiency and, separately, discriminate a privileged temporal reference, if any, among the complete admitted candidate population? The present result answers neither question.

Exact next action requiring PI authorization: PI review/acceptance of this bounded result and a separate authorization for the next research-design task. No further computation or BeatReference inference is authorized by this report. STOP FOR PI REVIEW.
