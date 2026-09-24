# Note-conditioned stem → full-mix attribution

PROCESS-BLINDED RESTART AFTER INVESTIGATOR PLP EXPOSURE

## Result

The prospectively frozen diagnostic does not resolve any episode. All 34 previous multiple-cue abstentions remain UNRESOLVED_ATTRIBUTION; zero become unique, multiple-confirmed or no-compatible-front cases. All 63 episodes remain unresolved, rather than being classified as no Bass activity. None of the 17 previous selections receives a declared Bass-compatible counterpart, earlier alternative or later alternative. These zero counts reflect the sufficiency gate, not evidence that Bass fronts are absent.

No upstream selector, candidate, window, BP output, fundamental, fragment classification, routing or historical timestamp was changed. No model was trained or applied to full-mix features. PLP was never loaded. Prior investigator exposure, including two legacy PLP-bearing rows and required bootstrap context, remains disclosed; attribution execution itself denied timing authority access.

## Frozen method and input verification

RULE_INPUT_FREEZE.json precedes inference. Its rule and exact copied inputs include all 63 frozen episodes, all 98 native member records, independent prior BP windows, prior stem decisions/candidates, fragment audit, and bounded full-mix population. Candidate generation was not repeated. Root and exact member pitch hypotheses are both retained, yielding 117 template evaluations and 4532 candidate–note evaluations. These are not counts of physical attacks. Every one of the 3842 previous full-mix query candidates is retained.

Both original PCM signals use their unchanged recording coordinates and 44100 Hz. Hann1024/hop44 gives 43.066 Hz FFT bins, 23.220 ms window support and 0.998 ms frame spacing. Note-specific descriptive power/energy changes are derived on this common grid; this adds attribution features without changing the frozen 30–250 Hz candidate generator.

Harmonic templates extend to 2000 Hz, with ±43.066 Hz bands. Mean stem energy over native member activity intersected with the frozen episode defines normalized empirical harmonic weights; the preceding equal-length interval supplies background context. A harmonic is operationally observable if its energy exceeds uniform spectral-density expectation. This is a convention, not an instrument/noise-calibrated observability test.

The prospective sufficiency gate requires nonoverlapping bands (f0 > 86.133 Hz) and at least three observable harmonics. At each unchanged FM candidate, 12-frame pre/post energy vectors, harmonic changes, enrichment over broadband expectation, coordinated harmonic-rise fraction, stem-signature cosine, synchronous stem/FM cosine, temporal derivative similarity and harmonic rank similarity are retained. Candidate gates are documented exactly in inference/input/RULE.json: cosine ≥0.8, target enrichment ≥1.5 and coherent fraction ≥0.5. No outcome-based adjustment was made. These are transparent diagnostic conventions, not controlled-validation thresholds.

## Why attribution remains unresolved

Of 117 templates, 59 fail the nonoverlap criterion. The remaining 58 fail the minimum-three-observable-harmonics criterion. None passes both. Some low-pitch templates show three or more elevated bands, but overlapping bands cannot count as independent harmonic evidence under this rule. Higher-pitch templates have sparse empirical harmonic energy under the uniform-density convention.

Therefore all 4532 candidate evaluations are INSUFFICIENT / UNRESOLVED before source-compatibility thresholds can establish attribution. It would be incorrect to infer that the source hypothesis is disproved, that the raw similarities contain no information, or that a different representation would fail. This experiment primarily identifies a limitation of the chosen resolution and sufficiency convention. Thresholds were not relaxed after inspecting outcomes.

## HF044 and HF047

Both preserve target MIDI53 (F3, f0 174.614 Hz). Only the fundamental band exceeds the empirical observability criterion. It accounts for 89.1% of template harmonic energy in HF044 and 97.0% in HF047. High one-band similarity can arise without a coherent multi-harmonic family and cannot reject percussion or another pitched instrument reliably.

The earlier generic cues and the existing FM candidate nearest the old stem selection are compared below solely as diagnostic samples, not selected attack alternatives. Every candidate is preserved in the full table. Coordinates are original recording seconds.

| Episode | FM coordinate | Role | Signature cosine | Synchronous stem/mix cosine | Harmonic coherence | Non-target change fraction |
|---|---:|---|---:|---:|---:|---:|
| HF044 | 63.131156 | earlier prior salience cues | 0.997 | 1.000 | 1.000 | 0.465 |
| HF044 | 63.172063 | earlier prior salience cues | 0.999 | 0.992 | 1.000 | 0.662 |
| HF044 | 63.309751 | nearest existing FM candidate to old stem selection (diagnostic only) | 0.993 | 0.996 | 1.000 | 0.284 |
| HF047 | 64.500045 | earlier prior salience cues | 1.000 | 0.005 | 1.000 | 0.188 |
| HF047 | 64.610794 | earlier prior salience cues | 1.000 | 1.000 | 1.000 | 0.569 |
| HF047 | 64.625760 | earlier prior salience cues | 0.001 | 0.001 | 0.000 | 0.899 |
| HF047 | 64.759456 | nearest existing FM candidate to old stem selection (diagnostic only) | 0.001 | 0.000 | 0.000 | 0.918 |

All rows remain UNRESOLVED regardless of raw similarity. Harmonic coherence here is computed over operationally observable bands; with one band it cannot establish multi-harmonic coherence. A nearest-FM diagnostic sample is not a replacement of the historical selection.

## Decisions

- BASIC-PITCH NOTE CONDITIONING REDUCES FULL-MIX TRANSIENT AMBIGUITY: NO under this frozen diagnostic.
- STEM SPECTRAL SIGNATURE ADDS SOURCE-ATTRIBUTION INFORMATION: INSUFFICIENT EVIDENCE; raw differences are available, but no attribution passes the sufficiency gate.
- FULL-MIX BASS TRANSIENT ATTRIBUTION FEASIBLE: PARTIAL as an executable local evidence comparison; successful source resolution has not been demonstrated.
- PROMISING CONTROLLED-CORPUS VALIDATION TARGET: YES as a research target, not a validated mechanism.

There is no historical onset/source Ground Truth. Piano may share the target pitch; drums can excite its bands. Demucs derives from the same mix and is not independent corroboration. No millisecond accuracy, physical correctness, Demucs latency, replacement timestamp or microtiming profile is claimed.

## Proposed next experiment — not executed

On controlled Gallegati recordings and explicitly labelled controlled mixtures, assess the sufficiency of this exact harmonic representation before training any attribution model. Compare harmonic observability against independent audio/annotation evidence across Fishman/DPA/NT5 and mixtures with percussion/pitched competitors. If inadequate, design any multi-resolution extension prospectively on controlled development data, with its temporal/frequency trade-off documented and a held-out evaluation. Do not relax thresholds or redesign the method on Ray Brown.

## Preservation and deliverables

PRE_RESULT_FREEZE.json hashes target identities, templates/signatures, all candidate evidence and classifications before aggregate results. RESULT_FREEZE.json hashes the aggregate outputs. The main CSV contains episode, BP member, target pitch/f0, template, signature, every local candidate, energy/coherence/similarity measures, source classification, episode status and previous selection status. Three PDFs provide 63 episode pages, 34 primary-cohort pages and two enlarged HF044/HF047 pages, with no PLP. Prior sources and freezes are verified unchanged. No canonical changes, commit, push, bootstrap update or external backup. STOP for PI review.
