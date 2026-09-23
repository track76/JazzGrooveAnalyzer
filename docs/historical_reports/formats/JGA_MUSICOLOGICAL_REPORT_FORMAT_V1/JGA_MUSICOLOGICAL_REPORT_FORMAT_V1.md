# JGA Musicological Report Format v1

Status: FROZEN — PI-approved reporting specification; reference-example data and all 15 pages validated. JGA v1 methodology remains closed. This is a reporting format, not a detector, identity classifier or physical-attack model.

Primary output: A4 portrait Microtiming Score, four measures per row, target four rows per page; readable spacing takes priority. Compact header, top BPM panel, local BPM above each row, no left information column. Final incomplete row/measure retained explicitly. Pre-anchor references retained without invented metric labels. No formal segmentation.

Require an authoritative human/recording metric origin. Preserve chronological Q IDs. Start M1 at validated Beat 1; do not reset labels between pages. 4/4 has four quarters per measure, 3/4 three; bold Beat 1 boundary, thin other quarter guides. Never infer meter changes or apply 4/4 arithmetic to other meters without authority. Report 001 renderer is scoped to its approved 4/4 data; generic 3/4 renderer is not claimed implemented.

Tempo curve: PI-authorized 32 complete quarter intervals, 33 frozen references; BPM=60*32/elapsed seconds, stride one quarter, x at elapsed-time midpoint. Joined observed values, no new smoothing. In 4/4 this is eight measures; in 3/4 retain interval count and do not call it eight measures. First full window begins at/after validated origin; last ends within scope. Central statistic retains its own frozen definition. State exact endpoint IDs and row-local display-window convention. Show signed endpoint change and percent; no arbitrary stability threshold or performer-intention claim.

Source-conditioned selected Bass: #286ea8 hollow circle. Drum: #c66a16 diamond. Context: #bfc3c7 with original source shape. Unknown triangle, unresolved Dual square. Do not recolor ambiguous Dual as exclusive Bass/Drum. Preserve global selection evidence separately. Native event x and signed delta y remain unchanged. Zero is the PLP reference. Signed ms labels; no invented ON tolerance.

Preserve stable pair IDs, thin links at original positions, signed Drum−Bass distinct from instrument-to-beat offsets. DUAL is one timestamp, never two attacks. Retain exact pair table, original source provenance, empty annotation fields until PI notes. Pxx* only for actual human annotations. Identify all lattice-tied minimum/maximum absolute separations while retaining sign.

Human report: tempo/start/central/end/change; primary Bass/Drum median,N,before/after/exact%; direct paired median,N,ordering%; per-beat descriptive statistics with visible small-N qualification; extreme pairs; one concise observable-onset/physical-gesture limitation. Engineering lineage remains supporting material. No stem/full-mix competition in main narrative.

Required package: report Markdown, complete PDF plus page PNGs, tempo figure/data, metric reference, beat table, pair table, machine-readable profile, reproducible report derivation, lineage and validation, additive freeze with parent hashes. Inspect every page; verify timestamp/state preservation, metric/quarter continuity, provenance and exact arithmetic. Keep historical freezes unchanged. Commit only after authorized validation.

FUTURE_NON_SPECIALIST_EXPLANATORY_PAGE: deferred. Formal analysis deferred; do not assume eight-bar or even-length sections.

Reference implementation/example: ../../JGA_HISTORICAL_REPORT_001/FINAL_SCORE_V1/.
