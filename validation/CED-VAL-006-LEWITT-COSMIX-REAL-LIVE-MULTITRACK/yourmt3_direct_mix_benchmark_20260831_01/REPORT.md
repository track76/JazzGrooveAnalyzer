# YourMT3 direct-mix bass benchmark

The 274 frozen `ELECTRIC_BASS_LABEL` candidates have bounded temporal correspondence with the original Double Bass authority, but they do not establish correct instrument classification and are insufficient as a standalone replacement.

- Candidate/original population: 274 / 1,055; density 1.1040162620789553 / 4.2508655346470725 events/s.
- Candidate temporal scope: 38.93958333333333–243.75 s (span 204.81041666666667 s); original scope: 26.538666666666668–244.704 s (span 218.16533333333334 s); benchmark scope 0–248.18475 s.
- Matched / original-only / YourMT3-only: 223 / 832 / 51.
- Precision / recall / F1: 0.8138686131386861 / 0.21137440758293838 / 0.3355906696764484.
- Median absolute displacement / RMSE / maximum: 0.023541666666666666 / 0.03855768190266403 / 0.21333333333333335 s.
- Matched partitions BOTH / htdemucs_ft-only / RX-only / NEITHER: 169 / 6 / 3 / 45.
- YOURMT3_RECOVERY_OF_NEITHER: 45 / 398 = 0.11306532663316583.
- Oracle htdemucs_ft union RX union YourMT3: 702 / 1,055 = 0.6654028436018957 recall. This is explanatory only.
- Classification: `COMPLEMENTARY_BUT_INSUFFICIENT`.
- Instrument conclusion: YourMT3 called these events Electric Bass. Temporal correspondence does not correct that classification to Contrabass.
