# Replay correction — replacement freeze and renewed review handoff

Date: 2026-09-10. Status: **CANDIDATE FOR REVIEW; NO REAL EXECUTION**.

## Authority and preservation

The PI accepted M01 in `INDEPENDENT_CODE_REVIEW.md`, SHA-256
`f3703b2127dd16b0aff07b9322622825260af18793f9ed68ba42b838c1b669c3`.
The old `implementation_binding.json`, SHA-256
`c303a6a13874573b811b4be6317c97889d321890301f9936007688146c042a33`,
is **INVALID FOR EXECUTION / SUPERSEDED** by `implementation_binding_v2.json`.
The old binding and original review remain unchanged. Original runner, test suite
and test-results bytes are preserved in `history/v1/`; all other files referenced
by the old binding remain at their original locations. Together these retain the
complete old freeze, including its known defect. Do not interpret the old binding's
historical status or README instructions as current release permission.

Only `runner.py`, `test_witness_audit.py`, and `test_results.json` are changed.
This report, the replacement binding, and the three historical copies are added.
Generator, checker, transport, fixtures, preregistration, input manifest and accepted
scientific evidence remain unchanged. No temporal arithmetic, witness semantics,
outcome vocabulary, recurrence eligibility or musical interpretation changed.

## Correction and exact execution-identity rule

`compare_replay` now requires an explicit `authority_directory` selected by the
custodian. It rejects operands that resolve to the same filesystem directory using
resolved paths and `samefile`, before comparing scientific bytes.

The orchestrator issues an `execution.json` receipt only after it launches and waits
for a fresh generator subprocess and a fresh checker subprocess, both exiting zero.
The generator requires a new destination; the checker creates its report/root.
The parent records each observed launch and completion. An execution ID and two launch
IDs come from OS random bytes; PIDs are diagnostic, not the sole identity. No timestamp
is used to assert execution independence. Direct worker/API calls without the parent
receipt cannot qualify as replay, even if their scientific output is otherwise valid.

The parent exclusively creates the matching receipt in the external custody ledger.
It binds:

- execution identity, distinct worker launch identities, roles, PIDs and exit codes;
- the custody ledger's resolved location;
- run directory resolved path, device and inode;
- input/authorization bytes, runner/generator/checker/transport source hashes,
  runtime version and executable hash;
- scientific input, implementation and environment authority carried by the result;
- the complete canonical output-file hash/size map, including checker and run root.

The comparator independently loads the custodian-selected ledger entry, checks exact
agreement with the run receipt, directory identity, completed worker roles, current
output hashes and result authority. The two executions must have different execution
IDs and disjoint worker-launch IDs, but identical input/software/runtime binding and
scientific authority. Only then do the unchanged canonical byte/root/checker comparisons
determine replay eligibility. Incomplete, relabelled, copied or inconsistent evidence
does not grant admissibility. Missing evidence raises rejection without an acceptance
artifact; the caller must preserve the exception in its operational log.

For future real runs, the PI execution authorization must additionally bind
`execution_authority_directory`. The runner requires that exact selected ledger and
loads `implementation_binding_v2.json`; no authorization record is created now.
An operational invocation uses `--execution-authority LEDGER_DIRECTORY`. The comparator
uses `compare_replay(first, second, destination, authority_directory=LEDGER_DIRECTORY)`.
These instructions replace the v1 README's invocation instructions only.

## Custody and determinism limits

The ledger is trusted execution provenance, issued by the authorized orchestrator and
preserved by the custodian outside run directories. It is not a user-edited claim copied
from a run. A copied run cannot qualify merely by changing a path or local ID: the original
receipt binds another inode/path/ID and the ledger will not corroborate the alteration.
Selecting another copied ledger likewise fails its location binding unless records are
forged. Keep the ledger intact and restrict its writers to the authorized execution
workflow/custodian. Relocation or loss of the bound storage identity withholds acceptance;
no automatic relocation/repair is authorized by this correction.

This is an auditability contract under trusted custody, not cryptographic attestation
against a malicious custodian rewriting code, ledger and receipts together. No file-only
scheme can prove historical execution under that threat model. This limitation is
explicit; different timestamps, UUIDs or filenames alone never count as proof.

Operational `execution.json` receipts are deliberately different between runs and excluded
from scientific root/stream byte equality. They bind those roots in the opposite direction,
avoiding circular hashes. Final `replay.json`, already a single cross-run artifact under
preregistration, adds both receipt digests. Scientific schema/ordering/numerical equality
is unchanged. Random execution IDs never enter scientific measurements or rankings.

## Regression qualification

The full suite retains original A–L/numerical checks and adds these named cases:

| Case | Expected result |
|---|---|
| SAME_PATH_SELF_COMPARISON | Reject before admissibility |
| RESOLVED_PATH_ALIAS_SELF_COMPARISON | Reject symlink alias to the same directory |
| SAME_EXECUTION_ID_DIFFERENT_PATH | Reject copied execution at a different directory |
| ONE_EXECUTION_ONLY | Reject absent second execution; no acceptance artifact |
| TWO_DISTINCT_EXECUTIONS_IDENTICAL_OUTPUT | Accept eligible fresh synthetic runs |
| TWO_DISTINCT_EXECUTIONS_DIFFERENT_OUTPUT | Reject divergent/tampered evidence; no acceptance artifact |
| TAMPERED_RUN_IDENTITY | Reject receipt/ledger disagreement |
| COPIED_RUN_PRESENTED_AS_FRESH_EXECUTION | Reject relabelled copy without independently issued authority |
| missing_execution_authority | Reject missing receipt despite canonical output files |

The earlier fresh-process byte-equality test now excludes only the operational receipt,
and supplies the explicit ledger. The earlier differing-fixture replay test still rejects
incompatible evidence, now at input-authority admission. The differing-output regression
also alters one fresh run's stream and confirms that its execution hash binding withholds
admissibility. No real population or recurrence result is used as a fixture.

Exact final counts, results and current source hashes are recorded in `test_results.json`.
The replacement manifest binds those results and the full implementation. The inherited
environment fingerprint is unchanged:
`13bd11b30796d461ef2cfd73053bb725e26bdd7a9c093226da0a21999911ca2c`.

## Renewed review pass and remaining sign-off

Codex `/root` performed a separate implementation-level review pass: traced issuance
through successful child exits, checked that receipts cannot enter canonical scientific
comparison, reviewed fail-closed alias/copy handling and verified unchanged generator/
checker hashes. This supports a bounded author-review conclusion that M01 is corrected
under the explicit custody contract. It is not a new scientific result.

**Computational checker independence** remains as previously implemented: distinct
producer-bit arithmetic/traversal and no generator scientific-helper imports in checker.
Shared runner/transport remain a common audit boundary, now with added execution authority.
This correction does not certify all previously uncompleted scientific-conformance review.

**Reviewer independence:** the author and this review pass are the same assistant identity.
Preregistration §8 requires independent computational derivation and review and declaration
of author/reviewer identities. Its wording does not explicitly mandate a human reviewer;
nevertheless this session cannot claim separately staffed human/agent independence or
close the prior review limitation merely by assigning itself another role. A PI-accepted
renewed independent review remains necessary; no positive independent sign-off is issued.

The reviewer should inspect the v1/v2 runner diff, receipt-issuance trust boundary, custody
requirements, tests, input/environment bindings, and every original scientific conformance
criterion. A new defect requires preservation and PI review, not real-input experimentation.

Next PI action: review this candidate freeze and arrange/accept renewed independent review
with an accurately declared reviewer identity and independence scope. Only after that
review may the PI separately authorize real-input generation, checker and replay.

No real input, accepted map computation, Double-Bass work, BeatReference, BPM, commit or
push occurred. Replacement freeze is a candidate for review, not execution-ready.
