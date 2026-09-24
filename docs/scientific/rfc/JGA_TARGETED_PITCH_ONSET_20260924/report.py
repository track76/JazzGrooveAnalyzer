from pathlib import Path
import json
P=Path(__file__).resolve().parent;S=json.load(open(P/'SUMMARY.json'));R=json.load(open(P/'inference/output/TARGET_OBSERVATIONS.json'))
text='''# Targeted pitch-onset localization in original full mix

PROCESS-BLINDED DIAGNOSTIC AFTER INVESTIGATOR PLP EXPOSURE

## Research question and scope

Given the frozen Bass/BP pitch hypothesis and native approximate time, can a beginning/rise of that pitched component be observed locally in the original mixture? This is conditional targeted-frequency observation, not independent Bass source recognition or validated physical attack localization. Prior investigator PLP exposure remains disclosed. No PLP or quarter mapping was loaded for this study.

The sole timing input was unchanged original full-mix PCM. Inference received only this audio, frozen episode/member identity and the predeclared method. It could not read Bass PCM, learned selector, prior stem-selected timestamps or PLP authorities. Historical acoustic outcomes were read only after OBSERVATION_FREEZE.json verified, for requested comparisons. Source hashes, frozen membership and full-mix coordinates remain unchanged.

## Prospective method

METHOD_INPUT_FREEZE.json precedes observation. All 63 frozen episodes and 98 exact native BP members are retained. Each member pitch is observed independently at its native BP onset; the frozen root pitch is also observed there when different. This yields 117 target queries. Their ±150 ms windows are independent and never bridged or resized. The original ambiguity flags remain intact.

A four-cycle symmetric Hann complex-demodulation kernel measures energy at f0 and ±35 cents; the maximum of these three channel powers is the target trace. Kernel length is 2·round(2·44100/f0)+1 samples. The kernel is normalized by its sum; amplitude is twice the complex coefficient magnitude, and power is its square. Traces are evaluated at original recording sample multiples of 44 (0.9977 ms). The original recording coordinates are retained; no timestamp interpolation, shift or correction occurs.

This uses a target-frequency trace rather than broadband flux peaks. It does not use a three-harmonic sufficiency gate or the Fishman-trained classifier. Harmonics 2f0 and 3f0 are tracked independently as optional supporting observations; no harmonic is mandatory.

## Frequency and temporal limitations

±35 cents is the tuning-channel range, NOT the effective filter bandwidth. Exact equivalent-noise bandwidth is 44100·sum(w²)/sum(w)². The Hann first-null half-width is approximately 2/T; adjacent pitches can therefore contribute substantial energy. At G2 (98 Hz), four-cycle support is approximately 40.8 ms, ENBW approximately 36.8 Hz, with first nulls roughly ±49 Hz around a tuning channel. This does not isolate G2 from every neighboring note or other instrument.

Across the actual hypotheses, kernel support ranges from 12.18 to 97.12 ms. Centered filtering uses audio outside the observation window only for filter support; it can smear an abrupt physical onset backward by up to half the kernel support. Observation remains restricted to the frozen ±150 ms window. Frame spacing must not be described as physical timing precision. The method trades pitch selectivity for temporal localization; its observed coverage is not evidence of 10–30 ms timing accuracy.

## Fixed target-rise rule

A local trace is NOT_OBSERVABLE if peak power is below 1e-8 or median target power divided by four times median Hann full-mix power is below 0.01. These are engineering proxy thresholds, not measured source/noise separation. Observable activity with peak/10th-percentile-baseline ratio below four is CONTINUOUS.

For traces with sufficient dynamic range, low and high levels are baseline +20% and +60% of the local peak-minus-baseline range. After observing power at/below the low level, the first existing frame above it is a prospective crossing. It is confirmed only if activity reaches the high level and stays there for at least one target period. Confirmation preserves the earlier native crossing coordinate; it does not create or average a timestamp. A new rise is possible only after return below the low level. Incomplete edge rises remain unresolved. Initial already-active energy does not manufacture a beginning before the window.

Exactly one confirmed rise without an incomplete alternative is CLEAR; multiple confirmed rises are MULTIPLE. Episode aggregation preserves every independent query: different clear pitch structures remain identity-unresolved; same-pitch distinct beginnings remain multiple. Clear structures spanning at most one hop receive SHARED_TARGET_ONSET, retaining every coordinate and pitch without averaging. A clear episode can coexist with non-observable/continuous hypotheses, but not an incomplete unresolved alternative. Full definitions are frozen in inference/input/METHOD.json. These rules were not retuned after outcomes.

## Results

| Episode outcome | Count |
|---|---:|
| TARGET_ONSET_CLEAR | 37 |
| TARGET_ONSET_MULTIPLE | 3 |
| TARGET_ACTIVITY_CONTINUOUS | 5 |
| TARGET_NOT_OBSERVABLE | 1 |
| TARGET_ONSET_UNRESOLVED | 17 |

CLEAR coverage is 37/63 = 58.73%. Median absolute full-mix target crossing minus its own BP origin is 42.882 ms over 41 clear query records belonging to the 37 CLEAR episodes. This is distance from BP, not timing error against Ground Truth. No global Bass-versus-quarter statistic is computed.

Four episodes have SHARED_TARGET_ONSET under the one-hop structural convention: HF016, HF039, HF060 and HF062. This does not independently resolve pitch identity or prove a shared physical attack.

Of the previous 25 SECURE_ROUTE abstentions, 21 show a clear target rise. Of the previous 34 generic multiple-cue abstentions, 22 now have CLEAR observations, 9 remain unresolved, 1 multiple, 1 continuous and 1 not observable. These are changes in diagnostic status under a different question/representation, not recovery-accuracy measurements or proof that all broadband alternatives have been correctly excluded.

## Requested special cases

All four named episodes show a single target-frequency rise. Prior stem coordinates below were introduced only after the observation freeze.

| Episode | Target | Full-mix target crossing (s) | Target−BP (ms) | Target−old stem (ms) |
|---|---|---:|---:|---:|
'''
for e in S['special']:
 for r in e['targets']:text+=f'| {e["episode_id"]} | {r["pitch"]} | {r["clear_target_s"]:.6f} | {r["target_minus_BP_ms"]:+.3f} | '+('N/A (prior abstention)' if r['target_minus_old_stem_ms'] is None else f'{r["target_minus_old_stem_ms"]:+.3f}')+' |\n'
text+='''
HF044 and HF047 therefore show earlier target-band rises than the frozen late stem selections. Their earlier coordinates are observations, not corrections or proof of the Bass attack. Centered smoothing, another pitched source and neighboring-frequency energy remain possible explanations. HF050 is close to the old coordinate, which likewise does not validate either one.

## Decisions

- TARGETED PITCH LOCALIZATION OBSERVABLE IN HISTORICAL FULL MIX: PARTIAL — single local target-band rises are measurable in 37 episodes.
- TARGETED APPROACH REDUCES GENERIC FULL-MIX AMBIGUITY: PARTIAL — 22/34 previously generic multiple-cue abstentions have one conditional target rise; correctness is untested.
- COVERAGE SUFFICIENT TO JUSTIFY CONTROLLED GT VALIDATION: YES.

This is sufficient to justify testing the exact frozen method against controlled Gallegati GT, not to adopt it as Bass-v1 timing authority. The next study should execute the identical method without GT access, freeze traces/coordinates, then evaluate recognition-conditioned coverage, signed/absolute errors, smoothing bias, outliers, ambiguity and register dependence against independent human references. Do not correct any offset before reporting raw performance. No controlled execution or historical microtiming calculation is performed here.

## Artifacts, verification and preservation

TARGETED_PITCH_ONSET_FULLMIX.csv has one row per target/member query, including exact BP origins, band widths, optional harmonic observations, all candidate crossings, clear coordinate where applicable, and episode status. TARGET_DEFINITIONS.json retains all63 frozen identities; TARGET_TRACES.npz retains every trace; TARGET_OBSERVATIONS.json and EPISODE_OBSERVATIONS.json retain all outcomes. OBSERVATION_FREEZE.json was saved before aggregation, comparison or figure rendering.

The three PDFs provide all63 episode pages, a chronological summary and enlarged special cases including representative successful/unsuccessful prior secure-route abstentions. No PLP appears. Silence, constant-energy and known-step controls check implementation state logic only; they do not validate physical onset accuracy. Source equality, window containment, native sample coordinates, episode counts, frozen observations and filesystem denial checks are verified separately.

No Basic Pitch/Demucs rerun; no existing model or upstream modification; no historical timestamp replacement; no canonical, Report001, bootstrap or prior-freeze change. No commit, push or external backup. STOP for PI review.
'''
(P/'RESULT.md').write_text(text)
