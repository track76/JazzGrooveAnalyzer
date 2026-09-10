# Canonical Observable Rhythm-Section Timing Report Millisecond Acceptance

Protocol ID: `H-VAL001-CANONICAL-TIMING-REPORT-MILLISECOND-ACCEPTANCE-01`

Status: **FROZEN BEFORE EXECUTION**

## Scientific target

Validate that JGA reports every authorized observable accompaniment EME with
its absolute timeline coordinate and neutral signed displacement relative to
the authorized Drum reference, expressed in milliseconds, with deterministic
provenance.

## Inputs and population

- `recordings/validation/stems/drums.wav`, SHA-256
  `d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd`,
  role `TEMPORAL_REFERENCE`, expected 63 EME.
- `recordings/validation/stems/piano.wav`, SHA-256
  `26fa1158f375598cc7c01e04379c00547ef1787f6862eb2f29a36aafd9007c7e`,
  role `ACCOMPANIMENT`, expected 49 EME.
- `recordings/validation/stems/double_bass.wav`, SHA-256
  `31d6f2e34d360c6f8f75362187433f2a2c1f5eb5cbbfe627305e99d07d8be6c5`,
  role `ACCOMPANIMENT`, expected 27 EME.

No symbolic Ground Truth is an input. No missing event is represented.

## Schema decision

Retain schema family ID `JGA_RHYTHM_SECTION_TIMING_REPORT_V1` and increment
`schema.version` from `1` to `2`. Version 2 is an additive serialization
revision. It preserves every version-1 seconds field and adds only:

- `distance_from_preceding_ms`;
- `distance_from_following_ms`; and
- `nearest_displacement_ms`.

Each value is the existing AD-038 property defined as its corresponding
authoritative seconds value multiplied by `1000.0`. A null seconds value maps
to null. No rounding, quantization, correction or additional precision claim
is permitted. Seconds remain authoritative.

## Acceptance procedure

Run the canonical CLI twice in fresh processes with identical scientific
arguments and different output paths. For each of the 76 accompaniment EME,
compare the serialized record with a fresh unchanged AD-038 construction from
the same authorized EME population. Require exact equality of target and Drum
identities, seconds timestamps, signed seconds displacements, boundary nulls,
tie status, temporal origin, lineage and rule/execution provenance.

Require exact binary64 equality between every non-null millisecond field and
the corresponding AD-038 millisecond property. Require byte-identical report
files and equal scientific fingerprints.

## Pass rule

Pass only if all of the following hold:

- Drums/Piano/Double Bass EME counts are 63/49/27;
- all 76 accompaniment EME have exactly one AD-038 localization and one AD-040
  relationship;
- producer frame/sample coordinates round-trip unchanged;
- all seconds, identities, signs, boundary/tie states and provenance match;
- all millisecond equalities hold;
- all relationships remain `GEOMETRIC_ONLY`;
- both canonical files and fingerprints are identical; and
- every firewall remains serialized.

Any failure yields `FAIL_SCIENTIFIC_INTEGRATION_CONFLICT` without repair or
reinterpretation.

## Claim firewall

This validates reporting of the already-observable controlled population only.
It establishes no BPM, meter, beat/downbeat identity, groove, swing,
rushing/dragging, musical correspondence, physical onset, missing-event
recovery, source recovery, Ground-Truth match, timing correction, added
measurement precision or acquisition-clock synchrony.
