# Acoustic attack recovery without secure BP identity

**Decision: conditional recovery observed, but the tested fallback is NOT validated for operational use because of catastrophic wrong-event selections. BP-blind mode is not executable.**

## Authorities and isolation

GT and freeze hashes match the PI-supplied authorities. Frozen model, scaler, 22 features, generator code, ±150ms query windows, threshold0.5, maximum-score ranking and exact-score-tie abstention are byte-verified unchanged. Native BP was not rerun. Already-frozen candidate coordinates and feature vectors for all760 native hypotheses were reused, not reconstructed. All12 audio-source hashes verified. The target is Fishman channel-specific observable onset; NOT physical string-release Ground Truth.

No GT, expected pitch, matched hypothesis ID or evaluation-event ID entered inference. It processed all760 hypotheses in opaque take coordinates, then saved137 operational regions and predictions before evaluation. macOS sandbox denied reference and cohort files; all3 negative read probes passed. Investigator prior exposure remains disclosed: process-isolated inference, not investigator blindness.

## Prospective union rule and compatibility

Activity-support intervals [ordinary BP window start, max(native offset,ordinary window end)] define connected components without pitch filtering. Actual acoustic interrogation is only the union of ordinary onset±150ms windows of every component member; gaps are not searched. Native activity can connect disjoint search windows. No GT limits group duration. This is the explicit experimental input-union rule, not a validated acoustic episode detector.

The exact frozen decide() ranks all original candidate-context feature vectors pooled in one component. Each context retains its own native BP-relative features. No substitute onset, averaged context, new classifier or new abstention threshold was introduced. All duplicates remain; exact top-score ties abstain as before. The union changes the set of candidates presented to the model, which is precisely the tested fallback extension.

Evaluation projects predefined13natural ambiguous cases and35secure holdout cases onto the frozen operational groups. If competing IDs had fallen in multiple groups, the prospective rule would abstain instead of choosing by GT. All tested cases fell within a single group. GT population membership is used only after prediction freeze for scoring, never to define or trim a region.

Mode2: BP-BLIND REGION DEFINITION NOT AVAILABLE. Additionally the frozen BP_signed_distance_ms, BP_absolute_distance_ms and BP_relative_activity_position features cannot be computed without BP. Prior continuous detector failures do not establish a compatible independent region authority. No BP-blind scores or coverage were manufactured.

## Population qualifications

Natural13 comprise8cases from development takes and5from holdout takes; thus their pooled result is not13independent holdout events. Their BP correspondences were previously unresolved, but development-take acoustic conditions have prior model exposure. PartB uses exactly the35previously resolved events from the4holdout takes; no model retraining occurred.

## Results

| Metric | Natural ambiguous13 | Masked holdout35 | Secure same35 |
|---|---:|---:|---:|
| Selected | 13.000 | 35.000 | 35.000 |
| Selection coverage % | 100.000 | 100.000 | 100.000 |
| Median signed ms | -4.766 | -5.203 | -5.213 |
| Mean signed ms | 1179.402 | 417.841 | -5.083 |
| Median absolute ms | 4.817 | 5.227 | 5.213 |
| P95 absolute ms | 6159.516 | 1666.794 | 5.621 |
| Maximum absolute ms | 15390.563 | 9250.057 | 5.915 |
| Within5ms % | 69.231 | 37.143 | 40.000 |
| Within10ms % | 92.308 | 94.286 | 100.000 |
| Within20ms % | 92.308 | 94.286 | 100.000 |
| Within30ms % | 92.308 | 94.286 | 100.000 |

Each evaluation cohort returned a selection for every case:13/13 and35/35, with0abstentions and0NO_CANDIDATE. This is output coverage, not successful recovery. Correct-within10ms yield is12/13=92.31% and33/35=94.29%. Catastrophic >100ms wrong-event rates are1/13=7.69% and2/35=5.71%. The tolerance is scoring-only, inherited from the prior study. All remaining errors are within10ms. P95 uses NumPy linear percentiles and is strongly affected by the small cohort and catastrophic outliers.

Human plausible intervals: natural12before/0inside/1after; masked33before/0inside/2after. Close landmarks retain the roughly5ms early tendency, without correction.

## Failure structure

- GAL09_20260914_S3_A_F_R02: +15390.563ms; selected query T10_N011; compatible other GT: ['GAL09_20260914_S3_A_F_R03']. Native sustained/fragmented activity bridges distant search windows; a later high-score front wins.
- GAL09_20260914_S3_E_F_R04: +9250.057ms; selected query T09_N061; compatible other GT: none within100ms. Native sustained/fragmented activity bridges distant search windows; a later high-score front wins.
- GAL09_20260914_S3_E_F_R10: +5542.179ms; selected query T09_N057; compatible other GT: none within100ms. Native sustained/fragmented activity bridges distant search windows; a later high-score front wins.

The union enlarged the decision domain beyond the original local-note task. The model recognizes a plausible front but does not know which connected activity episode owns it. Its frozen high-score rule has no abstention mechanism for two distant, individually plausible fronts. Good median timing therefore does not establish safe fallback behavior. No post-evaluation restriction, duration cap, threshold change or region split was applied.

## Original60 raw-query selections

All60prior records verified against the original holdout freeze. They are selections for BP query hypotheses, not60validated physical notes. They contain58distinct take/timestamp coordinates.18are temporally compatible (±100ms) with15known GT events;42have no compatible reference and remain UNVERIFIED_RAW_SELECTION. Agreement alone is not source/identity proof; absence of a reference here does not independently prove an additional false physical attack.

Eight of these raw queries directly belong to natural ambiguous BP correspondence sets. Eight share natural-cohort operational groups;41share masked-cohort groups (membership need not imply a correct front). All IDs, native pitches/onsets/offsets/amplitudes, component membership, compatible references and signed distances are preserved in RAW_60_QUERY_DETAILS.csv/json. No additional raw query was promoted solely because the model selected it.

## Decision

NATURAL BP-AMBIGUOUS EVENTS:13
AMBIGUOUS-EVENT ATTACK RECOVERY COVERAGE:100% selections;92.31% within10ms
AMBIGUOUS-EVENT MEDIAN ABSOLUTE ERROR:4.817ms
AMBIGUOUS-EVENT P95 ABSOLUTE ERROR:6159.516ms
BP-TEMPORAL-ONLY HOLDOUT COVERAGE:100% selections;94.29% within10ms
BP-TEMPORAL-ONLY MEDIAN ABSOLUTE ERROR:5.227ms
BP-TEMPORAL-ONLY P95 ABSOLUTE ERROR:1666.794ms
BP-BLIND MODE EXECUTABLE WITHOUT NEW METHOD:NO
BP-BLIND HOLDOUT COVERAGE:N/A
BP-BLIND MEDIAN ABSOLUTE ERROR:N/A
JGA CAN RECOVER ATTACK WITH AMBIGUOUS BP IDENTITY:CONDITIONAL — demonstrated on12/13, but fallback NOT operationally validated
JGA CAN RECOVER ATTACK WITHOUT BP TEMPORAL GUIDANCE:NOT TESTABLE WITH CURRENT FROZEN ARCHITECTURE

## Deliverables

- JGA_BP_AMBIGUITY_RECOVERY.csv:13natural +35masked rows, including all failures.
- JGA_AMBIGUOUS_BP_ATTACK_RECOVERY.pdf:13cases.
- JGA_SECURE_VS_MASKED_BP_HOLDOUT.pdf:all35paired errors, full-range and zoom views, plus wrong-event details.
- Complete raw/query/region/candidate/model-score provenance under inference/.
- Protocol, input, recovery and evaluation hash records; original authorities unchanged.

No historical transfer, PLP, timestamp correction, retraining, canonical change, commit or push. Stop for PI review.
