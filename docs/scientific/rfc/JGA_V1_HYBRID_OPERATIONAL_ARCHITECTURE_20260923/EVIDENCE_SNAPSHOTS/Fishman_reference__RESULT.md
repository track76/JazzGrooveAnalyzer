# JGA-CONTROLLED-DOUBLE-BASS-ATTACK-REFERENCE-REREVIEW-001

Status: PASS for completion of the blinded methodological audit. Scientific decision C — REFERENCE REPRODUCIBILITY NOT ESTABLISHED. Parent findings remain historically unchanged.

## Blinding and sequence
PI expressly authorized a fresh-context reviewer agent. Its context contained only the frozen review rule, neutral materials and minimal instructions. It accessed only those inputs and its new outputs, with no parent intervals, estimator, mapping, source names, splits or earlier states. This is NOT inter-rater human validation or an independent recording. The coordinator was previously exposed but did not author or alter the new judgments.

The reviewer generated36 channel records and12 multi-witness states and froze them before sending results. Fresh freeze SHA-256:38935840d1b88e77ad6d604e1834608aab32dd5504494462cf3d3f5ef3873e04. The coordinator verified that hash and both CSV hashes before opening the mapping or parent reviews. It then completed/froze old-versus-new comparisons before estimator-specific extraction and evaluation. Technical qualification: the parent multi-witness state CSV also contains consensus columns; that container was read for state comparison, with only state fields used before comparison freeze. No such information reached the fresh reviewer.

All12 locked events and36 source WAVs were preserved. Fixed windows and representations remained unchanged. No inference or estimator rerun, selection change or retuning occurred. New intervals are in local milliseconds; separate comparison columns map them to native source samples with outward rounding. This conversion adds at most a sample of boundary padding, not physical timing precision. The original frozen reviewer CSVs remain untouched.

## Channel reproducibility
| Channel | Old/new bounded | Both | Overlap | Disjoint | Old/new median width ms | Median absolute midpoint shift ms | Max shift ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| FISHMAN | 12/11 | 11 | 11/11 | 0 | 7.0/18.0 | 10.0 | 18.0 |
| DPA4099 | 12/12 | 12 | 8/12 | 4 | 8.0/7.5 | 4.7 | 24.5 |
| NT5 | 11/12 | 11 | 7/11 | 4 | 8.0/5.5 | 5.5 | 23.0 |
| ALL | 35/35 | 34 | 26/34 | 8 | 8.0/8.0 | 7.0 | 24.5 |

Overall:35 old bounded,35 new bounded,34 bounded in both.26/34 overlap (76.5%);8/34 are disjoint (23.5%). Median intersection3.0ms. Median set-union width13.5ms; median enclosing span17.0ms. The CSV reports both because disjoint interval union length differs from the enclosing envelope. All midpoint quantities are secondary descriptions, not ground truth. New width distributions are preserved in REPRODUCIBILITY_SUMMARY.csv, including wider Fishman pressure-transition bounds.

Overlap alone overstates agreement: broad new Fishman intervals overlap old ones while their midpoints move substantially. Several DPA/NT5 intervals shift earlier and are disjoint. The new reviewer often includes early low-level contact/emergence that the parent treated as a precursor to a later sustained response. This is evidence that the operational boundary is not reproducible under the present instructions; it does not prove either review locates physical excitation correctly.

## Multi-witness states
Old:11 CONSISTENT,1 UNRESOLVED. New:9 CONSISTENT,2 PARTIALLY_CONSISTENT,1 UNRESOLVED. Exact state agreement10/12. Changed events:

- REVIEW_009 / GAL09_20260914_S1_D_MF_R01: CONSISTENT → PARTIALLY_CONSISTENT. FISHMAN new interval 5.764989–5.783016s; DPA4099 new interval 5.783991–5.788005s; NT5 new interval 5.780998–5.787007s; the channels no longer share a triple intersection, although a pair overlaps. Raw arrival bounds are not propagation-adjusted.

- REVIEW_012 / GAL09_20260914_S2_E_CN_R01: CONSISTENT → PARTIALLY_CONSISTENT. FISHMAN new interval 3.440000–3.460000s; DPA4099 new interval 3.461995–3.466009s; NT5 new interval 3.460000–3.467007s; the channels no longer share a triple intersection, although a pair overlaps. Raw arrival bounds are not propagation-adjusted.

REVIEW_008 remains UNRESOLVED, but the reason changes: old NT5 abstention becomes new Fishman abstention, while NT5 receives a new early interval. Stable coarse state therefore does not imply stable channel interpretation.

## Existing held-out estimator versus new review
No estimator rerun.24 channel outputs:23 evaluable against new bounds;5 inside,18 outside. One is unevaluable because the new Fishman review abstained. Fishman3/7, DPA1/8, NT51/8 inside.

Eight consensus outputs:7 evaluable against a fully bounded multichannel enclosing interval;1 inside,6 outside. One remains unevaluable. This matches the parent's enclosing-union convention, not a claim that every time inside the hull belongs to an individual channel interval. Channel misses range0.113–21.429ms; consensus misses0.113–5.374ms. Small numerical boundary misses remain classified as outside, without post-hoc tolerance expansion; they do not carry sub-ms perceptual significance. Large misses remain material. Every miss:

| Review | Channel | Boundary distance ms |
|---|---|---:|
| REVIEW_012 | FISHMAN | 0.136 |
| REVIEW_004 | FISHMAN | 0.113 |
| REVIEW_004 | DPA4099 | 1.088 |
| REVIEW_004 | NT5 | 2.109 |
| REVIEW_007 | DPA4099 | 0.113 |
| REVIEW_007 | NT5 | 0.113 |
| REVIEW_002 | DPA4099 | 0.726 |
| REVIEW_002 | NT5 | 1.723 |
| REVIEW_008 | DPA4099 | 19.433 |
| REVIEW_008 | NT5 | 21.429 |
| REVIEW_005 | FISHMAN | 1.383 |
| REVIEW_005 | DPA4099 | 15.374 |
| REVIEW_005 | NT5 | 20.363 |
| REVIEW_003 | FISHMAN | 0.181 |
| REVIEW_003 | DPA4099 | 1.179 |
| REVIEW_003 | NT5 | 6.168 |
| REVIEW_001 | DPA4099 | 12.744 |
| REVIEW_001 | NT5 | 17.755 |
| REVIEW_004 | MULTICHANNEL_ENVELOPE | 1.088 |
| REVIEW_007 | MULTICHANNEL_ENVELOPE | 0.113 |
| REVIEW_002 | MULTICHANNEL_ENVELOPE | 0.726 |
| REVIEW_005 | MULTICHANNEL_ENVELOPE | 5.374 |
| REVIEW_003 | MULTICHANNEL_ENVELOPE | 1.179 |
| REVIEW_001 | MULTICHANNEL_ENVELOPE | 3.741 |

## Raw channel-delay diagnostic
| Raw difference | Comparable events | Old midpoint median ms | New midpoint median ms |
|---|---:|---:|---:|
| DPA4099_MINUS_FISHMAN | 11 | +3.5 | +10.0 |
| NT5_MINUS_DPA4099 | 11 | +0.5 | -2.0 |
| NT5_MINUS_FISHMAN | 11 | +5.0 | +7.5 |

All old bounded pair-delay intervals include zero; almost all new intervals do too, except two DPA-versus-Fishman pairs strictly later under the new review. There is no reproducibly isolated fixed physical delay. The new DPA/NT5 midpoint ordering changes in aggregate, while Fishman intervals broaden. These are raw judgment intervals through different transfer paths, not measured propagation latency. No corrections were applied.

CHANNEL-DELAY STABILITY: NO — the current bounds do not justify treating the pattern as a stable delay for calibration transfer. READY FOR CHANNEL-TRANSFER / PROPAGATION CALIBRATION: NO under the requested reference-readiness criterion. A future separately instrumented timing experiment may still be useful, but is not executed or claimed validated here.

## Scientific decision
REFERENCE REPRODUCIBILITY: NOT ESTABLISHED (C). CONTROLLED-DOMAIN BASS ATTACK TIMING: NOT ESTABLISHED under this re-review robustness test. READY FOR REAL-MUSIC TRANSFER: NO. The parent remains a preserved promising development result; this additive result does not rewrite it or modify the estimator. Source-exposed material remains useful, but a stable attack-boundary definition is still missing.

Recommended next action: PI adjudication of the early-contact versus sustained-response distinction in the frozen disagreement examples before any further timing calibration. Do not execute it now.

Source/freeze integrity PASS. No canonical changes, no source changes, no commit, no push.
