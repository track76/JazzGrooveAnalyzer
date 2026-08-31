# RX11 Bass-Separation Benchmark Result

- Result: `RES-CEDVAL006-RX11-BASS-SEPARATION-BENCHMARK-01`
- Protocol: `H-CEDVAL006-RX11-BASS-SEPARATION-BENCHMARK-01-R1`
- Evidence gate: `PASS`
- Decision: `WORSE_THAN_DEMUCS`
- Replay: `PASS_BYTE_IDENTICAL`

The manually exported RX file conforms to the frozen technical and operator
protocol. Its filesystem birth time is preserved as
`FILESYSTEM_EXPORT_TIMESTAMP_UTC` and is not represented as a manually
observed operator timestamp.

## Frozen Level-2 result

| Metric | RX 11.2.0 | Frozen htdemucs_ft |
|---|---:|---:|
| Bass EME | 653 | 646 |
| Matched | 593 | 619 |
| Original-only | 462 | 436 |
| Separated-only | 60 | 27 |
| Precision | 0.9081163859111792 | 0.958204334365325 |
| Recall | 0.5620853080568721 | 0.5867298578199052 |
| F1 | 0.6943793911007026 | 0.7278071722516166 |
| Median absolute displacement (s) | 0.010666666666666666 | 0.0068208616780045354 |
| Timing RMSE (s) | 0.020428242637232495 | 0.017893173606420704 |
| Maximum displacement (s) | 0.13866666666666666 | 0.18692063492063493 |

RX meets the frozen `WORSE_THAN_DEMUCS` gate because F1 is no greater than
the preregistered 0.7028071722516166 material-worsening cutoff. In addition,
without material population improvement, its median displacement is more than
125% of the Demucs median. This bounded classification concerns only the
authorized JGA event population and temporal localization; it is not a claim
about perceptual quality or commercial separator superiority.

Complete Level-1/2/3 evidence, AD-038, AD-040, decision gates, and replay
identities are preserved in `result.json` and the two scoring executions.
