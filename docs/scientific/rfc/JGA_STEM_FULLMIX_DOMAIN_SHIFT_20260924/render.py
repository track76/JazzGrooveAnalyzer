import os
os.environ['MPLCONFIGDIR']='/private/tmp/jga_domain_mpl'
import json,hashlib,shutil,csv
from pathlib import Path
import numpy as np,soundfile as sf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
P=Path(__file__).resolve().parent; I=P/'inference'; O=I/'output'
load=lambda f:json.load(open(f))
E=load(O/'EPISODE_DIAGNOSTICS.json');Q=load(O/'QUERY_EVIDENCE.json');S=load(O/'SUMMARY.json');L=load(O/'LATE_SELECTION_AUDIT.json')
z=np.load(O/'SYNCHRONIZED_CURVES.npz');Z={k:z[k] for k in z.files}
b,sr=sf.read(I/'input/BASS.wav');f,sr2=sf.read(I/'input/FULLMIX.wav');b=b.mean(axis=1);f=f.mean(axis=1)
plt.rcParams.update({'font.size':8,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
def page(e):
 ids=e['hypothesis_ids'];fig,axs=plt.subplots(4,len(ids),figsize=(max(11,5*len(ids)),9),squeeze=False)
 for col,bp in enumerate(ids):
  q=Q[bp];a=q['search_start_s'];end=q['search_end_s'];t=Z[bp+'_time'];sel=e['historical_selected_s'];relations=q['stem_relations']
  ix=np.arange(int(np.ceil(a*sr)),int(np.floor(end*sr))+1);tt=ix/sr
  axs[0,col].plot(tt,b[ix],color='#24677d',lw=.6);axs[2,col].plot(tt,f[ix],color='#444444',lw=.6)
  axs[1,col].plot(t,Z[bp+'_stem_flux'],color='#24677d',lw=1)
  axs[3,col].plot(t,Z[bp+'_fm_flux'],color='#444444',lw=1)
  st=[r['stem_candidate_s'] for r in relations];sv=np.interp(st,t,Z[bp+'_stem_flux']);axs[1,col].scatter(st,sv,c=[r['frozen_stem_score'] for r in relations],cmap='viridis',vmin=0,vmax=1,s=13)
  for r in q['fullmix_fronts']:
   axs[3,col].scatter(r['timestamp_s'],r['flux'],color='#d05d14' if r['salient_cue'] else '#b7b7b7',s=27 if r['salient_cue'] else 8,zorder=4)
  for j,ax in enumerate(axs[:,col]):
   ax.set_xlim(a,end);ax.axvline(q['BP_onset_s'],color='#9151a0',ls='--',lw=1)
   if sel is not None and a<=sel<=end:ax.axvline(sel,color='#1679d3',lw=1.5)
   ax.grid(alpha=.15);ax.ticklabel_format(useOffset=False,axis='x');ax.set_xlabel('Original recording coordinate (s)' if j==3 else '')
  axs[0,col].set_title(f'{bp} · MIDI {relations[0]["pitch"] if relations else "?"}\nBP {q["BP_onset_s"]:.6f} s; independent ±150 ms window')
  for j,label in enumerate(['Bass waveform','Bass flux / frozen candidates','Original full mix','Full-mix flux / all bounded peaks']):axs[j,col].set_ylabel(label)
 fig.suptitle(f'{e["episode_id"]} · {e["route"]} · {e["historical_status"]}\n{e["selected_crosscheck_class"] or e["diagnostic_class"]}',fontsize=12)
 fig.text(.02,.015,'Purple dashed: native BP origin. Blue: unchanged selected stem coordinate. Orange: descriptive salience + energy cue; gray: other FM peaks.\nStem dot color: frozen score (dark low / yellow high). No full-mix attack selected. No PLP. Stems and mix are not independent source Ground Truth.',fontsize=8)
 fig.tight_layout(rect=[0,.065,1,.925]);return fig
sets=[('JGA_STEM_VS_FULLMIX_63_EPISODES.pdf',E),('JGA_FULLMIX_ABSTENTION_RECOVERY_DIAGNOSTIC.pdf',sorted([e for e in E if e['historical_selected_s'] is None],key=lambda e:(e['diagnostic_class'],e['episode_id']))),('JGA_SELECTED_STEM_ATTACKS_FULLMIX_CROSSCHECK.pdf',[e for e in E if e['historical_selected_s'] is not None])]
for name,events in sets:
 with PdfPages(P/name) as pdf:
  for e in events:
   fig=page(e);pdf.savefig(fig)
   if name==sets[0][0] and e['episode_id'] in ['HF001','HF044','HF047']:fig.savefig(P/(e['episode_id']+'_REVIEW.png'),dpi=110)
   plt.close(fig)
 print(name,len(events),flush=True)
shutil.copyfile(O/'STEM_FULLMIX_ATTACK_INTERROGATION.csv',P/'STEM_FULLMIX_ATTACK_INTERROGATION.csv')
ref=load(I/'input/CONTROLLED_FEATURE_REFERENCE.json')['NEAR_INTERVAL_PROXY']
features=['log_flux_peak','low_energy_pre_log','low_energy_post_pre_logratio','rms_post_pre_logratio','BP_relative_activity_position']
rows=[]
for feat in features:
 rows.append([feat,ref['features'][feat]['median'],S['domain_summary']['SELECTED']['features'][feat]['median'],S['domain_summary']['ABSTAINED']['features'][feat]['median']])
with open(P/'DOMAIN_FEATURE_COMPARISON.csv','w') as out:
 w=csv.writer(out);w.writerow(['feature','controlled_near_interval_proxy_median_N90','historical_selected_representative_median_N17','historical_abstained_representative_median_N46']);w.writerows(rows)
report='''# Stem-guided full-mix interrogation: domain-shift diagnostic

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

'''
for x in L:
 report+=f'- {x["episode_id"]}: stem−BP {json.dumps(x["stem_minus_successful_BP_ms"])} ms; {len(x["earlier_salient_FM_fronts_s"])} earlier cue(s); {x["selected_crosscheck_class"]}.\n'
report+='''
## Domain evidence and selector behavior

The following medians compare controlled development near-interval proxy candidates (N=90, not 90 independent notes) with the highest existing-score historical candidate per episode (selected N=17; abstained N=46). These historical representatives describe score behavior, not a new choice of onset. The populations are differently sampled; this is descriptive and cannot isolate separation as the cause.

| Feature | Controlled proxy | Historical selected | Historical abstained |
|---|---:|---:|---:|
'''
for r in rows:report+='| '+r[0]+' | '+' | '.join(f'{v:.6f}' for v in r[1:])+' |\n'
report+='''
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
'''
(P/'RESULT.md').write_text(report)
