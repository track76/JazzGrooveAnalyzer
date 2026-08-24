# CED-VAL-005 Analytical Input Authority

Authority ID: **PR-CEDVAL005-ANALYTICAL-INPUTS-001**

Status: **FROZEN — PI REVIEW REQUIRED**

This authority executes only the verification required by
`PR-CEDVAL005-RAW-TRACK-ANALYTICAL-SOURCE-CONSTRUCTION-01`. It binds the
original checksum-authorized `09_Overheads.wav` to the experiment-local
`Drums / TEMPORAL_REFERENCE` role and the original checksum-authorized
`11_BassDI.wav` to the experiment-local `Double Bass / ACCOMPANIMENT` role.
Instrument identity does not assign either role automatically.

Two independent read-only verification passes reproduced the exact absolute
and relative paths, source labels, SHA-256 identities, WAVE container, signed
24-bit little-endian PCM encoding, 44,100 Hz sample rate, channel counts,
10,068,072-frame scope and `119858/525`-second duration. The first pass used
Python standard-library WAVE parsing and SHA-256; the second used `shasum`,
`file` and macOS `afinfo`. Their required results agree exactly.

The only shared temporal authority is
`COMMON_DISTRIBUTED_FILE_SAMPLE_COORDINATE`. Common hardware acquisition
clock, simultaneous capture, absence of editing, physical-onset Ground Truth
and sample-accurate human-microtiming Ground Truth remain `UNESTABLISHED`.

Calibration applicability remains `UNESTABLISHED`; correspondence remains
`GEOMETRIC_ONLY`. No controlled-dataset calibration transfers, H02 use,
strength use or `AUTHORIZED_EVENT_RELATION` are permitted. This freeze does
not establish physical onset, event correspondence, groove, rushing or
dragging, source isolation, or true performance microtiming.

No derived asset was created. JGA, EME, AD-038 localization and AD-040 profile
construction were not executed. The raw assets and production code remain
unchanged. Complete machine-readable evidence and the deterministic
fingerprint are preserved in `analytical_input_authority.json`.
