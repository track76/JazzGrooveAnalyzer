# H-VAL001-C1-09 — Independent-Audio Candidate Period Lineage Audit

## Status

Complete. Four WAV assets were analyzed independently and blindly through the
existing pipeline. No production implementation or architecture change was
required.

## Scientific question

Can lineage-supported Candidate Period correspondence be reproduced when
observations originate from independently rendered and independently detected
audio rather than from remeasurement of the same frozen observation
population?

## Evidence unavailable before this experiment

H-VAL001-C1-08 established lineage-supported correspondence only after a
deterministic transformation of one frozen observation population. It did not
test rendering variation or independent onset detection.

## Experimental design

The canonical and repeated-render WAV assets for both conditions of
`CED-VAL-001-RD-001` were assigned four neutral blind identities. Each was
processed independently with the existing `AnalysisPipeline`,
`NullSeparator`, filtered `PulseCandidate` population and AD-035 Candidate
Period discovery at a declared 512-sample frame length.

Ground Truth, MusicXML, rendering lineage, condition relationships, tempo,
beat, meter and metric level were excluded during blind discovery. Every
Candidate Period population was instantiated through the deeply immutable M91
representation before serialization. The complete blind execution was
repeated before post-blind evaluation.

The experiment-local criterion was:

> Under identical declared observation conditions and authoritatively shared
> symbolic/render lineage, Candidate Periods have independent-audio lineage
> support only when at least two independently detected adjacent observation
> pairs have exactly identical start and end timestamps.

The criterion introduces no tolerance, ordering substitution, proximity rule,
ranking or musical interpretation. It is sufficient within this experiment;
it is not asserted to be necessary generally.

## Blind observed facts

- BLIND-AUDIO-01 produced 39 PulseCandidates and 9 Candidate Periods.
- BLIND-AUDIO-02 produced 39 PulseCandidates and 9 Candidate Periods.
- BLIND-AUDIO-03 produced 37 PulseCandidates and 7 Candidate Periods.
- BLIND-AUDIO-04 produced 37 PulseCandidates and 7 Candidate Periods.
- Two complete blind executions were byte-identical.
- Blind scientific fingerprint:
  `5b759ea7f87b92fd6362daf5871e61d32c3d59466d63603d007907fd99ab969e`.
- Frozen blind record SHA-256:
  `db87bf3ca626866960e6f8f6fdc137affb6d514bb2457969486b31ed09a6a1c1`.

## Post-blind observed facts

The controlled dataset record declares each pair to share one symbolic
condition and rendering procedure. File and sample-data checksums establish
that the canonical and repeated WAVs are different audio assets.

- Condition A: all 39 detected timestamps were exactly shared; all 9 Candidate
  Periods satisfied the criterion.
- Condition B: all 37 detected timestamps were exactly shared; all 7 Candidate
  Periods satisfied the criterion.
- Every indexwise detected-timestamp offset was zero frames.
- The blind record checksum remained unchanged after post-blind evaluation.

## Scientific interpretation

Within these declared conditions, different independently rendered sample
populations can yield identical independently detected temporal observations.
Exact supporting-event lineage therefore reproduces all discovered Candidate
Period evidence without reusing or transforming a frozen observation
population.

The evidence does not establish correspondence when independently detected
timestamps differ. It does not show that exact timestamp identity is necessary,
does not isolate the renderer or detector contribution, and establishes no
beat, tempo, meter, tactus, subdivision, hierarchy or metric-level meaning.

## Scientific conclusion

**INDEPENDENT-AUDIO LINEAGE-SUPPORTED CORRESPONDENCE REPRODUCED WITHIN THE
DECLARED EXACT-DETECTION SCOPE.**

The H-VAL001-C1-08 lineage proposition gains empirical support beyond
deterministic remeasurement: all Candidate Periods in two independently
rendered pairs retained exact supporting-event lineage after independent blind
detection.

## Limitations and open question

- Rendering application, rendering-library version and generation date remain
  `not specified` in the authoritative provenance.
- The controlled primary/repeat assets share declared rendering settings.
- The experiment cannot evaluate correspondence for non-identical detected
  timestamps because no authorized criterion exists for that case.
- Procedural input blinding prevents condition semantics from entering the
  pipeline; it is not an investigator-blinding claim.

## Recommended next scientific objective

Test independent render/detection lineage under one declared rendering or
measurement perturbation that produces non-identical detected timestamps while
preserving authoritative source-event identity. This is the smallest evidence
gap remaining from the present result. No production implementation or
architectural change is currently justified.
