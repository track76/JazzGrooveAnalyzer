# Final anchored BMIG / DMIG — prospective candidate protocol

New candidate only, no canonical adoption. Recorded before new grid estimation and before any new cross-instrument differences. Previous results exposed, no investigator blindness. No selection/tuning against old+1.578ms or desired ahead/behind.

Use exactly the frozen same-instrument QUARTER_FIT_OBSERVATION representative at each Q131–Q194 from EVENT_PROVENANCE_127.csv. All additional63Bass/64Drum population events preserved; not additional grid slots. Q195 context preserved but not fitted. No new event/quarter selection. Same algorithm for each instrument, only own n=0..63 and own observed times enter.

Model: soft quarter anchors plus local quarter-duration continuity. Minimize
J(g) = sum_(observed n) (g_n−t_n)^2 + (1/16) sum_(n=1..62) (g_(n−1)−2g_n+g_(n+1))^2.
No equality g_n=t_n, no observation deletion, no robust downweighting of eligible anchors, no external instrument or PLP times. All eligible anchors have equal coefficient1; quarter is reconstruction unit. Additional-event identity/timestamps never changed. No whole-measure eligibility gate.

Why1/16: fixed prospectively to privilege local data. The local continuity stencil has interior diagonal6/16=0.375 and total absolute off-diagonal10/16=0.625, both below the unit data term at an observed slot. Thus anchored normal-equation rows are strictly diagonally dominant with gap1−4/16=0.75. This is a modeling preference, not validated physical calibration or an acceptance threshold. No tuning or sensitivity-based model selection in this task. Continuity couples only adjacent quarter durations, not a globally imposed line or BPM. It may retain local timing fluctuations; every duration and duration-change reported.

Let W have diagonal1 at observed slots and0 elsewhere, D2 be62×64 second-difference operator. Solve (W+(1/16)D2.T D2)g=W t. For conditioning subtract same-instrument median(t) before solution and add back afterward. Matrix positive definite with>=2 distinct observed slots. Missing slots follow the same coupled minimizer, not delta interpolation. Boundary: no exterior evidence, no reflected/synthetic points; natural finite-domain second-difference penalty. Isolated sparse measures are not fitted separately. No measure-boundary reset. Stop if numerical solve fails or any of63 intervals<=0; do not repair/tune after seeing results.

Write/hash own-only input and each independently estimated grid before comparison. Pure solver signature (n,t), no other data. Programmatically test counterpart-input perturbation invariance, verify normal equations, and verify all original event strings preserved. Model does not force strict monotonicity by moving outputs: monotonicity is an integrity gate on its actual solution.

After both output hashes saved: GRID_DELTA=BMIG−DMIG, negativeBass ahead. Each measure contributes median of four deltas, global=median16measure medians. Recalculate six frozen4/4 measures separately. Compare all prior existing grids per instrument (not only mutually eligible), plus previous common10measure subset and continuous Huber trial. No ms acceptance/materiality thresholds. A nonreproduced+1.6ms reader-facing value cannot be printed as current data. If the new result does not support the approved exact paragraph, STOP before candidate-report generation as explicitly required by the conclusion gate. Never tune to pass the paragraph.

Display-only midpoint decomposition retained, no scientific coordinate changes. BPM start/end: select first/last saved local_bpm row of global__PLP_REFERENCE.csv whose native time lies in [Q131,Q195); no mean/block/curve substitution or BPM recomputation. Frozen global32-quarter curve and approved extrema remain distinct saved display authority. 161.49902343750287 reference is median904elementary interval BPM.

No audio inference, canonical score change, freeze, bootstrap, commit/push. Software requirement record only: [TUTTO IL BRANO] or [DA MM:SS.xx]→[A MM:SS.xx]; subsequent analysis/report respects selected interval. No GUI implementation.
