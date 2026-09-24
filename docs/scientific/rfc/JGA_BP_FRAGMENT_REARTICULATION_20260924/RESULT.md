# Same-pitch segmentation versus rearticulation — experimental review

## Result

```json
{
  "same_pitch_boundaries": 18,
  "within_same_family": 16,
  "cross_family_ambiguous": 2,
  "SAME_NOTE_FRAGMENT": 13,
  "TRUE_REARTICULATION": 0,
  "AMBIGUOUS": 5,
  "native_root_segments_before": 79,
  "experimental_root_identity_units_after": 66,
  "all_native_hypotheses_before": 98,
  "all_identity_units_after": 85,
  "frozen_fundamental_episodes_before": 63,
  "frozen_fundamental_episodes_after": 63,
  "fragmentation_explains_excess": "PARTIAL",
  "classification_sha256": "22f1843c0e101c772bc255f5f94518ce6d24a8ae0be8f1c9b525c62996a71016"
}
```

Thirteen same-family splits are supported as segmentation continuation by the inspected waveform, low-band energy and flux morphology. Five remain ambiguous; no second physical same-pitch attack is established confidently. Zero TRUE_REARTICULATION classifications is not evidence that the recording contains no rearticulations.

## Population and interpretation

All successive same-MIDI pairs from the 98 native hypotheses were tested when B starts at or after A end and the gap is no more than512/22050 s (23.22 ms), the existing frozen family continuity window. This defines a bounded candidate population, not a fragment classifier. It finds16 same-family root pairs plus2 cross-family pairs. Those two remain ambiguous; harmonic ownership is unchanged. All six PI examples are included. Longer-gap repetitions are outside this short-segment study, not declared absent.

Classification used visual acoustic morphology, not PLP, pitch equality, gap length or an automatic probability threshold. All18 windows were individually inspected. Local range is B−260 to B+180 ms. RMS display uses221 samples (~5ms). The existing synchronized magnitude/positive-flux tensor was reused unchanged:30–250Hz, Hann1024, hop44,44100Hz. Energy is sum of squared magnitudes in the same band. Descriptive post/pre energy medians use +15..+60 / −60..−15ms; boundary/earlier flux ratios use maxima in ±30 / −220..−50ms. These numbers were not decision thresholds. Flux and energy normalization is solely per-plot display scaling.

For FR04, FR11 and FR12, a renewed front is observable before B but within A. The evidence does not determine whether A itself was a separate physical pizzicato or an early/misaligned transcription hypothesis. Those cases are not silently collapsed, and no second physical note is invented. FR01/FR05 remain ambiguous because frozen root/harmonic ownership changes. Amber shading shows reviewed front regions, not newly generated attack timestamps. All classifications are qualified, uncalibrated judgments; absence of a visible front is not proof of physical non-rearticulation.

## Counts are different layers

There are79 native root segments in63 frozen families. Collapsing13 supported same-family fragment boundaries produces66 experimental root identity units; including19 unchanged harmonic hypotheses yields85 total identity units from98 native hypotheses. These are not independently verified physical-note counts. The already frozen63-family reconstruction had provisionally grouped these root fragments; its count remains63 and is NOT reduced to50. Thus fragmentation explains part of the native excess segmentation, not the entire note-identification problem or the existence of a particular walking-note population.

## Independence and provenance

The investigator previously saw PLP-based diagnostics; this study is not investigator-blind. The acoustic and final classification processes were filesystem-isolated from PLP, with negative read tests saved in ISOLATION_VALIDATION.json. Only sanitized native note/family records, preserved Bass/full-mix PCM and saved spectral tensors were supplied. No PLP was subsequently reintroduced. No Basic Pitch/model inference, spectral parameter retuning or new continuous peak search was performed.

CLASSIFICATIONS.json and the CSV were saved and SHA-256 frozen before the collapsed representation was constructed. CLASSIFICATION_FREEZE.json records that experimental authority only. The collapsed representation is a hashed derived identity view containing all98 exact native source records. No original hypothesis, timestamp, episode, pitch, previous freeze, Report001 or canonical method is changed. No commit or push.

## PI review

SAME_PITCH_FRAGMENT_VS_REARTICULATION.pdf has one page for each18 boundaries, with exact A-end/B-start and synchronized signals. BASIC_PITCH_BEFORE_AFTER_FRAGMENT_COLLAPSE.pdf covers the entire frozen note sequence in four chronological pages. No quarter grid or musical timing interpretation. Review the five ambiguous cases before any further event-count inference. STOP for PI review.
