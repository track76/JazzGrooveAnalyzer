# DRUM-EXACT-RELATION-WITNESS-AUDIT-01 — renewed V2 review

Date: 2026-09-10. Reviewed implementation: **replacement freeze V2**.
Disposition: **TECHNICAL SIGN-OFF FOR PI EXECUTION-AUTHORIZATION REVIEW**.
No new material defect found. This report does not authorize execution or establish
any real recurrence result.

Reviewer: **Codex `/root`, PI-authorized renewed code-review pass**. This is the same
assistant identity as the implementation author. Computational independence and a
separate critical review pass are assessed below; separately staffed human/agent or
organizational reviewer independence is not claimed.

## 1. Authority and history verification

Observed facts: all five PI-specified hashes match, as do all source/document/test
hashes in the replacement binding. Exact paths below are relative to
`validation/VAL-001/exact_relation_witness_audit_20260910/`.

| Artifact | SHA-256 |
|---|---|
| `runner.py` | `64c59d7564749af33f63a41ac89a50b1c69dcbe57b9aa919cb250d646e638778` |
| `test_witness_audit.py` | `2b1531f496776bcfd27ed9ab70889abb58eadf9b080585dc926e82b6e7154734` |
| `test_results.json` | `085c1cf0095489edaeb8f8da7f0bf1fa8d495eeb5d1f527667cddc365e0c5e69` |
| `implementation_binding_v2.json` | `418d6f71f855414a0aed06d02e6906ede42efba3bab1a7f2044fac3b4df29dfe` |
| `REPLACEMENT_FREEZE_REVIEW.md` | `66d19aacbf59f87cfcc7b39ab059dabda1d04b01a69975b0e0dce3405e2efc62` |
| `generator.py`, unchanged | `289f5e83671a0f6deb4426f012b58b78635a0d6e0d300bbfa62dd48962070eed` |
| `checker.py`, unchanged | `e9128cfd412a2f085de5a4ce582d048bcd4810e2dcffd873e5cd51f119fb9b30` |

The canonical environment-object fingerprint remains
`13bd11b30796d461ef2cfd73053bb725e26bdd7a9c093226da0a21999911ca2c`.
All 629 bound runtime files and the 47-file upstream hash closure were rehashed and
matched. These were byte-integrity checks, not execution or numerical interpretation
of accepted observations. The review also authenticated `transport.py`, `fixtures.py`
and the bound handoff/README through the implementation manifest.

Protected preregistration:
`validation/VAL-001/preregistrations/H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01.md`,
SHA-256 `c609cfabdfd31f5122cd0883da861c2b742aa2af7a659cf691dbe0d56161e48a`.
Its `.authorities.json` SHA-256 remains
`477cd53b11778091907058ad6157bd0a881b85240d8fd13fa5e9dc3ef676e059`.

V1 `implementation_binding.json` retains hash
`c303a6a13874573b811b4be6317c97889d321890301f9936007688146c042a33`.
Every V1 bound artifact was verified using the three original files in `history/v1/`
and the other unchanged files at their original paths. V2 explicitly identifies V1
as INVALIDATED/SUPERSEDED and references the original defect report. V1 is preserved
history, not an executable authority. This review does not rewrite either binding.

## 2. Scientific conformance assessment

The following are bounded logical review conclusions from actual code inspection and
synthetic checks, not claims about a real population. Both complete generator/checker
files, transport, runner, fixture construction and all test methods were inspected.

| Requirement | Code evidence and assessment |
|---|---|
| Exact timestamp reconstruction | `generator.decode` unpacks producer bits and uses `as_integer_ratio`; `checker.producer` reconstructs sign/exponent/significand with integer shifts, including subnormal and signed-zero cases. Both check ratio, hex and token round trip. Conforming. |
| Exact positive separation/equality | Generator uses exact `Fraction` subtraction; checker uses integer cross-products/gcd through its own `Number` class. No float subtraction, epsilon, proximity, rounding buckets or clustering establishes equality. Conforming. |
| Canonical witness identity | Generator `pair_id` and checker-local `identity` separately implement the input-freeze/source UUID plus lexically ordered EME pair. Chronology is retained separately. Conforming. |
| Complete input/lineage | Unique EME and parent identities, source/asset/scope agreement, EME/observation timestamp agreement and input-catalogue consistency are checked. The real runner binds hashes before numerical admission. Preserved field pointers/strength/frame diagnostics remain provenance. |
| Deduplication and conservation | Generator rejects repeated authoritative pairs and checks the full unordered-pair set. Checker independently enumerates pairs and compares complete group membership to the catalogue. Same-pair reversed representation cannot add support. Missing/extra witnesses stop acceptance. |
| Window/center reuse | Primary witness counts come only from pair identities. Windows preserve separate membership/incidence; both programs check exact center/boundary geometry and complete window population. Coordinate reuse never contributes another witness. |
| Shared endpoints | Separate within-relation witness-pair records retain endpoint intersections and overlap/touch/disjointness. Distinct pairs sharing an endpoint remain eligible but explicitly dependent; event disjointness does not assert statistical independence. |
| Complete relations and candidates | All positive relations, including singletons, survive. Repeated membership is precisely at least two distinct witnesses. The checker independently derives and verifies the entire candidate population. No top-k or selective suppression occurs. |
| Ratios and multiple relations | All unordered pairs of repeated exact separations receive reduced exact ratios. Increasing exact-time order is serialization only; no preferred relation, metric hierarchy or beat/tempo score exists. |
| Numerical uncertainty and missingness | Exact numerical agreement is not physical-time accuracy. Physical timing/independence remain NOT_ESTABLISHED. Coincident distinct events are excluded from positive recurrence and retained separately; real distinct-center authority is not relaxed by synthetic coincidence fixtures. |
| Deterministic serialization | Shared `transport.canonical` emits sorted compact ASCII-safe JSON, integer strings and no binary floating output. JSON/JSONL writers terminate with LF. Both programs preserve prescribed ordering. Checker compares complete expected records byte for byte. |
| Outcomes and acceptance | Generator output is proposed/PENDING_INDEPENDENT_ACCEPTANCE. Checker and replay are subsequent gates. Frozen scientific outcome vocabulary is preserved; missing/conflicting evidence cannot become a negative recurrence observation. No recurrence-sufficiency claim is introduced. |
| Source/semantic firewall | No component identity, musical role, beat, tempo, BPM or response score drives eligibility. No audio/Fourier/tempo estimator is imported. Strength is retained without weighting relation selection. |
| Input-execution firewall | Real CLI requires PI authorization, review binding, implementation/environment/source/input hashes and the authorized output location. Synthetic CLI requires a synthetic tag/source, bounded fixture size and excludes the real UUID. No default call executes real evidence. |

Input/API guards are operational safeguards under the documented workflow, not a security
boundary against someone manually forging in-memory admission dictionaries or editing
Python. No such stronger adversarial guarantee is required for this review.

## 3. Replay correction and custody assessment

Inspected `runner.py:155–222` and the parent issuance path at `runner.py:261–306`.

1. `compare_replay` resolves both paths and rejects `samefile` before acceptance.
2. Each operand must contain a receipt matched exactly to an entry in the explicitly
   selected custody ledger. The receipt cannot choose its own trusted authority path.
3. Ledger location and the run's resolved path/device/inode must match. Copying or
   relabelling output therefore does not create another execution authority.
4. Each receipt requires completed generator/checker roles, zero exits and two distinct
   launch IDs. The issuing parent actually launches and waits for fresh subprocesses
   before exclusively creating the ledger/receipt records.
5. Across runs, execution IDs must differ and launch-ID sets must be disjoint. PIDs
   and random labels alone are not treated as proof: the issuer/custody chain supplies
   their execution meaning.
6. Input/software/runtime binding and scientific authority must agree; current output
   hashes must match each receipt. Only then are canonical scientific bytes, checker
   reports and roots compared.
7. Operational receipts stay outside identical scientific streams. The one final replay
   artifact binds both receipt digests and both canonical runs without a hash cycle.

Assessment: the original self-comparison defect is corrected. Distinctness is not reduced
to textual path inequality. Missing or contradictory execution evidence rejects without
granting admissibility. A byte mismatch that reaches final comparison yields the frozen
REPLAY_MISMATCH/INDETERMINATE/withheld outcome. Earlier admission failures raise and grant
no admissibility; the operator must retain their stderr/invocation records.

**Trust limit accepted for this bounded review:** receipts are issued by the authorized
orchestrator and preserved under trusted custody. A malicious custodian able to fabricate
the entire ledger, outputs and software is outside this contract. The preregistration
requires auditability and fresh execution, not hostile-host attestation or independent
cryptographic hardware. No stronger threat model is imposed here. Actual custody must
remain as documented; the code's ability to read a JSON file is not proof that an arbitrary
user-authored ledger has trustworthy provenance.

## 4. Test audit and reruns

Command rerun without source changes:

```sh
python3 -B -m unittest discover -s validation/VAL-001/exact_relation_witness_audit_20260910 -p 'test_*.py' -v
```

Observed result: **30 tests passed, zero failures/errors**, reported runtime 2.849 s.
All populations were literal/seeded synthetic fixtures. No real input was used. The
existing `test_results.json` was not overwritten by this review.

### Original 21 tests

| Test or group | Audited coverage |
|---|---|
| A | No recurrence; repeated query/window coordinates do not change singleton support. |
| B | One repeated positive separation with disjoint supporting pairs among four witnesses; coincident distinct synthetic events separately retained. Does not falsely claim exactly two total witnesses. |
| C | Shared endpoint, touching support and explicit absence of statistical-independence authority. |
| DE | One pair occurs in multiple windows and centers with conserved unique witness count. |
| FG | Multiple exact recurring relations and neutral ratios, including unavoidable cross-pair alternatives. |
| H | One-ULP change prevents merging numerically close separations. |
| I | Reversed catalogue ordering preserves canonical unordered IDs. |
| J | Duplicated authoritative pair rejected by both programs. |
| K | Wrong source/parent, missing period, invalid content ID, nonfinite bits and unreduced ratio rejected. |
| L | Two fresh subprocess runs, independent checking, byte-identical canonical files and eligible replay; operational receipt correctly excluded. |
| boundary_and_window_coverage_tampering | Corrupt membership rejected even with recomputed content ID. |
| checker_detects_every_output_file_tampering | Extra newline rejected in every scientific generator file; this is a byte-corruption test, not exhaustive semantic mutation coverage. |
| preflight_and_failure_vocabularies | Missing authorization stops before scientific input; failure vocabulary/withholding and real-source synthetic guards checked. |
| replay_mismatch_withholds_admissibility | Different fixture inputs rejected at authority agreement; does not claim they test identical-input nondeterminism. |
| duplicate_catalogue_and_window_records_rejected | Extra period/window record rejected by both programs. |
| no_semantic_fields_admitted | Extra event musical-role field rejected. |
| authority_bytes_and_serialization | Known SHA-256 vector, altered bytes, duplicate JSON keys, nonfinite JSON and binary-float output rejection. |
| opaque_identity_renaming | Nonsemantic coherent ID renaming preserves separation/count evidence. |
| exact_decoder_properties | Edge encodings plus 200 seeded bit patterns; generator/checker agree with supplied exact ratios. |
| seeded_small_population_properties | Sixteen small populations with independently calculated integer-gap count expectations. |
| input_order_permutation | Reordered events/catalogue preserve canonical output under the explicitly synthetic identity fixture. |

### Nine added regression tests

| Test | What it actually establishes |
|---|---|
| SAME_PATH_SELF_COMPARISON | Same directory rejected. |
| RESOLVED_PATH_ALIAS_SELF_COMPARISON | Symlink alias to that directory rejected. |
| SAME_EXECUTION_ID_DIFFERENT_PATH | Copied run rejected by filesystem/custody identity; need not reach the later ID-equality branch to reject the invalid case. |
| ONE_EXECUTION_ONLY | Missing second directory yields no replay acceptance artifact. |
| TWO_DISTINCT_EXECUTIONS_IDENTICAL_OUTPUT | Separate orchestrated executions with matching authority and output qualify. |
| TWO_DISTINCT_EXECUTIONS_DIFFERENT_OUTPUT | Post-execution stream corruption is rejected by its receipt hash. It does not induce genuine nondeterministic generator behavior. |
| TAMPERED_RUN_IDENTITY | Modified local worker identity conflicts with ledger authority and is rejected. |
| COPIED_RUN_PRESENTED_AS_FRESH_EXECUTION | Local relabelling/path/inode changes without an issued ledger entry are rejected. |
| missing_execution_authority | Missing run receipt is rejected; by itself this is not a missing-ledger test. |

The naming/coverage limits above are recorded precisely, not treated as new scientific
defects. Code inspection covers final byte-mismatch logic; additional probes below
exercise execution predicates not isolated by the frozen tests.

### Five additional review-only synthetic probes

Two new synthetic runs were created from `fixture([0,1,2,3])` by the normal CLI and
fresh worker path in a temporary directory. For the first four probes, the second run's
receipt and its temporary test-ledger counterpart were mutated together to reach inner
validation predicates; originals were restored after each probe. This is deliberate
invalid-fixture injection, not a claim that the trusted ledger is hostile-proof.

| Mutation | Observed rejection |
|---|---|
| Reuse first run's generator launch ID in second run | `worker execution reused` |
| Set second run checker exit code to `1` | `worker completion` |
| Remove checker worker from second receipt | `worker roles` |
| Set receipt status to `STARTED` | `incomplete execution` |
| Select empty custody directory despite valid run receipts | Missing ledger entry (`FileNotFoundError`) |

**All five probes passed their rejection expectations.** Their temporary artifacts were
removed by the temporary-directory context. No frozen test, receipt, source or scientific
authority was changed. These five probes are additional to, not part of, the 30-test suite.

## 5. Computational and reviewer independence

Computational checker independence is **acceptable for the preregistered bounded audit**:
the checker neither imports generator scientific helpers nor takes generator groups as
its source of truth. It derives times/pairs/groups/windows separately, then verifies the
full proposed files, not merely reported counts.

Shared CPython integer/runtime behavior, `math.gcd`, token/hex conversion, JSON parsing,
SHA-256 and canonical byte transport remain common primitives. The runtime/files are bound;
known-byte and malformed-input tests plus source inspection address their shared failure
modes. Shared orchestration/admission is scientifically consequential and was reviewed
directly; independent mathematical traversal alone would not validate it. No known new
material common-mode defect was found under the declared custody conditions.

Reviewer identity is **Codex `/root`**, the same assistant as author. This renewed pass
inspected code independently of the author's prose and used new adversarial probes,
but it does not create organizational/personnel independence.

Governance inspected: `AGENTS.md`, `docs/JGA_DEVELOPMENT_CONSTITUTION.md`,
`docs/scientific/JGA_SCIENTIFIC_RESEARCH_CONSTITUTION.md`,
`docs/scientific/JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md`,
`docs/scientific/JGA_SCIENTIFIC_MANIFESTO.md`,
`docs/scientific/foundations/JGA_KNOWLEDGE_MODEL.md`,
`docs/scientific/foundations/F-030_SCIENTIFIC_KNOWLEDGE_RECORD.md`, and preregistration §8.
Section 8 defines independent computational derivation/review and requires a separate
review pass with author/reviewer identities declared. It does not explicitly require
a separately staffed human reviewer. The Knowledge Model reserves scientific/architectural
decisions to human approval; it does not require all technical reviewers to be human.

Accordingly **the disclosed reviewer limitation is not an automatic blocker under the
inspected governance**, especially given the PI's express direction not to invent one.
This is a bounded technical review conclusion for PI acceptance, not a grant of PI authority
to the assistant. The PI retains the decision to accept the review or request another reviewer.

## 6. Residual risks, sign-off and next PI action

No new material implementation defect was found. No test suite proves the absence of
all defects. Shared-runtime failure modes and trusted-custody assumptions remain explicit;
physical timing, source-component identity, significance, recurrence sufficiency and metric
meaning remain outside the successful claim. The real input has not been exercised, so
this is not a claim of observed real-data conformance or an expected recurrence outcome.

The replacement freeze faithfully implements the reviewed preregistered hypothesis and
replay contract to the extent established by source review and synthetic qualification.
**V2 is valid for consideration of later PI real-input execution authorization.** This
report is the later review record; the immutable binding's earlier CANDIDATE_FOR_REVIEW
and pending-review fields remain historical and are not silently edited.

Exact next PI action: accept this bounded review and separately authorize the frozen V2
real-input generator, independent checker and one fresh-process replay. That authorization
must bind V2's SHA-256 and the explicitly selected custody ledger. The operational loader
also requires a JSON review record (`runner.py:68–74`) carrying the V2 hash, review-complete
flag, accurately disclosed reviewer identity and scope. It should reference this Markdown
report and its final hash; the Markdown file itself must not be passed to the JSON loader.
Preparing that minimal operational record can accompany the next authorization without
changing scientific definitions or claiming a new review. No execution authorization or
additional JSON record is created in this review-only task.

Maximum later successful claim remains repeated exact observed temporal relations in the
frozen source/measurement population and its complete neutral candidate set. RECURRENCE
SUFFICIENCY remains NOT ESTABLISHED. BeatReference and BPM remain unauthorized.

Only this review report is added. No code, tests, manifests, prior review, accepted map or
Double-Bass work is changed. No commit or push. Stop for PI review.

RENEWED INDEPENDENT CODE REVIEW COMPLETE:
YES

MATERIAL DEFECT FOUND:
NO

REPLACEMENT FREEZE VALID:
YES

REPLAY INDEPENDENCE ENFORCED:
YES

CHECKER INDEPENDENCE ACCEPTABLE:
YES

REVIEWER INDEPENDENCE LIMITATION:
PRESENT

REVIEWER LIMITATION BLOCKS EXECUTION:
NO

REAL SCIENTIFIC INPUT EXECUTED:
NO

RECURRENCE RESULT KNOWN:
NO

READY FOR PI REAL-INPUT EXECUTION AUTHORIZATION:
YES

BEATREFERENCE AUTHORIZED:
NO

BPM AUTHORIZED:
NO
