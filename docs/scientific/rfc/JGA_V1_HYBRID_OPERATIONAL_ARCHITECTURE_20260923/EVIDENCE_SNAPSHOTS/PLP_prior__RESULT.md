# EXACTLY LIKE YOU — PLP CONTRIBUTION

**Status: bounded development comparison completed. This is not new independent validation.**

Source SHA-256: `aec97cfb67096bd6a7c3d432f025523d1269b6b261e2dd6bc01a33c045acac45`. Scope [0,330) s from existing PI form annotation; [330,end) excluded prospectively. No other recording processed.

## What was tested

A strict pulse-proximity abstention/search prior at W=20/40/60 ms, not all possible PLP information. All widths were frozen and reported. No optimal width was selected. Native detector/source rules and acoustic estimator remain fixed; the new prior is the only conditional gate. PLP is not instrument identity or attack truth.

Frozen native population 1627; included 1606; excluded 21. Qualified source-reference clips in scope: 35. Exact notes retained in SOURCE_REFERENCE_LOCK.csv.

## Source association

| Source | W ms | A0 TP/FP/missed | A1 TP/FP/missed | Qualified result |
|---|---:|---|---|---|
| BASS | 20 | 13/0/12 | 6/0/19 | DEGRADES |
| DRUM | 20 | 30/0/5 | 9/0/26 | INSUFFICIENT_EVIDENCE |
| BASS | 40 | 13/0/12 | 12/0/13 | DEGRADES |
| DRUM | 40 | 30/0/5 | 19/0/16 | INSUFFICIENT_EVIDENCE |
| BASS | 60 | 13/0/12 | 12/0/13 | DEGRADES |
| DRUM | 60 | 30/0/5 | 23/0/12 | INSUFFICIENT_EVIDENCE |

These are selected PI-neighborhood comparisons, not exhaustive event accuracy. Unscored/UNCERTAIN labels remain in SOURCE_METRICS.json. UNKNOWN is abstention, not a verified negative. Dual support is preserved or jointly abstained; no independent pair of attacks is invented.

A1 cannot recover an unsupported baseline source by construction: recovered source associations = 0. Whole-track lost associations are not automatically false positives removed. SOURCE_ASSOCIATION_CHANGES.csv records every event/width, original timestamp, retained/lost Bass and Drum state and UNKNOWN transitions.

## Attack localization

Bass: INSUFFICIENT_EVIDENCE. No qualified same-recording Bass attack reference or accepted full-mix estimator. Fishman controlled T0 remains operational context only; no cross-recording timestamp transfer.

| Original stratum | W ms | B0 outputs / inside | B1 outputs / inside | B1 abstentions | Lost correct | Result |
|---|---:|---|---|---:|---:|---|
| DERIVATION | 20 | 2/2 | 0/0 | 2 | 2 | DEGRADES |
| DERIVATION | 40 | 2/2 | 0/0 | 2 | 2 | DEGRADES |
| DERIVATION | 60 | 2/2 | 1/1 | 1 | 1 | DEGRADES |
| VALIDATION | 20 | 7/7 | 1/1 | 7 | 6 | DEGRADES |
| VALIDATION | 40 | 7/7 | 2/2 | 6 | 5 | DEGRADES |
| VALIDATION | 60 | 7/7 | 3/3 | 5 | 4 | DEGRADES |

Paired output changes: 0 of 7 event-width pairs. Quarter-attraction/worsened-reference flags: 0. Lost correct outputs/reference exclusion remain separate selection-bias diagnostics; absence of snapping does not make the prior beneficial.

Boundary errors and secondary midpoint errors, native anchors, fixed reference intervals, all returned times and abstention reasons are in ATTACK_COMPARISON.csv. No averaging only over surviving outputs substitutes for all-N reference yield. Original held-out labels are retained for traceability but every outcome was previously exposed; current inference is developmental.

## Engineering decision

{
  "H1_by_source": {
    "BASS": "DEGRADES",
    "DRUM": "INSUFFICIENT_EVIDENCE"
  },
  "H1_overall": "INSUFFICIENT_EVIDENCE",
  "H2_BASS": "INSUFFICIENT_EVIDENCE",
  "H2_DRUM": "DEGRADES",
  "H2_overall": "INSUFFICIENT_EVIDENCE",
  "engineering": "DO_NOT_INTEGRATE_TESTED_PRIOR; no positive adoption gate demonstrated",
  "scope": "Only the registered pulse-proximity prior; not all PLP-derived context. PLP BPM adoption unchanged."
}

Do not integrate this tested prior into JGA. Do not infer that all periodicity/context priors fail, or that PLP tempo adoption is reversed. No claim about Ride/Hi-Hat follows. No false claim of physical Bass/Drum timing or groove recalculation.

## Limitations and next action

The source reference is small, overlapping, selected and already exposed; models and source links have development dependencies. The Drum estimator already has seven in-reference outputs and one contrast abstention on the original eight-event validation set, so a restrictive prior has little positive headroom. Visual-reference anchoring and 8-ms intervals limit accuracy claims. PLP peak time quantization is approximately 23.22 ms. Acoustic sub-quarter events need not coincide with quarter pulses. These are substantive limitations, not a post-hoc retuning invitation.

Next PI action: review this bounded result and decide whether to authorize independent Bass attack-reference qualification on the existing target evidence before any further PLP-prior trial. Not executed. No model search, source separation, tempo rerun, production modification, commit or push.
