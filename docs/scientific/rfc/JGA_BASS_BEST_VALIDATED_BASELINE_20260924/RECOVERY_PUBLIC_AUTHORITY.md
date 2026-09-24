# PI authority: best validated JGA Bass attack baseline

PI milestone decision recorded 2026-09-25; experiment authority JGA_LEARNED_LOCAL_ATTACK_SELECTOR_20260924. CURRENT BEST VALIDATED BASS ATTACK BASELINE. This is a controlled-domain comparison authority, not completion of historical Bass-v1.

## Architecture and scope

Audio → official Spotify Basic Pitch 0.4.0 (bundled ICASSP 2022 model) → native BP note identity + approximate onset → fixed local ±150 ms window → local acoustic candidates → frozen JGA Learned Local Attack Selector → selected existing acoustic attack coordinate / abstention.

The controlled September-14 Gallegati Fishman corpus has120 human-reference events in12 continuous takes. Target reference is channel-specific observable onset in Fishman Full Circle, NOT physical string release. The validated question is recognized note + approximate neighborhood → local attack selection. It does not validate autonomous note identity, raw-query event completeness, arbitrary audio domains or historical Ray Brown timing. Same-rater GT and1ms annotation steps do not establish sub-millisecond human accuracy.

## Exact implementation authority

All paths below are relative to docs/scientific/rfc. JGA_LEARNED_LOCAL_ATTACK_SELECTOR_20260924/development/selector.py defines candidate windows, features and decisions; development/morphology.py defines acoustic features. development/output/SELECTOR_RULE.json is the exact parameter authority; MODEL.joblib is the serialized scaler/model. SHA-256s:

- selector.py: c20687006752d2ec07c0de6be12d1f7055669e387d6f8c746c76c245686c3433
- morphology.py: ac003cdaf4799e696204d95c527ee8cb747d262d4a9e17ca80aa3669b1570b70
- SELECTOR_RULE.json: db998eaed9485edf913fd78d0698ad2fc9896a13d896dbffd5504e922dbc0a42
- MODEL.joblib: 6523e71a1788b05b8c112570b1dc5a20736bea33942f68ad00ffd70359fb2474

Local window is BP onset±0.15s, clipped only to source limits. Feature context extends0.15s on either side; candidate eligibility remains within the local window. Original44sample frame grid is preserved. Positive magnitude spectral flux30≤f<250Hz, Hann1024, hop44,44100Hz; all eligible local maxima from the exact frozen generator remain candidates. No refractory suppression or timing correction.

The frozen22feature order is listed in SELECTOR_RULE.json, alongside exact scaler means/scales, coefficients and intercept. It includes flux magnitude/prominence/width/rise/decay/integral, local flux ratios, RMS and low/broadband energy changes, centroid/slope, persistence/concentration and three BP-relative location features. Source code specifies exact transforms and frame ranges; it takes precedence over prose. In particular BP_relative_activity_position=(candidate−BP_onset)/max(BP_duration,1e-9), unchanged even where domain shift makes its distribution problematic.

Normalization is the fitted StandardScaler; logistic regression C=0.1, not the older C=1/threshold0.99 morphology classifier. Frozen decision threshold0.5: choose the highest predicted probability only if ≥0.5 and no top-score tie within1e-12. Otherwise ABSTAIN_AMBIGUOUS; empty candidates NO_CANDIDATE. Stable score ordering is implementation-defined in the frozen file. Exactly one existing coordinate is emitted for a selected query. No averaging, snapping or bias correction.

## Development/holdout and provenance

TAKE_SPLIT.json and SPLIT_FREEZE.json define8 complete development takes /4holdout takes, with no take overlap. Split SHA-256:151f1433d48ff99b1eafc48023ffd5424ba1bfd4349b2da9177dd3cf6fb84047. Development:0028,0029,0030,0033,0034,0036,0039,0040. Holdout:0031,0035,0037,0038 (all20260914).

PROSPECTIVE_PROTOCOL.json, development/train.py, CV_RESULTS.json and DEVELOPMENT_CANDIDATES.csv preserve candidate labels, take-level cross-validation and model selection. Development had72 uniquely recognized GT correspondences; positive training evidence included90 near-interval proxies, not90 independent notes. The exact original label distinctions and weights remain authoritative. Holdout predictions were saved before evaluation-GT reveal; prediction/selector/evaluation freezes and isolation checks remain unchanged. Investigator exposure predates this study; process isolation is not a pristine investigator-blind claim.

GT authority JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_120_20260924/GROUND_TRUTH/GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json SHA-256 a4047bf252f28fa3289279bdcaa5e90226dcf0af994a51e0dd5df05174484631; GT_FREEZE.json SHA-256535e3d3d930db323320a5959da3999bc605ba278234671d0540d04b281b3ebd7. Native BP provenance, settings, source hashes and all hypotheses are in JGA_NATIVE_BP_GT_120_20260924. TAKE_SPLIT.json records all12original WAV hashes and paths; MANIFEST references these without duplicating audio.

## Exact controlled holdout result

35/40 selected =87.5%; median absolute error5.213ms; P95 absolute error5.621ms;100% of selected within±10ms. Five GT events had unresolved BP correspondence: this is recognized-note-conditional performance, not guaranteed autonomous recognition. All35selected precede their plausible GT intervals; no offset correction was applied. Additional raw BP-query selections outside the matched cohort are not automatically verified attacks.

On the same35matched events the learned selector improves over native BP (MAE14.629/P9551.478ms), nearest-to-BP candidate (19.217/53.096ms), earliest candidate (148.039/179.044ms), and largest-flux candidate (5.227/36.775ms). EVALUATION.json retains unrounded values and all stratification; HOLDOUT_ATTACK_SELECTIONS.csv/HOLDOUT_RESULTS.json retain event-level evidence. The advantage over the largest-flux baseline is principally outlier control, not a large median change.

## Secondary contained fallback

JGA_CONTAINED_BP_FALLBACK_20260924 remains a separate secondary validated component using the unchanged selector. Each ambiguous BP hypothesis keeps its own ordinary window; never bridge them. One selected hypothesis yields its coordinate; multiple hypotheses at one exact acoustic sample yield shared identity-unresolved attack; distinct selected coordinates cause abstention; none selected causes abstention. Natural ambiguous cohort8/13, MAE4.822/P955.480ms; maskedholdout18/35, MAE5.240/P955.598ms; allselectedwithin10ms. Three prior catastrophic union-window cases became abstentions. These statistics MUST NOT be pooled with primary35/40validation. BP-blind/autonomous recovery is not established.

## Historical and diagnostic evidence — not replacement authorities

JGA_BASS_V1_HISTORICAL_TRANSFER_20260924 used fixed28UNFLAGGED/SECURE_ROUTE and35FLAGGED/AMBIGUOUS_ROUTE. These are operational identity routes, not independent identityGT. It selected17uniqueattacks/63episodes and abstained46 (secure3/28, ambiguous14/35). The walking structure was insufficiently recovered. The result remains a partial diagnostic map; historical Bass-v1 milestone NOT complete.

JGA_STEM_FULLMIX_DOMAIN_SHIFT_20260924 documents important Fishman→historical/Demucs feature-distribution shift; this is not a causal Demucs latency measurement. Generic full-mix cues remain ambiguous. JGA_NOTE_CONDITIONED_FULLMIX_20260924 resolved0/63 under its overly restrictive ≥3observable-harmonic/nonoverlap sufficiency convention; this does not disprove note-conditioned observation. JGA_TARGETED_PITCH_ONSET_20260924 yielded37/63CLEAR (58.73%) conditional full-mix target-energy observations. Its centered filtering/bandwidth and timing accuracy remain unvalidated against historicalGT. None supersedes the controlled baseline. No Ray Brown physical timing authority is finalized.

## Mandatory future comparison directive

Do not restart Bass development from scratch. Preserve this Learned Local Attack Selector as the comparison baseline. Every proposed improvement/extension must report: whether the baseline changed; controlled-domain coverage; median absolute error; P95 absolute error;±10ms performance; abstention behavior; historical/cross-domain coverage; and whether coverage gains sacrifice validated timing precision. A visually plausible historical result cannot supersede this baseline without independent validation.

RAW PLP remains the quarter-reference authority, never an acoustic-selection guide. Freeze historical attack timestamps before PLP evaluation. Original full mix remains original audio authority; stems provide complementary source/identity evidence. Next scientific goal: improve cross-domain/historical coverage while preserving this controlled baseline. No new science is executed by this milestone.

## Package and hash convention

This immutable core contains the PI authority without a self-referential digest. BASELINE_FREEZE.json binds this core and every referenced scientific payload by SHA-256, role and size; its byte SHA-256 is the baseline freeze hash. The public authority document quotes that hash. MANIFEST.json additionally hashes the public authority, freeze and operational package files; SHA256SUMS.txt verifies all manifest entries. Manifest/sums and outer citation-bearing documents are not recursively hashed into their own digest. Root bootstrap and commit/backup receipts are operational references, not mutable scientific payload. Audio is referenced with full hashes/paths and preserved in the external complete project backup. Git excludes large audio/raw arrays, but the complete backup preserves them.

Baseline freeze SHA-256: `fd768ec83bc77a5e32938bed743edef10d1355d0c1a961c623be5ea4728b850d`

[Manifest](JGA_BASS_BEST_VALIDATED_BASELINE_20260924/MANIFEST.json) · [Freeze](JGA_BASS_BEST_VALIDATED_BASELINE_20260924/BASELINE_FREEZE.json)
