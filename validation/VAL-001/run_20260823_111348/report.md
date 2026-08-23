# H-VAL001-RHYTHM-CORRESPONDENCE-01

Status: **INSUFFICIENT_CANDIDATES**

The checksum-bound blind input was verified and the frozen AD-037, AD-038 and
AD-040 populations were reconstructed without symbolic access: 63 Drums, 27
Double Bass and 49 Piano EME. Exact producer round-trip established unique
integer-frame authority for every event.

The complete blind result froze before Ground Truth access. The rule produced
zero candidate relations and retained all 76 accompaniment relations as
`UNRESOLVED / GEOMETRIC_ONLY` (27 Double Bass, 49 Piano). Failed-condition
incidences were: signature mismatch 68, reverse nearest non-unique 17, Drum
signature boundary 5, target signature boundary 4 and target-to-Drum nearest
non-unique 2. Reasons may co-occur. Deterministic replay was byte-identical.

After blind freeze, checksum-bound Calibration Zero absolute correspondence
and symbolic-pair authority scored the immutable result. Piano–Drums has
TP=0, FP=0, FN=36; Double Bass–Drums has TP=0, FP=0, FN=18. Overall TP=0,
FP=0 and FN=54. Precision and F1 are undefined because no blind candidates
exist; recall is 0.0. There are zero ambiguous/unscorable blind candidates and
one Double Bass symbolic relation without a valid JGA pair.

The frozen first-match classification is `INSUFFICIENT_CANDIDATES`. The rule
does not provide useful candidate correspondence evidence and does not justify
production promotion to `AUTHORIZED_EVENT_RELATION`. Raw EME, PulseCandidates,
AD-038 localization, AD-040 profile and Calibration Zero artifacts are
unchanged. No BPM, meter, threshold, correction or musical interpretation was
used.

Blind fingerprint:
`7a11a950a60d79f1a75099bdf9e083b7fc35a3f3845d5041304f8ec637c2f3d6`.

Result fingerprint:
`471664e57ace2a21ffbf6e1a54940bfe773d99f5baa3023eefc3fc1e1a67d045`.
