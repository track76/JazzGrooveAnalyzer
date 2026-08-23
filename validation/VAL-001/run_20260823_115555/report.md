# H-VAL001-RHYTHM-CORRESPONDENCE-02

Status: **LOW_RECALL**

Preregistration commit:
`62cebe2c46402d80803c82c4ea74d9b4d61006a7`.

The checksum-bound AD-037/AD-038/AD-040 blind populations were verified and
reconstructed: 63 Drums, 49 Piano and 27 Double Bass EME. Exact producer
round-trip established unique frame authority throughout. Hypothesis 01
remains frozen as `INSUFFICIENT_CANDIDATES`; Hypothesis 02 removed exactly the
cross-source signature-equality condition and changed no other criterion.

Before Ground Truth access, 13 candidates froze with deterministic replay:
12 Piano–Drums and 1 Double Bass–Drums. The remaining 63 relationships are
`UNRESOLVED / GEOMETRIC_ONLY`: 37 Piano and 26 Double Bass. Hypothesis 01 had
zero candidates, so the exact candidate-count change is +13.

After blind freeze, checksum-bound Calibration Zero absolute-correspondence
and symbolic-pair authorities scored only the frozen population. Piano–Drums:
TP=11, FP=1, FN=25, precision=0.9166666666666666,
recall=0.3055555555555556, F1=0.4583333333333333. Double Bass–Drums: TP=1,
FP=0, FN=17, precision=1.0, recall=0.05555555555555555,
F1=0.10526315789473684. Overall: TP=12, FP=1, FN=42,
precision=0.9230769230769231, recall=0.2222222222222222 and
F1=0.35820895522388063. No blind candidate is ambiguous/unscorable; one
Double Bass symbolic relation lacks a valid JGA pair.

The frozen first-match classification is `LOW_RECALL`. The result supplies
useful conservative blind correspondence evidence, but production promotion
remains unauthorized and requires separate PI review. Raw EME,
PulseCandidates, AD-038 localizations, AD-040 profiles, Calibration Zero and
Hypothesis 01 are unchanged. No BPM, meter, threshold, correction or musical
interpretation entered the experiment.

Blind fingerprint:
`259246226fee627934708eeb9aafc8bd8eb8e3ebbe7340b76935f2a4c0d8b674`.

Result fingerprint:
`2bf5ddb3c40620c3ddf5ebf8cbf7aad6d6ed74d770481d8eb921b579ad96c082`.
