# Current final anchored report authority

The PI-adopted final M33–M48 report is [JGA_FINAL_REPORT.pdf](FINAL_BPM_TEXT_CORRECTION_20260925/JGA_FINAL_REPORT.pdf); [freeze record](FINAL_BPM_TEXT_CORRECTION_20260925/FREEZE_RECORD.json). Earlier report versions below remain historical evidence and are not overwritten.

# JGA HISTORICAL REPORT 001 — Ray Brown Trio, Exactly Like You

Phase: HISTORICAL JAZZ CORPUS ANALYSIS / REPORT PRODUCTION.

- [Authoritative historical report](REPORT.md).
- [Machine-readable summary and precise cohort definitions](SUMMARY.json).
- [Reusable JGA Historical Report Template v1](../JGA_HISTORICAL_REPORT_TEMPLATE_V1.md).
- [Human summary field record](HUMAN_SUMMARY_FIELDS.json).
- [Reused table/figure provenance and hashes](LINEAGE.json).
- [Parent verification](PARENT_VERIFICATION.json).
- [Quality-control receipt](VALIDATION.json).
- [Report freeze](REPORT_FREEZE.json).

`figures/` contains five existing figures in their original PNG and PDF formats. No visual redesign, new detector, separation or PLP run was performed. `data/` contains byte-copied frozen event/assignment/statistic tables and parent manifests, plus report-only arithmetic and provenance joins.

New report-level derivations are limited to: 904 adjacent-reference interval descriptors; machine/human summary assembly; the native-event-to-frozen-stem-match provenance join; and an explicit unmatched-stem inventory. No event was reselected, relabelled in the original evidence, retimed or snapped. `HYBRID_EVENT_PROVENANCE.csv` preserves original source states and timestamps while recording complementary source evidence. “FULL-MIX + STEM CONFIRMED” denotes compatible representations, not independent identity truth; `original_source_support_agrees` distinguishes original source agreement from additive separator hypotheses. DUAL remains visible in the original source-state field and source-conditioned assignment table.

Copied manifests retain their original member-path semantics: resolve them against the original study directory recorded in `LINEAGE.json`. The report's own freeze lists package paths directly. All report figures, source tables and summaries needed to read the report are committed; original commercial audio and large stem assets remain at their established external paths and hashes. The source-provenance links in copied rows are historical, not instructions to regenerate evidence.

The v1 architecture decision file remains unchanged. Its sealed historical versions of project/session/bootstrap documents are recoverable at the commit recorded in `PARENT_VERIFICATION.json`; authorized Report 001 completion notices update current recovery documents only. This is normal current-state evolution, not rewriting a prior freeze.

`build_report.py` documents the bounded assembly. It is not an instruction to rerun models or regenerate scientific evidence. `validate_report.py` performs read-only checks. No Report 002 work is executed here.
