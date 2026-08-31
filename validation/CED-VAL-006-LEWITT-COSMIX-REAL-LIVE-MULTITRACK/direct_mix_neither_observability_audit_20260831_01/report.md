# Direct-Mix Observability of the Neither Population

- Audit: `AUD-CEDVAL006-DIRECT-MIX-NEITHER-OBSERVABILITY-01`
- Corrected protocol fingerprint: `c77fbba2835b334e16b932966c388967faf74f08c6994b4287e767c6d511b128`
- Outcome: `NO`
- Replay: byte-identical

## Observability

| Population | Observable | Fraction | Without Drum coincidence | Without strong Drum coincidence |
|---|---:|---:|---:|---:|
| BOTH | 174/555 | 0.313514 | 12/555 | 95/555 |
| htdemucs_ft-only | 14/64 | 0.218750 | 1/64 | 6/64 |
| RX-only | 0/38 | 0 | 0/38 | 0/38 |
| NEITHER | 12/398 | 0.030151 | 0/398 | 6/398 |

NEITHER does not satisfy the preregistered substantial-fraction requirement.
Its observable fraction is less than one tenth of the BOTH control fraction,
and all 12 criterion-positive cases coincide with an authorized Drum EME
within 30 ms. Six remain after excluding the prospectively defined strong-Drum
subset, still only 1.51% of NEITHER.

The median controlled-mix 30–500 Hz attack contrast is 9.05 dB for BOTH and
2.05 dB for NEITHER. Median original/mix low-frequency transient-map cosine is
0.722 versus 0.439; median strongest-flux time difference is 23 ms versus
27 ms. Fixed-band median contrasts for NEITHER are -0.97, 0.30, 3.77, 0.93,
0.13, and 0.48 dB across 30–80, 80–160, 160–320, 320–500, 500–1000, and
1000–2000 Hz. The corresponding BOTH values are 9.57, 9.32, 9.86, 5.95,
3.33, and 4.48 dB. Thus no frozen region supports a substantial, Drum-independent
NEITHER observability claim.

The result denotes spectro-temporal location association only. It does not
identify Bass from the mixture, establish physical onset, or authorize a
mixed-audio detector rule.
