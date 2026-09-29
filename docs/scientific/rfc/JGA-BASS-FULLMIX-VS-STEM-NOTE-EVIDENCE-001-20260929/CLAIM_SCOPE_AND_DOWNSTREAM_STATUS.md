# Claim scope and downstream status

Closure task: `JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-CLOSURE-001-20260929`
PI decision: `PI-BASS-FULLMIX-VS-STEM-CLOSURE-20260929`
Accepted result: `JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-001-20260929`

## Accepted claim scope
**CONVERGENT COMPUTATIONAL EVIDENCE ACROSS RELATED REPRESENTATIONS**

Permitted statement:

> Full Mix and Bass stem expose convergent computational event evidence under an identical extractor.

## Forbidden in this package
This result may **not** be described as any of the following:

- verified Bass note
- true Bass note
- Ground Truth
- independent confirmation
- source-identification accuracy
- `STEM_BETTER`
- `FULLMIX_BETTER`
- quarter
- beat
- PLP-relative microtiming

This list is binding on every derived document, figure caption, summary field and downstream
consumer of this package. Violating it re-opens the accepted result.

## Independent audit
Copilot audit of the accepted result:

| question | answer |
|---|---|
| scientific result contaminated | NO EVIDENCE OF CONTAMINATION |
| final reported numbers reconstructible | YES |
| scientific rerun required | NO |
| claim scope | VALID |
| downstream readiness | READY_WITH_QUALIFICATIONS |

## Downstream status: READY_WITH_QUALIFICATIONS

**Permitted use.** The result may be used as INPUT EVIDENCE for a future source-identification design.

**Prohibited use.** It may **not** be treated as verified source identity.

### Intended future architecture (NOT executed in this task)

| role | evidence |
|---|---|
| FULL MIX | primary event timing evidence |
| BASS STEM | corroborative source-identification witness |
| FULL-MIX PLP | separately established metric-quarter reference |

Recording this architecture is a design intention only. No downstream experiment, no PLP
access, no quarter-grid construction and no cross-method comparison was performed or is
authorized by this closure.

## Scientific integrity
- Scientific rerun: NOT PERFORMED (forbidden by PI disposition).
- Scientific bytes modified: NO.
- Quantile values preserved: T1 p95 = 60 cents, T0 p95 = 70 cents, under the preregistered
  formula `index = round(f * (n - 1))`. See `QUANTILE_TERMINOLOGY.json`.
- Deviation records DEV-1..DEV-7 preserved with PI review dispositions in
  `EXECUTION_PROVENANCE.json`.
