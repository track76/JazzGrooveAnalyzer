# CED-VAL-006 Canonical Rhythm Section Report Repeat Acceptance

Preregistration ID:
`H-CEDVAL006-CANONICAL-RHYTHM-SECTION-REPORT-ACCEPTANCE-02`

Status: **FROZEN PROSPECTIVE REPEAT ACCEPTANCE PROTOCOL — NOT EXECUTED**

## Motivation and immutable negative evidence

This protocol repeats exactly the scientific acceptance question frozen by
`H-CEDVAL006-CANONICAL-RHYTHM-SECTION-REPORT-ACCEPTANCE-01` after the bounded
Reporting/Application correction at commit
`c1990328a08976de21c5e712d6fce9a8cde9abe2`. The original failed acceptance
`ACC-CEDVAL006-CANONICAL-RHYTHM-SECTION-REPORT-01`, result fingerprint
`68778f240a91e57cca92d5e30b5849bcc7ad160a569e7c9439847d52480cb811`,
remains immutable negative scientific evidence.

## Scientific question

Can `JGA_RHYTHM_SECTION_TIMING_REPORT_V1` compose the same frozen CED-VAL-006
real-audio sources while preserving AD-037 EME, AD-038 neutral geometry,
AD-040 profile authority, calibration applicability/application/correction,
the acquisition-clock firewall, and exact fresh-process replay without new
scientific meaning?

## Frozen inputs and roles

- Dataset authority:
  `PR-CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK-001`; fingerprint
  `9d837f710fbf3292c80490d499bc96df0a8fe1140bc9139b65de8a553c4c2eca`.
- Analytical/role and calibration-applicability authority:
  `PR-CEDVAL006-ANALYTICAL-INPUTS-001`; fingerprint
  `cf89598f0f198cb14ee4f455b4094cffe3e4b4597da4fd92d2fffba41a233bae`.
- `Drums` / `TEMPORAL_REFERENCE`:
  `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw/Dums Overheads LCT 640 TS-Dual Output Mode.wav`;
  SHA-256
  `dbfc4c3c59cac2c42cb2bbd33f1e55dbb1ec8c2fe6c6d095e30efc791dd57b8d`.
- `Double Bass` / `ACCOMPANIMENT`:
  `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw/BASS - DI.wav`;
  SHA-256
  `c0a99f65158d12a69e062cc990e86631a0d29d7e83f30537d34eb301516855a9`.
- Both inputs: unmodified signed 24-bit PCM, 48,000 Hz, 11,912,868 frames.

## Frozen invocation

Two fresh processes use execution ID
`EXEC-CEDVAL006-CANONICAL-REPORT-ACCEPTANCE-02`, the source labels and roles
above, exact checksum gates, dataset provenance ID, analytical role authority,
implementation revision `c1990328a08976de21c5e712d6fce9a8cde9abe2`, and:

- calibration applicability: `UNESTABLISHED`;
- calibration application: `NOT_APPLIED` (workflow invariant);
- calibration correction: `NONE` (workflow invariant);
- calibration authority ID/fingerprint: the frozen analytical-input authority.

Only output transport paths differ between calls and they are not scientific
content.

## Prospective invariant comparison

Against immutable historical execution
`EXEC-CEDVAL006-REAL-LIVE-AUDIO-20260824-183919`, fingerprint
`8c5723fbeabe2031516b2eeee0c83fb42ad84f46824cf65f5d485c6cf6c82b5c`:

- Drums EME: 909;
- Double Bass EME: 1,055;
- AD-038 eligible/localized/unresolved: 1,055 / 1,055 / 0;
- AD-038 equal-distance ties: 4;
- AD-040 represented: 909 Drums + 1,055 Double Bass = 1,964;
- correspondence: `GEOMETRIC_ONLY`;
- calibration applicability/application/correction:
  `UNESTABLISHED` / `NOT_APPLIED` / `NONE`;
- firewall contains `ACQUISITION_CLOCK_SYNCHRONY_NOT_ESTABLISHED` and every
  previously serialized prohibition.

Historical serialization, execution identities and fingerprints are not
equality targets.

## Replay and decision rule

After checksum-freezing this protocol, execute the complete CLI twice in fresh
processes. Canonical JSON bytes, scientific content, identities/timestamps,
AD-038 content, AD-040 content and report fingerprints must agree exactly.
Every input, invariant, provenance, firewall and fingerprint gate must pass for
`PASS_REAL_AUDIO_ACCEPTED`; otherwise stop as
`FAIL_SCIENTIFIC_INTEGRATION_CONFLICT` without repair.

## Claim firewall

This acceptance establishes workflow integration and reproducibility only. It
does not establish beat identity, musical correspondence, BPM, tempo, meter,
downbeat, swing, groove, rushing, dragging, intention, human microtiming,
physical onset, acquisition-clock synchrony or calibrated correction. It uses
no H02, strength, external tracker, Ground Truth or automatic role inference.
