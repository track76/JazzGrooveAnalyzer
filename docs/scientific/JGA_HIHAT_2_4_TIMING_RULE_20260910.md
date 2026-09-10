# PI decision — qualified jazz Hi-Hat 2&4 timing reference

Decision ID: `JAZZ_HIHAT_2_4_TIMING_RULE`. Date: 2026-09-10.

Status: **PI-ADOPTED PROSPECTIVE DOMAIN HYPOTHESIS/RULE; NOT PROSPECTIVELY VALIDATED.** Authority: the PI instruction “JAZZ HI-HAT 2&4 INTERNAL TIMING REFERENCE.” This record changes the current source-conditioned research route; it does not amend experimental results or authorize execution in this documentation task.

## Domain rule and scope

In admissible jazz audio, an identified Hi-Hat stream that qualifies as recurrent, locally persistent timekeeping may be interpreted under this rule as a drummer's 2-and-4 reference. Presence of Hi-Hat alone never activates the rule. The musical interpretation is a PI-adopted domain hypothesis; it is not a mathematical consequence of recurrence and not a universal historical-jazz fact.

For a qualified persistent Hi-Hat timekeeping interval `T_HH`:

`T_BEAT = T_HH / 2`

`BPM_INTERNAL = 60 / T_BEAT = 120 / T_HH`

These definitions assign two beat periods between consecutive timekeeping anchors under the rule. They do not assign this interpretation to every adjacent raw prediction. Recognition omissions can leave larger observed gaps; they must not be repaired or used to infer beat multiplicity without supporting authority. Unknown gaps remain unknown.

The source-conditioned reference identifies an alternating 2/4 role; it does not by itself determine which initial anchor is 2 rather than 4, a bar origin, or downbeat. Such phase labels must remain unresolved unless separately established. No inferred intermediate beat is an acoustic observation.

The rule belongs to musical Domain interpretation, downstream of source-labelled observations and temporal evidence. Core observation semantics, EME/source identity authority and existing architectural decisions are unchanged. No implementation, schema or classifier is introduced here.

## Activation and abstention

All conditions must be supported by recorded evidence for the population/interval under examination:

| Condition | Required meaning |
|---|---|
| Admissible jazz input and source identity | Preserve input/recording authority, source identity, recognition uncertainty and timeline binding. A detector candidate is not automatically an identified or verified event. |
| Recurrent structure | Preserve exact or otherwise independently authorized temporal measurement semantics, witnesses, alternatives and dependence. Presence/count alone is insufficient. |
| Successive local persistence | Show locally distributed timekeeping support, not only distant pairs or one isolated region. |
| Sufficient temporal coverage | State the authorized interval, supported portions and missingness; broad first/last span alone is insufficient. |
| Timekeeping qualification | Evidence must support sustained timekeeping rather than a population explained only by isolated fills/accents. Lack of annotation is not proof that this condition holds. |
| Reproducibility | Bind inputs, numerical method, parameters, local support and checking/replay evidence. |

If these conditions are insufficient, materially ambiguous, contradicted, or cannot distinguish a usable timekeeping interval, return **`HIHAT_2_4_REFERENCE_UNAVAILABLE`**. Irregular, decorative, fill-based, absent or uncertain streams must not be forced through the rule. Missing predictions alone do not invalidate an otherwise qualified interval; equally, they do not authorize invented anchors. Retain observed events outside the supporting relation.

The PI decision freezes these activation semantics, not an invented numerical PASS threshold. The next blind validation must bind its operational qualification/evaluation choices and anchor-admission procedure before results or external tempo are examined. Neither 6/6 regions nor any CED-VAL-005 count becomes a universal criterion by retrospective convenience. Do not tune the gate to obtain external-tempo agreement.

## Observation, qualification and inference lineage

| Record/role | Authority and preservation |
|---|---|
| `OBSERVED_HIHAT_EVENT` | Preserve original timestamp, file/channel, observation/detector lineage and uncertainty. Existing Vogl outputs remain candidates, not retroactively promoted Ground Truth. |
| `HIHAT_TIMEKEEPING_EVENT` | Event admitted into a qualified timekeeping stream, with qualification evidence and supporting-relation membership. |
| `HIHAT_2_4_REFERENCE_ANCHOR` | An actual admitted event interpreted under the active rule, retaining its original timestamp and domain-rule provenance. |
| `INFERRED_INTERMEDIATE_BEAT` | A derived location under the admitted relation, separately labelled inferred, with parent anchors, method and uncertainty. Never represented as an observed strike. |

Observed timestamps are not quantized to an ideal grid. Qualification and reference construction must preserve every original event and rejected/unsupported/indeterminate memberships. This document does not manufacture an anchor list from the 141 existing predictions.

## CED-VAL-005: retrospective motivation only

The following is recorded from accepted evidence and the PI's supplied interpretation, not a new calculation or experiment:

- 141 frozen Hi-Hat candidates; 1,649 recurrent exact relations; 5,444 supporting distinct pairs.
- Exact `T_HH = 0.500 s` is the strongest descriptive local-persistence candidate, supported in all six primary and five shifted regions. This established bounded local support, not independently validated metric function or missing-event robustness.
- The [frozen internal decision](../../validation/RIDE-HIHAT/CEDVAL005_INTERNAL_PULSE_20260910/REPORT.md) selected 0.500 s → **120 BPM**, with half/double metric ambiguity **UNRESOLVED**. It remains unchanged, including its scoring and claim limits.
- Under the **new** rule, the PI-supplied retrospective interpretation is `T_HH = 0.500 s`, `T_BEAT = 0.250 s`, **`BPM_INTERNAL_2_4_RULE = 240 BPM`**.
- External documented tempo supplied for this retrospective comparison: **approximately 246 BPM**. The PI independently identified the timekeeping role as 2 and 4. Neither fact is permitted as input to a future blind result.

**CED-VAL-005 PROSPECTIVE VALIDATION: NO.** Its tempo is now known; the new interpretation is motivating evidence, not a blind validation, a correction of the earlier frozen prediction, or proof of universal accuracy. The domain hypothesis was adopted after exposure to this result. No new BPM is computed in this task.

Preserved records:

| Record | SHA-256 |
|---|---|
| [Hi-Hat comparison](../../validation/RIDE-HIHAT/HIHAT_JAZZ_COMPARISON_20260910/REPORT.md) | `1b7c5d12d081af728aabdb362501e7f11c2e57720aca0cc43b48051c6bf0dbc4` |
| [Hi-Hat local persistence](../../validation/RIDE-HIHAT/HIHAT_LOCAL_PERSISTENCE_20260910/REPORT.md) | `e3fb48286033accf07657d793791c7a6c895df3f130ae1db2998118afcf66ea0` |
| [Ride recurrence](../../validation/RIDE-HIHAT/CEDVAL005_RIDE_RECURRENCE_20260910/REPORT.md) | `9bcc40b9a125892af643de3a86cff2ece6c449306fd80ba64f1b13fb9697baa2` |
| [Cross-source result](../../validation/RIDE-HIHAT/CEDVAL005_CROSS_SOURCE_20260910/REPORT.md) | `6a66d7598c5836859d6a8d6e284a1c2837f804a5e44d7a3ebceafe3adc433f9c` |
| [Synchronization check](../../validation/RIDE-HIHAT/CEDVAL005_SYNC_20260910/REPORT.md) | `dab98518bfc58211834adba08d110f399324d94886d0894e7d8d60c4e1d575bb` |
| [Frozen internal decision](../../validation/RIDE-HIHAT/CEDVAL005_INTERNAL_PULSE_20260910/REPORT.md) | `225d014ca2fe2f7dadd9617a87fde48d3f379a7d3825c0e87bc36999c45e9910` |

Each record continues to bind its external evidence under `/Volumes/SSD Track/JGA/experiments/`. All prior GMD/ENST/Vogl, global Drum map/recurrence and associated validation histories remain unchanged. No heavy evidence is copied or moved.

## Ride, Double-Bass and visualization

Ride remains a separate timing/articulation evidence stream for later study of swing structure, subdivisions, microtiming, drummer-specific placement and historical change. It is not required to corroborate an otherwise qualified Hi-Hat reference. Do not pool the two streams, discard Ride evidence, or assume any Ride articulation in advance. Independent source preservation does not imply statistical independence.

Future Double-Bass event analysis may use the independently established Hi-Hat reference. Preserve original Bass timestamp, nearest admitted 2/4 anchor and its identity, signed offset, relation to any separately inferred intermediate beat, confidence and source/time authority. Never snap Bass events to the reference or use Bass timing to establish the reference against which it is measured. Ahead/on/behind interpretation requires appropriate timing uncertainty; no numerical on-time threshold is invented here. Current Double-Bass research, capture and experiments are untouched and unexecuted.

Future visualizations should emphasize events supporting the displayed relation and show other observed events lightly/secondarily. Unsupported events are not errors: articulation, fills, comping, embellishment or microtiming are possible explanations, not automatic labels. Preserve their scientific lineage and original timestamps.

## Current roadmap and prospective validation

**Primary route where applicable:** jazz audio → Hi-Hat identity → timekeeping qualification → source-conditioned 2&4 reference → internal beat period → internal BPM. Ride remains separate articulation/timing evidence. Generic BeatReference discrimination is **FALLBACK** when qualified Hi-Hat 2&4 evidence is unavailable; it remains separately authorized future research, not an automatic fallback execution in this task. The global recurrence-sufficiency track remains DEFERRED_PARALLEL with its prior authority gaps unchanged.

This supersedes only the primary-route priority of the [historical Ride-first decision](JGA_RIDE_FIRST_TIMING_RESEARCH_DECISION_20260910.md), not its preserved results. It does not claim every jazz Hi-Hat event is 2 or 4, universal beat detection, or validated coverage across historical eras.

**Next minimal scientific step:** prospective blind validation on another admissible jazz performance. Required order: audio → Hi-Hat recognition → recurrence → local persistence → frozen activation gate → `T_HH` → `T_BEAT = T_HH / 2` → internal BPM → freeze complete result, including abstention/ambiguity → only then reveal external BPM. External tempo, tapping, metadata tempo, meter labels and expected patterns must not select or tune any internal decision. Freeze the evaluation and provenance plan before acquisition/inference outcomes are inspected; no new dataset is searched in this task.

Authorization boundary: **BeatReference — source-conditioned Hi-Hat 2&4 rule only; BPM — prospective validation only.** This documentation task runs no validation, no new timing/BPM computation and no production implementation. Stop for PI review; no commit or push.
