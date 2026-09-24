# Contained multi-hypothesis BP fallback — frozen JGA selector

**Result: all3previous catastrophic selections become abstentions. Zero catastrophic outputs in the selected cohorts; substantially reduced coverage. Fallback remains CONDITIONAL.**

## What changed and what did not

The model, scaler, feature definitions, candidate generator, native candidate coordinates, threshold0.5 and per-window abstention logic are unchanged and hash verified. Each native BP hypothesis retains its original ±150ms window and its own candidate-context features. The exact frozen decide() runs independently for each of760preserved BP queries. No candidate set or search interval is merged across hypotheses.

For a like-for-like masking comparison, the exact prior BP-only hypothesis-set membership is retained solely as bookkeeping for the requested consensus/abstention test. Old activity envelopes are not used as search windows. This avoids silently restoring the GT-matched BP identity or narrowing the masked population. Same13natural ambiguous and35masked holdout GT IDs.

Consensus: one successful query yields a selection; multiple successful queries at the exact same original PCM sample yield SHARED_ATTACK_IDENTITY_UNRESOLVED; different sample coordinates yield ABSTAIN_MULTIPLE_DISTINCT_ATTACKS; no successful query abstains. Shared means identical observed spectral coordinate, not independent proof of one physical pluck. No millisecond clustering radius, timestamp averaging or proximity-based collapse was added. The selected timestamp remains an original candidate coordinate.

The prior investigator exposure remains a limitation. Inference was filesystem-isolated from GT, prior evaluation results and cohort IDs;3negative-read probes passed. All per-window outputs and consensus predictions were saved/hashed before GT evaluation. GT target remains Fishman channel-specific observable onset, NOT physical string release.

## Results

| Metric | Natural ambiguous | Masked holdout |
|---|---:|---:|
| Cohort events | 13.000 | 35.000 |
| Selected | 8.000 | 18.000 |
| Coverage % | 61.538 | 51.429 |
| Median signed ms | -4.822 | -5.240 |
| Mean signed ms | -4.959 | -5.125 |
| Median absolute ms | 4.822 | 5.240 |
| P95 absolute ms | 5.480 | 5.598 |
| Maximum absolute ms | 5.484 | 5.724 |
| Within ±5ms, selected % | 75.000 | 27.778 |
| Within ±10ms, selected % | 100.000 | 100.000 |
| Within ±20ms, selected % | 100.000 | 100.000 |
| Within ±30ms, selected % | 100.000 | 100.000 |
| Useful within10ms yield / all events % | 61.538 | 51.429 |

Natural13:6single-hypothesis selections,2shared-coordinate selections,5distinct-attack abstentions. Masked35:14single-hypothesis selections,4shared-coordinate selections,17distinct-attack abstentions. No zero-candidate/zero-selected abstentions in these cohorts. Combined shared cases6. Catastrophic wrong-event outputs (>100ms, prior scoring criterion):0in both cohorts. No selected error exceeds10ms.

## Previous3 catastrophic cases

| Event | Previous error ms | Contained outcome |
|---|---:|---|
| GAL09_20260914_S3_A_F_R02 | +15390.563 | ABSTAIN (2 distinct coordinates) |
| GAL09_20260914_S3_E_F_R04 | +9250.057 | ABSTAIN (4 distinct coordinates) |
| GAL09_20260914_S3_E_F_R10 | +5542.179 | ABSTAIN (2 distinct coordinates) |

All three are ABSTAIN, not recovered correct attacks. The rule removes the union’s cross-window maximum-score winner: distant competing fronts now trigger explicit ambiguity. It does not solve temporal ownership among competing windows.

## Interpretation

TEMPORAL CONTAINMENT SOLVES UNION-WINDOW FAILURE: PARTIAL. It eliminates the observed catastrophic emissions through abstention, while selected-event timing stays around5ms. However natural useful yield drops from12/13to8/13, masked useful yield from33/35to18/35. Zero failures among these small selected cohorts is not proof of a controlled universal wrong-event rate.

AMBIGUOUS-BP FALLBACK VALIDATED: CONDITIONAL — useful conservative recovery in this bounded corpus, not complete fallback validation. Natural13includes8development-take cases; investigator has prior corpus exposure. The masked test has35previously resolved holdout events. No new independent test corpus or BP-blind capability is established. No rule adjusted after evaluation.

FROZEN JGA SELECTOR MODIFIED:NO
CONTAINED FALLBACK COVERAGE:61.54% (8/13 natural)
CONTAINED FALLBACK WITHIN ±10ms:100% of8selected
CONTAINED FALLBACK MEDIAN ABSOLUTE ERROR:4.822ms
CONTAINED FALLBACK P95 ABSOLUTE ERROR:5.480ms
CATASTROPHIC WRONG-EVENT SELECTIONS:0
PREVIOUS3CATASTROPHIC CASES:ABSTAIN / ABSTAIN / ABSTAIN
MASKED HOLDOUT COVERAGE:51.43% (18/35)
MASKED HOLDOUT WITHIN ±10ms:100% of18selected
SHARED_ATTACK_IDENTITY_UNRESOLVED CASES:6 (2natural,4masked)

## Artifacts

CONTAINED_FALLBACK_RESULTS.csv preserves all48rows; CONTAINED_FALLBACK_REVIEW.pdf shows all cohort outcomes and the3previous failures. inference/output contains760independent-window decisions,137hypothesis-set decisions and prediction hashes. Input and evaluation freezes preserve provenance.

GT, native BP, prior selector and all previous artifacts unchanged. No historical transfer, canonical change, commit or push. Stop for PI review.
