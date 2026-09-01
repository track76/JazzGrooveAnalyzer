# CED-VAL-005 Rhythm-Section Timing Sufficiency Study

Protocol: `H-CEDVAL005-RHYTHM-SECTION-TIMING-SUFFICIENCY-01`  
Protocol fingerprint: `309a10fdf93aaf20b8dbaca2ffd414e461835be7c672992a45807e9fad38e4e3`  
Classification: **INSUFFICIENT**

## Authorities and populations

The verified frozen authorities were the original BassDI/Overheads EME and AD-038/AD-040 artifacts (1,138 Bass; 907 Drums), the frozen htdemucs_ft JGA observation (825 Bass; 1,070 Drums), and the frozen correspondence (782 preserved original Bass; 356 missed; 43 separated-only). All five input SHA-256 values matched the preregistration.

## Global profile

Original versus end-to-end separated signed displacement medians were both 0 s. Q1 changed from -34.830 ms to -11.610 ms; Q3 remained 23.220 ms. IQR contracted from 58.050 ms to 34.830 ms (40.0%). Wasserstein-1 distance was 13.625 ms, KS was 0.1061, and positive-direction balance changed by 0.0720. Absolute-displacement medians were both 23.220 ms and absolute IQRs were effectively identical (58.050 ms). The prospective global gate failed on signed IQR contraction and Wasserstein distance; the Q1 change was within the inclusive two-hop bound subject only to floating representation.

## Temporal coverage

All ten equal-duration recording-time bins retained observations. Preserved-original retention ranged from 0.6528 to 0.7438; retention CV was 0.0364. All ten separated/original density ratios were within 0.40–1.25. The coverage gate passed.

## Local stability

Five of ten windows passed all local criteria; the preregistered requirement was at least eight for SUFFICIENT and six for PARTIALLY_SUFFICIENT. No window was severe. Local W1 ranged from 13.140 to 46.080 ms. Failures reflected W1 in windows 1, 2, and 10 and directional-balance differences in windows 4 and 8.

## Missingness bias

Preserved-original versus missed-original Bass observations differed by 23.220 ms in signed median, 38.406 ms W1, KS 0.3605, and directional-balance difference 0.1338. The prospective material-missingness gate was triggered.

## Same-size subsampling control

Using PCG64 seed 20260901, 1,000 subsets of 782 original observations were sampled without replacement. Reference p95 values were: W1 9.323 ms, median shift 0 ms, relative IQR change 0.20, and directional difference 0.01957. Both the preserved-original subset and end-to-end separated profile exceeded p99 for W1, relative IQR change, and directional difference. Their deviations therefore exceeded variation expected from the frozen same-size random-observation control.

## Gates and interpretation

- Global: FAIL.
- Temporal coverage: PASS.
- Local: FAIL (5/10 pass; 0 severe).
- Missingness not material: FAIL.
- Subsampling p95/p99 criterion: FAIL.
- SUFFICIENT: FAIL.
- PARTIALLY_SUFFICIENT: FAIL.
- INSUFFICIENT: PASS by the frozen hierarchy.

Within this bounded CED-VAL-005 authority, the incomplete pathway does not preserve the preregistered neutral timing-profile properties sufficiently for the intended analysis. Improved Bass observation evidence is scientifically necessary before treating the pathway as sufficient, but this result does not authorize or specify a recovery method.

This is observation-to-observation, GEOMETRIC_ONLY evidence. It does not establish physical onsets, random missingness, causal Demucs effects, musical correspondence, groove, swing, rushing/dragging, beat, meter, downbeat, or generalization beyond CED-VAL-005.

## Replay and integrity

Two runs produced byte-identical result JSON. Result SHA-256: `78248ba05ef92dc5e2e0cef58d138d9554f2efad12206a0193fd188682009894`. Result fingerprint: `6b53fe3f90f18c7c15ee77a7bade082184981ac952e13558be15dbdd05032f43`.
