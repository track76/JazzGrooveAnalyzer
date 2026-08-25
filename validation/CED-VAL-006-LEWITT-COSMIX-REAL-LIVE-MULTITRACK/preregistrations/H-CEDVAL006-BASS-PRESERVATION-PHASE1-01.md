# CED-VAL-006 Bass Preservation — Phase 1

Preregistration: `H-CEDVAL006-BASS-PRESERVATION-PHASE1-01`

Status: **FROZEN PREREGISTRATION — NOT EXECUTED**

## Question

Determine whether the severe Bass EME population deficit frozen by
`EXEC-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01` can be materially
reduced by removing Demucs' random shift or preserving float32 output. This
phase does not change `htdemucs`, JGA, or any scientific semantics.

The machine-readable same-ID JSON record is controlling authority.

## Conditions

- A is the immutable two-run baseline: `htdemucs`, CPU, shifts 1, split,
  overlap 0.25, jobs 0, default segment, rescale, signed 16-bit WAV. It is not
  rerun.
- B is identical except `shifts=0`; signed 16-bit WAV.
- C is B plus Demucs `--float32`; rescale remains unchanged.

B and C each require two independent fresh-process executions. Preserve all
four stems and their complete technical/checksum authority. Never select or
average a run. Run unchanged JGA v0.3.0-alpha on each Drum/Bass pair, freeze
the reports, and only then score twice using the existing Level-1/2/3 rules.

## Decision gate

A candidate produces a material Bass-population improvement signal only if
both runs exceed the best frozen baseline for matched count (>625), recall
(>0.5924170616113744), and F1 (>0.7212925562608193), with original-only count
below 430. Timing remains required descriptive evidence but cannot compensate
for poor population recovery.

The severe deficit persists only if all four B/C runs remain at or below the
best baseline recall and retain an absolute EME deficit of at least 377.
Intermediate evidence is `MIXED_OR_INDETERMINATE`. Every outcome stops for
scientific review.

`htdemucs_ft`, `htdemucs_6s`, and `mdx_extra` are explicitly deferred. No
download, checkpoint authority, or execution is authorized in Phase 1.

No latency correction, H02, strength, GT-derived tuning, model change,
production change, or scientific-semantic change is allowed.
