# H-VAL001-C1-08 — Candidate Period Discrete Measurement Correspondence Audit

## Status

Complete. Blind Candidate Period populations were frozen before the controlled
transformation and condition assignment were revealed. Ground Truth, MusicXML,
tempo, beat, meter and metric level were never loaded or used.

## Scientific question

Under which declared measurement conditions can two Candidate Period
observations be scientifically considered corresponding?

## Evidence unavailable before this experiment

Existing records preserved independently discovered Candidate Period
populations and numerical cross-condition differences, but they did not
preserve an identity relation between the supporting observations in each
condition. Numerical proximity therefore could not distinguish correspondence
from accidental similarity.

No production implementation was required. The existing immutable Candidate
Period representation already preserves supporting observation indices,
measurement configuration, provenance and recurrence evidence.

## Experimental design

The experiment consumed only the frozen 39-event observation population from
`H-VAL001-C1-07` `BLIND-CONDITION-01`. Stable zero-based event indices
preserved observation identity.

Two neutral populations were produced:

- `BLIND-POPULATION-01`: identity transformation;
- `BLIND-POPULATION-02`: every source sample position transformed by the
  non-musical declared scale `7/10`.

Blind discovery did not receive the transformation identity or condition
semantics. It used the existing exact recurrence definition under three
preregistered measurement regimes:

| Regime | Frame length | Grid origin | Sample rate | Rounding |
|---|---:|---:|---:|---|
| GRID-512-PHASE-0 | 512 samples | 0 samples | 44,100 Hz | ROUND_HALF_EVEN |
| GRID-512-PHASE-256 | 512 samples | 256 samples | 44,100 Hz | ROUND_HALF_EVEN |
| GRID-256-PHASE-0 | 256 samples | 0 samples | 44,100 Hz | ROUND_HALF_EVEN |

The preregistered experiment-local correspondence criterion was:

> Two Candidate Periods have lineage-supported correspondence when at least
> two identical adjacent source-observation pairs support the first period and,
> after the declared controlled transformation and measurement operation,
> support the second period.

The criterion uses the recurrence minimum already governing candidature. It
defines no numerical tolerance, nearest-neighbour rule, ranking or musical
interpretation.

## Blind Candidate Period populations — Observed Facts

Values are `frame interval: occurrence count`.

| Regime | BLIND-POPULATION-01 | BLIND-POPULATION-02 |
|---|---|---|
| GRID-512-PHASE-0 | 32:3, 33:7, 34:3, 66:5, 67:3, 99:2, 100:3, 133:2, 232:3 | 22:2, 23:8, 24:3, 46:5, 47:3, 70:5, 163:3 |
| GRID-512-PHASE-256 | 31:2, 32:2, 33:6, 35:2, 65:2, 66:3, 67:3, 99:2, 100:2, 231:2, 233:2 | 22:2, 23:10, 46:4, 47:5, 69:2, 70:3, 93:2, 116:2, 162:2 |
| GRID-256-PHASE-0 | 64:3, 66:7, 68:3, 132:5, 134:3, 198:2, 200:3, 266:2, 464:3 | 45:3, 46:7, 48:2, 92:2, 93:3, 94:3, 138:2, 140:3, 186:2, 325:3 |

Blind execution and deterministic replay produced the identical scientific
fingerprint:

`a4b1c764475c306912be05ff2e3905361f9320467903d00cf930a3bec9f6c437`

Every population was instantiated through the deeply immutable M91
`CandidatePeriodPopulation` representation before serialization.

## Post-blind lineage evidence — Observed Facts

After blind freezing, the `7/10` transformation and neutral-condition mapping
were revealed. The preregistered criterion established:

- 8 lineage-supported Candidate Period correspondences under
  GRID-512-PHASE-0;
- 5 under GRID-512-PHASE-256; and
- 10 under GRID-256-PHASE-0.

All 23 correspondence pairs had different integer frame values. Examples:

- 33 → 23 frames, supported by the same seven event pairs;
- 66 → 46 frames, supported by the same five event pairs at 512/phase 0;
- 100 → 70 frames, supported by the same three event pairs;
- 66 → 46 frames at 256-sample resolution, supported by the same seven event
  pairs; and
- 132 frames split into correspondence with 92 frames for two supporting pairs
  and 93 frames for three supporting pairs at 256-sample resolution.

The 132-frame result demonstrates that one Candidate Period measurement can
divide into more than one lineage-supported Candidate Period measurement after
a controlled transformation and independent quantization.

Some Candidate Periods lost the minimum shared recurrence required by the
criterion. For example, 133 frames under GRID-512-PHASE-0 mapped its two
supporting pairs to different transformed intervals, so no transformed
Candidate Period received two shared supports. This absence was preserved as
indeterminate and was not classified as unrelatedness.

## Scientific interpretations

Grid phase changed the measured Candidate Period inventories while source
event identities, temporal transformation, frame length, sample rate and
recurrence definition remained fixed. At 512 samples, shifting the grid origin
from 0 to 256 samples changed the number of lineage-supported
correspondences from eight to five.

Grid resolution also changed the measured populations and correspondence
structure. Changing from 512 to 256 samples at phase zero changed the number
of correspondences from eight to ten and exposed a one-to-many 132 → 92/93
relationship.

Within this controlled remeasurement scope, supporting-event lineage provides
evidence of correspondence without requiring numerical identity or proximity.
The evidence supports correspondence as a relation between measurements, not
as equality between their discrete values.

## Hypothesis evaluation

### Supported within the declared scope

1. Non-identical discrete Candidate Period measurements can preserve
   lineage-supported correspondence.
2. Grid phase can change Candidate Period measurements while source
   observation identities remain fixed.
3. Grid resolution can change Candidate Period measurements while source
   observation identities remain fixed.
4. Shared supporting-event lineage can establish correspondence evidence
   without a numerical tolerance.
5. Correspondence need not be one-to-one after discrete remeasurement.

### Not rejected but not established beyond this scope

- The same criterion applies to independently rendered audio observations.
- Frame quantization is the sole cause of H-VAL001-C1-07 discrepancies.
- Candidate Periods without shared lineage are unrelated.
- Correspondence establishes equivalence or musical metric identity.
- The experiment-local criterion is necessary or sufficient for all Candidate
  Period protocols.

## Scientific conclusion

**LINEAGE-SUPPORTED CORRESPONDENCE ESTABLISHED WITHIN CONTROLLED REMEASUREMENT
SCOPE.**

Two non-identical Candidate Period measurements can be scientifically treated
as corresponding in this experiment when all of the following are declared
and preserved:

- one traceable source observation population;
- stable observation identities;
- a preregistered deterministic transformation;
- sample rate, frame length, grid origin and rounding rule;
- unchanged observation ordering;
- exact Candidate Period recurrence in both measured populations; and
- at least two identical supporting adjacent event pairs across the two
  measurements.

This conclusion does not establish a tolerance, numerical equivalence,
correspondence for independently detected audio events, beat, tempo, meter,
tactus, subdivision, hierarchy or metric level.

## Open questions and limitation

The second condition is a deterministic experiment-local transformation of a
frozen observation population, not an independent audio observation. The
experiment therefore isolates discrete remeasurement but does not test onset
detection, rendering variation, source separation or independent event
identity recovery.

It remains unknown whether supporting-event lineage can be established between
independently rendered and independently detected audio conditions without an
unauthorized temporal tolerance.

## Recommendation

The next scientifically justified objective is a controlled independent-audio
lineage experiment: determine whether independently rendered observations with
authoritatively preserved event identity reproduce the lineage-supported
correspondence demonstrated here.

No production implementation or architectural change is justified by this
experiment. Provisional F-033 should remain non-canonical until independent
audio evidence tests the criterion beyond deterministic remeasurement.
