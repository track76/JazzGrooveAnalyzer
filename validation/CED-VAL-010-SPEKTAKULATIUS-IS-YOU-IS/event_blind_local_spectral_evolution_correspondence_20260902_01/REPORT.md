# CED-VAL-010 event-blind local spectral-evolution correspondence

Protocol: `H-CEDVAL010-EVENT-BLIND-LOCAL-SPECTRAL-EVOLUTION-CORRESPONDENCE-01`

Protocol fingerprint: `dd434d28d8c57818c74e0157b3a630553fa664b0a4b405e0a02d0f9e54581996`

Protocol commit: `f7c87f3ee171dd080016eb64d510d41063d0d4d2`

PRE-GT commit: `e07e83fe9a568aa600dfa5ef4aa72eb5e4640f30`

PRE-GT fingerprint: `f5f8fbb5456735d086659ada34edfdc60f0aa0db044451c3056baf4d4a1568d9`

## Method and authority

The experiment reused the frozen controlled-mix STFT without recomputation or
duplication. PRE-GT evidence preserved all 28,985 native adjacent-frame
relations at 256-sample displacement. BassDI and frozen coordinate populations
were opened only after the PRE-GT commit.

BassDI and mix frequency arrays, float64 power convention, native frame starts,
frame/hop/FFT geometry and shared-scope shapes matched exactly. Coordinates
were projected by the frozen exact-Decimal rule without search, tolerance,
alignment or adjustment.

## Decision-bearing result

Positive effects mean the first population has greater correspondence.

| Population | Total | Available | Q1 | Median | Q3 |
|---|---:|---:|---:|---:|---:|
| PRESERVED | 416 | 416 | -0.05217 | 0.19409 | 0.55687 |
| MISSED | 220 | 220 | -0.00014 | 0.10624 | 0.35808 |
| NEGATIVE | 636 | 613 | -0.05767 | 0.14340 | 0.41051 |

NEGATIVE denotes frozen non-event coordinates, not verified Bass absence.

| Comparison | Cliff's delta | Rank AUC | 95% delta CI |
|---|---:|---:|---:|
| MISSED minus NEGATIVE | +0.01849 | 0.50925 | [-0.06130, 0.10090] |
| MISSED minus PRESERVED | -0.07078 | 0.46461 | [-0.16303, 0.02187] |
| PRESERVED minus NEGATIVE | +0.08372 | 0.54186 | [0.00993, 0.15206] |

The MISSED-minus-NEGATIVE interval contains zero. Under the frozen decision
rule, the classification is:

`LOCAL_SPECTRAL_EVOLUTION_ATTRIBUTION_INDETERMINATE`

## Descriptive components

These components cannot alter or rescue classification.

| Observable | PRESERVED median | MISSED median | NEGATIVE median | MISSED−NEGATIVE delta | Rank AUC | 95% CI |
|---|---:|---:|---:|---:|---:|---:|
| Spectral state | 0.68823 | 0.48855 | 0.56232 | -0.24569 | 0.37715 | [-0.33199, -0.15868] |
| Positive/re-articulation | 0.29121 | 0.15374 | 0.18318 | -0.03444 | 0.48278 | [-0.12020, 0.04942] |
| Negative/decay | 0.34177 | 0.19586 | 0.25020 | -0.05898 | 0.47051 | [-0.14633, 0.02878] |

All descriptive observables were available at 416/416 PRESERVED, 220/220
MISSED and 613/636 NEGATIVE coordinates. Spectral-state correspondence was
lower at MISSED than NEGATIVE coordinates. Positive and negative evolution
components were unresolved between those populations.

## Reproducibility and limits

Two fresh evaluations produced byte-identical rows and results. Evaluation
fingerprint:
`ecb0cb299e6d862aec5046c3c0f1bdd73aa631910237a2a58cb5a6286ca43b48`.

The evidence does not establish Bass identity, Bass recognition, Bass-event
recovery, source continuity, source persistence, source tracking, physical
onset, perceptual equivalence, classifier or production-detector validity, or
generalization. It characterizes only numerical local adjacent-frame
correspondence under the frozen authorities. No production code was modified.
