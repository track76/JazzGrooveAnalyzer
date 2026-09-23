# {{REPORT_ID}} — {{ARTIST_ENSEMBLE}}: {{TRACK}}

JGA HISTORICAL REPORT TEMPLATE v1. Scope: the frozen JGA v1 hybrid historical-recording analysis architecture. This template defines presentation and provenance requirements, not a new scientific method. Fill absent facts with UNKNOWN / NOT AVAILABLE; never substitute zero for missing evidence.

## 1. Recording identification

Artist/ensemble; title; supported album/session/date/personnel or bibliographic enrichment status; source path/identifier and SHA-256; duration and decoded lineage; analyzed and excluded intervals; metric-domain annotation and its authority. Do not infer historical metadata from timing results.

## 2. JGA analysis method — short form

The original commercial full mix is primary. Frozen/adopted full-mix PLP supplies the internal temporal reference. Native observable onsets retain original coordinates. Qualified full-mix source support and complementary authorized separator evidence inform attribution. Prefer compatible full-mix timestamps; preserve separator-only observations separately. Measurements describe source-associated observable onset geometry, not exact physical gesture timing.

## 3. Musical form

Table 1: start, end, independently supplied section label, supported description and boundary uncertainty. Cite the annotation source. Never derive form from onset distributions.

## 4. Internal tempo / PLP

Report central internal BPM with its exact statistic, interval population, units and qualification. Separate raw/discrete inter-peak values from musical tempo interpretation. Identify any report-level arithmetic derived from frozen references. No smoothing, new tempo model or interpretation of lattice saw-tooth as literal performer acceleration. Exclude intervals outside the declared population explicitly.

## 5. Observable event population

Table 2: native events, reference cells, global selected/context/EMPTY counts and coverage denominator; exclusive original source states and inclusive support counts; source-conditioned coverage; matching/confirmation, full-mix-only, stem-only and ambiguity. Distinguish event, evidence-slot and cell denominators. Dual is one event. Numerical confidence is not inferred from provenance.

## 6. Global quarter-nearest geometry

Explain nearest existing native event per exact midpoint cell, frozen tie rules, no borrowing/reuse and retained context. Figure 1: frozen global whole-performance view with source-shaped gray context where prescribed. Table 3: per-category N, median, mean, IQR, MAD, sample SD, median absolute offset and range, or a compact table with full values in accompanying data. State the measurement population.

## 7. Quarter-centered Bass / Drum geometry

Figure 2: source-conditioned whole-performance view. Report Bass-to-reference, Drum-to-reference and distinct Drum-minus-Bass pairs. Distinguish PRIMARY_NONSHARED, ALL_SUPPORT_SLOTS and DISTINCT_PAIRS_ONLY populations. Report N, coverage and signs; shared-Dual/same-timestamp cases are unresolved, not zero-ms pairs. Do not infer source absence from losing global selection.

## 8. Hybrid full-mix / stem evidence

Table 5: compatible source-supported matches, full-mix-only and stem-only evidence; original source-state crossmatches and Dual qualifications where available. Figure 3: aligned full mix/stems or equivalent frozen provenance view. Separate model-derived source hypotheses from independent truth. Prefer native full-mix coordinates for compatible observations. Retain unknown/conflicting and unmatched evidence; do not silently reclassify frozen geometry. State whether hybrid summaries are joins of existing evidence or new authorized operational assignments.

## 9. Section-by-section groove analysis

Table 4: reference/selected coverage, source coverage, source-conditioned N, global median/spread, source and pair medians where supported. Use the independent form map. Describe differences and small-N qualifications. Figure 4: pre-existing independently defined informative zoom; disclose selection authority. Figure 5: source-observability diagnostic only when it materially explains a limitation; otherwise NOT APPLICABLE with reason.

## 10. Musical interpretation

Separate **OBSERVATION** from **INTERPRETATION**. Discuss supported signed clustering, spread, section contrasts and source coverage. No performer-intention inference, universal swing rule, causal separation claim or physical-attack conclusion. Positive/negative refers to the frozen reference or explicitly defined pair sign; no invented ON tolerance.

## 11. Limitations

Commercial full-mix onsets are observable landmarks, not physical gesture Ground Truth. Source support is qualified; separator labels may leak, suppress or alter landmarks. Stem-only provenance is separate. Dual does not establish two attacks. Reference and detector timestamps have finite resolution; raw BPM contains lattice effects. Selection and representation affect distributions. No invented numerical uncertainty bounds. Findings are recording-specific; report unavailable metadata and excluded regions.

## 12. JGA result summary

Mandatory human block and machine record, with identical definitions:

| Field | Value |
|---|---|
| REPORT ID | {{REPORT_ID}} |
| ARTIST / ENSEMBLE | {{ARTIST_ENSEMBLE}} |
| TRACK | {{TRACK}} |
| ANALYZED DURATION | {{SECONDS_AND_INTERVALS}} |
| PRIMARY METER DOMAIN | {{METER_AND_ANNOTATION_AUTHORITY}} |
| CENTRAL INTERNAL BPM | {{VALUE_STATISTIC_N_QUALIFICATION}} |
| QUARTER CELLS | {{N}} |
| EVENT COVERAGE | {{SELECTED_OVER_CELLS_AND_PERCENT}} |
| BASS OBSERVABILITY | {{SUPPORTED_EVENTS_CELLS_NONSHARED_N_SEPARATE_STEM_COVERAGE}} |
| DRUM OBSERVABILITY | {{SUPPORTED_EVENTS_CELLS_NONSHARED_N_SEPARATE_STEM_COVERAGE}} |
| DUAL / AMBIGUITY RATE | {{COUNTS_WITH_EXPLICIT_DENOMINATORS}} |
| BASS MEDIAN Δt | {{MS_COHORT_N_OR_NULL}} |
| DRUM MEDIAN Δt | {{MS_COHORT_N_OR_NULL}} |
| BASS↔DRUM MEDIAN | {{DRUM_MINUS_BASS_MS_DISTINCT_PAIR_N_OR_NULL}} |
| SECTION WITH NARROWEST DISPERSION | {{LABEL_IQR_AND_POPULATION}} |
| SECTION WITH WIDEST DISPERSION | {{LABEL_IQR_AND_POPULATION}} |
| PRIMARY MUSICAL OBSERVATION | {{SUPPORTED_OBSERVATION}} |
| PRIMARY LIMITATION | {{BOUNDING_LIMITATION}} |

Machine record must include schema/template version, source/parent hashes, exact unrounded numeric values, units, cohort names, numerator/denominator pairs, null for unavailable values, section identifiers and evidence paths. Human tables may round transparently. Never pool shared evidence slots as independent attacks.

## Package and quality-control requirements

Authoritative Markdown report; generic template version; machine summary; compact tables; per-event provenance/assignment data; reused figures with original path/hash and captions; parent manifests; report-level derivation script if needed; validation receipt; report freeze. Preserve external source/stem paths and hashes without unnecessary audio duplication. Mark untracked/external holdings explicitly.

Verify source and parent hashes, original timestamp/source-state preservation, statistics and denominators, graphical bytes/style, human-machine agreement, supported observations, explicit interpretations and generic template placeholders. Keep methodology and historical freezes unchanged. Update current report/session status only as needed. Follow PI authorization for commit/push; do not automatically start a new report or methodological experiment.
