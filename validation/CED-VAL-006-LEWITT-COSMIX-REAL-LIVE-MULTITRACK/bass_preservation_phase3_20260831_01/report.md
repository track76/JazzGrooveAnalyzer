# CED-VAL-006 Bass Preservation Phase 3 Result

Decision: **INDETERMINATE**

Both frozen transforms completed with the required audio format and produced
identical decoded float32 sample arrays. The complete WAV files were not
byte-identical: their SHA-256 values differ because libsndfile emitted
different `PEAK`-chunk timestamps at one byte. The preregistration requires
byte-identical output and classifies transformation replay disagreement as
`INDETERMINATE`.

JGA and scoring were not executed after this mandatory authority failure.
Consequently processed Bass EME recovery, matched/original-only/separated-only
populations, precision/recall/F1, timing distributions, AD-038 effects and
AD-040 effects are not available. The frozen unprocessed htdemucs_ft values
remain context only and are preserved in `result.json`.

The dynamics hypothesis did not establish recovery of additional original
Bass temporal evidence. No Phase 4 or new experiment was started.

Result fingerprint: `ae4a3c5efb3514e81ca7d65e3ce07c3f2b731a340eeb1c9732ee40f94dcbd6cb`
