# H-VAL001-C1-10 — Measurement-Process Perturbation Invariance Audit

## Status

Complete. No production implementation or architecture change was required.

## Scientific question

What observational properties remain invariant, and which cease to remain
invariant, under controlled perturbations of the measurement process?

## Evidence unavailable before this experiment

H-VAL001-C1-08 varied discrete measurement after freezing observations.
H-VAL001-C1-09 used different audio sample populations, but independent
detection remained exactly identical. Neither experiment measured independent
detection after a perturbation that changed detector/grid phase while
preserving exact source-sample lineage.

## Perturbation selection

A 256-sample audio-origin shift was selected because it is exactly half the
existing 512-sample observation hop. It changes one declared measurement
condition while preserving all nonzero sample values, sample ordering, sample
rate, bit depth, channel count, sample count, duration and analysis
configuration. The removed 256-sample tail was verified to contain only zeros.

Changing Candidate Period frame length or grid origin without redetection was
already tested by C1-08. Rendering variation was tested by C1-09. Resampling,
noise and compression would introduce additional transformations and were not
required for this first discriminating experiment.

The derived 24-bit WAV is preserved under external operational storage and is
referenced by checksum; it is not duplicated in the repository.

## Blind design

The source and perturbed WAVs were assigned neutral identities and processed
independently through the existing `AnalysisPipeline`, `NullSeparator`,
filtered `PulseCandidate` population and AD-035 Candidate Period discovery.
The perturbation, condition relationship, MusicXML, Ground Truth and all metric
semantics were unavailable to blind discovery.

The complete blind execution was repeated. Candidate Period populations were
instantiated through the immutable M91 representation before serialization.

## Blind observed facts

- BLIND-AUDIO-01 produced 39 PulseCandidates and 9 Candidate Periods.
- BLIND-AUDIO-02 produced 41 PulseCandidates and 9 Candidate Periods.
- Complete replay was byte-identical.
- Blind fingerprint:
  `9b2622c9828ce109bd3f9600e59c8013ba0c44e6bdf09f03c522ecc740defe94`.
- Frozen blind record SHA-256:
  `5c5ec892ca74876e6af950a30eb584c0c6900571d4974821362924d0f89884e4`.

## Post-blind observed facts

After revealing the declared 256-sample shift:

- zero detected timestamps were exactly aligned after reversing the shift;
- observation count changed from 39 to 41;
- strength sequences differed;
- confidence sequences differed because their lengths differed;
- deterministic replay remained identical for both inputs;
- both Candidate Populations contained 9 periods;
- 7 Candidate Period durations occurred numerically in both populations;
- the complete Candidate Populations were not identical;
- source-only durations were `0.37151927437641724` and
  `1.5441269841269842` seconds;
- perturbed-only durations were `0.18575963718820862` and
  `1.9156462585034013` seconds;
- none of the 7 shared durations retained two exactly aligned supporting
  timestamp pairs under the C1-09 criterion;
- the frozen blind record checksum remained unchanged.

Indexwise offset values were preserved only as descriptive quantities. Because
observation counts differ, index order does not establish event identity.

## Scientific interpretation

The current observation process is deterministic but sensitive to audio origin
relative to its frame grid. Reproducibility therefore does not imply invariance
under a declared measurement perturbation.

Candidate count alone remained invariant, and most durations were numerically
shared, while recurrence populations and supporting observations changed.
Under F-032, numerical sharing does not establish correspondence. Exact
lineage-supported correspondence was not established for any candidate in the
perturbed condition.

The result does not prove that correspondence is broken: no authorized rule
establishes identity between the 39 and 41 independently detected observation
populations. Absence of exact support remains scientifically indeterminate.

## Hypothesis evaluation

### Supported

1. Some aggregate properties can remain invariant while their supporting
   observations and complete Candidate Population change.
2. Candidate Period numerical recurrence alone is insufficient to establish
   cross-condition correspondence.
3. A half-frame audio-origin perturbation can reproducibly change observation
   count, localization and Candidate Period evidence.
4. Identical-input observation and Candidate Period production remains
   deterministic under both declared conditions.

### Rejected within this scope

1. Independent detection is invariant under a 256-sample audio-origin shift.
2. Equal Candidate Period count implies preservation of the Candidate
   Population.
3. A numerically shared Candidate Period duration alone preserves the C1-09
   exact supporting-event correspondence.

### Not established

- that any Candidate Period correspondence is broken rather than presently
  unidentifiable;
- that timestamp difference is the fundamental variable;
- that frame-grid phase is the sole causal mechanism;
- any beat, tempo, meter, tactus, subdivision, hierarchy or metric identity.

## Scientific conclusion

**DETERMINISTIC OBSERVATIONAL SENSITIVITY ESTABLISHED; CROSS-PERTURBATION
CANDIDATE CORRESPONDENCE REMAINS INDETERMINATE.**

## Recommended next scientific objective

Determine which existing observation evidence, if any, can preserve source
event identity when a controlled perturbation changes the number and location
of detected PulseCandidates. This is an evidence audit, not an implementation
objective. No production implementation or architectural evolution is yet
justified.
