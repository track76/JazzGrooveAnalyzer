# Prospective Chet Baker Hi-Hat-rule validation

2026-09-10. PI-authorized single blind execution. **Activation gate: FAIL. Reference: HIHAT_2_4_REFERENCE_UNAVAILABLE. Status: FAILED.** External tempo comparison NOT PERFORMED. No external BPM used.

Source: `/Volumes/SSD Track/JGA/downloads/III_Chet Baker - I fall in love too easily.mp3`; SHA-256 `3906369e80a62cf202e1c27e2574ef42dec84b6033f69522c3da47d9db8db0e1`. PI declares admissible real jazz. Only format/stream fields needed for decoding were inspected; embedded tags, source-related project tempo records and external tempo sources were not consulted. The frozen rule was read, including its unrelated retrospective CED-VAL-005 example; those example values were not used as candidate intervals or expected tempo for this track.

Rule SHA-256: `0c9e921b835c33047afaef47ee3252d9f2fcbbb536dc0d9c7751f2a7baa6a244`. Model freeze SHA-256: `1e6535e4669bb520882d80b76506d8b1daa3e024f0cd41ae26e62d542ce0d2f4`. All bound package files/weights and dependency versions passed verification. One full-file CRNN_8 inference, unchanged supplied threshold/preprocessing/peak picker. No training, tuning, window search or fallback model. Decoder mapped only the first audio stream, stripped metadata and preserved decoded samples as PCM24; no normalization. Decoded sample rate 44100, 8928047 frames. Source-relative time is decoder-output time; physical session origin and encoder delay are not independently established.

## Prospectively fixed qualification

The external protocol was written before inference. All native binary64 Hi-Hat outputs (MIDI42, no subtype inference) were frozen before timestamp analysis. No Ride/Double-Bass prediction influenced any decision. All-class predictions/activations are preserved but only HH candidates were consumed by qualification.

All exact positive unordered pair differences were grouped without tolerance or rounding. Shared endpoints are not independent witnesses. A reversed traversal with manual binary64 reconstruction independently checked all pair groups; a synthetic reconstruction check passed. This was one authorized inference/analysis, not repeated candidate selection.

All complete 10-second regions from file zero and all complete 10-second regions shifted by 5 seconds were fixed by decoded duration; shorter edge residuals remain in the complete candidate population. Local support requires both endpoints inside a region. Candidate ranking is the existing lexicographic (occupied regions, locally repeated regions, total contained witnesses) rule. No specific period was supplied.

For this conservative prospective full-region claim, PASS requires one unique top relation with at least two distinct contained pair witnesses in every full primary and shifted region. This is an operational sufficient-coverage gate, not a universal musical threshold or proof of identity. Partial distributed support returns INDETERMINATE; absence of any repeated/local recurrence returns FAIL. No shorter favorable excerpt is tried. Missing detections are not evidence that the performer omitted a stroke; partial support cannot be repaired to obtain PASS. This conservative choice may abstain on valid timekeeping with detection gaps.

Only PASS permits T_BEAT=T_HH/2 and internal BPM under the frozen domain rule. Exact recurrence alone does not establish physical Hi-Hat identity or eliminate every articulation confound. Confidence remains uncalibrated. The rule is a prospective musical-domain hypothesis, not a universal truth.

## Frozen observations

- Hi-Hat candidates: **0**, native-time span `None` seconds.
- Primary regions: 20; shifted regions: 19.
- Primary region event counts: `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`.
- Recurrent exact relations: 0; supporting distinct pairs: 0.
- Selected T_HH: `None`; inferred T_BEAT: `None`; internal BPM: `None`. Null means unavailable, not a numerical estimate.

| Descriptive exact-relation approximation (s) | Global pair support | Primary local pair counts | Shifted local pair counts |
|---|---:|---|---|

These unselected diagnostic intervals are not BPM estimates. No absent anchors or inferred observed strokes are invented. Failed/incomplete gate evidence is preserved regardless of external tempo. This result concerns the frozen recognition/qualification pipeline, not proof of absent physical Hi-Hat or failure of the musician's timekeeping.

## Freeze and stop

Complete candidates, exact relations, region counts, gate result, selections/nulls and ambiguity are frozen externally. No external lookup, PI-tempo comparison, production integration, unrelated experiment, commit or push occurred. No prior scientific record or domain rule changed.

Next step is external BPM comparison only after separate PI authorization; if the internal result abstains, such comparison cannot create a retrospective internal estimate.

External package: `/Volumes/SSD Track/JGA/experiments/CHET-HIHAT-24-BLIND-20260910/`.

- `protocol.json` SHA-256 `782ac028462670d1bc0a718f948ad226cb854743376695333b3c9b8297a025b4`
- `run.py` SHA-256 `fde0b8d84d30d69e94203f229911fcca2771ab4d8d07ce1a8686703c8d90749a`
- `hihat_predictions.json` SHA-256 `a2e83c84d4f433209f3c494ebe043f9933344cf0294154480e23b0086d9e95c8`
- `candidate_freeze.json` SHA-256 `fffa521a13d01b2dfd2f49f8529b2b92ba132a2ca83b8d4bec477162b60c9d8f`
- `result.json` SHA-256 `585748386fd710cc86c587c7431b0dd0e8c4f28da5250c25b7cacdff6ccdb85d`
- `SHA256.json` SHA-256 `bbe7c6bb40c5c70f2fb268ad1bd4b0c116729f005ed3717c42c49a9775e684c0`
