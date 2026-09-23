# Final operational JGA v1 analysis — Exactly Like You

**Decision: USABLE_WITH_QUALIFICATION for reproducible source-associated observable onset geometry.** This applies the PI-authorized operational measurement semantics; it does not overturn the preceding physical-attack-qualified trial or historical PLP independent FAIL. No claim of cross-recording validation is made from this development recording.

## Operational authority and lineage

The original full mix is the sole signal authority. Source SHA-256 `aec97cfb67096bd6a7c3d432f025523d1269b6b261e2dd6bc01a33c045acac45`. No decoding, model inference, source separation, new detector, attack refinement, tempo inference or PLP retuning occurred. Frozen PLP freeze `4384911f6086ba8a1a6f9deaa8370ae9ba22f6339ae42b3b0b4a015204efa7ac` supplies the unchanged reference timestamps. Exact parent paths/hashes and byte-identical snapshots are in INPUT_LINEAGE.json and INPUT_SNAPSHOTS.

Analyze [0,330) s; exclude [330,347.8117006802721) s using the independent approximate PI form boundary. The first/last midpoint cells are clipped to the common analysis domain, as the original algorithm clips to its declared domain. No new reference peak is synthesized. The final included reference uses the next frozen peak only for its forward interval-BPM descriptor.

## Exact reused representation

The original selection block is executed with the PLP grid adapter. Decimal midpoint cells use (left,right] internally, exact midpoint to earlier reference; first boundary closed, final domain boundary open. Winner order: absolute distance, earlier native timestamp, lexical event ID. UNKNOWN competes equally. No distance threshold, borrowing, reuse, timestamp change or identity change. Empty cells remain EMPTY. Every nonwinner remains CONTEXT, shown light gray regardless of identity. Historical joined-grid fields are retained as provenance, not used as authority. See PLOTTING_ADAPTATION.md.

Selected `BASS_SUPPORTED` means operational BASS_ONSET, `DRUM_SUPPORTED` means DRUM_ONSET; DUAL is one timestamp with two support hypotheses. These are observable landmarks, not physical gesture times. Generic Drum does not imply Ride or Hi-Hat. No numerical ON tolerance was found in the governing selection contract; none is invented. Report signed delta only.

## Population and historical comparison

| Population | Frozen historical full domain | Historical matched [0,330) | PLP [0,330) |
|---|---:|---:|---:|
| References | 946 | 912 | 905 |
| Native events | 1627 | 1606 | 1606 |
| Selected | 898 | 880 | 891 |
| EMPTY | 48 | 32 | 14 |
| Gray CONTEXT | 729 | 726 | 715 |
| Selected BASS_ONSET | 6 | 6 | 3 |
| Selected DRUM_ONSET | 513 | 510 | 593 |
| Selected DUAL | 122 | 121 | 174 |
| Selected UNKNOWN | 257 | 243 | 121 |

PLP selection coverage is 98.45% versus 96.49% with the old reference in the same domain. Exactly 685 native events change PRIMARY/CONTEXT role; all 1,606 original timestamps and states remain identical. Full historical comparisons additionally differ in scope (21 excluded ending events and the ending references). The matched-domain comparison isolates the reference-input change under identical selection/domain rules. Changes are not identity reclassification.

| All selected statistic | Historical matched | PLP |
|---|---:|---:|
| median_ms | -0.03 | 11.61 |
| mean_ms | 1.51 | 1.04 |
| IQR_ms | 97.53 | 58.05 |
| MAD_ms | 49.53 | 23.22 |
| SD_ms | 75.56 | 37.36 |
| median_abs_ms | 49.51 | 23.22 |
| min_ms | -182.82 | -116.10 |
| max_ms | 182.43 | 81.27 |

Smaller selected distances are reference-dependent geometry, not proof of improved physical accuracy. Nearest selection structurally favors close events and depends on candidate density.

## Selected landmark statistics

No CONTEXT event is pooled into these statistics. DUAL is never duplicated. Coverage uses all 905 reference cells; sample standard deviation uses ddof=1; MAD is median absolute deviation from the sample median. Reporting precision below does not imply physical accuracy.

| Category | N | Coverage % | Median ms | Mean ms | IQR ms | MAD ms | SD ms | Median abs ms | Range ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ALL SELECTED | 891 | 98.45 | 11.61 | 1.04 | 58.05 | 23.22 | 37.36 | 23.22 | -116.10 to 81.27 |
| BASS_ONSET | 3 | 0.33 | 34.83 | 11.61 | 46.44 | 11.61 | 50.61 | 46.44 | -46.44 to 46.44 |
| DRUM_ONSET | 593 | 65.52 | 11.61 | 4.64 | 46.44 | 23.22 | 36.80 | 23.22 | -104.49 to 81.27 |
| DUAL | 174 | 19.23 | 11.61 | 13.41 | 34.83 | 11.61 | 23.20 | 11.61 | -116.10 to 58.05 |
| UNKNOWN | 121 | 13.37 | -34.83 | -34.64 | 34.83 | 11.61 | 35.78 | 46.44 | -104.49 to 69.66 |

## Form-linked reading

Section membership follows reference timestamps, as in the validated method; original selected timestamps are preserved separately. All current selected timestamps happen to remain within their reporting section. Boundaries are approximate PI musical annotations, not estimated from offsets.

| Section | Selected / references | EMPTY | CONTEXT | BASS / DRUM / DUAL / UNKNOWN | Median ms | IQR ms |
|---|---:|---:|---:|---|---:|---:|
| M1 Opening | 128/131 | 3 | 124 | 0/74/33/21 | 23.22 | 49.34 |
| M2 Piano / walking Bass | 257/257 | 0 | 178 | 2/151/73/31 | 11.61 | 46.44 |
| M3 Piano–Bass exchanges | 124/125 | 1 | 127 | 0/91/0/33 | 11.61 | 58.05 |
| M4 Piano–Drum exchanges | 117/127 | 10 | 90 | 0/99/6/12 | -11.61 | 69.66 |
| M56 Final theme / turnaround | 265/265 | 0 | 196 | 1/178/62/24 | 11.61 | 34.83 |

Opening selected landmarks have median +23.22 ms. The walking-Bass section has full cell coverage and median +11.61 ms, but only two Bass-only selections; 73 are Dual. The Piano–Bass exchanges have no Bass-supported selected events (nor Bass-supported native candidates in that region), so they support observable-field description rather than an isolated Bass trajectory. This is missing source support, not absent Bass.

The Piano–Drum exchanges have the broadest selected IQR (69.66 ms), median −11.61 ms and ten EMPTY cells. This is a section-specific change in selected landmark distribution and coverage, not proof of intentional performer anticipation. Final-theme/turnaround has full cell coverage and narrower IQR 34.83 ms. Recurring positive selected medians in opening, piano/walking, Piano–Bass and final material are descriptive; source composition changes and source mixtures preclude a continuous same-instrument trajectory.

PLP maxima lie on the frozen 512/22050-second analysis lattice. Inter-peak BPM takes discrete neighboring values near 152.00, 161.50 and 172.27. The upper plot preserves these unmodified; its rapid zigzags are not evidence of rapid performer acceleration/deceleration. Native markers also retain their sampling lattice. Neither precision is a calibrated physical uncertainty bound.

## Observable Bass–Drum relationships

The separate selected Bass-only and Drum-only distributions permit a limited source-associated comparison. In M2, two Bass-only selections versus 151 Drum-only give Bass-minus-Drum median-offset contrast −11.61 ms; in M56, one versus 178 gives +23.22 ms. These tiny Bass samples are not stable ensemble-lag estimates and are not simultaneous event pairs. DUAL is excluded from both contrasts. Other sections lack Bass-only selections, so the contrast is unavailable. The trial does not require physical gesture Ground Truth to describe this observable geometry, but it does not manufacture a paired Bass–Drum delay.

## Visualization and completeness

[Whole performance](QUARTER_NEAREST_GROOVE_WHOLE_TRACK.png) · [Reference 02:02–02:08.5](QUARTER_NEAREST_REFERENCE_WINDOW.png), also PDF/SVG. Original validated colors/shapes retained: Drum orange diamonds, Bass hollow blue circles, Dual purple squares, UNKNOWN dark triangles, context light-gray circles, gray reference guides and unfilled red EMPTY rail. Every one of 715 context events is plotted. Whole plot contains all 905 references, 891 selected landmarks and 14 EMPTY cells. Reference view contains 19 selected landmarks and 15 context events across intersecting cells, with neighboring edge context retained; it was not chosen from favorable output.

## Decision and limits

**USABLE_WITH_QUALIFICATION** as the PI-defined operational historical-recording analysis format: deterministic source-associated observable onset geometry relative to PLP, not sample-perfect physical performer reconstruction. Missing numerical physical attack uncertainty does not invalidate this operational measurement. Main qualifications are source coverage, provisional identity, source mixture, grid/marker resolution, density-dependent nearest selection and development-recording reuse. Changes in reference alter selections and distributions; do not silently compare them as the same measurement. No new generalization success or universal quarter authority is claimed.

This engineering assessment uses the newly explicit operational acceptance target. It neither edits the preceding PARTIALLY_USABLE attack-qualified trial nor rewrites independent PLP FAIL (10 aligned,10 mostly,3 misaligned,1 uncertain). No physical-timing evidence has been upgraded by wording. The rejected restrictive PLP attack prior remains excluded. All historic negative and qualified evidence remains intact.

Recommended next action: PI approve an operational JGA v1 format freeze for subsequent historical-corpus analysis. Do not automatically initiate another research cycle.

## Validation

Source and parent hashes verified; original selection and figure contracts preserved; independent exhaustive cell-membership/winner check passed for PLP and matched historical domains; exact ties checked; no reuse, borrowing, event loss or timestamp/state changes. All 637 closure-preservation hashes remain unchanged. Figures visually inspected; all context retained. No software runtime changed. No commit or push performed for this bounded application package.
