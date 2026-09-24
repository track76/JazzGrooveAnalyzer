# JGA Bass-v1 historical report — Exactly Like You

**Completed unchanged transfer; partial diagnostic usability; not ready for Bass-v1 milestone freeze.**

## Research question

Can a frozen, controlled-corpus local attack selector recover useful historical Bass timing without Ray Brown retuning? This completed transfer tests the approved Bass-v1 architecture on M33–M48. The outcome is a sparse diagnostic result, not a complete walking-Bass timing account.

## Historical material

Ray Brown Trio, “Exactly Like You.” The same63 frozen fundamental episodes and98 native Basic Pitch hypotheses were preserved. Original full-mix PCM and Demucs Bass source hashes verify. RAW PLP derives from the original full mix; selected attack timestamps in this run derive from the unchanged separated Bass PCM. No full-mix attack correspondence or Demucs latency correction is claimed.

## Frozen architecture

PI-approved routing was frozen before inference:28 UNFLAGGED / SECURE_ROUTE episodes use their native root;35 FLAGGED / AMBIGUOUS_ROUTE episodes use exact frozen family members. SECURE_ROUTE is an operational label, not Ground-Truth-correct identity. The unchanged logistic selector operates within each BP onset±150 ms window. Ambiguous hypotheses remain contained; exact shared candidate coordinates may agree, distinct selected fronts cause abstention. No windows are bridged.

## Controlled Gallegati validation

The frozen selector selected35/40 controlled holdout events, with5.213 ms median absolute error and5.621 ms P95;100% of selected events were within10 ms. Validation is conditional on recognized-note correspondence. Contained fallback selected8/13 natural ambiguous cases and18/35 masked holdout cases, with roughly5 ms selected-event error and zero observed catastrophic outputs. Three earlier catastrophic cases became abstentions. These results do not provide independent GT for historical audio.

## Historical transfer protocol

PROCESS-BLINDED RESTART AFTER INVESTIGATOR PLP EXPOSURE. The investigator was previously exposed to PLP; no investigator-blind claim is made. Routing used frozen flags/member IDs only. Filesystem isolation denied PLP, metric mapping, Report001 timing and previous Bass timing tables. Exact candidate generation, feature definitions, normalization, model, thresholds and abstention rules were reused. All98 queries,63 episode decisions and unique attacks were hashed before RAW PLP reveal. Candidate timestamps retain original Bass-stem frame-center/sample coordinates.

## Bass attack recovery coverage

17 unique acoustic attacks were selected;46/63 episodes abstained. UNFLAGGED / SECURE_ROUTE selected3/28 and abstained25/28(89.29%). FLAGGED / AMBIGUOUS_ROUTE selected14/35 and abstained21/35(60.00%). No shared selected coordinate occurred. Four ambiguous episodes produced distinct per-hypothesis attacks and abstained. Coverage is17/64 quarters(26.56%):47 ZERO,17 ONE,0 MULTIPLE. No missing quarter was filled. All17 attacks remain in the result; no ±100 ms filter was applied.

## Bass-vs-PLP results

JGA-estimated historical Bass attack timing using a controlled-corpus-validated selector: N=17; median−1.723 ms; mean+4.690 ms; IQR145.760 ms; P95 absolute distance to PLP158.984 ms. Nine onsets precede their nearest quarter, eight follow, none is exact. Before/after/exact:52.94%/47.06%/0%. Counts within±10/20/30/50/100 ms:3/4/6/6/9. The near-zero median does not establish “on the beat”: the sparse selected population spans a wide range of positions relative to the quarter.

## Measure/beat observations

The selected population does not display a complete four-quarter walking pattern. Beat medians, conditional on the sparse observations, are Beat1:+54.875 ms; Beat2:+83.673 ms; Beat3:−2.268 ms; Beat4:−95.147 ms. These describe nearest-reference geometry, not independently established metrical roles. Extra/intermediate events were retained. Abstentions appear in a separate context lane located using native BP roots; no timing measurement is invented for them.

## Route-specific timing

SECURE_ROUTE:3 unique attacks, median+130.249 ms, mean+89.766 ms, IQR71.791 ms, P95 absolute140.209 ms;1 before/2 after/0 exact. All3 map to Beat3. AMBIGUOUS_ROUTE:14 unique attacks, median−13.696 ms, mean−13.541 ms, IQR189.569 ms, P95 absolute160.195 ms;8 before/6 after/0 exact. The flagged route’s higher output rate does not prove better identity. Complete route/beat metrics are retained in RESULTS.json. Pitch labels denote frozen fundamental hypotheses; all native member pitches and timings are preserved in NATIVE_HYPOTHESIS_PROVENANCE.csv.

## Comparison with Report001

CANNOT DIRECTLY COMPARE. Report001’s BASS PRIMARY_NONSHARED cohort had N=23, median−34.83 ms, mean−22.72 ms. The new result covers onlyM33–M48 and uses a different population and Bass-stem spectral landmark. The old whole-performance cohort remains unchanged. These pooled values neither confirm nor refute its timing description.

## Limitations

Fishman pickup validation does not establish Demucs-stem or historical full-mix timing accuracy. Separation can alter attack morphology and amplitude; no historical GT verifies these selected fronts. A large ΔB is not automatically an error and a small ΔB is not proof of correct identity. Catastrophic cross-event errors CANNOT BE VERIFIED WITHOUT HISTORICAL GT. Containment restricts window selection and causes abstention on distinct fronts, but does not prove the historical BP query itself is correct. Sparse coverage, uncertain identity, prior investigator exposure and the absence of full-mix attack validation limit interpretation. No correction was applied.

## Architectural conclusion

HISTORICAL TRANSFER COMPLETED:YES. FROZEN SELECTOR MODIFIED:NO. FOUR-QUARTER WALKING STRUCTURE MUSICALLY INTERPRETABLE:NO from this recovered population. JGA BASS-v1 HISTORICAL RESULT USABLE:PARTIAL, as a reproducible diagnostic map rather than a final complete Bass account. READY FOR BASS-v1 MILESTONE FREEZE:NO. The controlled local-selector result remains preserved, but this transfer does not establish useful broad historical recovery. No further detector, routing change, retuning or transfer was attempted.

## Review artifacts

- JGA_BASS_V1_EXACTLY_LIKE_YOU_ATTACKS.csv —17unique attacks plus46explicit unresolved records.
- JGA_BASS_V1_EXACTLY_LIKE_YOU_GROOVE.pdf
- JGA_BASS_V1_MEASURE_BY_MEASURE.pdf
- JGA_BASS_V1_HISTORICAL_ATTACK_AUDIT.pdf —63episode pages; no PLP.
- Routing, input, historical-acoustic and post-PLP evaluation freezes preserve exact provenance.

COMMIT:NONE · PUSH:NONE · BOOTSTRAP UPDATE:NONE · EXTERNAL BACKUP:NONE. No closure package proposed because milestone readiness is NO. Stop for PI review.
