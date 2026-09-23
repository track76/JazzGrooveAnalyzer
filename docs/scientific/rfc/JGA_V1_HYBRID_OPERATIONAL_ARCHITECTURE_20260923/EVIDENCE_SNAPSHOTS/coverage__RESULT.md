# Candidate-coverage sensitivity result

STUDY: JGA-QUARTER-NEAREST-ONSET-COVERAGE-SENSITIVITY-001. STATUS: PASS (procedural completion). DECISION: **B — COVERAGE ROBUSTNESS SUPPORTED WITH QUALIFICATION**.

## Measured observations

Parent integrity passed. All 946 cells, 1,627 candidates, 898 selected markers, 729 contextual events and 48 EMPTY quarters are preserved. Selection coverage remains 94.93%, event reuse 0 and ties 0. No parent winner was changed. The 52 frozen comparison windows are unchanged.

Of 898 nonempty quarters, 308 (34.30%) have one candidate and 590 (65.70%) multiple candidates. Bilateral coverage occurs in 381 (42.43%); 517 (57.57%) are unilateral. Percentages here use nonempty quarters. These are descriptive conditions, not quality Ground Truth.

The 590 available nearest–second margins range 0.105–153.174 ms, median 63.601 ms, IQR 58.050 ms. Counts in preregistered successive bands 0–5, >5–10, >10–20, >20–35, >35–50, >50–100 and >100 ms are 22, 19, 40, 92, 71, 242 and 104. Margins are unavailable for 308 singleton cells; they are not infinity.

Removing only the selected marker hypothetically leaves 590 replacements and 308 empty cells. Among replacements, 348/590 (58.98%; 38.75% of all 898) reverse offset sign and 386 change source state. Median signed offset change is +46.44 ms; median absolute change is 104.49 ms. Individual markers are therefore not generally stable to losing their selected candidate.

| Candidate loss | Phases | Selected identity retained | Both window shift/slope directions retained | Phase range of joint retention |
|---|---:|---:|---:|---:|
| 5% | 20 | 95% | 927/1040 = 89.13% | 84.62–94.23% |
| 10% | 10 | 90% | 432/520 = 83.08% | 75.00–90.38% |
| 20% | 5 | 80% | 194/260 = 74.62% | 67.31–82.69% |

All phases of every-20th/10th/5th chronological-candidate removal were frozen in advance. Identity-retention percentages follow the removal design and are not independent evidence of robustness. Joint direction denominators count 52 window/scenario combinations per phase, not independent replications. None is unevaluable. Median absolute half-shift changes are 2.16, 6.73 and 12.77 ms; median absolute slope changes 0.53, 1.74 and 2.74 ms/s. New-empty fractions among parent-selected quarters are 1.71%, 3.43% and 6.86%.

Substantial exceptions remain: at 5% loss (THIN_05_PHASE_03), W050 (318.802–325.302 s) changes half-shift from +117.20 to −92.65 ms, a −209.86-ms change, despite its median changing by only −0.89 ms. Its negative slope remains negative. The maximum absolute half-shift change at 20% loss is 223.55 ms. Window robustness must not be generalized to every window or every magnitude.

## Reference and recurrence

Reference 122–128.5 s has 17 selected quarters: 13 multi-candidate, four singleton, three bilateral and 14 unilateral. Its parent shift is −41.38 ms and slope −11.14 ms/s. All 17 individual winner-loss scenarios retain both negative directions, including the four cases without replacements. Shift ranges −44.84 to −39.95 ms and slope −12.83 to −10.10 ms/s. All 35 thinning phases also retain both directions. At 20% loss, shift ranges −52.73 to −39.33 ms and slope −13.49 to −11.07 ms/s. Candidate counts, margins and every hypothetical alternative are in REFERENCE_COVERAGE_AUDIT.csv. Reference survival: YES within tested loss scenarios.

All three prior recurrence windows retain negative shift and slope in every individual selected-marker removal and every thinning phase:

| Window, s (rounded display; frozen exact boundaries used) | Parent shift / slope | 20% thinning shift range, ms | 20% slope range, ms/s |
|---|---|---|---|
| 65.302–71.802 | −89.64 / −28.27 | −124.74 to −56.83 | −33.02 to −17.80 |
| 71.802–78.302 | −130.28 / −41.88 | −155.39 to −83.13 | −44.12 to −36.66 |
| 240.802–247.302 | −63.14 / −7.84 | −99.87 to −51.51 | −15.78 to −8.62 |

Recurrence survival: ALL under tested candidate loss, not a claim about unobserved candidate addition or independent physical attacks.

## Coverage, large distances and missing quarters

Among 199 selected distances >100 ms, 118 (59.30%) are singleton cells, compared with 34.30% overall. However, 81 (40.70%) have alternatives and 75 are bilateral. Large distances are associated partly with sparse coverage; they remain the actual nearest observable geometry in these populated cells. This does not establish that missing observations caused any particular offset.

Absolute selected distance has Spearman associations with candidate count −0.364 (N898), cell density −0.341 (N898), margin −0.309 (N590), bilateral coverage −0.144 (N898), and largest event-free interval +0.834 (N898). These quantities share mathematical dependencies with nearest selection; no causal conclusion follows.

UNKNOWN-selected quarters (N257) have median absolute distance 38.69 ms versus 52.37 ms for source-supported selections (N641); median candidate count is two in both. Bilateral proportions are 52.53% versus 38.38%; margin medians 57.19 versus 67.43 ms (N202/388 evaluable). UNKNOWN cannot be equated with poor candidate coverage or replaced by a farther supported marker.

The 48 EMPTY quarters form 33 runs: 28 isolated and five consecutive runs. Consecutive runs occur at quarter times 207.630–208.977 s (5), 230.330–230.681 s (2), 231.382–231.731 s (2), 338.406–339.140 s (3), and 339.875–342.447 s (8, longest). The terminal concentration is retained. Local density, existing source-evidence context and BPM are recorded in EMPTY_QUARTER_AUDIT.csv. Empty cells do not establish silence.

The preregistered better-covered subset (multi-candidate AND bilateral) has 381 quarters. Its window medians span −121.15 to +97.28 ms across 52 windows. Within its source-supported subset (246 selected quarters), 50 windows are populated and medians span −132.67 to +85.46 ms. Variation remains measurable, although sparse subset windows and changing composition qualify comparisons; these secondary summaries do not replace the all-quarter result.

## Interpretation and closure

The coordinate remains useful as a conditional description of the observed candidate population. It is not a loss-invariant estimate of an intended or physical beat attack. Whole-window directions often survive periodic loss; reference and recurrence examples survive all tested losses, while some other windows change substantially. This combination supports decision B, not universal coverage robustness.

**Preferred JGA v1 research representation: YES-WITH-QUALIFICATION. Basic descriptive groove-coordinate problem: CLOSED FOR JGA v1 RESEARCH WITH QUALIFICATION.** Use QUARTER-ANCHORED NEAREST-OBSERVABLE-ONSET GEOMETRY with per-quarter candidate count, margin, laterality, EMPTY status and provisional source provenance available. Window claims must carry the observed sensitivity qualifications. Do not redesign the coordinate unless new evidence directly falsifies it. This is not canonical production architecture.

Core answers: deterministic YES; generally stable to single selected-marker loss NO; moderate thinning YES-WITH-QUALIFICATION; >100-ms offsets sparse-coverage explanation PARTIALLY; reference YES; recurrence ALL; better-covered variation YES-WITH-QUALIFICATION.

## Limitations and unresolved quantities

- Candidate-loss sensitivity does not test unknown events that were never observed; no candidate additions were made.
- Periodic thinning phases are deterministic stress scenarios, not independent random samples or confidence intervals; clustered/source-specific loss is not exhaustively tested.
- Individual selected markers are not generally stable to losing their winner. Window directions and magnitudes are not universally stable.
- Candidate count, selection margin and event-free gaps are mathematically related to nearest-distance selection; associations are descriptive, not causal.
- UNKNOWN is not evidence of poor coverage or absence. Source states remain provisional; dual support is one marker, not two independently timed attacks.
- The frozen grid is numerically continuous but not whole-track physical/perceptual pulse Ground Truth.
- Continuous mixed-source trajectory, physical full-mix Bass timing and physical Bass-vs-Drum microtiming remain NOT ESTABLISHED. No physical performer early/late claims.

JGA Drum attack timing and controlled Fishman T0 remain PROMISING. The previous insufficient continuous mixed-source trajectory validation is preserved. No model inference, candidate generation, timing-estimator development or parent mutation occurred.

## One next scientific phase — not executed

PREDEFINED MUSICAL-SECTION GROOVE COMPARISON using the frozen quarter-anchored representation and independently supplied form boundaries; do not derive boundaries from groove curves.

The next study must use this frozen representation. Stop for PI review. NO COMMIT. NO PUSH.
