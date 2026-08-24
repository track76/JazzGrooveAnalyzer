# CED-VAL-006 Minimal Analytical Input Authority

Authority ID: **PR-CEDVAL006-ANALYTICAL-INPUTS-001**

Status: **FROZEN ANALYTICAL INPUT AUTHORITY**

Analytical-input fingerprint:
`cf89598f0f198cb14ee4f455b4094cffe3e4b4597da4fd92d2fffba41a233bae`

This authority is bound to
`PR-CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK-001`, dataset fingerprint
`9d837f710fbf3292c80490d499bc96df0a8fe1140bc9139b65de8a553c4c2eca`,
at commit `0ac756e1abef8e1c25fe4cc501db008e064210b1`.

## Frozen selections and roles

The exact original raw file
`Dums Overheads LCT 640 TS-Dual Output Mode.wav` is frozen as:

- analytical source: `Drums`;
- experiment-local role: `TEMPORAL_REFERENCE`; and
- handling: original raw file selected directly without derivation or
  processing.

The exact original raw file `BASS - DI.wav` is frozen as:

- analytical source: `Double Bass`;
- experiment-local role: `ACCOMPANIMENT`; and
- handling: original raw file selected directly without derivation or
  processing.

Instrument identity does not assign either role automatically. These bindings
are the PI-approved experiment-local authority.

## Verification

Two fresh-process, read-only verification passes independently reproduced the
exact paths, dataset-manifest bindings, SHA-256 values, RIFF/WAVE headers,
signed 24-bit little-endian PCM representation, 48,000 Hz sample rate,
channel counts, 11,912,868-frame scopes, and 248.184750-second durations.
Their complete derived authority records were byte-identical.

Drums authority:

- absolute path:
  `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw/Dums Overheads LCT 640 TS-Dual Output Mode.wav`;
- SHA-256:
  `dbfc4c3c59cac2c42cb2bbd33f1e55dbb1ec8c2fe6c6d095e30efc791dd57b8d`;
- stereo, 48,000 Hz, signed 24-bit little-endian PCM;
- 11,912,868 frames per channel; file-coordinate scope
  `[0, 11912868)`; and
- exact duration `11912868/48000` seconds (248.184750 seconds).

Double Bass authority:

- absolute path:
  `/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw/BASS - DI.wav`;
- SHA-256:
  `c0a99f65158d12a69e062cc990e86631a0d29d7e83f30537d34eb301516855a9`;
- mono, 48,000 Hz, signed 24-bit little-endian PCM;
- 11,912,868 frames per channel; file-coordinate scope
  `[0, 11912868)`; and
- exact duration `11912868/48000` seconds (248.184750 seconds).

The frozen shared authority is
`COMMON_DISTRIBUTED_FILE_SAMPLE_INDEX_SCOPE`. It establishes equal file-local
sample-zero, sample rate, frame count, and distributed scope for these two
assets. Their exact cross-file mapping to a common session-time origin remains
`UNESTABLISHED / NOT EXPLICITLY DOCUMENTED`; shared hardware acquisition clock
also remains `UNESTABLISHED / NOT EXPLICITLY DOCUMENTED`.

## Preserved scientific limits

LEWITT's primary provider declaration supports the live band recording and
supports RAW/no-editing/no-tuning exactly to the extent stated by LEWITT.
Undocumented acquisition-system details are not inferred. Overall acquisition
authority remains `ACQUISITION_AUTHORITY_PARTIAL`.

Physical-onset Ground Truth remains `NOT ESTABLISHED`. Calibration
applicability remains `UNESTABLISHED`. This authority does not establish event
correspondence, physical onset, source isolation, acquisition-time human
microtiming, synchronization, rushing/dragging, swing, groove, intention, or
performance quality.

No derived analytical asset was created. Bleed, if present, remains unchanged.
No mixing, trimming, shifting, alignment, normalization, resampling,
filtering, gating, denoising, compression, EQ, transient processing, source
separation, quantization, warping, or timing correction was performed.

JGA and external beat trackers were not executed. H02, strength, BPM, musical
interpretation, and CED-VAL-005 comparison were not used. Raw assets,
production code, and historical scientific authorities remain unchanged.

The complete machine-readable evidence is frozen in
`analytical_input_authority.json`; deterministic verification is provided by
`verify_analytical_inputs.py`.
