# Stem-guided full-mix interrogation: domain-shift diagnostic

PROCESS-BLINDED RESTART AFTER INVESTIGATOR PLP EXPOSURE

## Scope and authorities

Exactly Like You, the previously frozen target region. All 63 episodes, 28 SECURE_ROUTE / 35 AMBIGUOUS_ROUTE, exact independent BP ±150 ms query windows, 4030 prior candidate records and frozen scores were reused. No prior stem candidate was regenerated, moved or replaced. No selector was applied to full-mix features. No PLP was loaded at any stage. Original source hashes, input copies and implementation are recorded in INPUT_AUDIT.json and INPUT_FREEZE.json; inference read-denial checks are in inference/output/ISOLATION_CHECKS.json. Previous predictions, routing and scientific authorities remain unchanged.

The two earlier legacy TARGET_NOTES.csv rows with PLP fields had been exposed to the investigator before the original identity-region freeze. This is process isolation, not investigator blindness.

## Coordinates and descriptive method

Both sources are stereo FLOAT PCM at 44100 Hz with 15338496 frames. Mono channel means are analyzed on the same original sample/frame grid; declared coordinate offset is zero. Equal coordinates establish compatibility, not sample-perfect reconstruction or validated Demucs latency.

The unchanged representation uses a 1024-sample Hann (23.22 ms support), 44-sample hop (0.998 ms), positive magnitude spectral flux, 30 ≤ f < 250 Hz. Fine frame spacing is not sub-millisecond acoustic accuracy. The full-mix peaks are retained only inside each pre-existing independent window; windows are never bridged. Feature context follows the existing implementation and may extend beyond the window, but cannot emit an outside-window peak.

PROTOCOL.json prospectively specifies a descriptive cue: prominence greater than the window median plus three unscaled MADs, with positive pre/post low-band energy and RMS changes. All other peaks remain in the evidence. This new diagnostic salience flag is unvalidated, not a model threshold change, a Bass attribution rule or an attack selection. Counts are criterion-dependent. Absence of a flagged cue is not absence of a physical attack.

A flagged full-mix cue within one hop of a preserved stem candidate is corresponding; a single cue within half the Hann support is nearby distinct; multiple such cues remain multiple. All exact-coordinate evidence, nearest raw peaks and displacement values are saved. Episode summaries deduplicate identical cue coordinates across independent windows only. A single episode cue is called clear descriptively; multiple cues remain ambiguous. No cue is promoted to a final Bass timestamp.

## Observed populations

- Historical episodes: 63; previous selected physical attacks: 17; abstained episodes: 46.
- Abstentions: 6 single salient full-mix cues, 34 multiple cues, 6 no clear cue.
- SECURE_ROUTE abstentions (25): 2 single cues, 20 multiple, 3 no clear cue.
- Selected cross-check (17): 0 uniquely corresponding, 3 single earlier cues, 1 single later cue, 11 ambiguous, 2 unsupported by the cue criterion.
- Complete bounded full-mix peak population: 3842 query records, including 219 salience-flagged records. Overlapping independent queries can contain the same physical coordinate; these are not counts of physical attacks.

A zero uniquely corresponding count does not mean all 17 stem selections lack any nearby full-mix activity. The strict episode-level cross-check calls any episode with multiple salient cues ambiguous, even if one is near the stem selection. The candidate-level CSV preserves that distinction.

## Late selections

Fifteen selected episodes have a successful native-BP query more than one Hann support earlier than the selected stem coordinate. This is a descriptive late-to-BP comparison; BP is not Ground Truth. HF044 is +130.576 ms and HF047 +118.422 ms relative to their successful BP origins. Both contain earlier full-mix salient cues but multiple alternatives; neither identifies a correct earlier Bass attack. The complete late-event inventory follows.

- HF002: stem−BP {"BP_0004": 148.28526077097592} ms; 5 earlier cue(s); FULLMIX_AMBIGUOUS.
- HF005: stem−BP {"BP_0008": 149.8272108843537} ms; 0 earlier cue(s); FULLMIX_NO_SUPPORT.
- HF012: stem−BP {"BP_0018": 147.62222222221766} ms; 5 earlier cue(s); FULLMIX_AMBIGUOUS.
- HF014: stem−BP {"BP_0023": 144.53832199546213} ms; 0 earlier cue(s); FULLMIX_NO_SUPPORT.
- HF027: stem−BP {"BP_0040": 146.0380952380902} ms; 2 earlier cue(s); FULLMIX_AMBIGUOUS.
- HF029: stem−BP {"BP_0043": 140.59591836735308} ms; 1 earlier cue(s); FULLMIX_SUPPORTS_DIFFERENT_EARLIER_FRONT.
- HF039: stem−BP {"BP_0058": 149.91020408164246} ms; 3 earlier cue(s); FULLMIX_AMBIGUOUS.
- HF040: stem−BP {"BP_0061": 137.2117913832227} ms; 1 earlier cue(s); FULLMIX_SUPPORTS_DIFFERENT_EARLIER_FRONT.
- HF041: stem−BP {"BP_0063": 147.73333333333483} ms; 7 earlier cue(s); FULLMIX_AMBIGUOUS.
- HF044: stem−BP {"BP_0066": 130.57641723356284} ms; 2 earlier cue(s); FULLMIX_AMBIGUOUS.
- HF046: stem−BP {"BP_0069": 134.4766439909364} ms; 4 earlier cue(s); FULLMIX_AMBIGUOUS.
- HF047: stem−BP {"BP_0070": 118.42222222222176} ms; 3 earlier cue(s); FULLMIX_AMBIGUOUS.
- HF052: stem−BP {"BP_0076": 113.41950113379085} ms; 0 earlier cue(s); FULLMIX_AMBIGUOUS.
- HF055: stem−BP {"BP_0082": 138.71156462585077} ms; 1 earlier cue(s); FULLMIX_SUPPORTS_DIFFERENT_EARLIER_FRONT.
- HF060: stem−BP {"BP_0094": 109.03764172336139} ms; 0 earlier cue(s); FULLMIX_SUPPORTS_DIFFERENT_LATER_FRONT.

## Domain evidence and selector behavior

The following medians compare controlled development near-interval proxy candidates (N=90, not 90 independent notes) with the highest existing-score historical candidate per episode (selected N=17; abstained N=46). These historical representatives describe score behavior, not a new choice of onset. The populations are differently sampled; this is descriptive and cannot isolate separation as the cause.

| Feature | Controlled proxy | Historical selected | Historical abstained |
|---|---:|---:|---:|
| log_flux_peak | -1.461054 | -2.260574 | -2.076655 |
| low_energy_pre_log | -4.536858 | -3.359900 | -2.601801 |
| low_energy_post_pre_logratio | 2.752770 | -0.056424 | -0.081555 |
| rms_post_pre_logratio | 1.152751 | -0.027141 | -0.044107 |
| BP_relative_activity_position | 0.000129 | 0.848313 | 0.475306 |

Historical candidates show far weaker energy rise and higher pre-existing low-band activity than controlled attack proxies. Lower absolute flux alone does not explain abstention: abstained representatives have slightly higher median flux than selected representatives. Calibration, continuous overlapping instrumental activity, articulation and separation all remain potential contributors.

A material additional issue is BP relative-activity position: its controlled proxy median is near zero, whereas historical representatives lie much later within short BP activity segments. In the unchanged logistic score, median standardized contribution from this feature is +7.984 for selected representatives and +4.476 for abstained representatives. This supports a feature-distribution/score extrapolation concern and a tendency to favor later positions, not proof of a delayed physical attack. It prevents attributing all failure to Demucs smearing. No feature or model was changed.

The original mix contains additional local energy/flux structures, including earlier cues in HF044/HF047, but coexistence of other instruments prevents declaring those structures Bass or more faithful physical onsets. Multiple full-mix cues dominate. Neither waveform agreement nor disagreement alone establishes latency or truth.

## Decisions and limits

- FISHMAN→DEMUCS-STEM DOMAIN SHIFT EVIDENT: YES, as descriptive feature-distribution shift; its causal decomposition remains unresolved.
- FULL MIX PRESERVES USEFUL ATTACK EVIDENCE LOST/ALTERED IN STEM: INSUFFICIENT EVIDENCE for Bass-specific preservation/loss; additional acoustic cues are observed.
- LATE STEM SELECTION FAILURE MECHANISM SUPPORTED: PARTIAL; late-relative-BP score behavior and earlier mix cues are observed, but physical correctness is unknown.
- FULL-MIX INTERROGATION PROMISING FOR BASS-v1: PARTIAL, as a diagnostic representation comparison only.

No historical Ground Truth exists. Full-mix cue salience is not Bass identity, BP origin is not a physical onset, and Demucs is not independent evidence. No new Bass timing profile, correction or replacement timestamp is produced. Bass-v1 is not solved.

## Smallest next experiment — proposed, not executed

Use controlled Bass recordings with independent channel-specific onset references to construct a clearly labelled mixture/separation engineering control with competing percussion. Preserve the original Bass timing coordinates, verify any mixing offsets, and compare original Bass, mixture and separated Bass under the same frozen BP windows and features. Test whether the relative-activity-position distribution and energy-rise features explain score failure before designing a full-mix decision rule. A later controlled real-ensemble validation is still needed; a synthetic mixture alone cannot establish historical validity. Do not train or retune on Ray Brown.

## Deliverables and preservation

STEM_FULLMIX_ATTACK_INTERROGATION.csv contains every routed stem-candidate interrogation. QUERY_EVIDENCE.json and ALL_FULLMIX_FRONTS.json retain all bounded full-mix candidates/features. EPISODE_DIAGNOSTICS.json, LATE_SELECTION_AUDIT.json and STEM_DOMAIN_REPRESENTATIVES.json preserve classifications and their evidence. The three PDFs contain 63, 46 and 17 episode pages respectively. Diagnostic classifications were hashed in inference/output/DIAGNOSTIC_FREEZE.json before report rendering. Report artifacts are separately manifested. No canonical, Report 001, upstream, bootstrap or historical prediction changes; no commit, push or backup. STOP for PI review.
