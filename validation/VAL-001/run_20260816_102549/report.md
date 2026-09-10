# H-VAL001-EME-BASS-01 — Double-Bass Peak Sensitivity

## Baseline and preregistration

The installed detector normalizes the onset envelope and uses peak-picking
defaults `pre_max=2`, `post_max=1`, `pre_avg=8`, `post_avg=9`, `wait=2` frames
and `delta=0.07` at 44.1 kHz with a 512-sample hop. Only `delta`, the
peak-above-local-average requirement, varied. The preregistered scale-symmetric
set was `0.035`, `0.07`, and `0.14`. Production defaults, temporal windows and
the downstream 0.10-strength/30-ms filter remained unchanged.

Each configuration ran twice on the checksum-bound double-bass WAV. Blind
records were byte-identical and frozen before MusicXML access.

## Blind populations

| Configuration | Raw peaks | Filtered PulseCandidates / derived EME | Added frames vs baseline | Lost frames vs baseline | Ordered |
|---|---:|---:|---:|---:|---|
| DELTA_HALF (`0.035`) | 28 | 28 | 2 | 1 | yes |
| BASELINE (`0.07`) | 27 | 27 | 0 | 0 | yes |
| DELTA_DOUBLE (`0.14`) | 26 | 26 | 2 | 3 | yes |

All frames common with baseline retained exact timestamps. `DELTA_HALF` did
not simply add one event: it shifted one baseline detection by one frame and
introduced one further frame. `DELTA_DOUBLE` similarly substituted frames
rather than producing a strict subset.

## Post-blind validation

Ground Truth was loaded only after the blind record checksum was frozen. The
authoritative population contained 28 bass events. Expected timestamps used
the declared score-zero/WAV-zero origin and 78 quarter BPM. Correspondence
required unique one-to-one assignment within the preregistered single-frame
measurement-resolution bound of `0.011609977324263039` seconds.

| Configuration | Correspondences | Missed symbolic | Extra candidates | Duplicate assignments | Status |
|---|---:|---:|---:|---:|---|
| DELTA_HALF | 0 | 28 | 28 | 0 | FAILED |
| BASELINE | 0 | 28 | 27 | 0 | FAILED |
| DELTA_DOUBLE | 0 | 28 | 26 | 0 | FAILED |

The 28-count result is not accepted. Count equality coincides with population
substitution and no scientifically supported event correspondence. Existing
score-to-audio localization evidence is insufficient for selecting any tested
configuration.

## Conclusion

Bass status: **FAILED** under the preregistered success rule. No production
change is justified. The next causal issue is the controlled bass
score-to-physical-attack mapping; further peak-threshold tuning would be
implementation-driven until that mapping is validated.

