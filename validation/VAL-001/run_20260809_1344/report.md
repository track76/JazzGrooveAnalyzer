# Scientific Validation Campaign 1 — Candidate Relationship Evidence Audit

Experiment ID: `H-VAL001-C1-04`

Run ID: `run_20260809_1344`

Status: COMPLETED

## Scientific objective

Determine whether the temporal observations already preserved for VAL-001
contain reproducible relationship evidence among Candidate Periods beyond
exact consecutive-gap recurrence, without assigning musical metric meaning.

## Repository authority state

- Branch: `scientific/translation-layer-finalization`
- Source revision: `ea31e03fd4837491723d4f8a80b6d16dfa892bea`
- Bootstrap revision: `ea31e03`
- Phase: Phase II Scientific Validation
- Governing authorities: F-031, F-032, AD-034 and SVP-001
- Source blind record: `H-VAL001-C1-03`
- Source blind-record fingerprint:
  `7a1ebec978115094e751f78eee84abd718933d6cff91200a2920adbd83c6de3c`

The Baseline Evidence Conflict, Document-State Evidence Conflict and
Experimental Artifact Path Evidence Conflict remain preserved. No historical
artifact was modified.

## Experimental boundary and configuration

Observed Fact: The blind audit consumed only the frozen distinct
ElementaryMetricEvent frame populations in the first blind execution of
`H-VAL001-C1-03`.

Observed Fact: No audio analysis, Candidate Period discovery, Candidate Period
selection or M91 materialization was executed.

Observed Fact: The blind relationship record was frozen at
`2026-08-09T13:47:02.722559+00:00` before the Ground Truth loader was invoked.

The experiment-local operations were:

- exact positive frame differences between all event pairs for the
  non-consecutive lag audit;
- supporting occurrence start frame modulo the exact candidate frame interval
  for phase description;
- raw support span, occurrence-start counts in four equal observation-span
  partitions, and support-start gaps for temporal distribution; and
- exact cross-source frame-interval comparison plus unclassified nearest
  numerical differences.

No tolerance, equivalence rule, metric interpretation, ranking or threshold
was introduced.

## Consecutive recurrence baseline — Observed Facts

| Source | Recurrent frame interval: consecutive occurrence count |
|---|---|
| Full mix | 3:3, 31:9, 32:9, 33:16, 34:7, 35:2, 36:3, 64:2, 66:8, 67:2, 69:5, 101:2 |
| Double bass | 33:8, 132:2, 232:6, 265:2 |
| Drums | 30:7, 33:19, 37:3, 66:15, 67:6, 70:3 |
| Piano | 17:4, 32:5, 33:6, 34:13, 65:5, 66:3, 100:2, 132:3, 165:2, 166:4 |
| Tenor sax | 3:2, 265:2 |
| Voice | 3:10, 4:12, 5:7, 6:13, 7:5, 8:5, 9:8, 10:6, 11:10, 12:11, 13:7, 14:4, 15:5, 16:5, 17:5, 18:3, 19:4, 20:6, 21:3, 22:2, 23:2, 24:3, 32:3 |

## Non-consecutive lag evidence — Observed Facts

Counts below are `consecutive + non-consecutive = all exact pairs`.

| Source | 33 frames | 66 frames | 132 frames |
|---|---:|---:|---:|
| Full mix | 16 + 2 = 18 | 8 + 11 = 19 | 0 + 15 = 15 |
| Double bass | 8 + 0 = 8 | 1 + 1 = 2 | 2 + 0 = 2 |
| Drums | 19 + 0 = 19 | 15 + 2 = 17 | 1 + 11 = 12 |
| Piano | 6 + 0 = 6 | 3 + 7 = 10 | 3 + 0 = 3 |
| Tenor sax | 0 + 0 = 0 | 0 + 0 = 0 | 0 + 0 = 0 |
| Voice | 0 + 11 = 11 | 0 + 8 = 8 | 0 + 3 = 3 |

Observed Fact: Non-consecutive relations add exact 33-, 66- or 132-frame
pairs not present in the consecutive inventory for several sources.

Observed Fact: Every non-consecutive lag is a sum of intervening consecutive
gaps from the same preserved event population. Full-mix 66-frame examples
include `33+33`, `34+32`, `3+63`, `63+3`, `33+17+16`, and `35+31`.

Logical Inference: The extra pairs provide additional descriptive temporal
relationships, but this experiment does not establish their statistical or
observational independence from consecutive recurrence.

## Phase evidence — Observed Facts

The table reports `modal start residue count / supporting occurrence count`
under the declared modulo operation. No concentration threshold is applied.

| Source | 33 frames | 66 frames | 132 frames |
|---|---:|---:|---:|
| Full mix | 4/16 | 1/8 | Not in consecutive baseline |
| Double bass | 2/8 | Not in consecutive baseline | 1/2 |
| Drums | 4/19 | 2/15 | Not in consecutive baseline |
| Piano | 2/6 | 1/3 | 1/3 |
| Tenor sax | Not present | Not present | Not present |
| Voice | Not present | Not present | Not present |

Observed Fact: Supporting starts occupy multiple residues for every audited
candidate. Exact residue inventories and signed circular residual sequences
are preserved in `blind_relationship_audit.json`.

Logical Inference: A single repeated phase is not established by these
descriptive results. The absence of a threshold prevents a stronger
classification, as required by the experiment.

## Temporal-distribution evidence — Observed Facts

Values are `support-span fraction; occurrence starts by observation quarter`.

| Source/candidate | Distribution |
|---|---|
| Full mix 33 | 0.8741; [3, 6, 6, 1] |
| Full mix 66 | 0.6100; [0, 4, 2, 2] |
| Double bass 33 | 0.5908; [1, 3, 4, 0] |
| Double bass 132 | 0.2091; [0, 0, 2, 0] |
| Drums 33 | 0.8444; [4, 5, 7, 3] |
| Drums 66 | 0.7991; [4, 5, 4, 2] |
| Piano 33 | 0.8093; [1, 1, 2, 2] |
| Piano 66 | 0.4363; [1, 1, 1, 0] |
| Piano 132 | 0.2544; [0, 1, 2, 0] |

Observed Fact: Support distributions differ by source and duration. Some span
most of the observation, while others occupy fewer temporal partitions.

Logical Inference: These distributions are fully recoverable from preserved
supporting occurrence indices and timestamps. They do not require a separate
canonical persistence or locality concept.

## Cross-source evidence — Observed Facts

Exact consecutive recurrence is independently present in the canonical WAV
observations as follows:

- 33 frames: full mix 16, double bass 8, drums 19, piano 6;
- 66 frames: full mix 8, drums 15, piano 3; and
- 132 frames: double bass 2, piano 3.

Voice has a consecutive 32-frame candidate with difference `-1` frame from 33,
but no equivalence or closeness is asserted. Tenor sax contains none of the
three audited target intervals.

Observed Fact: DummyMultiStemSeparator duplicates were excluded. The full mix
is represented once by its distinct event population; independent source
support comes only from the five canonical WAV assets.

Logical Inference: Exact cross-source recurrence strengthens provenance-rich
description of the evidence, but occurrence in several sources does not assign
metric meaning or privilege a candidate.

## Evidence-value classification

| Evidence family | Classification | Numerical justification |
|---|---|---|
| Consecutive recurrence | ESSENTIAL | It supplies the recurrence evidence required by F-032 and the frozen baseline population. |
| Non-consecutive recurrence | USEFUL BUT NON-ESSENTIAL | It adds pairs, including full-mix 132 frames `0+15`, but all are combinations of the same events and independence is not established. |
| Phase evidence | NOT ESTABLISHED | Modal residue counts range from 1/8 to 4/16 for the full mix and are distributed across multiple residues; no threshold authorizes a stronger claim. |
| Temporal distribution | REDUNDANT | The numerical distributions are derivable from the occurrence indices/timestamps already required by F-032 and represented by M91. |
| Cross-source recurrence | USEFUL BUT NON-ESSENTIAL | Exact 33-frame support occurs in four source populations and exact 66-frame support in three, but F-032 does not require multi-source support for candidature. |

## Reproducibility — Observed Facts

- First blind analytical fingerprint:
  `5e8824ce37cf36a687112ba5d1ddc778598c0ad1f68f91e3ba0c8025b755e477`
- Repeated blind analytical fingerprint: identical
- Deterministic reproduction: `true`
- Frozen blind-record fingerprint:
  `5460094a50779f68341a306cb9f11b63a79e39806a98f2c0513407c00eced4d7`
- Post-blind record fingerprint:
  `b3b8e607abb5d634a4427997c9e90380dedbd24e646e7158869fa173bd75cba0`

All six canonical audio checksums were independently verified before the blind
record was written.

## Post-blind Ground Truth comparison

Observed Fact: `GT-VAL-001-v1` supplies quarter note = 78 BPM through the
authoritative MusicXML checksum
`809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778`.

Logical Inference: The derived reference durations are:

- half quarter duration: `0.3846153846153846153846153846` seconds;
- quarter duration: `0.7692307692307692307692307692` seconds; and
- double quarter duration: `1.538461538461538461538461538` seconds.

Logical Inference: At 44.1 kHz with the preserved 512-sample frame length:

- 33 frames = `0.383129251700680287` seconds, difference from the derived half
  quarter duration `-0.0014861329147043283846153846` seconds;
- 66 frames = `0.766258503401360574` seconds, difference from the derived
  quarter duration `-0.0029722658294086567692307692` seconds; and
- 132 frames = `1.532517006802721148` seconds, difference from the derived
  double quarter duration `-0.005944531658817313538461538` seconds.

These numerical correspondences do not identify beat, subdivision, tempo,
metric hierarchy or equivalence.

## Scientific conclusions

Scientific Conclusion: Within the VAL-001 frozen event populations,
non-consecutive lags and exact cross-source recurrence provide reproducible
descriptive relationships beyond the consecutive inventory. This conclusion
does not establish that those relationships are independent evidence or
musically significant.

Scientific Conclusion: The experiment does not demonstrate that phase or a
separately represented temporal-distribution dimension is indispensable for a
first Candidate Period discovery mechanism. Phase concentration remains
scientifically unclassified, while temporal distribution is recoverable from
existing occurrence evidence.

Scientific Conclusion: F-032 remains scientifically sufficient. Exact
recurrence with supporting observations, provenance, declared scope and
reproducibility evidence is sufficient for a first production discovery
implementation within the evidence tested here. This does not establish that
exact consecutive recurrence is sufficient for every performance or every
future protocol.

Scientific Conclusion: AD-034 and the M91 representation remain sufficient.
`CandidatePeriodOccurrence` can preserve adjacent or non-adjacent supporting
pairs; timestamps permit phase and distribution calculations; population
scope and provenance preserve source identity. No additional representation
is experimentally required.

## Limitations and risks

- Only one validation item was audited.
- The audit uses frozen observations rather than repeating audio analysis.
- Exact frame equality is experiment-local and not a production discovery
  authority.
- Non-consecutive relationships are combinatorial products of the same event
  population; independence is not established.
- No phase, closeness or distribution threshold exists.
- Cross-source equality does not establish common physical cause or metric
  identity.

## Smallest recommended next objective

Audit which already-existing observational population—PulseCandidate,
distinct ElementaryMetricEvent, or EnsembleMetricEvent—provides the minimum
reproducible input evidence for an initial Candidate Period discovery
protocol. This is the smallest unresolved scientific input question exposed by
C1-03 and C1-04. No implementation or architectural change is approved by this
recommendation.
