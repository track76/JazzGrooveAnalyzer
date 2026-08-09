# H-VAL001-C1-05 — Candidate Metric-Level Discrimination Audit

## Scientific question

Does existing VAL-001 observational evidence contain a reproducible property
that distinguishes one Candidate Period from the others in a way that could
later support metric-level interpretation?

## Authority and method

**Architectural Decision.** Observation and Candidate Period discovery remain
pre-interpretive under AD-008, F-031, F-032, AD-034, and AD-035. Metric-level
interpretation belongs to the Domain. No tempo production is authorized.

**Observed Fact.** The experiment used repository revision
`44ffffae226192d145739714dffc69c33cc7922f` and bootstrap state
`M93 / 44ffffa`. Candidate and relationship evidence was read from the frozen
blind C1-03 and C1-04 records. Ground Truth was loaded only after
`blind_metric_discrimination.json` had been serialized.

**Observed Fact.** The full-mix Pulse/InternalMetricTimeline path was executed
twice with the canonical MP3 and `DummyMultiStemSeparator`. Both executions
produced identical scientific-content fingerprints:
`ff5013f2ed24e0ad7c6d4631628104a086563e07a2d1cd2be79f20069511a45f`.

## Blind candidate comparison

| Evidence dimension | 33 frames | 66 frames | 132 frames |
|---|---:|---:|---:|
| Full-mix consecutive occurrences | 16 | 8 | 0 |
| Full-mix relative frequency | 0.210526 | 0.105263 | 0 |
| Exact consecutive source populations | 4 | 3 | 2 |
| Full-mix non-consecutive pairs | 2 | 11 | 15 |
| Full-mix support-span fraction | 0.874107 | 0.609951 | unavailable |
| Full-mix occurrence starts by observation quarter | 3/6/6/1 | 0/4/2/2 | unavailable |
| Modal phase-residue support | 4 of 16 | 1 of 8 (eight tied residues) | unavailable |

**Observed Fact.** The evidence dimensions distinguish the candidates
numerically. Thirty-three frames has greater consecutive recurrence, wider
full-mix coverage, and broader exact consecutive source support than 66 or
132 frames. Sixty-six and 132 frames have more full-mix non-consecutive-pair
support than 33 frames.

**Observed Fact.** The 33-frame phase audit has one modal start residue with
4/16 occurrences and circular residuals from -6 to +6 frames. The 66-frame
audit has eight tied residues with 1/8 occurrence each and residuals including
-26 and -25 frames. No canonical phase threshold exists.

**Logical Inference.** Each evidence dimension would privilege a different
property: consecutive recurrence and coverage favour 33 frames, while
non-consecutive-pair support favours 132 frames. Choosing which property is
metric-level evidence would require a scientific interpretation not present
in current authority.

**Logical Inference.** Exact relationships among recurrent durations provide
relational evidence, but numerical ratio alone cannot establish hierarchy
under F-031.

## Pulse and Internal Metric Timeline audit

**Observed Fact.** Each blind execution produced 77 filtered PulseCandidates,
12 Candidate Periods, 385 ElementaryMetricEvents, 77 BeatReferences, 77
MetricClusters, 77 Pulses, and 77 InternalMetricTimeline entries.

**Observed Fact.** All 77 Pulse timestamps are exactly equal to their
BeatReference timestamps. All 77 InternalMetricTimeline timestamps are exactly
equal to the Pulse timestamps. Their constant interval is approximately
0.4857858933 seconds.

**Observed Fact.** `PulseBuilder` copies `cluster.beat_reference.timestamp` to
`Pulse.timestamp`. `InternalMetricTimelineReconstructor._reconstruct_sequence`
validates and returns the Pulse tuple unchanged. The timeline builder stores
that tuple without adding temporal evidence.

**Observed Fact.** MetricCluster association counts are non-zero at only four
grid positions (five duplicated full-mix ElementaryMetricEvents at each) and
zero at the remaining 73 positions under the 0.010-second cluster window.

**Scientific Conclusion.** In this execution, Pulse and InternalMetricTimeline
do not supply independent evidence capable of discriminating among Candidate
Periods. They inherit the already selected and regularized BeatReference grid.
This conclusion does not judge the correctness of that grid and does not claim
that Pulse or IMT can never carry other scientifically relevant information.

## Blind result

**Scientific Conclusion.**

**BLIND EVIDENCE DOES NOT YET SUPPORT METRIC-LEVEL DISCRIMINATION**

Supporting observations are reproducible numerical differences in recurrence,
coverage, source support, relations, and phase residuals, combined with the
absence of an authorized evidence-to-metric-level relation and the lack of
independent Pulse/IMT evidence. The conclusion is limited to VAL-001 and the
currently preserved evidence. It does not establish that the candidates lack
musical meaning.

## Post-blind Ground Truth evaluation

**Observed Fact.** After the blind record was frozen, GT-VAL-001-v1 supplied
quarter-note tempo 78 BPM from the authoritative MusicXML with SHA-256
`809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778`.

**Logical Inference.** The derived quarter duration is
0.7692307692307692308 seconds; its half is 0.3846153846153846154 seconds and
its double is 1.538461538461538462 seconds.

| Frozen candidate | Duration (s) | Difference from derived reference (s) |
|---|---:|---:|
| 33 frames | 0.3831292517006802721 | -0.0014861329147043433 from half-quarter |
| 66 frames | 0.7662585034013605442 | -0.0029722658294086866 from quarter |
| 132 frames | 1.5325170068027210884 | -0.0059445316588173731 from double-quarter |

**Logical Inference.** The three candidates are each numerically close to a
different derived reference duration. This evaluates the frozen population but
does not choose a metric level, because the same numerical relationship exists
at all three levels and Ground Truth did not participate in discovery.

## LocalTempo authority conflict

**Evidence Conflict.** The older LocalTempo specification derives LocalTempo
from consecutive Pulse relations, while F-031 states that duration or rate
alone cannot establish tempo or metric level. This experiment does not resolve
the conflict. It strengthens neither formulation into a superseding decision:
the Pulse/IMT path is reproducible, but it contains no independent beat-unit or
metric-level identity.

## Limitation and smallest missing evidence

**Scientific Conclusion.** The smallest missing evidence class is an
independently justified relation between observation-derived candidate
properties and metric-level identity. Current recurrence, coverage,
cross-source support, phase descriptions, Candidate Period ratios, Pulse, and
IMT do not provide that relation. This statement identifies missing evidence;
it does not define or authorize a new concept, algorithm, or architecture.

**Architectural Decision.** No architecture change is authorized. The current
Candidate Period representation remains sufficient to preserve the evidence
used by this audit.

## Preserved Evidence Conflicts

- **Evidence Conflict:** Baseline Evidence Conflict.
- **Evidence Conflict:** Document-State Evidence Conflict.
- **Evidence Conflict:** Experimental Artifact Path Evidence Conflict.
- **Evidence Conflict:** LocalTempo Authority Evidence Conflict.

