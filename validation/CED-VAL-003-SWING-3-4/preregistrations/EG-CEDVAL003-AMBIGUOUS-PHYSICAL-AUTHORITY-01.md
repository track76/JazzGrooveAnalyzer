# EG-CEDVAL003-AMBIGUOUS-PHYSICAL-AUTHORITY-01

Status: **FROZEN EVIDENCE GAP — NO EXPERIMENT PREREGISTERED**

Authority: PI decision; frozen scorability audit
`AUD-CEDVAL003-H02-SCORABILITY-01` at commit `aae86a1`; frozen CED-VAL-003
Calibration Zero at commit `3f2a368`; frozen CED-VAL-003 H02 result at commit
`59b604a`; AD-037/038/039/040.

## Scientific question

Does the complete frozen CED-VAL-003 population of
`AMBIGUOUS_MULTIPLE_OBSERVED` Calibration Zero cells contain an already
preserved, provenance-bound physical observational dimension sufficient to
support one falsifiable Ground-Truth-independent rule for discriminating among
the observations within a cell?

Discrimination here would require evidence beyond record identity: it would
have to justify a physical preference or distinction relevant to observation
authority without using the symbolic event time, symbolic cell center, musical
plausibility or a correspondence outcome.

## Frozen inputs and complete population

- Calibration Zero event-level results SHA-256:
  `3c2d22300de63de57885a1c786dea1679136410860558f3e093e6bf2b5233c31`;
- H02 blind result SHA-256:
  `061968ece6e534d097b18936488c4fa551b216e9bb55beece4ba87cf8f13172a`;
- scorability-audit result SHA-256:
  `5da81ca50b072c4af332acf8e403c1d1c520e86af8378ba6125fabd764ce4af4`;
- accepted scorability-audit fingerprint:
  `34dafe335a0965ff2321bfc176386b974f1ee5a0425e153894e96bde8f939348`.

The complete in-scope population is 56 cells containing 112 observations:

| Source | Ambiguous cells | Contained observations | Observations per cell |
|---|---:|---:|---:|
| Drums | 54 | 108 | 2 |
| Double Bass | 2 | 4 | 2 |
| Piano | 0 | 0 | not applicable |
| Overall | 56 | 112 | 2 |

All cell, symbolic-authority, EME and supporting PulseCandidate identities,
timestamps, source/asset identities, lineage and provenance remain immutable.
The population is inventoried only; no cell is adjudicated.

## Evidence inventory

### A — preserved and authorized for physical description

- immutable EME identity and exact observed timestamp;
- contributor and sound-source identity;
- source-asset SHA-256, temporal scope and materialization rule;
- supporting PulseCandidate identity lineage;
- deterministic observation frame/index where present in the frozen blind
  frame inventory;
- within-source temporal order, exact frame intervals, two-sided signatures
  and recurrence counts where present in frozen H02 evidence; and
- Calibration Zero cell identity/status and complete candidate membership as
  authority context, never as a discriminator.

These quantities distinguish observations as physical records and describe
their temporal context. None is authorized to select one observation as the
preferred physical authority within an ambiguous symbolic capture cell.
Timestamp distance to `t_GT` or to a symbolic cell center is expressly
excluded.

### B — preserved in the model or another scientific context, but not
authorized for this discrimination

- `PulseCandidate.strength`: the Domain model preserves strength and uses it
  in deterministic PulseCandidate identity construction, but the frozen
  CED-VAL-003 calibration/H02 artifacts preserve only the supporting
  PulseCandidate IDs, not the numeric strength values. Prior authority does
  not validate strength as a within-cell discriminator.
- `PulseCandidate.confidence` and EME confidence: supported by immutable
  representations, but numeric values are not retained in the frozen
  CED-VAL-003 event evidence and no discrimination semantics are authorized.
- H02 two-sided interval-signature/recurrence evidence: authorized as part of
  frozen blind candidate discovery, not as authority for selecting a symbolic
  manifestation inside a Calibration Zero cell.

Within-source or within-cell use avoids a cross-source comparability claim but
does not by itself establish discriminative meaning. Before strength can be a
study variable, its exact value must be preserved for every lineage-linked
observation and independently shown to be deterministic, repeatable and
physically interpretable within source under the bound detector configuration.

### C — unavailable

- frozen numeric PulseCandidate strength/confidence and EME confidence values
  for every contained observation;
- validated event-level attack/transient, spectral or envelope descriptors;
- Drum component identity (including kick, snare, ride or hi-hat identity);
- any independently validated physical observation class that distinguishes
  multiple acoustic attacks within one capture cell; and
- any authorized non-symbolic rule that turns temporal order, interval
  recurrence or identity into a preferred calibration observation.

## Frozen evidence-gap decision

Existing evidence does **not** support one scientifically defensible,
falsifiable discrimination hypothesis. Exact timestamps already distinguish
the observations as records, but using timestamp proximity to symbolic
authority is prohibited, and temporal ordering alone supplies no independent
physical reason to prefer one observation. Existing sequence evidence and
PulseCandidate lineage do not carry authorized within-cell selection
semantics. No experiment is therefore preregistered or authorized by this
record.

The minimum additional physical observation is the exact, lineage-bound
PulseCandidate strength value for every observation in the frozen ambiguous
population, accompanied by independent deterministic-replay and within-source
repeatability validation that establishes strength as a stable physical
measurement under the checksum-bound asset and detector configuration. This
does not authorize a higher-strength selection rule; a later PI-reviewed
preregistration would still be required before any discrimination test.

Generic Drum discrimination remains scientifically testable in principle
without component identity if a component-agnostic physical descriptor first
receives that independent authority. Any proposition requiring Drum component
identity is rejected rather than inferred.

## Firewalls and historical effect

Ground Truth cannot select, rank, threshold, remove, merge or rematch an
observation, and symbolic time/cell geometry cannot define a physical
criterion. Ground Truth could score only after a future physical criterion is
independently preregistered, frozen, executed and fingerprinted under separate
PI authority.

This record cannot retroactively change CED-VAL-003 candidates, unscorable
statuses, TP/FP/FN, metrics, Calibration Zero, the three-dataset conclusion,
H02 or production authority. H02 is unchanged, no H03 exists, AD-040 is
unchanged and `GEOMETRIC_ONLY` remains authoritative. Architecture, production
and production code impacts are none.

The scientific chain remains: H02 → CED-VAL-003 blind result → 56 unscorable
candidates → scorability audit → Calibration Zero authority bottleneck → this
frozen physical-evidence gap.
