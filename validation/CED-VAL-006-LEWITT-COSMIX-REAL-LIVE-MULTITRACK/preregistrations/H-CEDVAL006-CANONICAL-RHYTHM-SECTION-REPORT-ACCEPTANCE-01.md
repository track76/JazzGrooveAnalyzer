# CED-VAL-006 Canonical Rhythm Section Report Acceptance

Preregistration ID:
`H-CEDVAL006-CANONICAL-RHYTHM-SECTION-REPORT-ACCEPTANCE-01`

Status: **FROZEN PROSPECTIVE ACCEPTANCE PROTOCOL — NOT EXECUTED**

## Scientific question

Can the unchanged implementation at commit
`39620901048053e4159faad78065a2703a586b5e` compose the frozen CED-VAL-006
real-audio analytical sources into `JGA_RHYTHM_SECTION_TIMING_REPORT_V1`,
preserving AD-037 EME, AD-038 neutral geometry, AD-040 profile authority and
exact deterministic replay without introducing new scientific meaning?

## Input and role authority

- Dataset authority:
  `PR-CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK-001`;
  fingerprint
  `9d837f710fbf3292c80490d499bc96df0a8fe1140bc9139b65de8a553c4c2eca`.
- Analytical-input authority: `PR-CEDVAL006-ANALYTICAL-INPUTS-001`;
  fingerprint
  `cf89598f0f198cb14ee4f455b4094cffe3e4b4597da4fd92d2fffba41a233bae`.
- `Drums` / `TEMPORAL_REFERENCE`:
  `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw/Dums Overheads LCT 640 TS-Dual Output Mode.wav`;
  SHA-256
  `dbfc4c3c59cac2c42cb2bbd33f1e55dbb1ec8c2fe6c6d095e30efc791dd57b8d`.
- `Double Bass` / `ACCOMPANIMENT`:
  `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw/BASS - DI.wav`;
  SHA-256
  `c0a99f65158d12a69e062cc990e86631a0d29d7e83f30537d34eb301516855a9`.
- Both inputs remain original unmodified signed 24-bit PCM at 48,000 Hz with
  exactly 11,912,868 frames on the frozen distributed-file coordinate.

## Frozen invocation

The execution ID for both fresh-process replay calls is
`EXEC-CEDVAL006-CANONICAL-REPORT-ACCEPTANCE-01`. The provenance ID is the
dataset authority ID; role authority ID/fingerprint are the analytical-input
authority ID/fingerprint. The implementation revision is the exact commit
above. The two output paths differ only as transport destinations and are not
scientific-content fields.

The canonical entry point is:

```text
PYTHONPATH=src .venv/bin/python tools/run_rhythm_section_timing_report.py
  --source TEMPORAL_REFERENCE=Drums=<frozen Drum path>
  --source ACCOMPANIMENT=Double Bass=<frozen Bass path>
  --expected-sha256 Drums=<frozen Drum SHA-256>
  --expected-sha256 Double Bass=<frozen Bass SHA-256>
  --execution-id EXEC-CEDVAL006-CANONICAL-REPORT-ACCEPTANCE-01
  --provenance-id PR-CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK-001
  --role-authority-id PR-CEDVAL006-ANALYTICAL-INPUTS-001
  --role-authority-fingerprint <frozen analytical-input fingerprint>
  --jga-revision 39620901048053e4159faad78065a2703a586b5e
  --output <execution-specific JSON path>
```

## Prospective invariants

The immutable historical authority is
`EXEC-CEDVAL006-REAL-LIVE-AUDIO-20260824-183919`, scientific fingerprint
`8c5723fbeabe2031516b2eeee0c83fb42ad84f46824cf65f5d485c6cf6c82b5c`.
Only invariant scientific quantities are compared:

- Drums EME: 909;
- Double Bass EME: 1,055;
- AD-038 eligible/localized/unresolved: 1,055 / 1,055 / 0;
- AD-038 equal-distance ties: 4;
- AD-040 represented: 909 Drums + 1,055 Double Bass = 1,964;
- correspondence: `GEOMETRIC_ONLY` throughout accompaniment relationships;
- calibration applicability: `UNESTABLISHED`; correction: none.

Historical serialization, execution IDs, report/profile identities and
fingerprints are not equality targets.

## Replay and verification

Two complete executions must run in fresh processes after this protocol is
checksum-frozen. Their canonical JSON bytes and report fingerprints must be
identical. Mechanical verification must independently confirm schema/version,
invocation and source authorities, checksums, roles, environment provenance,
observation/EME populations, AD-038 content, AD-040 content, correspondence,
calibration, claim firewall and recomputed report fingerprint.

## Acceptance classification

`PASS_REAL_AUDIO_ACCEPTED` requires every authority, invariant, replay,
fingerprint, provenance and firewall gate to pass. Any discrepancy is
`FAIL_SCIENTIFIC_INTEGRATION_CONFLICT` and stops without repair or semantic
reinterpretation.

## Scientific firewall

This acceptance cannot establish beat identity, musical correspondence, BPM,
tempo, meter, downbeat, swing, groove, rushing, dragging, intention, human
microtiming, physical onset, acquisition-clock synchrony or calibrated timing
correction. It does not use H02, strength, external trackers, Ground Truth or
musical-role inference. CED-VAL-006 acquisition authority remains partial.
