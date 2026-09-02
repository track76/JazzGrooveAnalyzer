# CED-VAL-010 known-source spectro-temporal timbre characterization

Protocol: `H-CEDVAL010-BASS-PIANO-SPECTROTEMPORAL-TIMBRE-01`

Protocol fingerprint: `0504d3745ee1ab06cdab1ecb82efc1244f19c13ed112b9b89af0c92e5d153332`

Protocol commit: `e55678a`

Primary freeze commit: `ed55745`

## Method and evidence

The primary populations are 206 deterministic source-local windows from the
provider-labelled `06_BassDI.wav` and 206 windows from `07_Piano.wav`. One
maximum positive-flux anchor was retained per jointly eligible fixed one-second
block without a magnitude cutoff. This construction controls long digital
silence only; it is not a note, onset, activity, source-identity or classifier
rule.

For every source, the experiment preserves all complete-frame 4096-point STFT
power spectra through 8 kHz (2048-sample periodic-Hann frames, 256-sample hop),
frame coordinates, frequency coordinates, and complete window indices. The
separate measurements are attack power rise/time-to-peak/flatness/high:low
ratio; centroid attack/change; bandwidth attack/change; low/mid/high flux
attack/persistence; spectral slope attack/change; harmonic-partial
decay/persistence; and F0-estimator availability/continuity. No composite was
formed.

Both fresh primary executions were byte-identical for representations,
episodes, measurements and result. Primary result fingerprint:
`bde797f90f556213fd0aa9cd9b46d02ae04be4c961f80d6dc978846a1e1ff40d`.

## Primary BassDI versus Piano

Positive effects mean BassDI is higher; negative effects mean Piano is higher.
All frozen endpoints are shown, including weak and null results.

| Family / endpoint | BassDI median | Piano median | Cliff's delta | Rank AUC | 95% delta CI |
|---|---:|---:|---:|---:|---:|
| Attack: log-power rise dB | 14.8745 | 10.6713 | +0.2811 | 0.6406 | [0.1699, 0.3922] |
| Attack: time to peak s | 0.01161 | 0.01161 | -0.3317 | 0.3342 | [-0.4338, -0.2279] |
| Attack: spectral flatness | 6.15e-8 | 8.62e-4 | -0.9601 | 0.0199 | [-0.9896, -0.9181] |
| Attack: high/low ratio dB | -80.6224 | -19.6308 | -0.9847 | 0.0076 | [-0.9988, -0.9665] |
| Centroid: attack Hz | 67.9517 | 453.6030 | -0.9983 | 0.0008 | [-0.9998, -0.9959] |
| Centroid: late-minus-attack Hz | 2.1705 | -39.9894 | +0.3721 | 0.6860 | [0.2587, 0.4837] |
| Bandwidth: attack Hz | 35.6734 | 275.8334 | -0.9735 | 0.0132 | [-0.9996, -0.9440] |
| Bandwidth: late-minus-attack Hz | 7.4330 | 12.8822 | -0.0357 | 0.4822 | [-0.1589, 0.0906] |
| Flux: low attack | 0.9340 | 0.5349 | +0.5741 | 0.7870 | [0.4831, 0.6602] |
| Flux: low persistence | 0.5633 | 0.8532 | -0.2750 | 0.3625 | [-0.3820, -0.1664] |
| Flux: mid attack | 0.6108 | 0.5265 | +0.2462 | 0.6231 | [0.1360, 0.3509] |
| Flux: mid persistence | 0.9673 | 0.9851 | -0.0441 | 0.4780 | [-0.1562, 0.0678] |
| Flux: high attack | 0.2754 | 0.3015 | -0.0592 | 0.4704 | [-0.1776, 0.0599] |
| Flux: high persistence | 1.1732 | 1.0735 | +0.0578 | 0.5289 | [-0.0651, 0.1781] |
| Slope: attack | -5.0483 | -3.4009 | -0.8273 | 0.0863 | [-0.8888, -0.7589] |
| Slope: late-minus-attack | 0.6567 | 0.1523 | +0.3273 | 0.6636 | [0.2088, 0.4449] |
| Harmonic: decay dB/s | 0.9859 | -9.6331 | +0.3556 | 0.6778 | [0.2489, 0.4605] |
| Harmonic: persistence | 0.2446 | 0.2183 | +0.0274 | 0.5137 | [-0.0819, 0.1419] |
| F0: availability fraction | 1.0000 | 1.0000 | 0.0000 | 0.5000 | [0.0000, 0.0000] |
| F0: adjacent continuity cents | 2.3945 | 2.4384 | -0.1918 | 0.4041 | [-0.2990, -0.0812] |

All seven preregistered dimension families contain at least one endpoint meeting
the frozen non-negligible-effect and interval rule. Strong distinctions occur
in attack spectral distribution, centroid, bandwidth, slope and low-band
attack flux. Null or weak evidence occurs for bandwidth change, mid/high flux
persistence or attack, harmonic persistence, and F0 availability.

Final primary classification:
`DISTINCT_TIMBRAL_STRUCTURE_OBSERVED`.

This is a classification of bounded observational structure, not Bass
recognition.

## Secondary BassMic check

BassMic was first opened for outcome analysis after primary commit `ed55745`.
Its 206-window acquisition and complete result replayed byte-identically.
Secondary result fingerprint:
`51f670d37689d0cb95e43bbc0940aeb52e0c8e911181f5b5b057773c6956b6f7`.

| Endpoint | BassMic median | Piano median | BassMic−Piano delta | BassMic−BassDI delta |
|---|---:|---:|---:|---:|
| Log-power rise dB | 12.4347 | 10.6713 | +0.1707 | -0.1327 |
| Time to peak s | 0.01161 | 0.01161 | -0.0245 | +0.3301 |
| Attack flatness | 2.29e-4 | 8.62e-4 | -0.6450 | +0.9467 |
| Attack high/low dB | -37.5250 | -19.6308 | -0.9176 | +0.9548 |
| Attack centroid Hz | 100.3490 | 453.6030 | -0.9892 | +0.7131 |
| Centroid change Hz | 21.7851 | -39.9894 | +0.4846 | +0.2805 |
| Attack bandwidth Hz | 85.6425 | 275.8334 | -0.9319 | +0.9048 |
| Bandwidth change Hz | 54.3966 | 12.8822 | +0.3139 | +0.4639 |
| Low attack flux | 0.5301 | 0.5349 | +0.0136 | -0.6213 |
| Low flux persistence | 1.0454 | 0.8532 | +0.1868 | +0.3853 |
| Mid attack flux | 0.3367 | 0.5265 | -0.2736 | -0.5729 |
| Mid flux persistence | 0.8522 | 0.9851 | -0.1195 | -0.0804 |
| High attack flux | 0.2612 | 0.3015 | -0.1003 | -0.1392 |
| High flux persistence | 0.9272 | 1.0735 | -0.3261 | -0.7241 |
| Attack slope | -2.3326 | -3.4009 | +0.8310 | +0.9495 |
| Slope change | -0.2365 | 0.1523 | -0.4165 | -0.9203 |
| Harmonic decay dB/s | -8.9904 | -9.6331 | +0.0884 | -0.2594 |
| Harmonic persistence | 0.0706 | 0.2183 | -0.1986 | -0.2034 |
| F0 availability | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| F0 continuity cents | 3.2451 | 2.4384 | +0.3137 | +0.5130 |

BassMic reproduces the Bass-associated direction strongly for lower attack
centroid, bandwidth, flatness and high/low spectral balance, and for positive
centroid evolution. Other dimensions are heterogeneous or contradictory:
attack slope reverses relative to BassDI, low attack flux is null versus Piano,
and harmonic decay is weak. This secondary evidence supports capture-robustness
for part of the primary spectral-envelope structure but not for a single,
capture-invariant Bass signature. It is non-decisional and does not alter the
primary classification.

## Limitations and firewalls

This is one recording, one provider-labelled performance, and two capture paths
of the same labelled Bass source. Source identity is confounded with register,
notes, dynamics, technique, polyphony, arrangement, channel processing and
capture response. The one-anchor-per-second mechanism can select noise,
sustain changes or multi-event windows and omit other acoustic episodes.

The result does not establish unique Bass identification in a mixture,
Bass-event recovery, physical-onset authority, human auditory equivalence,
source separation, classifier or threshold validity, causal timbre mechanism,
or musical correspondence beyond the available provider labels. No production
code or canonical scientific documentation was modified, and Demucs was not
run.
