# AUD-CEDVAL003-H02-SCORABILITY-01

Status: **FROZEN — AUDIT NOT YET EXECUTED**

Authority: PI decision; frozen three-dataset conclusion at commit `c7a1670`;
frozen CED-VAL-003 H02 result at commit `59b604a`; frozen Calibration Zero at
commit `3f2a368`; H02 preregistration and AD-037/038/039/040.

## Frozen Question

For every frozen CED-VAL-003 H02 candidate and symbolic scoring relation, what
existing provenance-bound authority condition determines scorability, and are
the 56 candidate-level unscorable statuses caused by absent blind-candidate
evidence, calibration/scoring-authority limitations, both, or evidence that is
irreducibly indeterminate?

This is a read-only authority audit. It cannot create, remove, rematch, rescore,
promote or demote a candidate, symbolic relation or TP/FP/FN record.

## Frozen Inputs

- H02 blind result SHA-256
  `061968ece6e534d097b18936488c4fa551b216e9bb55beece4ba87cf8f13172a`;
- H02 scoring result SHA-256
  `993fd8c05285e2402c03f7e813f3dfbbc30e54c40a5577e195c9c31997796828`;
- Calibration Zero event results SHA-256
  `3c2d22300de63de57885a1c786dea1679136410860558f3e093e6bf2b5233c31`;
- symbolic pair authority SHA-256
  `10cee0e96fc21b854714f426ca27543b94a63071b19861c7e28832f7e790fbf7`;
- Calibration Zero pair results SHA-256
  `a25cb0179f0f527b86d309d06da2c8ebb33d2e1afda63d0ff54ce5f5d7059a8e`;
- three-dataset conclusion SHA-256
  `f416d8efc8c10b520bc5257a475f075b022ba343ff1c615e6316798afd2d686c`;
- frozen H02 preregistration SHA-256
  `10f4f445b257a42e0bdb7cd98277ebbd6689c0f76315c04ca115b0f875e50784`.

Execution fails closed on any checksum, identity, population or fingerprint
conflict.

## Complete Populations

Audit all 89 blind candidates, 61 blind unresolved records, all frozen scoring
records, all 56 unscorable candidates and all 55 unscorable symbolic
relations. Preserve Piano and Double Bass independently before any overall
summary. Expected frozen candidate/scorable/unscorable counts are Piano
14/5/9 and Double Bass 75/28/47.

## Deterministic Join Procedure

1. Join each blind candidate by exact source EME ID and Drum EME ID to its
   frozen scoring record. Missing, duplicate or inconsistent joins are an
   identity/provenance failure and stop the audit.
2. Build a complete EME authority inventory from every Calibration Zero
   `VALID` record, every candidate in an `AMBIGUOUS_MULTIPLE_OBSERVED` cell,
   every `AMBIGUOUS_BOUNDARY` record and every `UNMATCHED_OBSERVED` record.
3. Join each candidate-side EME independently to this inventory. Preserve the
   exact calibration status, symbolic cell/event identity, candidate set and
   lineage; never select within an ambiguous cell.
4. Join any resolved symbolic identities to the frozen exact-equality symbolic
   pair authority and pair result without manufacturing a pair.
5. Audit every frozen valid symbolic pair whose JGA pair status is unresolved,
   preserving source and Drum absolute-correlation statuses and identities.

## Cause Classification

Cause labels must be derived only from repository-native frozen statuses.
Preserve the exact low-level status and map it without precedence loss:

- candidate evidence exists and both absolute event identities are `VALID`:
  candidate is scorable; symbolic pair presence determines frozen TP/FP only;
- candidate evidence exists and only Drum absolute authority is non-`VALID`:
  `DRUM_CALIBRATION_AUTHORITY_UNRESOLVED`;
- candidate evidence exists and only accompaniment absolute authority is
  non-`VALID`: `ACCOMPANIMENT_CALIBRATION_AUTHORITY_UNRESOLVED`;
- both are non-`VALID`: `BOTH_CALIBRATION_AUTHORITIES_UNRESOLVED`;
- absent/duplicate identity join: `IDENTITY_PROVENANCE_JOIN_FAILURE`;
- another explicit frozen status: retain that status and label
  `OTHER_EVIDENCED_AUTHORITY_LIMITATION`;
- no supported cause: `INDETERMINATE_FROM_EXISTING_EVIDENCE`.

For every non-`VALID` side, preserve whether the direct cause is an ambiguous
multiple-observed cell, ambiguous boundary, unmatched observed authority,
unmatched symbolic authority, or another exact frozen status. Symbolic pair
authority absence is reported separately: when both event identities are
valid it makes the frozen candidate FP, not unscorable; when either event
identity is unresolved the chain stops before pair adjudication.

High-level counts are mutually exclusive:
`CANDIDATE_DISCOVERY_LIMITATION`, `CALIBRATION_SCORING_AUTHORITY_LIMITATION`,
`MIXED_LIMITATION`, or `INDETERMINATE`. A frozen blind candidate cannot be a
candidate-discovery limitation merely because it is unscorable: its existence
is positive discovery evidence. Mixed requires an independently evidenced
candidate-record defect plus an authority limitation; no counterfactual is
permitted.

## Firewalls and Verification

No nearest symbolic choice, tolerance, sequence alignment, metric context,
musical plausibility or alternative TP/FP/FN calculation is permitted. Frozen
metrics remain unchanged. H02, H03, Calibration Zero, raw observations,
AD-038/040 and production code remain unchanged.

Execute twice and require identical canonical case records, reason counts and
fingerprint. Independently verify 89 candidate joins, 56 unscorable candidate
classifications, 55 unscorable symbolic-relation records, source subtotals,
mutually exclusive high-level totals and all referenced identities. Preserve
case-level audit JSON, summary/report, completion protocol and checksum
manifest.
