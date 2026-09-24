from pathlib import Path
import os,json,numpy as np,soundfile as sf
os.environ['MPLCONFIGDIR']='/private/tmp/jga_bp120_mpl'
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
W=Path(__file__).resolve().parent;rows=json.loads((W/'EVENT_RESULTS.json').read_text());res=json.loads((W/'RESULTS.json').read_text()); audit=json.loads((W/'ALL_HYPOTHESES_ASSOCIATION_AUDIT.json').read_text());matched=[r for r in rows if r['signed_error_ms'] is not None]
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
with PdfPages(W/'GALLEGATI_NATIVE_BP_ONSET_VS_GT_120.pdf') as pdf:
 fig,axs=plt.subplots(4,1,figsize=(14,11),layout='constrained')
 for j,ax in enumerate(axs):
  subset=rows[j*30:(j+1)*30];ax.axhline(0,color='black',lw=.7)
  for k,r in enumerate(subset):
   if r['signed_error_ms'] is not None:ax.scatter(k,r['signed_error_ms'],facecolor='none',edgecolor='tab:blue',s=40)
   else:ax.scatter(k,80,marker='x',color='tab:orange');ax.text(k,85,'multiple',rotation=90,fontsize=6)
  ax.set_xticks(range(len(subset)),[r['GT_event_id'].split('_')[-1] for r in subset],rotation=90);ax.set_ylim(-85,115);ax.set_ylabel('BP − GT (ms)')
  for k in [0,10,20]:
   r=subset[k];ax.axvline(k-.5,color='.7');ax.text(k,107,f"{r['take']} · {r['string']} · {r['condition']}",fontsize=8)
 fig.suptitle('Native Basic Pitch vs Fishman observable-onset GT — all 120 events\n○ unique correct-pitch match · × unresolved multiple candidates (status lane, not a timing value)\nChronological within each take; no octave-equivalent or missed events under the fixed protocol')
 pdf.savefig(fig);plt.close(fig)
with PdfPages(W/'GALLEGATI_NATIVE_BP_ERROR_BY_STRING_CONDITION.pdf') as pdf:
 fig,axs=plt.subplots(2,1,figsize=(11,9),layout='constrained')
 for ax,key,groups in [(axs[0],'string',['E','A','D','G']),(axs[1],'condition',['mf','comfortable-natural','forte'])]:
  vals=[[r['signed_error_ms'] for r in matched if r[key]==g] for g in groups];ax.boxplot(vals,tick_labels=[f'{g}\nN={len(v)}' for g,v in zip(groups,vals)],showfliers=True)
  for i,v in enumerate(vals,1):ax.scatter(i+np.linspace(-.10,.10,len(v)),v,s=12,alpha=.5)
  ax.axhline(0,color='black',lw=.7);ax.set_ylabel('Native BP − Fishman GT (ms)')
 fig.suptitle('Uncorrected native timing — unique matches only\nBoxes Q1–Q3, median, 1.5×IQR whiskers; all observations and outliers shown')
 pdf.savefig(fig);plt.close(fig)
examples=[('Smallest absolute error',min(matched,key=lambda r:r['absolute_error_ms'])),('Typical absolute error',min(matched,key=lambda r:abs(r['absolute_error_ms']-res['pooled']['median_absolute_ms']))),('Largest early error',min(matched,key=lambda r:r['signed_error_ms'])),('Largest late error',max(matched,key=lambda r:r['signed_error_ms'])),('Multiple exact-pitch candidates',next(r for r in rows if r['match_classification']=='MULTIPLE_BP_CANDIDATES'))]
# Show octave hypotheses as competing context without falsely labelling an octave-equivalent match.
octrow=next((r for r in rows if any(a['GT_event_id']==r['GT_event_id'] and a['candidate'] and a['midi_pitch']!=r['expected_pitch'] and (a['midi_pitch']-r['expected_pitch'])%12==0 for a in audit)),None)
if octrow:examples.append(('Octave-related competing hypotheses (not an octave-equivalent selected match)',octrow))
with PdfPages(W/'GALLEGATI_NATIVE_BP_TIMING_EXAMPLES.pdf') as pdf:
 for title,r in examples:
  t=r['GT_onset'];ns=[n for n in audit if n['GT_event_id']==r['GT_event_id'] and n['candidate']];focus=[n for n in ns if n['highest_pitch_tier']];left=min([t-.15]+[n['onset_local_s']-.03 for n in focus]);right=max([t+.2]+[n['onset_local_s']+.08 for n in focus]);ns=[n for n in ns if n['onset_local_s']<right and n['offset_local_s']>left];audio=W/'inference/input'/f"{r['clip_id']}.wav"
  with sf.SoundFile(audio) as f:
   sr=f.samplerate;start=max(0,int(left*sr));f.seek(start);x=f.read(int((right-start/sr)*sr));x=x.mean(axis=1) if x.ndim>1 else x
  ts=(np.arange(len(x))+start)/sr-t
  fig,axs=plt.subplots(2,1,figsize=(12,7),sharex=True,layout='constrained');axs[0].plot(ts*1000,x,color='.3',lw=.5);axs[0].set_ylabel('Fishman amplitude')
  for ax in axs:
   ax.axvspan((r['GT_lower_bound']-t)*1000,(r['GT_upper_bound']-t)*1000,color='green',alpha=.2);ax.axvline(0,color='green',label='Human GT')
  for n in ns:
   s=(n['onset_local_s']-t)*1000;e=(n['offset_local_s']-t)*1000;sel=n['native_note_id']==r['matched_BP_event_id'];color='tab:blue' if sel else 'tab:orange';axs[1].plot([s,e],[n['midi_pitch']]*2,color=color,lw=4,alpha=.7);axs[1].axvline(s,color=color,lw=.7);axs[1].text(s,n['midi_pitch']+.3,f"{n['native_note_id']} {s:+.2f} ms",fontsize=7)
  axs[1].set_xlim((left-t)*1000,(right-t)*1000);axs[1].set_ylabel('Native MIDI hypothesis');axs[1].set_xlabel('Milliseconds relative to human GT (no BP correction)');fig.suptitle(f"{title}\n{r['GT_event_id']} · expected MIDI {r['expected_pitch']} · {r['match_classification']}")
  pdf.savefig(fig);plt.close(fig)
  if title=='Largest early error':figpath=W/'EXAMPLE_PREVIEW.png';fig.savefig(figpath,dpi=120)
p=res['pooled'];s=['# Native Basic Pitch onset vs human GT — Gallegati 120','', '**Decision: native BP onset is NOT suitable as a general JGA Bass microtiming landmark on this evidence.**','', 'Target: channel-specific observable onset in Fishman Full Circle; NOT physical string-release Ground Truth. Human annotation interface used 1 ms steps; decimal coordinates do not imply sub-millisecond human accuracy.','', '## Evidence and procedure','', 'Both supplied GT/freeze hashes and all 12 original source hashes verified. Existing BP evidence covers 36 isolated excerpts, not these complete takes. Official Basic Pitch 0.4.0 bundled ICASSP 2022 CoreML model ran with documented defaults on all 12 complete WAVs. Opaque byte-identical audio copies were the only inference inputs. Filesystem isolation denied repository references and /Volumes; a Python audit hook provided a second guard. Native model arrays, MIDI and all 760 note hypotheses were saved and hashed before GT comparison. Model, defaults, source and output hashes are preserved in PHASE0_AUDIT.json and inference/output/.','', 'The CoreML runtime emitted optional-backend/conversion warnings and a cache-cleanup permission warning. All 12 outputs completed, were finite, and passed saved-hash verification; no fallback model or changed settings were used.','', 'MATCHING_PROTOCOL.json was saved before inference and GT-center inspection. Chronological territories use midpoints between adjacent human events. Candidates must begin in that territory and persist to the human earliest plausible bound. Expected pitch has priority, then octave equivalence, then other pitch. More than one candidate in the highest available tier remains unresolved; no nearest-error, amplitude or duration ranking. This is reference-assisted correspondence, not an autonomous note selector. Persistence filtering excludes pre-attack-ending fragments and can condition the timing distribution; it does not validate those discarded fragments as nonphysical events.','', '## Recognition and matching','', '120 GT events; 107 unique correct-pitch matches; 0 octave-equivalent; 0 wrong-pitch; 13 multiple-candidate events; 0 missed under this association rule. Expected pitch appears in all 120 association sets.','', '760 native hypotheses = 107 selected + 26 highest-tier hypotheses in 13 ambiguous events + 347 other associated hypotheses + 280 unassociated additional hypotheses. Additional hypotheses are not automatically false physical notes. No raw prediction was deleted. Timing statistics exclude the 13 ambiguous events and therefore are conditional on defensible matching, not 120-event accuracy.','', '## Raw timing, N=107','']
for k,v in p.items():s.append(f'- {k}: {v}')
s+=['','## Stratified timing','', '| Group | N | Signed median ms | Mean ms | Absolute median ms | Signed IQR ms | Absolute P95 ms | Max absolute ms | ≤10 ms % |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for typ in ['by_string','by_condition','by_take']:
 for key,v in res[typ].items():s.append(f"| {key} | {v['N']} | {v['median_signed_ms']:.3f} | {v['mean_signed_ms']:.3f} | {v['median_absolute_ms']:.3f} | {v['IQR_signed_ms']:.3f} | {v['P95_absolute_ms']:.3f} | {v['maximum_absolute_ms']:.3f} | {v['within_10_ms_pct']:.2f} |")
s+=['','All threshold percentages, interval counts and ranges for every group/take are in RESULTS.json.','', '## Interpretation — inference, not a causal claim','', 'TIMING BIAS: CONDITION-DEPENDENT, with substantial within-condition instability. E-string median absolute error is 32.79 ms versus G-string 5.68 ms. A-string take medians switch from late in mf/forte to early in comfortable-natural; this is inconsistent with one constant global delay. One take per string/condition confounds take effects with condition, so it cannot establish a causal dynamic effect. E comfortable-natural alone has a 90.46 ms signed IQR.','', 'The pooled signed median −3.92 ms masks large event errors. MAE 13.22 ms, P95 56.88 ms, max 68.07 ms, and 13 unresolved correspondences are material relative to JGA’s 10–30 ms effects. No arbitrary pass threshold or bias correction was introduced. Strong pitch recognition does not establish onset correctness. Recognition is PARTIAL for an unambiguous timing test, sufficient for this conditional 107-event comparison.','', 'No PLP, spectral-flux selection, historical audio, model tuning, timestamp correction, or alternative detector was used. GT and previous artifacts remain unchanged.','', '## Deliverables','', '- GALLEGATI_NATIVE_BP_VS_GT_120.csv: exactly 120 rows.','- GALLEGATI_NATIVE_BP_ONSET_VS_GT_120.pdf','- GALLEGATI_NATIVE_BP_ERROR_BY_STRING_CONDITION.pdf','- GALLEGATI_NATIVE_BP_TIMING_EXAMPLES.pdf','- ALL_HYPOTHESES_ASSOCIATION_AUDIT.json and ADDITIONAL_UNASSOCIATED_BP_NOTES.json','- RAW_RESULTS_FREEZE.json and inference/output/TRANSCRIPTION_COMPLETE.json','', 'NATIVE BASIC PITCH TIMING TEST COMPLETED: YES','BP NOTE RECOGNITION SUFFICIENT FOR TIMING TEST: PARTIAL','NATIVE BP ONSET SUITABLE AS JGA BASS MICROTIMING LANDMARK: NO','', 'COMMIT: NONE · PUSH: NONE. Stop for PI review.']
(W/'RESULT.md').write_text('\n'.join(s)+'\n')
print('Three requested PDFs and complete report generated.')
