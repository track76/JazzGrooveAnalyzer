# Chet Baker full-pipeline blind Hi-Hat validation

2026-09-10. PI-authorized **full mix → approved source separation → Drums stem → unchanged Vogl → frozen Hi-Hat qualification**. No external tempo used or checked. Gate: **FAIL**; reference: **HIHAT_2_4_REFERENCE_UNAVAILABLE**; brush-condition recognition: **FAILED**.

## Input and separation authority

Original full mix: `/Volumes/SSD Track/JGA/downloads/III_Chet Baker - I fall in love too easily.mp3`, SHA-256 `3906369e80a62cf202e1c27e2574ef42dec84b6033f69522c3da47d9db8db0e1`. The PI's brush-performance observation is context only, not model input, tuning authority or independent event labels. The prior direct-full-mix test is preserved unchanged as a control, not called a complete JGA analysis: [control report](../CHET_HIHAT_24_BLIND_20260910/REPORT.md), SHA-256 `a0ed99113a07741215cae180877c2ad7f2d73f95974bde96a20e44982647d344`.

Approved JGA execution: `FileAudioSource.load` → `DemucsSeparator.separate_authorized` → `AuthorizedDemucsRunner` → isolated pinned backend. Method **Demucs 4.1.0, htdemucs_6s**, registry revision `053e1404489b3dc58bf718224fac4b7316de8c93`. Model/checkpoint hashes, native configuration and isolated dependency versions were checked by the existing backend, offline. CPU, shifts=0, overlap=0.25, split enabled, native segment, all six float32 outputs preserved. Only the parent binding/authorization/role was instantiated for this new PI-authorized source; no separator implementation or model configuration was changed. No custom source separation or model search occurred.

Parent source UUID `311cc634-297a-5f62-8ae9-91f4e250f4f7` is authority/instance-key derived, not filename-derived. Every native output retains a distinct source UUID, asset hash and parent transformation lineage. Drums output is model-declared source separation, not verified per-event source identity. Other stems were preserved for provenance only, not analyzed for this decision.

Drums stem: `/Volumes/SSD Track/JGA/experiments/CHET-HTDEMUCS6S-HIHAT24-20260910/stems/drums.wav`; SHA-256 `51ae377b168f742c974dc4f87996627590653810b652a14009d66c4025b82ad1`; source UUID `4931d6ce-ebf2-5e52-8c40-2e1dd5be23d1`. Native sample rate 44100, frames 8930304. It was supplied directly to Vogl as float32 WAV, without PCM24 requantization or extra normalization; native Demucs normalization/reconstruction and supplied Vogl preprocessing remain authoritative. No assumption of physically exact onsets or source completeness follows from separation.

## Decode-length diagnostic

The JGA parent loader and prior control decoder yielded 8,928,047 samples; the native Demucs outputs each contain 8,930,304 samples at 44.1 kHz, a difference of 2,257 samples (approximately 51 ms). A read-only frame-equality check therefore failed. No stem was trimmed, shifted or repaired. This decoder-path difference is preserved, not treated as a detected musical offset; encoder-delay/padding placement and exact MP3-to-stem onset mapping were not measured. Internal interval inference uses native stem time, and both decodes still provide the same twenty complete ten-second regions. No cross-decoder event matching is claimed.

## Blind inference and qualification

The Vogl model/package/dependency freeze was verified unchanged. One full-stem inference; no threshold adjustment, retraining, calibration, favorable excerpt selection or brush-specific feature change. All model outputs remain preserved; only MIDI42 HH candidates enter the rule. HH subtypes are not invented. No Ride or Bass output selected a period.

The source changed from mix to stem; the predeclared exact recurrence and activation gate from the control were retained unchanged: complete 10-second regions plus 5-second-shifted regions, exact binary64 pair relations, unique leading local-support relation repeating with >=2 contained witnesses throughout both grids for conservative PASS. Partial support is INDETERMINATE; absent local recurrence FAIL. This is an operational sufficient full-region gate, not a universal musical threshold. Candidate errors/omissions remain possible, and missing predictions never imply missing physical playing. The frozen JAZZ_HIHAT_2_4_TIMING_RULE is unchanged.

Only PASS authorizes T_HH/2 and internal BPM. Candidates were frozen before pair analysis; independent reverse traversal/manual binary64 reconstruction checked pair grouping. No external tempo, metadata tempo, tapping, score, expected pattern or previous tempo estimate was read or used.

## Frozen result

- Hi-Hat candidates: **0**; native-stem time span `None` seconds.
- Primary/shifted regions: 20/19.
- Primary region event counts: `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`.
- Recurrent exact relations: 0; distinct recurrent witnesses: 0.
- Activation gate: **FAIL**.
- Selected T_HH: `None`; inferred T_BEAT: `None`; internal BPM: `None`. Null is unavailable, not an estimate.

| Diagnostic relation (s) | Global support | Primary local counts |
|---|---:|---|

If the reference is unavailable, this is consistent with a likely recognition-domain limitation under the PI-reported brush condition; that explanation is a hypothesis, not demonstrated causation or proof of physical Hi-Hat absence. Separation artifacts, mixture differences and detector sensitivity remain possible contributors. A SPARSE label denotes insufficient usable local support, not a universal numerical event-count threshold. A usable stream would still be candidate evidence under a prospective domain rule, not externally validated tempo.

## Preservation and stop

All six native stems, source/separator bindings and inference results remain on the external SSD. This record adds the full-pipeline result without rewriting the direct-mix control. No external comparison occurred. No production code or frozen rule was modified; no commit/push. Stop for PI review.

- `separator_authority.json` SHA-256 `68e78a6cd77649eb2fe903db9f4eafa750ff52e930bc3f209a46d30370d184f5`
- `parent_source_authority.json` SHA-256 `acd50880517c19a2adf079f6d926ac8cfdc0c14796f1e63fe864c6388f3ce115`
- `separation_result.json` SHA-256 `78afd2810cb176ad00dcb66d29871288cea13cf734ce6f14daf19339dd9355d7`
- `inference/protocol.json` SHA-256 `7269700ab43e7a522b1d91c983f030bf8fcaf9a786642949c534cb349aea339d`
- `inference/candidate_freeze.json` SHA-256 `6b048df329a066677605419595893f39ed69a1243d68f5ea0ff698bc261232b6`
- `inference/result.json` SHA-256 `585748386fd710cc86c587c7431b0dd0e8c4f28da5250c25b7cacdff6ccdb85d`
- `inference/SHA256.json` SHA-256 `c63900c7a2a06049acd0fa3207aa671b6efd99bc8f814f07af5df7a95306da04`
