# Pilot 002 — preregistration before execution

EXPERIMENTAL / DIAGNOSTIC / NOT PROMOTED. PI takeover and preflight disposition authorize this corrected rerun only. No commit, push, candidate freeze or scientific promotion.

The machine configuration is consumed directly. Its constants are heuristic, inherited where specified by the partial OpenCode configuration and made explicit before any new extraction. No parameter search, expert reference, stem source, existing event table or PLP is used by extraction. The original two JSON files and their hashes are preserved in PREEXISTING_INPUTS.json.

Corrections to the partial plan: real environment is measured; ambiguous pYIN threshold is replaced with explicit resolution/default parameters; contrast is named six-subband energy coefficient of variation; post-event energy is not an exponential decay estimate; full-mix harmonic-bin magnitudes distinguish fundamental from overtones and do not claim source identity. The original Bass harmonic/flux factor and Cymbal conjunctive rules remain heuristics. Continuity is explicitly only prior voiced-frame frequency difference. All low-band pitch and high-band descriptors remain preprocessing-dependent.

Processing has 0.5 s post-event support plus half-window plus 0.5 s guard on each side. Offline zero-phase IIR filtering can deform transients; it removes nominal phase delay, not physical landmark bias. Whole-context filtering, pYIN Viterbi and adaptive thresholds mean evidence availability/decision sample is context end, not the event time. Local frame and post-event support are stored separately; crossing evaluation boundaries is not missing source evidence.

Frame center = processing-start native sample + frame*hop. No half-window subtraction. Synthetic impulses verify conversion and filter symmetry only, without scientific tuning. Samples are frame-derived coordinates, not sample-accurate physical attacks.

ALL_LOCAL_MAXIMA retains every scipy computational local maximum admitted to the evaluation interval, including rejected ones. Full context maxima/flux are retained in external arrays. Distance filtering precedes prominence as in scipy; each failed condition is recorded. Dedup uses adjacent-gap chains and earliest representative independent of class. Member features and classifications remain intact. Span greater than pairwise tolerance is flagged; no same-attack claim.

Figures use saved arrays/tables only, with first/middle/last chronological examples by available class/boundary. Confuser labels are hypotheses, not confirmed identities. No successful/ground-truth labels. All counts and summaries are recomputed by a separate read-only validator; manifests cover completed package bytes with an explicit self-hash exception. No grid, quarter relevance, precision, recall, note/hit count, microtiming or groove conclusion.
