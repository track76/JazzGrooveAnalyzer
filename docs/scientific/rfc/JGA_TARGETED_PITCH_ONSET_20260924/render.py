import os
os.environ['MPLCONFIGDIR']='/private/tmp/jga_domain_mpl'
from pathlib import Path
import json,csv,hashlib,datetime,shutil,collections
import numpy as np,soundfile as sf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
P=Path(__file__).resolve().parent;I=P/'inference/input';O=P/'inference/output';load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
freeze=load(O/'OBSERVATION_FREEZE.json');assert all(sha(O/k)==h for k,h in freeze['files'].items())
E=load(O/'EPISODE_OBSERVATIONS.json');R=load(O/'TARGET_OBSERVATIONS.json');T=load(O/'TARGET_DEFINITIONS.json');Z0=np.load(O/'TARGET_TRACES.npz');Z={k:Z0[k] for k in Z0.files};x,sr=sf.read(I/'FULLMIX.wav');x=x.mean(axis=1)
# Post-freeze read of historical acoustic records ONLY. No PLP/timing-to-quarter files.
oldpath=P.parent/'JGA_STEM_FULLMIX_DOMAIN_SHIFT_20260924/inference/output/EPISODE_DIAGNOSTICS.json';old={e['episode_id']:e for e in load(oldpath)}
secure=[e['episode_id'] for e in E if old[e['episode_id']]['route']=='SECURE_ROUTE' and old[e['episode_id']]['historical_selected_s'] is None];assert len(secure)==25
clear={e['episode_id'] for e in E if e['status']=='TARGET_ONSET_CLEAR'};d=[abs(r['selected_minus_BP_ms']) for r in R if r['episode_id'] in clear and r['selected_minus_BP_ms'] is not None];primary=[e for e in E if old[e['episode_id']]['historical_selected_s'] is None and old[e['episode_id']]['diagnostic_class']=='MULTIPLE_LOCAL_FRONT_CUES']
S={'episodes':63,'counts':dict(collections.Counter(e['status'] for e in E)),'clear_coverage_percent':100*len(clear)/63,'clear_query_records_in_clear_episodes':len(d),'median_absolute_FM_minus_BP_ms':float(np.median(d)),'secure_abstentions_with_clear':sum(k in clear for k in secure),'secure_abstention_population':25,'previous34_multiple_cue_statuses':dict(collections.Counter(e['status'] for e in primary)),'shared_target_onset_episodes':[e['episode_id'] for e in E if e['shared_target_onset']],'special':[],'observation_freeze_sha256':sha(O/'OBSERVATION_FREEZE.json'),'postfreeze_acoustic_context_sha256':sha(oldpath)}
for eid in ['HF044','HF045','HF047','HF050']:
 rr=[r for r in R if r['episode_id']==eid];sel=old[eid]['historical_selected_s'];S['special'].append({'episode_id':eid,'status':next(e['status'] for e in E if e['episode_id']==eid),'old_stem_s':sel,'targets':[{'pitch':r['pitch_name'],'BP_onset_s':r['BP_onset_s'],'clear_target_s':r['selected_clear_onset_s'],'target_minus_BP_ms':r['selected_minus_BP_ms'],'target_minus_old_stem_ms':None if sel is None or r['selected_clear_onset_s'] is None else (r['selected_clear_onset_s']-sel)*1000} for r in rr]})
(P/'SUMMARY.json').write_text(json.dumps(S,indent=2)+'\n');shutil.copyfile(O/'TARGETED_PITCH_ONSET_FULLMIX.csv',P/'TARGETED_PITCH_ONSET_FULLMIX.csv')
plt.rcParams.update({'font.size':8,'pdf.fonttype':42})
def page(e,comparison=False):
 rr=[r for r in R if r['episode_id']==e['episode_id']];fig,ax=plt.subplots(4,len(rr),figsize=(max(11,4.4*len(rr)),10),squeeze=False)
 for col,r in enumerate(rr):
  k=r['query_id'];t=Z[k+'_t'];y=Z[k+'_fundamental'];obs=r['target_observation'];a=r['window_start_s'];b=r['window_end_s'];ix=np.arange(int(np.ceil(a*sr)),int(np.floor(b*sr))+1)
  ax[0,col].plot(ix/sr,x[ix],color='#4b4b4b',lw=.65)
  ax[1,col].plot(t,y,color='#146c7d',lw=1.5,label='Target power');ax[1,col].axhline(obs['low'],ls=':',color='#c18e26',label='20% rise');ax[1,col].axhline(obs['high'],ls=':',color='#793576',label='60% confirmation');ax[1,col].legend(fontsize=6)
  for j,harm in enumerate([2,3]):
   yy=Z[k+f'_harmonic{harm}'];hh=r['harmonic_observations'][j];ax[2,col].plot(t,yy/(yy.max()+1e-20),label=f'{harm}f0: {hh["status"].replace("TARGET_","")}',lw=1);ax[2,col].legend(fontsize=5)
  ax[3,col].plot(t,y/(obs['peak']+1e-20),color='#146c7d');ax[3,col].fill_between(t,0,1,where=y>=obs['high'],alpha=.15,color='#146c7d');ax[3,col].set_ylim(-.04,1.05)
  for j in range(4):
   aa=ax[j,col];aa.set_xlim(a,b);aa.axvline(r['BP_onset_s'],ls='--',color='#9751a0',lw=1)
   for c in r['target_onset_candidates_s']:aa.axvline(c,color='#d46716',lw=1.3)
   if comparison and old[e['episode_id']]['historical_selected_s'] is not None:aa.axvline(old[e['episode_id']]['historical_selected_s'],color='#267dd1',ls='-.',lw=1)
   aa.ticklabel_format(axis='x',useOffset=False);aa.grid(alpha=.13)
  ax[0,col].set_title(f'{r["BP_member_id"]} · {r["pitch_name"]} · {r["f0_hz"]:.2f} Hz\n{r["target_onset_status"]}',fontsize=8)
  for j,l in enumerate(['Original mix','Target-frequency power','Optional harmonics (normalized)','Normalized target / confirmation']):ax[j,col].set_ylabel(l)
  ax[3,col].set_xlabel('Original recording coordinate (s)')
  ax[3,col].text(.02,.97,f'Hann support {obs["support_ms"]:.1f} ms\nENBW {obs["ENBW_hz"]:.1f} Hz\nCrossings: '+', '.join(f'{v:.6f}' for v in r['target_onset_candidates_s']),transform=ax[3,col].transAxes,va='top',fontsize=6)
 fig.suptitle(f'{e["episode_id"]} · {e["status"]}'+(' · SHARED_TARGET_ONSET' if e['shared_target_onset'] else ''),fontsize=12)
 fig.text(.015,.015,'Purple: native BP; orange: original-grid target-energy crossing; blue (special review only): prior stem coordinate, read after observation freeze.\nCentered filtering can smear energy before the physical onset. No PLP. Clear is conditional pitched activity, not validated Bass onset or exclusive source identity.',fontsize=8)
 fig.tight_layout(rect=[0,.06,1,.94]);return fig
with PdfPages(P/'JGA_TARGETED_PITCH_ONSET_63.pdf') as pdf:
 for e in E:
  fig=page(e);pdf.savefig(fig);plt.close(fig)
print('63 episode pages rendered',flush=True)
# All episodes, per-query native observations and statuses, no winner selection.
fig,ax=plt.subplots(figsize=(16,12));colors={'TARGET_ONSET_CLEAR':'#168268','TARGET_ONSET_MULTIPLE':'#c27e00','TARGET_ACTIVITY_CONTINUOUS':'#4674ab','TARGET_NOT_OBSERVABLE':'#777','TARGET_ONSET_UNRESOLVED':'#ae4265'}
for i,e in enumerate(E):
 rr=[r for r in R if r['episode_id']==e['episode_id']]
 for r in rr:
  ax.scatter(r['BP_onset_s'],i,marker='|',color='#8953a0',s=45)
  for c in r['target_onset_candidates_s']:
   ax.plot([r['BP_onset_s'],c],[i,i],color=colors[e['status']],lw=.5);ax.scatter(c,i,color=colors[e['status']],s=10,marker='o' if e['status']=='TARGET_ONSET_CLEAR' else 'x')
 ax.text(1.005,i,e['status'].replace('TARGET_',''),transform=ax.get_yaxis_transform(),fontsize=6,color=colors[e['status']])
ax.set_yticks(range(63),[e['episode_id'] for e in E],fontsize=7);ax.invert_yaxis();ax.set_xlabel('Original recording time (s); purple ticks = native BP origins');ax.set_title('Complete 63-episode target-frequency observation map\nAll query candidates preserved; no PLP or metrical assignment');ax.grid(alpha=.15);fig.tight_layout(rect=[0,0,.85,1]);fig.savefig(P/'JGA_TARGETED_PITCH_ONSET_SUMMARY.pdf');plt.close(fig)
ids=['HF044','HF045','HF047','HF050']
for wanted in ['TARGET_ONSET_CLEAR','TARGET_ONSET_UNRESOLVED','TARGET_ACTIVITY_CONTINUOUS','TARGET_ONSET_MULTIPLE','TARGET_NOT_OBSERVABLE']:
 options=[e['episode_id'] for e in E if e['status']==wanted and e['episode_id'] not in ids];secure_options=[k for k in options if k in secure];
 if options:ids.append((secure_options or options)[0])
with PdfPages(P/'JGA_TARGETED_PITCH_SPECIAL_CASES.pdf') as pdf:
 for eid in ids:
  fig=page(next(e for e in E if e['episode_id']==eid),True);pdf.savefig(fig)
  if eid in ['HF044','HF047']:fig.savefig(P/(eid+'_REVIEW.png'),dpi=110)
  plt.close(fig)
S['special_figure_episode_ids']=ids;(P/'SUMMARY.json').write_text(json.dumps(S,indent=2)+'\n')
print(json.dumps(S,indent=2))
