# H-CEDVAL003-WITHIN-CELL-STRENGTH-DISCRIMINABILITY-01

Status: **FROZEN — NOT YET EXECUTED**

Authority: PI approval of frozen strength measurement authority
`H-CEDVAL003-PULSECANDIDATE-STRENGTH-AUTHORITY-01`, result commit `8bba617`,
scientific fingerprint `6903decb…`; evidence gap `EG-CEDVAL003-AMBIGUOUS-PHYSICAL-AUTHORITY-01`.

## Frozen scientific question

Within each frozen `AMBIGUOUS_MULTIPLE_OBSERVED` cell, can the existing
lineage-bound `PulseCandidate.strength` values distinguish the contained
observations by a unique deterministic within-cell ordering?

## Frozen hypothesis and classification

For every frozen cell:

- if exactly one observation has the strictly greatest exact binary64
  strength, classify `UNIQUE_STRENGTH_MAXIMUM`;
- if two or more observations share the greatest exact binary64 strength,
  classify `STRENGTH_TIED`;
- if any required strength/identity/provenance authority is absent or replay
  fails, classify `STRENGTH_UNRESOLVED`.

`UNIQUE_STRENGTH_MAXIMUM` means only that existing physical strength evidence
provides a deterministic within-cell distinction. It is not a correspondence,
selection, correctness, preference or musical claim.

## Frozen inputs and population

The only scientific input is frozen artifact
`run_20260823_211259/strength_measurements.json`, SHA-256
`1772b2817b0a6aa075b91cff20b830791c14f245a5c219d6a65feee7f19450cc`,
with scientific fingerprint
`6903decbe3175db300002f148d5e4192f9c51ba8959a6534921675af753aa94d`.
The preregistration and artifact manifest are also checksum-bound.

Expected population: Drums 54 cells/108 observations, Double Bass 2/4,
Piano 0/0, overall 56/112. No case may be added or removed.

## Exact procedure

1. Verify input hashes, scientific fingerprint, population, unique cell/EME/
   PulseCandidate identities, lineage completeness and exact replay status.
2. For each cell, decode every `strength_hex` with binary64 `float.fromhex`
   and require exact equality with the preserved JSON number. No rounding,
   normalization, rescaling, epsilon, tolerance or transformation is allowed.
3. Group observations by exact binary64 strength. Serialize groups in strictly
   descending strength order; within an equal-strength group, sort identities
   only for deterministic serialization and do not claim an ordering.
4. Apply the frozen status rule. For a unique maximum preserve its EME and
   PulseCandidate identity. For a tie preserve no selected maximum identity.
5. Preserve highest-minus-second-highest exact binary64 subtraction as a
   descriptive value and hexadecimal representation. For a tied maximum the
   difference is exact zero. If unresolved, it is null.
6. Execute the complete transformation twice and require byte-identical
   canonical scientific content and fingerprint.

Report the complete sorted difference population and descriptive N, minimum,
maximum, mean, median, population standard deviation and NumPy-linear
Q1/Q2/Q3 independently for Drums and Double Bass. No cross-source statistic is
authorized.

## Firewalls

Execution must not access Ground Truth, symbolic timing/identity, Calibration
Zero cell centers/correspondence outcomes, H02 scores or musical information.
No observation is selected for correspondence, no hypothesis is scored, and
no TP/FP/FN or threshold is calculated.

Historical unscorable cases, H02, H03, Calibration Zero, raw observations,
AD-037/038/039/040, `GEOMETRIC_ONLY`, architecture, production behavior and
production code remain unchanged. Any later correspondence question requires
separate preregistration and PI authority.
