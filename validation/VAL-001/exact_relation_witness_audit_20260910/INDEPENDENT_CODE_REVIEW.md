# DRUM-EXACT-RELATION-WITNESS-AUDIT-01 — review finding and withheld sign-off

Date: 2026-09-10. Status: **STOP — MATERIAL IMPLEMENTATION DEFECT CONFIRMED**.
No real scientific input was executed or inspected for recurrence. No code was patched.

## Reviewer and scope

Reviewer identity: **Codex `/root`, PI-authorized code-review role in this session**.
This review inspected frozen source and constructed a new adversarial synthetic check,
rather than adopting the author's implementation report as evidence. The reviewer is
the same assistant identity that authored the implementation in the preceding turn;
this is not an independently staffed reviewer sign-off. No different reviewer identity
or organizational independence is claimed. In all cases sign-off is withheld because
of the concrete defect below, independently of that personnel limitation.

The bootstrap is a historical starting snapshot. Subsequent explicit PI authorizations
permit this implementation review; they do not change the accepted map's scientific
limits. The protected preregistration remains authoritative.

Review stopped at the first confirmed material defect under the PI's stop rule.
The complete twenty-item acceptance checklist and exhaustive A–L test audit are therefore
**not certified complete**. No later execution-readiness inference may be drawn from
the bounded observations in this report.

## Authority verification — observed facts

All five PI-specified artifact hashes match:

| File, relative to this package | SHA-256 |
|---|---|
| `generator.py` | `289f5e83671a0f6deb4426f012b58b78635a0d6e0d300bbfa62dd48962070eed` |
| `checker.py` | `e9128cfd412a2f085de5a4ce582d048bcd4810e2dcffd873e5cd51f119fb9b30` |
| `test_witness_audit.py` | `bd4185ddddb9c8e52647465fb234db80b1dcef42956016596b10ea2a7c92857b` |
| `test_results.json` | `24d42bebdd28af7d2884df242f375b6f6d05dd09c5ed413d7668d102528b041c` |
| `implementation_binding.json` | `c303a6a13874573b811b4be6317c97889d321890301f9936007688146c042a33` |

Every file listed in `implementation_binding.json` → `implementation_files` also
matches its bound hash, including runner, transport and fixtures. Recomputing the
canonical fingerprint of the bound environment object yields
`13bd11b30796d461ef2cfd73053bb725e26bdd7a9c093226da0a21999911ca2c`.
This fingerprint check does not claim a fresh rehash of every installed runtime file.

Protected preregistration:
`validation/VAL-001/preregistrations/H-VAL001-DRUM-EXACT-RELATION-WITNESS-AUDIT-01.md`,
SHA-256 `c609cfabdfd31f5122cd0883da861c2b742aa2af7a659cf691dbe0d56161e48a`.
Its `.authorities.json` SHA-256 remains
`477cd53b11778091907058ad6157bd0a881b85240d8fd13fa5e9dc3ef676e059`.

Source inspection covered `runner.py`, `transport.py`, generator admission/numerical/
identity/grouping paths, checker numerical/identity/all-pairs/catalogue paths, and the
test paths relevant to output corruption and replay. `test_results.json` and the
implementation manifest were authenticated; their prior PASS report is not treated
as a substitute for review. No accepted event, pair, window or response population
was loaded during this review.

## M01 — replay can accept one execution as two

**MATERIAL DEFECT FOUND: YES.**

Exact location: `validation/VAL-001/exact_relation_witness_audit_20260910/runner.py`,
`compare_replay`, lines **155–178**, with the resulting admissibility grant at
lines **179–186**, particularly **183**.

The function accepts two directory arguments without requiring them to designate
different execution artifacts. It compares their hashes and bytes, checks internally
consistent checker/root records, and sets `valid = not mismatches`. When both arguments
refer to the same completed run, every comparison succeeds by construction. It emits
`ADMISSIBLE_COMPLETE_POPULATION` even though the required replay never happened.

Preregistration §9 requires one complete generator execution and checker followed by
a fresh-process replay with checking on both outputs. It explicitly withholds candidate
admissibility when replay is incomplete. Preregistration §6 makes final replay acceptance
the gate between proposed and admissible candidates. Comparing a run to itself does
not supply that required evidence.

### Synthetic reproduction — observed fact

Only literal synthetic timestamps `[0, 1, 3]` were used. Exactly one generator call,
one checker call and one root freeze were made in a temporary directory. There was no
second generator/checker execution. The following call then succeeded:

```python
bundle = fixture([0, 1, 3])
generate(bundle, one_run)
verify(bundle, one_run)
freeze_run(one_run)
report = compare_replay(one_run, one_run, temporary_root / 'self_replay.json')
```

Observed output:

```text
actual generator runs: 1
actual checker runs: 1
Same directory supplied twice: True
Replay integrity: CONTRACT_VALID
Candidate acceptance: ADMISSIBLE_COMPLETE_POPULATION
Mismatch list: []
```

The temporary files were confined to a system temporary directory and removed by its
context manager. This report preserves the literal reproduction and observed result.
No repository test, fixture, source, binding or protected authority was changed.

### Scientific consequence — bounded logical inference

The acceptance mechanism can certify the replay prerequisite without the required
second execution. This can promote a proposed outcome/candidate population to admissible
status without the preregistered evidence. It does not demonstrate that exact separation
arithmetic is wrong or that any real relation has been manufactured. It demonstrates a
material failure of the scientific acceptance contract; a process-dependent error could
escape the missing replay check. An operator accidentally supplying the same directory
twice is sufficient; no forgery or source modification is necessary.

### Required disposition

- **Current freeze valid for execution: NO.** Preserve its bytes and hashes as the
  reviewed defective version; do not erase or silently replace it.
- **Implementation amendment required: YES**, under new PI authorization, followed
  by adversarial synthetic qualification, a new implementation binding and renewed review.
- **Preregistration amendment required for this defect: NO.** The existing requirement
  already excludes self-comparison as replay.
- Remediation must establish distinct run identity and the required execution provenance,
  not merely two strings naming paths. Alias/copy/reuse cases need prospective integrity
  treatment; this report does not claim to have exhaustively tested those cases.
- No real-input readiness or execution authorization may proceed from this freeze.

## Test review and shared assumptions

The 21-test suite was **not rerun as a whole**. One new targeted synthetic review probe
was executed to confirm M01, after which the review stopped.

`test_witness_audit.py:147–161` constructs two separate subprocess runs and confirms
their byte equality. That is a positive replay test; it does not test rejection when
only one run exists. `test_witness_audit.py:184–191` tests different synthetic outputs
and correctly expects withholding, but likewise does not test self-comparison.
Thus their prior PASS results do not cover the material acceptance failure reproduced
here. `test_checker_detects_every_output_file_tampering` at lines 135–145 appends a
newline to each generator stream; that bounded corruption coverage must not be described
as exhaustive semantic tamper coverage. Remaining A–L coverage is not newly certified
because the material-defect stop rule took precedence.

Inspected generator and checker arithmetic uses different derivations: generator
`decode` at lines 43–57 uses `as_integer_ratio()`; checker `producer` at lines 73–96
decodes binary64 sign/exponent/significand, and its pair traversal at lines 159–170
uses integer cross-products. Canonical witness construction appears separately at
generator lines 60–62 and checker lines 149–152. These are bounded code observations,
not whole-program sign-off.

Shared primitives include CPython integer/runtime behavior, `math.gcd`, binary64
token/hex round-trip facilities, JSON parsing, canonical serialization, SHA-256 and
file indexing from `transport.py`. Both worker processes also use the shared
`runner.authenticate_real` authority path. Shared transport and admission can propagate
a common error that two mathematical traversals alone would not detect. Their risk
must be assessed independently of generator/checker agreement. M01 is in the common
final acceptance layer and is scientifically material. It is not evidence of a bug
in SHA-256 or in the separate rational decoders.

**Checker independence acceptable: NOT SIGNED OFF.** Distinct mathematical traversal
is visible, but the incomplete review and defective replay gate do not support full
acceptance of the frozen package. The final requested YES/NO field is NO, meaning
approval withheld, not a claim that both numerical algorithms are identical.

No style-only changes are requested. The code and all existing hashes remain intact.

## PI decision required

Reject this freeze for execution and authorize a bounded implementation correction of
M01, synthetic regression checks and a replacement freeze, followed by renewed review.
The independent-review staffing/identity limitation above must also be addressed before
a positive independent sign-off is asserted. No correction is implemented here.

The review finding is complete as a stop report; exhaustive independent code review
and positive sign-off are **not complete**. No real scientific input, accepted map,
Double-Bass work, BeatReference or BPM was executed or modified. No commit or push.
