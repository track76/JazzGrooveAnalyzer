# H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01

Date: 2026-09-10. Status: **PREREGISTERED DESIGN — NOT IMPLEMENTED — NOT EXECUTED**. Scientific/input/checker design complete; execution requires PI authorization and a reviewed frozen implementation binding. This document does not authorize computation.

## 1. Question, hypothesis and PI direction

Within the frozen accepted source-instance observation population, does any positive exact temporal separation have more than one distinct EME-pair witness? H_exists: there exists a relation T with at least two distinct canonical event-pair identities satisfying |t_b−t_a|=T under the accepted numerical authority. H_none: no such T exists. Two distinct pairs is the logical meaning of repetition, not a sufficiency, significance or statistical-independence threshold.

The PI accepts the design audit `docs/scientific/rfc/DRUM_PERIODICITY_RECURRENCE_SUFFICIENCY_RESEARCH_DESIGN.md`, SHA-256 `9a2a48381675ae9013afd04799257b2d238887c07e7cd4f586481036c1cbea10`, and directs that all subsequently established recurrent exact temporal relations become the neutral **ADMISSIBLE_RECURRENT_TEMPORAL_CANDIDATE_POPULATION** from which future BeatReference discrimination may start. This records the present PI decision; it does not claim such a population has been observed. No member is a beat, privileged level or preferred candidate. No musically implausible duration may be discarded.

Non-hypotheses: recurrence above chance, physical recurrence under timing error, statistical significance, recurrence sufficiency, robust timing invariance, source-component identity, complete musical-event coverage, metric hierarchy/preference, BeatReference, tactus, meter/downbeat, BPM, groove/swing or Bass/Piano correspondence. No strong/frequent/short/long period is selected. RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED remains unchanged even after successful execution.

## 2. Frozen authorities and admission

Sibling manifest: `H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01.authorities.json`.
SHA-256: 477cd53b11778091907058ad6157bd0a881b85240d8fd13fa5e9dc3ef676e059.

The manifest binds repository authorities and the existing external run_1 root/index/input/period/window catalogue bytes. It deliberately does not copy the accepted event population or giant response files into a new input file. Its references are enough to reconstruct all permitted inputs. This preregistration binds that manifest; a future implementation binding binds both documents, avoiding circular hashes.

Accepted map: `validation/VAL-001/complete_real_drum_periodicity_20260908/`, scientific fingerprint `03146e8794151bb91faa938eb3f0f8ea1cfda34a12faaaf84158e820c39e96fc`, logical fingerprint `1e5030acfa48d976832c31ebff220c5094ff14a7567bc67648cdbd01de8d54a9`. Its `.inputs.json` preregistration sibling hash is `ba21b73d7fe122b29b522f442a3724a89b8fec96549a34b39db62bb7830b29e7`; root hash `0e9290e7cf47f9c87abfbadf5df92e1099b4c870429b6cb3723df2d8d85df4d2`. Replay is evidence of deterministic preservation, not another observation population.

Frozen population: **63 EME, 63 unique supporting PulseCandidates, one source UUID**, 63 distinct centers, 1,953 unordered distinct-ID pairs, 1,056 positive exact period coordinates and 3,864 center-specific windows. Existing 4,080,384 response queries and 133,195,392 operator accumulations are provenance only; neither is an observation count for recurrence. Expected number of repeated relations is **not preregistered or computed in this task**.

Source UUID `c46d6cb9-b99c-5bd6-8d81-656dc1ad48ec`, authority `VAL-001-DIRECT-INPUT-SOURCE-AUTHORITY-V1`, key `VAL001_SOURCE_001`. Asset reference hash `d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd`. Scope is the frozen closed interval [0, accepted binary64 42.30675736961451 s]; use its exact ratio, not the sample-count/rate quotient. The source authority’s `rendered_stems.Drums` entry provides binding context, not component identity or acoustic ground truth. Do not infer identity from names. AD-015/037/038/040/041 remain unchanged; htdemucs_6s is a separate operational source binding, not this input path.

Admission before any witness arithmetic: independently hash all manifest repository/external entries, verify accepted input/implementation authority manifests transitively as bound, and verify root links to index/catalogues. No accepted validators or preservation scripts are rerun. Parse only allowlisted observation/catalogue fields; reject duplicate JSON keys, nonfinite values, invalid rationals, inconsistent scope/source, missing identities, broken parent links or divergent input/catalogue events. Validate content-addressed catalogue IDs using the accepted canonical encoding. The full numeric shards are neither needed nor read: index authentication is provenance, not a claim to have freshly checked every response shard. Absolute path relocation requires an operational alias binding to identical bytes and PI review; never silently substitute run_2 or another dataset.

Original canonical report, audio, accompaniment, declared references, score/DAW tempo, human tapping, beat/meter annotations and external trackers cannot supply discovery or checker decisions. Canonical report and historical source files may be hashed as authority but no semantic fields are loaded into the analysis. The numerical input freeze supplies the already admitted field pointers/producer values. Historical C1-07/C1-10 are governance limits, not expected labels. No future Drum-component or pending Double-Bass work is required.

## 3. Numerical temporal authority

Canonical temporal unit: seconds. Each producer binary64 timestamp is preserved as its exact dyadic rational n/d, d>0, gcd(|n|,d)=1, serialized as two decimal integer strings. Preserve original JSON token, 64-bit hex payload, float.hex representation, EME and observation field pointers, diagnostic frame/sample fields and measurement limitations by immutable event reference. They must remain consistent with the accepted freeze. Do not use decimal-token arithmetic, re-round to a sample/frame grid, subtract binary64 floats, impose epsilon or substitute physical-time accuracy for numerical exactness. Signed zero in the input metadata remains preserved; relation zero is canonical [0,1].

For unordered different-ID pair {a,b}, compute exact T=|n_b/d_b−n_a/d_a| with integer/rational arithmetic. Positive T is the relation domain inherited from the complete-map period catalogue. A distinct-ID zero-separation pair is COINCIDENT_DISTINCT_EVENTS, preserved separately and never treated as positive-period recurrence. Self-pairs are forbidden. The frozen population has 63 distinct centers; an unexpected coincident pair inconsistent with that authority is an admission mismatch, not a new population to accept.

Native strengths and frame diagnostics remain preserved through event references; they are not eligibility weights, loudness, accents, equality criteria or score inputs. No complex coefficient, phase, magnitude, approximate distance or threshold is used. This experiment computes exact witness relations, **not periodicity responses**, and never invokes the accepted Fourier evaluator.

## 4. Witness identity, distinctness and source conditioning

Canonical event identity is (input-freeze hash, source-authority ID, source-instance key, source UUID, EME UUID), with its unique parent PulseCandidate link. A witness ID is the structured tuple

["EXACT_PAIR_V1", input_freeze_sha256, source_uuid, min_lex(EME_a,EME_b), max_lex(EME_a,EME_b)].

Lexical order is serialization only; record chronological endpoint order separately. Deduplicate by this whole pair identity, not timestamp, duration, catalogue row, window, center or query. Relation ID is ["EXACT_RELATION_V1", input_freeze_sha256, source_uuid, [n,d]]. Original catalogue IDs are retained as lineage, not substituted for pair IDs.

**Distinct witness** means a different unordered EME pair in the same admitted population. It is not automatically statistically independent or a different physical strike pair. Distinct EME are observation-supported events; no additional physical-event consolidation is authorized. Classify pair-to-pair reuse by exact endpoint intersection:

- SAME_PAIR: both EME IDs match; one witness even if represented repeatedly or reversed.
- SHARED_ENDPOINT: different pairs share one EME; distinct witnesses with dependent support explicitly visible.
- EVENT_DISJOINT: no common EME; separate observation support, without independence of detection errors, physical source, session or time process.

Record each pair’s closed interval [earlier timestamp,later timestamp], temporal overlap/touch/disjointness with other same-T witnesses, and endpoint identity intersections. Equal spans do not merge distinct identities; distinct spans do not manufacture event independence. Separate representation reuse (same pair in multiple windows/catalogues) from different relations sharing an event or endpoint pair. A pair must belong to exactly one positive T; conflicting relation assignments are contract failure.

Shared source means common authority/measurement population, not same Ride/Hi-Hat/Snare/Kick or musical function. Event-disjointness is descriptive, not an extra recurrence eligibility filter. H_exists concerns distinct pairs, including shared-endpoint pairs; reports must never summarize them as independently replicated physical evidence.

## 5. Catalogue construction and coordinate-repetition prohibition

Generator uses only authenticated existing period catalogue entries and references to frozen events. Validate every listed witness against exact input time, then retain its canonical ID once. Any duplicate within the supposedly unique authoritative catalogue is reported as a contract mismatch, not silently corrected to claim success. Repeated references across windows are expected reuse and counted only in the reuse ledger. All 1,953 pairs and all 1,056 positive relation entries must be accounted for, including singleton and missing/unresolved cases; no “best window,” selected center or extra pairs from another source.

For each T, n(T) is the cardinality of its canonical distinct witness set. A repeated relation has n(T)≥2. No count of centers, scales, queries, rows or repeated appearance of T contributes to n(T). The accepted policy queries every T at every admitted (u,L); coordinate repetition is therefore specifically inadmissible as a witness.

Window incidence is a secondary exact audit. For each accepted window preserve original center IDs/u/L, membership sets, requested/available support and clipping. For each pair record endpoint membership masks in contained, positive and boundary sets; both-positive marks positive-support containment, not nonzero Fourier strength. Preserve cases with one/no endpoint in a window and period generation outside evaluation support. Efficient factorization is allowed: immutable membership sets plus complete endpoint pairs define all masks, and materialized both-contained/both-positive pair-ID lists expose positive incidence; zero/one-endpoint masks need not be redundantly expanded. Derivation formula and endpoint references are mandatory, so omitted expansion is not lost evidence. Incidence lists deduplicate pair IDs per window but never change primary witness counts.

All windows are retained; no similar-L interpolation or local-region binning. For temporal distribution, preserve ordered witness intervals, exact endpoint sets, first/last support and exact gaps between chronologically ordered witness start times; retain ties and shared events. “Separated” means disjoint closed intervals (strict end<start), not an invented large-gap threshold or an independence claim. Wider occurrence coverage does not select a candidate.

## 6. Prospective output schema and future usability

All files below are prospective outputs, not created now. Use factorization rather than copying event or response payloads repeatedly.

| Output | Required content |
|---|---|
| `events.json` | Complete 63-event allowlisted identity/time/source/parent/strength/provenance record with exact numerical authority, scope and canonical-report field references; no metric labels |
| `relations.jsonl` | Every T, relation ID, canonical exact seconds, source/input authority, all witness IDs and original catalogue references, n(T), status SINGLETON/REPEATED/UNRESOLVED, temporal extent and missingness; complete singleton retention |
| `witnesses.jsonl` | Each canonical pair exactly once; EME/PulseCandidate identities, chronological endpoints, exact separation, source/asset/measurement authority, original representation references and support interval |
| `witness_relations.jsonl` | Every unordered pair of distinct witnesses within the same T, shared-endpoint/event-disjoint classification, exact endpoint intersection and support overlap/touch/disjointness; no similarity score |
| `windows.jsonl` | All 3,864 accepted window IDs/geometry/memberships/clipping plus factorized incidence and distinct both-contained/both-positive witness lists, including empty lists; shared evidence is explicit |
| `reuse_audit.json` | Unique pair counts, original catalogue occurrences, reversed/duplicate violations, window-incidence reuse, conservation checks; coordinate-query multiplicity explicitly excluded |
| `relation_ratios.jsonl` | Every unordered pair of established repeated T values in increasing exact T order; reduced exact positive ratio T_b/T_a and relation IDs. Integer/doubling may be typed arithmetic facts; no root, rank, grouping or metric hierarchy |
| `candidate_population.json` | Exact object defined below, complete and unranked; nonqualifying records stay in full catalogue |
| `result.json` | Scientific outcome, population classification, exact counts, contract status, missingness, scope/limitations and input/output hashes; no generic scientific PASS |
| `checker.json`, `replay.json`, `root.json` | Independent assertion totals and discrepancies, replay equality, file/hash/content bindings and logical fingerprints; operational path/time/memory logs stored separately |

All relations remain preserved, including exact values not exported as repeated candidates. Full catalogue n/d values permit any later exact ratio to be derived without re-running witness discovery; explicit ratios among repeated members meet the immediate future-preservation need. Rational connectivity is not hierarchy because every rational T has a rational ratio to every other T. No approximate clustering or low-denominator filtering.

**ADMISSIBLE_RECURRENT_TEMPORAL_CANDIDATE_POPULATION** contains: experiment/preregistration/manifest/implementation/checker/replay authorities; source-instance/asset/measurement scope; all and only independently checker-established T with n(T)≥2; relation IDs and exact seconds; witness count and all witness references; chronological witness locations; shared-endpoint/dependency references; complete event/parent/source lineage; window incidence/coverage references; uncertainty/missingness; exact ratio references; and scientific status RECURRENCE_SUFFICIENCY_NOT_ESTABLISHED with beat_reference_authorized=false and bpm_authorized=false. Membership has no priority. Ascending T is canonical serialization, never ranking. No beat/tempo score or “preferred” field exists.

**Hash/admission dependency order:** generator files contain proposed membership and outcome, marked PENDING_INDEPENDENT_ACCEPTANCE; checker/replay authority fields reference this protocol and the frozen implementation binding, not future report hashes. After generator freeze, the checker verifies those files and writes a report referencing their hashes. Each run root then binds generator files plus checker report. The final external `replay.json` binds both run roots and grants or withholds admissibility; it is not part of either hashed run root. Consumers must require its complete acceptance before treating proposed members as the ADMISSIBLE_RECURRENT_TEMPORAL_CANDIDATE_POPULATION. No generator file changes after output freeze. `result.json` references only input and generator-data hashes, excluding itself, checker, root and replay; checker references exclude its own/root/replay hashes. This acyclic dependency prevents self-referential hashes and avoids treating unverified output as established evidence.

If complete checking establishes no repeated relation, preserve an empty candidate population with status EMPTY_NO_EXACT_RECURRENCE. If admission, checking, replay or completeness fails, candidate export is **WITHHELD_INCOMPLETE_AUTHORITY**, not an empty negative population or a partial admissible set. Preserve partial catalogues as non-admissible evidence. Future authorized component identities can join on preserved EME/PulseCandidate/source authority; no component identity is inferred now.

## 7. Outcomes and maximum claims

Scientific outcomes are separate from integrity/execution status.

| Outcome | Preregistered condition | Maximum claim |
|---|---|---|
| EXACT_RELATION_RECURRENCE_OBSERVED | Complete admitted population, exact checker agreement and replay, at least one T with two distinct pairs | Repeated exact observed temporal relations exist and are recoverable in this frozen source/measurement population; complete repeated population admissible as neutral future research input |
| NO_EXACT_RELATION_RECURRENCE_OBSERVED | Same complete checks, no T with two distinct pairs | No repeated positive exact temporal separation under this numerical/identity contract; approximate/physical recurrence remains unknown |
| INSUFFICIENT_EVIDENCE | Required input/evidence missing, incomplete run/storage or unavailable complete output prevents full evaluation | Bounded hypothesis not decided; no admissible candidate population exported |
| INDETERMINATE | Conflicting identity/time authority, unresolved checker/replay disagreement or an unresolvable relation binding | No trustworthy final decision; preserve conflicting evidence; no candidate export |

Population classification after complete checking: NO_REPEATED_EXACT_RELATIONS if zero repeated T; ONE_REPEATED_EXACT_RELATION if one; MULTIPLE_REPEATED_EXACT_RELATIONS if more. Otherwise AMBIGUOUS_OR_UNRESOLVED_RELATIONS with cause. Exact rational equality is never itself ambiguous for admitted finite inputs; ambiguity indicates authority/execution defects, not a license for tolerance.

Integrity vocabulary: ADMITTED / STOP_PREFLIGHT / CONTRACT_VALID / FAIL_CONTRACT / STOP_INCOMPLETE / CHECKER_DISAGREEMENT / REPLAY_MISMATCH. A claimed false witness is FAIL_CONTRACT, not evidence that physical recurrence is absent. Missing files stop before computation and are not scientific negatives. There is no generic PASS that can be confused with recurrence sufficiency. Preserve all failures, singleton classes and unresolved references; no repair/rerun without PI review.

## 8. Independent checker and controls

Independence here is **independent computational derivation and review**, not an independent performance dataset, detector or statistical sample. Both programs necessarily share the frozen scientific definition; independence concerns implementation failure modes and input verification. Actual checker implementation must be separately reviewed before execution; author/reviewer identities and shared dependencies are declared.

Generator may decode the accepted exact rational timestamp fields and traverse the period catalogue. Checker must not import the generator’s relation, decoder, pair-ID, deduplication, membership or outcome routines. It independently decodes original producer binary64 bit strings using sign/exponent/significand integer arithmetic, including subnormal/zero handling; verifies ratio/hex/token roundtrip against the accepted freeze; and computes absolute differences using integer cross-products and gcd reduction. No float subtraction or original-token-as-exact-decimal arithmetic. Standard cryptographic/JSON libraries may be shared and disclosed; a common scientific helper cannot substitute for independent checking.

Checker independently enumerates all unordered distinct EME-ID pairs from the 63 frozen events, rather than trusting the generator’s period groups. It compares the complete resulting relation→pair incidence to both the authenticated accepted catalogue and proposed output. This is exact witness verification during future execution, not rerunning the accepted Fourier map. It independently reconstructs each claimed pair identity/parent/source, zero exclusion, membership mask and window support using exact endpoints; verifies all requested/catalogued windows and same-pair reuse. For window completeness, independently compare exact center/boundary geometry to the frozen input authority without running the accepted constructor. It checks all 1,953 pairs, 1,056 relations and 3,864 windows, every candidate membership, every repeated-relation ratio, retained singleton/missingness and canonical output ordering. Never use expected number of repeated relations as a fixture answer.

Prospective adversarial fixtures, defined/checked independently before real-input execution: reversed duplicate pair; same pair referenced in several windows; shared-endpoint versus disjoint witnesses; different parent/source; same T but different pair; near-but-not-equal exact dyadics; distinct-ID coincidence; boundary-only window membership; missing catalogue pair; incorrect ratio/count; nonfinite timestamp; altered authority byte. Expected outcomes follow these contracts, not the real-map output. Same-pair duplication must not create recurrence; near equality must remain different; physical/statistical independence must never be inferred from disjoint IDs. Opaque-ID renaming and input-order permutation preserve relations after inverse renaming; source/parent links must transform coherently. No statistical null/chance claim is made, so no arbitrary stochastic null is introduced.

The independent checker does not supply or inspect musical Ground Truth. Freeze generator outputs before checker scoring and preserve their hashes. Checker disagreement stops; do not tune either implementation until agreement on the real data. A later fix requires a new reviewed binding and PI rerun decision, retaining failed output.

## 9. Deterministic replay and execution binding

Before execution create an experiment-local, reviewed implementation binding containing generator/checker/orchestrator/test sources and all transitive dependencies, exact runtime/build/executable/library versions and hashes, canonical serializer rules and resource/storage plan. Bind this preregistration and its input manifest. The existing CPython 3.13.14 / python-flint 0.9.0 / FLINT 3.6.0 authority explains accepted numeric data; this audit requires only exact integers/rationals and must not load the Fourier operator. A new runtime must be explicitly frozen rather than assumed to be the prior map environment. No future source hash is fabricated in this design.

One complete generator execution, independent checker, then one fresh-process replay with identical bound inputs/software and empty process state. Checker runs on both outputs. No accepted map run is modified, overwritten, rerun or used as output destination. Proposed external root: `/Volumes/SSD Track/JGA/experiments/H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01/`, new `run_1/` and `run_2/`; directories are not created now. Stream window/incidence and ratio records with bounded buffers. Implementation review must bind conservative capacity from schema bounds and available disk, not change the scientific population to fit resources. No arbitrary runtime/resource limit can become scientific failure or success.

Canonical scientific serialization: sorted JSON object keys, compact ASCII-safe UTF-8, no NaN, binary floats, wall clocks or absolute paths; integer quantities as canonical decimal strings; rationals reduced with positive denominator. Structured IDs are arrays. Events sort by exact time then EME ID; relations/candidates by exact increasing T; witnesses by relation then lexical pair; witness-relations by relation then pair IDs; windows by exact u,L; incidence lists by canonical witness identity; ratios by exact T_a,T_b. JSONL has one record plus LF per line; JSON files also end LF. Logical fingerprint is SHA-256 over each named canonical stream in a fixed root-declared filename order, with stream names/lengths delimited, or equivalently a canonical map of stream hashes/byte counts; choose **the latter** for this protocol. Root binds schema, authorities, all stream hashes/counts, scientific outcome and unchanged boundary status.

Semantics must match exactly (identities, supports, membership, outcome). Numeric equality is exact integer/rational equality, with input bit provenance unchanged. All canonical output files, results and checker scoring must be byte-identical between runs; no float tolerances or percentages. Paths, clocks, runtime, memory and process IDs belong only to separate operational logs. `replay.json` is a single final comparison artifact binding both runs’ canonical roots/checksums, not required to equal a per-run file. Independent replay comparator checks every canonical output byte/hash and records all mismatches. Incomplete replay withholds candidate admissibility.

## 10. Negative results, limits and stops

Do not loosen equality, change source or EME identity, switch to frame differences, add events/audio, retune detection, rank responses or regenerate periods after a negative result. Preserve the empty repeated population and singleton catalogue. Negative exact results do not reject approximate or physical recurrence. All metric interpretation, significance and hierarchy remain forbidden even if many relations recur.

STOP_PREFLIGHT: any authority/hash/source/scope/input-count conflict, missing accepted catalogue, unreviewed/missing implementation binding, unapproved runtime, unavailable external storage, existing output directory or missing PI execution authorization. Stop without recurrence computation. Preserve discrepancy; do not repair accepted authority.

FAIL_CONTRACT / CHECKER_DISAGREEMENT: identity collision, missing/extra/repeated pair asserted as independent, wrong exact separation, incorrect membership, unsupported candidate, omitted singleton/alternative, leaked musical inputs or disagreement. Stop and retain output. REPLAY_MISMATCH withholds acceptance; no automatic patch-and-rerun. STOP_INCOMPLETE for interruption/capacity/I/O preserves partial files and cannot be mistaken for NO_EXACT_RELATION_RECURRENCE_OBSERVED.

Future BeatReference work may inspect all established neutral candidates only after this experiment is independently checked and replayed, under separate PI authorization. It must allow one, several, none or unresolved interpretations. RECURRENCE != BEATREFERENCE; BEATREFERENCE != BPM. Future component labels require independent join authority. Double-Bass capture availability is irrelevant to this audit.

## 11. Readiness and next authorization

This preregistration and minimal frozen-input manifest complete the scientific/input/checker **design**. No unresolved equality/source/witness definition is deferred to implementation. However, executable generator/checker code, independent review, exact runtime/source hashes, resource plan and replay binding do not yet exist for this experiment. They cannot truthfully be described as validated or execution-ready.

**Exact next action requiring PI authorization:** implement and independently review the generator/checker and their adversarial integrity checks under this preregistration, and freeze the implementation/environment/resource binding, **without real-input execution**. Then return for a separate PI execution decision. No preregistration or input amendment is required merely to bind conforming implementation; any scientific-rule change requires PI review before execution.

Only this preregistration and one authority manifest are created now. Hash-only input checks and document consistency checks are allowed; no relation counts, candidate membership, window incidence or ratios are computed on the real population in this task. Accepted map and Double-Bass files remain unchanged. No commit or push.

PREREGISTRATION COMPLETE:
YES

FROZEN INPUT AUTHORITY COMPLETE:
YES

INDEPENDENT CHECKER DESIGN COMPLETE:
YES

NEW AUDIO REQUIRED:
NO

PERIODICITY RECOMPUTATION REQUIRED:
NO

RECURRENCE SUFFICIENCY AUTHORIZED:
NO

BEATREFERENCE AUTHORIZED:
NO

BPM AUTHORIZED:
NO

READY FOR PI EXECUTION AUTHORIZATION:
NO
