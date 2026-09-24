# PROCESS-BLINDED RESTART AFTER INVESTIGATOR PLP EXPOSURE

Basic Pitch fundamental / harmonic-family tracking — saved Ray Brown Bass-stem transcription. Identity/activity experiment only.

**Result: PARTIAL visual/structural coherence; PARTIAL suitability as provisional local-search hypotheses.** The tracker retains a plausible lower-pitch sequence and lets older harmonic hypotheses persist across new roots. It does not independently validate the melody, note count or harmonic ownership. Thirty-five of63 episodes remain ambiguous.

Investigator previously saw temporal-reference results; the experiment is not investigator-blind. Both tracking and the later native-event crosscheck ran in filesystem sandboxes that denied reference/prior timing artifacts. Tracking also could not read native detector events. No reference grid was opened for evaluation in this study.

## Three interpretations

| Interpretation | Count | Overlaps and tails | Fragments and transitions |
|---|---:|---|---|
| Raw native hypotheses |98|47 overlapping hypothesis pairs; no ownership interpretation|Every native hypothesis retained independently|
| Lowest-active-note baseline |73|Chooses lowest active pitch regardless of family; may return to an older tail|9 segments begin at a note offset rather than any new native onset|
| Fundamental/harmonic tracker |63|19 hypotheses provisionally assigned to families; old tails do not block incompatible new roots|16 possible fragments merged into family episodes; all original pieces retained|

## Fixed exploratory rule

Observed Basic Pitch pitches alone propose fundamentals. Harmonic tests use actual equal-tempered frequencies and integer ratios2–8, within50cents to accommodate semitone quantization. No invented subharmonic pitch. A root proposal is ranked by native amplitude plus amplitude/k support from compatible notes in its near-onset group. Ranking is heuristic, not calibrated confidence and not “lowest wins”.

Same-pitch continuation of the most recent family within two output frames can be a fragment. Otherwise a note can join an active compatible family; incompatible new pitches open new root hypotheses even while previous members remain active. Ambiguous multiple-parent membership is retained rather than forced. Root fragments and octave/higher-note alternatives are flagged. No parameter sweep, note-count target or musical-grid input. See `PROTOCOL.md` and frozen code for exact ordering/parameters.

All98 onsets, offsets, pitches, amplitudes and pitch-bend fields are preserved. Family membership changes interpretation, not native measurements. The bold current-root line is visually truncated when another root opens, while native tails remain in faint/dashed layers; this is a display convention, not retiming.

## Outcome

| Metric | Value |
|---|---:|
| Raw hypotheses |98|
| Naive lowest-active episodes |73|
| Harmonic-family episodes |63|
| Harmonic hypotheses |19|
| Harmonic hypotheses starting after their root |13|
| Lingering harmonic hypotheses / transition pairs |2 /2|
| New roots opening below lingering harmonics |2|
| Possible fragmented hypotheses collapsed |16|
| Unresolved multiple-family memberships |0|
| Ambiguous episodes |35|

Zero unresolved multiple-parent memberships does not mean correct ownership: every assigned harmonic retains the alternative that it could be a separate higher note. Ambiguity also includes fragments versus rearticulation and overlapping roots. Flag counts overlap: {"OVERLAPPING_FUNDAMENTAL_HYPOTHESES": 23, "HARMONIC_VS_NEW_HIGHER_FUNDAMENTAL": 17, "FRAGMENT_OR_REARTICULATION": 16}.

## Explicit lingering cases

| Previous family → new family | Harmonic hypothesis | Transition s | Previous F0 MIDI | New F0 MIDI | Lingering MIDI |
|---|---|---:|---:|---:|---:|
| HF034 → HF035 | BP_0052 | 59.416969161 | 34 | 39 | 46 |
| HF052 → HF053 | BP_0077 | 66.968590023 | 38 | 43 | 50 |

Both cases preserve the old harmonic while opening the lower new-root hypothesis. This demonstrates the tracker behavior, not independent acoustic confirmation that these are genuinely lingering harmonics.

## Musical coherence and limits

Root range: MIDI28–57 (E1–A3). Median absolute successive pitch change: 4.0semitones; 4 changes exceed an octave. Median native root-support duration: 0.290s. These descriptors are not success criteria and were not used to tune the tracker.

Visual assessment: stretches of the lower line are coherent, and family ownership avoids some spurious lowest-note switches. However, large leaps, overlapping roots and35 flagged episodes prevent declaring a verified monophonic Bass melody. An early high hypothesis can become its own root before a later lower fundamental appears; this chronological tracker does not retroactively correct that possible octave error. A new octave note can also be mistaken for a harmonic, and repeated same-pitch attacks can be merged as fragments. These are material limitations, not adjudicated by the algorithm.

Suitability for local attack searches is PARTIAL: the families offer explicit activity hypotheses and uncertainty flags, but bounds may contain a tail, fragment or wrongly assigned component. No final attack regions or attack timestamps were generated. Basic Pitch activity beginnings are not accurate timing authority.

## Post-freeze Bass-stem diagnostic

Existing native Bass events fall inside 34/63 activity intervals; 29/63 contain none. The complete per-episode nearest-event offset and interval-membership table is saved in `crosscheck/output/NATIVE_ACTIVITY_CROSSCHECK.json`. No acceptance window, matching score optimization, relabeling or boundary update was applied. An event before an episode start can reflect Basic Pitch timing error or detector behavior; absence inside the interval is not proof of no Bass note. Both derive from the same separated representation and are not independent Ground Truth.

## Freeze and technical checks

Episode table SHA-256: `52aff9d008fe108d747a529e925ba7e12af940088e75439e8e040ed786e6b5ef`.

Membership/alternatives SHA-256: `3f85ea1ac413be102b5d073a9a71a82381cc6c5fadffa59e8d3ff93c15fc87f2`.

Tracking freeze: 2026-09-24T13:03:26.610050+00:00. Crosscheck completed: 2026-09-24T13:05:53.924034+00:00. Input/export hashes, unchanged98 native records, unique hypothesis coverage, compatible integer-frequency relationships and phase order validate. Bass source hash unchanged. No model run or reference-grid evaluation.

## Review outputs

- `figures/EXACTLY_LIKE_YOU_FUNDAMENTAL_TRACKING.pdf`: complete four-page sequence, raw notes, lowest baseline, reconstructed roots, family membership and lingering tails; no beat/measure/reference grid.
- `figures/FUNDAMENTAL_TRACKING_ENLARGED_EXAMPLES.pdf`: five enlarged examples: delayed overtone, both lingering transitions and two possible fragmentation cases.
- `FUNDAMENTAL_EPISODES.csv`: chronological episode bounds, plausible root, member IDs, inherited hypotheses, opening reason and flags.
- `HYPOTHESIS_MEMBERSHIP.csv`: all98 hypotheses, family assignments, alternatives, integer harmonic and cents error.
- `NAIVE_LOWEST_EPISODES.csv`, `LINGERING_CASES.csv`, `RESULTS.json`: baseline and diagnostic data.

Freeze: experimental fundamental/episode representation only. Canonical JGA, Report001 and prior studies unchanged. No attack-timing claims or corrections. COMMIT: NONE. PUSH: NONE. STOP for PI review.
