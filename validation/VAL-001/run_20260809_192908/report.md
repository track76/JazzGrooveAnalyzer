# H-VAL001-C1-07 — Controlled Temporal-Scaling Experiment

## Status

Complete. Asset validation passed, both neutral conditions were frozen before
Ground Truth access, and post-blind evaluation completed.

## Controlled conditions

- Condition A: `CED-VAL-001-TS-001-A` — quarter note = 78 BPM
- Condition B: `CED-VAL-001-TS-001-B` — quarter note = 110 BPM

Condition A is byte-identical to the authoritative VAL-001 MusicXML. Condition
B differs only in both authoritative `<per-minute>` declarations. All six
audio assets use the declared identities; the Condition B WAVs are distinct
from H-VAL001-C1-06.

## Asset evidence

All WAVs are stereo 24-bit PCM at 44.1 kHz. Condition A contains 1,983,488
samples per channel (44.9770521542 seconds); Condition B contains 1,470,464
samples (33.3438548753 seconds). Canonical and repeat extents match within each
condition. All four WAVs have first acoustic activity at frame 1.

Condition A repeated renders differ at the sample level but produce identical
Candidate Period duration/count populations. Condition B canonical and repeat
WAVs are byte-identical and likewise produce identical populations. Independent
rendering remains a Declared Experimental Procedure rather than an independently
observed provenance fact.

## Blind evidence

Ground Truth, MusicXML, tempo declarations, condition meaning and expected
scaling were unavailable during discovery.

| Blind condition | PulseCandidates | Candidate Periods | Frame intervals |
|---|---:|---:|---|
| BLIND-CONDITION-01 | 39 | 9 | 32, 33, 34, 66, 67, 99, 100, 133, 232 |
| BLIND-CONDITION-02 | 39 | 6 | 23, 24, 47, 71, 116, 165 |

Deterministic replay and the corresponding repeated-render populations were
identical for both conditions.

## Post-blind evaluation

Ground Truth supplies quarter note = 78 BPM for A and quarter note = 110 BPM
for B. The mathematically derived temporal scale B/A is `78/110`, or
`0.709090909090909...`.

Several frozen B candidates are numerically near scaled A durations. Examples
include 34 → expected 24.109... versus observed 24 frames; 66 → expected 46.8
versus observed 47; 100 → expected 70.909... versus observed 71; and 232 →
expected 164.509... versus observed 165. These are descriptive numerical
relationships only.

No exact frame-domain pair satisfies the authoritative `78/110` scale. Because
repository authority defines no correspondence tolerance, the experiment
cannot classify near frame relationships as equivalent.

## Scientific classification

**EVIDENCE INSUFFICIENT**

The observations are compatible with temporal scaling for several candidate
durations, but exact support is absent under the authorized equality semantics.
This result neither supports nor rejects musical meaning, beat, tempo, tactus,
subdivision, hierarchy or metric level.

## Evidence records

- `audio_asset_validation.json`
- `blind_results.json`
- `post_blind_evaluation.json`
- `validator_result.json`
- `artifact_manifest.json`
