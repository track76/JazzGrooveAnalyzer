# PR-CED-VAL-008-VARIABLE-TEMPO-BENCHMARK-001

Status: **PASS — FROZEN PROSPECTIVE SYMBOLIC BEAT GROUND TRUTH**

This record freezes the independent input authority for
`CED-VAL-008-VARIABLE-TEMPO-BENCHMARK`. It precedes and is independent of any
JGA, librosa, or Essentia observation. The repository artifacts bind the
unchanged source assets, technical PCM scope, prospectively authored Ableton
tempo map, and its analytically derived 64-event symbolic beat schedule.

## PI filename adjudication

The earlier one-space filename declaration is classified
`SUPERSEDED_DESCRIPTIVE_FILENAME_DECLARATION`. The PI accepted the exact
checksum-bound filenames physically present, each containing two spaces after
`v0.1`, as `AUTHORITATIVE_RAW_ASSET_IDENTITIES`. No source was renamed,
modified, or regenerated. Exact paths and checksums are frozen in
`input_authority_manifest.json`; AppleDouble `._*` files are not scientific
assets.

## Prospective musical and tempo-map authority

The PI declares 4/4, sixteen measures, 64 quarter-note positions indexed
0–63, and arrangement `1.1.1` as both symbolic time zero and exported sample
zero. Direct inspection of the checksum-bound primary Ableton Live Set found
matching discontinuous master-tempo automation: 120 BPM through arrangement
beat 16, then 100 BPM; 140 BPM at beat 32; and 110 BPM at beat 48. These are
positions `5.1.1`, `9.1.1`, and `13.1.1`. The transport range is 0–64 beats.

`symbolic_beat_reference.json` is the `SYMBOLIC_BEAT_GROUND_TRUTH`. Its event
times are analytic cumulative rational values from the frozen tempo map, not
detections from either WAV. Beat spacings are `1/2`, `3/5`, `3/7`, and `6/11`
seconds, or `22050`, `26460`, `18900`, and `264600/11` samples at 44,100 Hz.
Fifty positions are integer sample coordinates. Fourteen positions in the
110 BPM segment are non-integer; the exact irreducible rational coordinate and
its surrounding floor and ceiling samples are preserved. Neither bounding
sample is substituted for symbolic authority or claimed as physical onset.

## PCM and render scope

Both scientific WAVs independently verify as readable RIFF/WAVE signed
24-bit linear PCM, stereo, 44,100 Hz, with 1,463,433 frames and exact scope
`[0,1463433)`. Their common duration is `487811/14700` seconds. The exact
symbolic end of measure 16 is `12776/385` seconds or `16097760/11` samples;
the discrete WAV scope ends at the first integer frame boundary after that
symbolic endpoint. No normalization, mono conversion, dither, trimming,
resampling, or regeneration was performed by this objective.

## Scientific roles and response firewall

`DRUM GT` is a candidate controlled audio input for the future comparison.
`MARKER GT` is a candidate rendered temporal-reference channel, not Ground
Truth. No rendered onset, latency, displacement, physical response, threshold
crossing, beat detection, onset detection, or musical correspondence was
measured. No result or calibration constant was transferred from CED-VAL-004
or CED-VAL-007.

## Future purpose and execution firewall

The later purpose is to compare JGA observational timing, librosa
`beat_track`, and Essentia `RhythmExtractor2013` against exactly this same
prospectively frozen nonuniform schedule. That future study may evaluate beat
recovery, precision, recall, F1, signed and absolute error, RMSE, transition
behavior, regional stability, nonuniform-timeline usefulness,
reproducibility, local-tempo usefulness, independence, and provenance. This
authority freeze executes none of those systems and selects no winner.

JGA, librosa, Essentia, H02, strength, and confidence-based selection were not
executed or accessed. Production code, architecture, historical authorities,
CED-VAL-007, the Live Set, and raw audio remain unchanged.
