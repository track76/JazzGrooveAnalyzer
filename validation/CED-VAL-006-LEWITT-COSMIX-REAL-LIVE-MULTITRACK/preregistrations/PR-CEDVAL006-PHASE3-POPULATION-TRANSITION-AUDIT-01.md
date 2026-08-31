# PR-CEDVAL006-PHASE3-POPULATION-TRANSITION-AUDIT-01

Status: **PREREGISTERED — NOT EXECUTED**

This read-only audit explains the frozen Phase-3 population transition without
rerunning JGA, changing matching, or modifying audio. Populations A–E are
defined by set operations on the frozen original-EME assignments. Matching
identity means selected separated-event producer timestamp, not asset-derived
UUID.

Amplitude and spectrum use fixed 50 ms event-centered windows. A/B/C/E are
anchored on original EME time; D is anchored on processed-event time.
Amplitude uses all channel samples. Spectrum uses arithmetic-mean mono, a Hann
window, float64 real FFT, and fixed 20–80, 80–250, 250–1000, 1000–4000, and
4000–Nyquist Hz bands. No band may be added or changed after execution.

An EQ hypothesis is supported only if a fixed band separates recovered B from
processed-only D in the unprocessed audio with at least 0.10 median energy-
fraction difference and absolute Cliff's delta at least 0.474, with the same
median-difference direction after processing. Adequate populations with no
qualifying band produce `NO`; missing/invalid authority produces
`INDETERMINATE`. This gate authorizes no EQ design or execution.

The adjacent JSON freezes full authority, method, replay and firewalls.
