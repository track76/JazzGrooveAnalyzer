# CED-VAL-010 event-blind attack-timbre observability

Protocol: `H-CEDVAL010-EVENT-BLIND-ATTACK-TIMBRAL-OBSERVABILITY-01`

Protocol fingerprint: `fdc9b6edd3645af674d8d0d102b90e686e820291fbd90f8b52a70a9ff562fe53`

Protocol commit: `e394bda`

PRE-GT commit: `2089815f912d7b69c0eaa709df54bc8938bdce85`

PRE-GT evidence fingerprint: `ae07bed9904a9d9d067c62d10ed1567fb70ae2be630c778c1d2fbf36f6819f0d`

## Event-blind evidence

The checksum-frozen controlled mix was the sole acoustic input. The previously
frozen separated-bass WAV was unavailable and Demucs was not rerun. The frozen
STFT representation produced 28,974 continuous observations: 28,654 available
and 320 explicitly unavailable/null. No threshold, selection, composite or
candidate formation was applied. Two fresh acquisitions were identical.

The complete 172,763,288-byte representation is authoritative external
scientific evidence with SHA-256
`4f6a972470f701d147c20ae9d3841d663ebb37b732b924ca1a7d8c48f437d82f`
and scientific fingerprint
`9bb372e243c5fb7f354823e8f59edb986a1eaacc59c2fcf766b2f5b2760c2ed4`.

Ground Truth and population coordinates were opened only after the PRE-GT
commit existed and was verified.

## Frozen evaluation

Population sizes are PRESERVED 416, MISSED 220 and NEGATIVE 636. PRESERVED and
MISSED availability is 100% for every dimension. NEGATIVE availability is
613/636 (96.38%) for every dimension. Lower values are the previously frozen
Bass-associated direction. Effects are oriented first population minus second.

| Dimension | Population | Available | Q1 | Median | Q3 |
|---|---|---:|---:|---:|---:|
| Centroid Hz | PRESERVED | 416/416 | 130.7196 | 253.8327 | 411.9128 |
|  | MISSED | 220/220 | 155.4773 | 290.0430 | 477.0769 |
|  | NEGATIVE | 613/636 | 107.2870 | 326.8653 | 510.3198 |
| Bandwidth Hz | PRESERVED | 416/416 | 211.4007 | 329.5772 | 492.6474 |
|  | MISSED | 220/220 | 212.9185 | 338.3664 | 480.9849 |
|  | NEGATIVE | 613/636 | 205.8854 | 307.0037 | 511.8743 |
| Spectral flatness | PRESERVED | 416/416 | 0.001197 | 0.001996 | 0.003210 |
|  | MISSED | 220/220 | 0.001222 | 0.001934 | 0.003271 |
|  | NEGATIVE | 613/636 | 0.000963 | 0.001212 | 0.002133 |
| High/low balance dB | PRESERVED | 416/416 | -27.9406 | -21.6074 | -13.5158 |
|  | MISSED | 220/220 | -26.6311 | -20.0205 | -12.4910 |
|  | NEGATIVE | 613/636 | -26.4707 | -21.0487 | -11.2820 |

| Dimension | Comparison | Cliff's delta | Rank AUC | 95% delta CI |
|---|---|---:|---:|---:|
| Centroid | MISSED−PRESERVED | +0.0954 | 0.5477 | [0.0078, 0.1882] |
|  | MISSED−NEGATIVE | -0.0204 | 0.4898 | [-0.1028, 0.0597] |
|  | PRESERVED−NEGATIVE | -0.1065 | 0.4468 | [-0.1762, -0.0344] |
| Bandwidth | MISSED−PRESERVED | +0.0044 | 0.5022 | [-0.0904, 0.0982] |
|  | MISSED−NEGATIVE | +0.0084 | 0.5042 | [-0.0727, 0.0936] |
|  | PRESERVED−NEGATIVE | +0.0029 | 0.5015 | [-0.0696, 0.0719] |
| Spectral flatness | MISSED−PRESERVED | +0.0038 | 0.5019 | [-0.0918, 0.0984] |
|  | MISSED−NEGATIVE | +0.2921 | 0.6460 | [0.2057, 0.3773] |
|  | PRESERVED−NEGATIVE | +0.2915 | 0.6458 | [0.2264, 0.3606] |
| High/low balance | MISSED−PRESERVED | +0.0969 | 0.5484 | [0.0003, 0.1912] |
|  | MISSED−NEGATIVE | +0.0242 | 0.5121 | [-0.0637, 0.1115] |
|  | PRESERVED−NEGATIVE | -0.0551 | 0.4724 | [-0.1238, 0.0156] |

MISSED events have continuous measurements, but none of their four
MISSED-versus-NEGATIVE effects meets the frozen Bass-associated negative-effect
condition. Centroid, bandwidth and high/low balance are indistinct from the
negative control. Flatness is higher at MISSED and PRESERVED coordinates than
at NEGATIVE coordinates, opposite to the frozen lower-is-more-Bass-associated
direction.

Frozen classification: `SOURCE_ATTRIBUTION_INDETERMINATE`.

Evaluation fingerprint:
`6aab59043f94082a1933c8cf8197cb8d344715c0dd3b8bae3a59dd728e4e75f8`.

## Firewalls and limitations

This result neither rescues nor redefines source attribution. It establishes
that the four measurements are available around MISSED events in the mix, but
the negative control prevents attributing that evidence to Bass timbre.

The experiment used one recording and mix-only evidence; the frozen separated
Bass WAV was unavailable. It does not establish Bass recognition, Bass source
identity, recovered events, physical onset, human auditory equivalence,
classifier or threshold validity, a composite score, a causal mechanism or
generalization. No production code was modified.
