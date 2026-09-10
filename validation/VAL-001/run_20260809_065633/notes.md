# Scientific Validation Campaign 1 — VAL-001 Experiment 1

Experiment ID: `H-VAL001-C1-01`

Run ID: `run_20260809_065633`

Hypothesis: `H-VAL001-C1-01`

Status: COMPLETED

## Pre-execution authority record

- UTC timestamp: `2026-08-09T06:56:33Z`
- Local timestamp: `2026-08-09T08:56:33+02:00` (`CEST`)
- Branch: `scientific/translation-layer-finalization`
- Source revision: `be811a8a2a5608d2d91418f2627203d97d1073e0`
- Bootstrap revision: `be811a8`
- Bootstrap phase: `Phase II Scientific Validation`
- Pipeline version: `v0.2.0-alpha`
- Scientific Validation Protocol: `SVP-001`
- Validation Item: `VAL-001`
- Ground Truth identity reserved for post-analysis loading: `GT-VAL-001-v1`
- Controlled Dataset: `CED-VAL-001`

### Pre-existing working-tree state

The experiment begins from HEAD plus unrelated pre-existing working-tree
changes. None is an experiment input except the committed canonical WAV files.

- modified `output/chet_baker_metric_plot.png`;
- modified `recordings/03 THE COST OF LIVING versione intro + 8 bar.sib`;
- untracked `AGENTS.md`;
- untracked `output/dummy_stems/`;
- untracked `output/stability_curve.csv`;
- untracked obsolete MP3 stems under `recordings/validation/stems/`.

### Canonical input identities

- MP3: `recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3`
- MP3 SHA-256: `d358d1bca5144ea1dabee4d970fa5deabf81a209922481a77db0f01bd8bdbbbb`
- MusicXML: `recordings/validation/ground_truth/03 THE COST OF LIVING versione intro + 8 bar.musicxml`
- MusicXML SHA-256: `809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778`
- `double_bass.wav`: `31d6f2e34d360c6f8f75362187433f2a2c1f5eb5cbbfe627305e99d07d8be6c5`
- `drums.wav`: `d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd`
- `piano.wav`: `26fa1158f375598cc7c01e04379c00547ef1787f6862eb2f29a36aafd9007c7e`
- `tenor_sax.wav`: `89dd7e5c6063d3c4d5e4ac59c9119c265df4257dfb1b4a1e01b5f117ee87182e`
- `voice.wav`: `0fa95a3eff06d1ab075caf2f388c17d536e614aca397647967805045521c655a`

### Existing execution configuration

- MP3 separator: `DummyMultiStemSeparator` (canonical M87 reference path)
- Controlled WAV separator: `NullSeparator` (existing single-source path)
- `PulseCandidateFilter.MIN_STRENGTH = 0.10`
- `PulseCandidateFilter.MIN_DISTANCE = 0.030` seconds
- `EnsembleMetricConsensus.CONSENSUS_WINDOW = 0.05` seconds
- `BeatPeriodEstimator`: periods greater than `0.8` seconds are divided by two
- `ReconstructedMeasureRunner`: injected `4/4`
- `ReconstructedMeasureRunner`: injected four pulses per beat
- `ReconstructedMeasureRunner`: injected `120.0` internal BPM
- measure grouping: 16 BeatReferences per reconstructed measure

These implementation values are Observed Facts about the current source. They
are not modified and are not classified as scientifically correct or
incorrect by this pre-execution record.

### Blind-analysis control

Ground Truth content will not be loaded, queried or passed to the official MP3
analysis or Immutable Analysis Representation materialization. Ground Truth
loading occurs only after both operations complete.

### Preserved Evidence Conflicts

- Baseline Evidence Conflict: historical bootstrap/test-count discrepancy.
- Document-State Evidence Conflict: stale milestone sections coexist with the
  current M90 bootstrap and metadata.
- Experimental Artifact Path Evidence Conflict: the historical run remains at
  `validation/VAL-001/runs/run_20260808_1501/`; this new run follows the locked
  protocol path and does not alter the historical record.

## Execution order

1. The MP3 was analyzed blind with `AnalysisPipeline` and
   `DummyMultiStemSeparator`.
2. The completed MP3 analysis was materialized as Immutable Analysis
   Representation schema revision `1`.
3. Each authoritative WAV was analyzed independently and blind with the
   existing default `NullSeparator` path.
4. Blind execution completed at `2026-08-09T07:00:16.411778+00:00`.
5. Only then were the Validation Catalog and `GT-VAL-001-v1` loaded.
6. The existing Comparator and Scientific Validation Record materializer were
   executed.

No Ground Truth content was loaded, queried or supplied during blind analysis
or immutable materialization.

## Blind MP3 evidence — Observed Facts

- Audio duration processed: `42.24` seconds at `44100` Hz.
- PulseCandidates: `77`.
- PulseCandidate timestamps: `0.046439909297052155` through
  `36.96616780045351` seconds. The full sequence is in `diagnostics.json`.
- Strength mean/median/range: `4.313100805530301` /
  `3.525602102279663` / `1.871424913406372`–`15.991703033447266`.
- Every PulseCandidate confidence is `1.0`, as assigned by the current builder.
- SourcePulseSequences: `5`; each contains the same `77` candidates because
  the approved M87 path uses `DummyMultiStemSeparator`.
- Source names: `Other-1`, `Other-2`, `Piano`, `Bass`, and `Drums`.
- PeriodicitySegments: `5`; each reports mean interval
  `0.4857858933046903` seconds and stability `0.6677612949308122`.
- MetricContext contains 5 source sequences, 5 periodicity segments, and 5
  metric segments.
- ElementaryMetricEvents: `385`, representing 77 distinct timestamps.
- EnsembleMetricEvents: `74`.
- BeatReferences, MetricClusters, Pulses, and InternalMetricTimeline pulses:
  `77` each.
- MetricCluster event-count median is `0`; 4 clusters contain 5 events and 73
  contain no ElementaryMetricEvent within the configured 0.010-second cluster
  window.
- StabilityCurve: 69 points; score mean `0.6924970092474654`, median
  `0.6900845901031313`, range `0.5870495027207564`–`0.7787990699210852`.
- Reconstructed measures: `4`; each contains 16 BeatReferences and reports
  injected `4/4` and `120.0` internal BPM.

## MP3 BeatReference interval evidence — Observed Facts

- Interval count: `76`.
- Mean: `0.4857858933046903` seconds.
- Median: `0.4857858933046906` seconds.
- Population standard deviation: `1.6483388224980871e-15` seconds.
- Minimum: `0.48578589330468347` seconds.
- 25th percentile: `0.48578589330469035` seconds.
- 75th percentile: `0.4857858933046906` seconds.
- Maximum: `0.4857858933046941` seconds.
- BeatReference event-rate equivalent from the median: `123.51120283018861`
  events/minute.

The event-rate equivalent is a mathematical transformation of BeatReference
spacing. It is not identified as musical tempo.

## Immutable validation chain — Observed Facts

- Immutable Analysis Representation schema: `1`.
- IAR content fingerprint:
  `e8f3846664c958a7414904549efab96e8e781bf1728ed2713278f2015c9f05cc`.
- `tempo`: `NOT_PRODUCED`.
- `time_signature`: `NOT_PRODUCED`.
- `sections`: `NOT_PRODUCED`.
- `instrumentation`: `NOT_PRODUCED`.
- Comparator result ID: `098277eb-6896-4974-ac43-7bcf981fd6d7`.
- Comparator execution ID: `68394793-ce6e-48b6-8918-9690906967b9`.
- Comparator preserves `NOT_PRODUCED` for all four quantities.
- Scientific Validation Record ID:
  `JGA-SVR-57cb96f8a9d644872234702fc5c9470a4aa49f24095f4e78f4f0b6786f8df986`.
- Record fingerprint:
  `57cb96f8a9d644872234702fc5c9470a4aa49f24095f4e78f4f0b6786f8df986`.

## Ground Truth — post-analysis Observed Facts

- Ground Truth identity: `GT-VAL-001-v1`.
- Ground Truth schema and normalization versions: `1` and `1`.
- Time signature: `4/4`.
- Metronome indication: quarter note = `78` BPM.
- Explicit pickup followed by 12 normalized complete measures.
- Intro: four complete measures beginning at normalized measure 1.
- Section A: eight complete measures beginning at normalized measure 5.
- Canonical instrumentation: Voice, Saxophone, Piano, Double Bass, Drum Set.

## Derived Ground Truth quantities — Logical Inferences

- Quarter-note duration: `60 / 78 = 0.7692307692307693` seconds.
- Half of that duration: `0.38461538461538464` seconds.
- Twice that duration: `1.5384615384615385` seconds.

## MP3 quantitative relationship — Logical Inferences

- Observed median / Ground Truth quarter duration: `0.6315216612960977`.
- Ground Truth quarter duration / observed median: `1.5834769593613924`.
- Absolute difference from the Ground Truth quarter duration:
  `0.2834448759260787` seconds.
- Relative numerical difference: `0.3684783387039023`. This is a dimensionless
  descriptive difference, not accuracy.
- Absolute difference from half the Ground Truth quarter duration:
  `0.10117050868930594` seconds.
- Absolute difference from twice the Ground Truth quarter duration:
  `1.052675645156848` seconds.
- With exploratory ratios constrained to denominators no greater than 8, the
  nearest ratio for observed median / quarter duration is `5/8`; the measured
  ratio differs from `5/8` by `0.006521661296097658`.

No repository theory identifies `5/8` as the musical meaning of the reconstructed
periodicity. It is preserved only as an exploratory numerical relationship.

## Controlled WAV evidence — Observed Facts

The WAV files were processed independently with no Ground Truth supplied.

| Source | Candidates | Raw estimator input mean (s) | >0.8 rule | BeatReference median (s) | Event-rate equivalent (/min) | Measures |
|---|---:|---:|:---:|---:|---:|---:|
| double bass | 27 | 1.4195429966858537 | yes | 0.7097714983429269 | 84.53424819125512 | 1 |
| drums | 63 | 0.5887382049594031 | no | 0.5887382049594034 | 101.91286975190835 | 3 |
| piano | 49 | 0.729493575207861 | no | 0.7294935752078615 | 82.24883952254635 | 3 |
| tenor sax | 16 | 1.589792894935752 | yes | 0.7948964474678757 | 75.48152994157745 | 1 |
| voice | 150 | 0.1605137804562541 | no | 0.16051378045625597 | 373.79968143203445 | 9 |

Strength distributions, all timestamps, confidence values, periodicity
segments, BeatReferences, stability curves, timelines and reconstructed-measure
groups are preserved in `diagnostics.json`.

The declaration `MusicXML score time zero = WAV sample zero` remains a
**Declared Experimental Procedure**. This experiment does not promote it to an
Observed Fact.

## Cross-source relationships — Logical Inferences

- The six reconstructed median periods diverge substantially, from
  `0.16051378045625597` to `0.7948964474678757` seconds.
- Numerically, tenor sax is closest to the derived Ground Truth quarter-note
  duration, with absolute difference `0.025665678237106415` seconds.
- Piano is next at `0.03973719402290776` seconds, followed by double bass at
  `0.05945927088784242` seconds.
- The full MP3 absolute difference is `0.2834448759260787` seconds.
- This numerical proximity does not establish that any stem BeatReference is a
  quarter note or that the stem pipeline recognizes tempo.

## Implementation-consequence trace — Observed Facts

### BeatPeriodEstimator

- MP3: the raw mean of consecutive distinct ElementaryMetricEvent timestamps
  is `0.48578589330469024` seconds. The `> 0.8` rule is not activated, and the
  output is `0.4857858933046903` seconds.
- Double bass: `1.4195429966858537` enters the rule and
  `0.709771498342927` exits it.
- Tenor sax: `1.589792894935752` enters the rule and
  `0.794896447467876` exits it.
- Drums, piano, and voice do not activate the rule.
- The output period propagates into `BeatGridReconstructor`, which constructs
  `origin + index × period` for the number of distinct seed timestamps.
- Consequently, every resulting BeatReference interval is uniform to floating
  point precision, even though the MP3 input interval population has standard
  deviation `0.24169845925129807` seconds.

### Reconstructed measures

- `120.0` BPM is injected by `ReconstructedMeasureRunner`; it is not observed
  or estimated from audio.
- `4/4` and four pulses per beat are injected by the same runner.
- Sixteen BeatReferences per measure are therefore imposed by construction.
- Measure starts and the first 15 within-group intervals derive from the
  reconstructed BeatReference grid; the final end extension is `60/120 = 0.5`
  seconds. Measure duration is therefore a combination of reconstructed
  temporal evidence and an injected value.
- The reported `4/4` agrees numerically with Ground Truth by construction, not
  by observation.
- The MP3 measure count of four is `floor(77/16)`; thirteen residual
  BeatReferences are not represented in a completed reconstructed measure.

## Numerical reproducibility — Observed Facts

Two additional blind in-memory executions produced identical SHA-256
fingerprints of all preserved numerical evidence:

- MP3: `732b296835b547ce7ceefac64bd09bbc2b376d83df9a1068d34f56316a3418c1`
- double bass: `6fd1a019092082cbd63570057a107e4dd405a79eb8b2f68a349479999b08fb8d`
- drums: `bf87e5deef9aec03cbe201e54d7990fe73b30e5058af998c210917f80d5b60f7`
- piano: `07e5310ee154c776e8ea548ab0dc8ef18179fb182d60c33e54fd60060c78237d`
- tenor sax: `aae6e4e5d578b788bd92391bdac7e5a037d73e32004e54dba5ae86ee53bdea5e`
- voice: `2fc82fabbf82aa597ec018769c16627592b683ef0d4cfdd5f8c2ccea77333987`

Runtime UUIDs and creation timestamps were excluded from these numerical
fingerprints because execution identity is distinct from scientific content.

## Scientific Conclusions

### SC-C1-01

**Scientific Conclusion:** H-VAL001-C1-01 is supported within the scope of
temporal evidence preservation. The completed blind analysis produces a
reproducible BeatReference interval sequence that can be characterized
quantitatively against the independent VAL-001 reference without changing the
architecture.

Supporting observations are the identical repeated numerical fingerprints,
the preserved 76-interval MP3 sequence, and post-analysis reference loading.
This does not establish that BeatReference represents a Ground Truth musical
beat or that its event-rate equivalent is musical tempo.

### SC-C1-02

**Scientific Conclusion:** The current reconstructed BeatReference grid is a
regularized representation determined by the mean spacing of distinct
ElementaryMetricEvent timestamps, with conditional halving above 0.8 seconds.
It does not preserve the dispersion of those input intervals in its output
spacing.

This conclusion applies to the current implementation and VAL-001 executions.
It does not determine whether regularization or conditional halving is
scientifically appropriate.

### SC-C1-03

**Scientific Conclusion:** Current reconstructed-measure meter and internal BPM
fields cannot serve as recognition evidence in Campaign 1 because they are
injected downstream. Measure duration combines the reconstructed grid with the
injected 120 BPM end extension.

This does not establish that the injected values are scientifically wrong; it
establishes only their provenance and observable consequence.

## Scientific risks

- The canonical MP3 path uses duplicated full-mix stems rather than independent
  source observations, limiting what its ensemble-consensus evidence can
  establish.
- Source-specific candidate populations and estimator outputs differ greatly;
  the current global-mean estimator is sensitive to which source evidence is
  supplied.
- The thresholded halving rule changes double-bass and tenor-sax periods but not
  other sources, without establishing musical metrical level.
- Beat-grid regularization produces near-zero output interval dispersion and
  may conceal input temporal variability.
- Most MP3 MetricClusters contain no event inside the 0.010-second association
  window after grid reconstruction.
- Injected measure semantics may be mistaken for recognized meter or tempo if
  provenance is not inspected.
- Controlled WAV single-source runs identify their internal source as `Mix`;
  external asset identity is therefore required to distinguish the stems.

## Proposed Architectural Impact

No architectural change is approved or required to preserve this experiment.

The evidence identifies `BeatPeriodEstimator` and its propagation through
`BeatGridReconstructor` as the smallest existing scientific boundary requiring
further controlled validation before any architectural proposal. No change is
proposed in this record.

## Smallest recommended next objective

Perform a controlled BeatPeriodEstimator hypothesis test that preserves the
actual distinct ElementaryMetricEvent interval population and evaluates the
observable consequence of the global-mean and `> 0.8 / 2` rules across the MP3
and five canonical stems. Do not implement a replacement estimator or assign a
musical metrical level in that experiment.

## Limitations

- `DummyMultiStemSeparator` does not provide independent MP3 sources.
- The four validation-facing recognition quantities remain `NOT_PRODUCED`.
- No tolerance, accuracy, score, PASS/FAIL or musical-equivalence rule exists.
- Controlled-dataset software version, generation date and rendering library
  remain `not specified` under M90.
- The experiment does not validate MusicXML-to-WAV temporal correspondence at
  the event level.

## Development Completion Protocol

- Documentation updates: **Not Applicable —** no canonical scientific or
  architectural claim was changed; evidence is preserved only in this new
  non-overwriting experimental record.
- Cross-reference verification: **Not Applicable —** canonical documentation
  was unchanged. All repository-relative input paths in the record were
  verified to exist.
- Focused automated tests: 34 passed, 2 dependency deprecation warnings.
- Complete automated suite: 981 passed, 1 known environment-dependent
  Demucs/MPS failure, 3 warnings.
- Scientific validation with VAL-001: completed through blind MP3 analysis,
  Immutable Analysis Representation, Comparator, and Scientific Validation
  Record.
- Controlled experimental validation: all five canonical WAV stems completed
  independently with the existing `NullSeparator` path.
- Repository consistency: JSON artifacts parsed successfully; `git diff
  --check` passed; canonical input checksums matched; the historical run was
  unchanged; unrelated working-tree changes remain excluded.
- Bootstrap regeneration: **Not Applicable —** canonical project knowledge,
  architecture, implementation, metadata, and test inventory were unchanged.
- Scientific Knowledge Record evaluation: applicable as a new immutable
  experimental record under F-030; no F-030 text change is required.
- Atomic commit readiness: ready as one experiment-only change containing
  `validation/VAL-001/run_20260809_065633/`.
- Push readiness: **Not Applicable —** push requires explicit human approval
  and was not performed.

## Artifact integrity

- `baseline.json`: `9f219660d933b9084190708b8b7ae9ef092c987aff767390750351e83a93090d`
- `diagnostics.json`: `8063519bae4d60696515194d9982af755635b29cefc89ffbc6cb98cd82f86198`
- `report.json`: `1b62a7eed9b213a29b64e1ea557da7d7406734478d5bee5198db0dda3937ba9d`
- `runtime.log`: `ceaa3d6adaef444de4a0240b16a9bb7e785038bd23c6abe70724190fe765efeb`

These checksums exclude `notes.md` to avoid a self-referential integrity field.
