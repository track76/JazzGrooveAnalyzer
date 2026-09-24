from pathlib import Path
import json,csv,hashlib,datetime
import numpy as np,soundfile as sf,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter
O=Path(__file__).resolve().parents[1];F=O/'figures';read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();LABEL='PROCESS-BLINDED RESTART AFTER INVESTIGATOR PLP EXPOSURE'
episodes=read(O/'tracking/output/FUNDAMENTAL_EPISODES.json');members=read(O/'tracking/output/HYPOTHESIS_MEMBERSHIP.json');naive=read(O/'tracking/output/NAIVE_LOWEST_EPISODES.json');lingering=read(O/'tracking/output/LINGERING_CASES.json');summary=read(O/'tracking/output/SUMMARY.json');freeze=read(O/'tracking/output/EPISODE_FREEZE.json')
for n,h in freeze['files'].items():assert sha(O/'tracking/output'/n)==h
byid={e['episode_id']:e for e in episodes};notes={m['note_id']:m['native_hypothesis'] for m in members};colors={e['episode_id']:plt.get_cmap('tab20')(i%20) for i,e in enumerate(episodes)};x,sr=sf.read(O/'tracking/input/bass.wav',always_2d=True);x=x.mean(axis=1);lingerids={r['note_id'] for r in lingering}
fmt=FuncFormatter(lambda t,pos:f'{int(t)//60:02}:{t%60:05.2f}')
def draw(lo,hi,title,detail=False):
 fig,axs=plt.subplots(4,1,figsize=(12,11),sharex=True,gridspec_kw={'height_ratios':[1,1.5,1,1.8]});fig.subplots_adjust(top=.88,bottom=.12,hspace=.3,left=.09,right=.98);fig.suptitle(title,fontsize=13,y=.98);fig.text(.5,.94,LABEL,ha='center',fontsize=8);fig.text(.5,.913,'Identity/activity hypotheses only · episode starts are not validated attacks',ha='center',fontsize=9)
 ix=np.arange(max(0,int((lo-45)*sr)),min(len(x),int((hi-45)*sr)),8 if detail else 24);axs[0].plot(45+ix/sr,x[ix],color='.35',lw=.55);axs[0].set_ylabel('Bass stem')
 for m in members:
  n=m['native_hypothesis']
  if n['offset']<=lo or n['onset']>=hi:continue
  color=colors.get(m['family_id'],'.5');axs[1].add_patch(Rectangle((n['onset'],n['pitch']-.33),n['offset']-n['onset'],.66,facecolor=color,alpha=.8))
  if m['role']=='HARMONIC_HYPOTHESIS':
   axs[3].plot([n['onset'],n['offset']],[n['pitch']]*2,color=color,lw=1.2,ls='--');
   if detail:axs[3].text(n['onset'],n['pitch']+1,f"h{m['harmonic_number']} {m['family_id']}",fontsize=7,color=color)
  if n['note_id'] in lingerids:axs[3].plot([n['onset'],n['offset']],[n['pitch']]*2,color=color,lw=3,alpha=.45)
  if m['role']=='UNRESOLVED_FAMILY_OR_NEW_ROOT':axs[3].plot([n['onset'],n['offset']],[n['pitch']]*2,color='.4',ls=':',lw=2)
 for e in naive:
  if e['end_s']>lo and e['start_s']<hi:axs[2].plot([e['start_s'],e['end_s']],[e['pitch']]*2,color='#505050',lw=2)
 for i,e in enumerate(episodes):
  if e['end_s']<=lo or e['start_s']>=hi:continue
  c=colors[e['episode_id']];p=e['fundamental_midi']
  for nid in e['root_note_ids']:
   n=notes[nid];axs[3].plot([n['onset'],n['offset']],[p]*2,color=c,lw=3,alpha=.25)
  axs[3].plot([e['root_onset_s'],e['display_current_end_s']],[p]*2,color=c,lw=2.5)
  if lo<=e['start_s']<hi:
   axs[3].axvline(e['start_s'],color=c,lw=.45,alpha=.6);axs[3].text(e['start_s'],69 if i%2 else 73,e['episode_id']+('?' if e['ambiguity'] else ''),rotation=90,fontsize=7 if detail else 5,ha='center',va='top')
 for ax in axs[1:]:ax.set_ylim(26,75);ax.set_yticks([28,36,43,52,60,64]);ax.set_yticklabels(['E1/28','C2/36','G2/43','E3/52','C4/60','E4/64'],fontsize=7);ax.grid(axis='y',alpha=.15)
 axs[1].set_ylabel('Raw BP notes');axs[2].set_ylabel('Lowest active');axs[3].set_ylabel('Fundamentals\n+ family members');axs[3].set_xlim(lo,hi);axs[3].xaxis.set_major_formatter(fmt);axs[3].set_xlabel('Original recording time (MM:SS.xx)')
 fig.text(.09,.025,'Solid: current fundamental hypothesis · faint solid: native root tails/fragments · dashed: harmonic hypothesis\nThick translucent dashed line: lingering harmonic · ? ambiguous family/fragment/overlap · color tracks family ownership\nNo note timestamps moved; current-line truncation is a display convention. Original native durations remain in raw/faint layers.',fontsize=8)
 return fig
lo=min(n['onset'] for n in notes.values())-.15;hi=max(n['offset'] for n in notes.values())+.15
with PdfPages(F/'EXACTLY_LIKE_YOU_FUNDAMENTAL_TRACKING.pdf') as pdf:
 for j,start in enumerate(np.arange(lo,hi,6)):
  fig=draw(start,min(start+6,hi),f'Basic Pitch interpretations — complete sequence, page {j+1}');pdf.savefig(fig);fig.savefig(F/f'TRACKING_PAGE_{j+1:02}.png',dpi=105);plt.close(fig)
examples=[]
late=[m for m in members if m['role']=='HARMONIC_HYPOTHESIS' and m['native_hypothesis']['onset']>byid[m['family_id']]['root_onset_s']]
if late:
 m=late[0];e=byid[m['family_id']];examples.append(('Overtone hypothesis starts after its root',max(45,e['root_onset_s']-.12),min(74,m['native_hypothesis']['offset']+.12),[m['note_id']]))
for r in lingering:
 e=byid[r['parent_family']];n=notes[r['note_id']];examples.append(('New lower root under a lingering prior-family harmonic' if r['new_root_below_harmonic'] else 'Prior harmonic survives a new root',max(45,min(e['root_onset_s'],r['transition_s'])-.15),min(74,max(n['offset'],r['transition_s']+.35)+.1),[r['note_id'],r['new_family']]))
frag=[e for e in episodes if len(e['root_note_ids'])>1]
for e in frag[:2]:examples.append(('Possible same-pitch fragments; rearticulation remains uncertain',max(45,e['start_s']-.12),min(74,e['end_s']+.12),e['root_note_ids']))
with PdfPages(F/'FUNDAMENTAL_TRACKING_ENLARGED_EXAMPLES.pdf') as pdf:
 for j,(title,start,stop,ids) in enumerate(examples):
  fig=draw(start,stop,title,True);pdf.savefig(fig);fig.savefig(F/f'EXAMPLE_{j+1:02}.png',dpi=110);plt.close(fig)
(O/'review/EXAMPLE_INDEX.json').write_text(json.dumps([dict(title=t,start_s=a,end_s=b,ids=ids) for t,a,b,ids in examples],indent=2)+'\n')
# Readable CSV views of already frozen content; no segmentation update.
for name,rows in [('FUNDAMENTAL_EPISODES',episodes),('HYPOTHESIS_MEMBERSHIP',members),('NAIVE_LOWEST_EPISODES',naive),('LINGERING_CASES',lingering)]:
 with (O/(name+'.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows([{k:json.dumps(v) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in rows])
line=np.array([e['fundamental_midi'] for e in episodes]);diagnostic={'root_pitch_range':[int(min(line)),int(max(line))],'median_absolute_successive_pitch_change_semitones':float(np.median(abs(np.diff(line)))),'successive_leaps_greater_than_octave':int(np.sum(abs(np.diff(line))>12)),'same_pitch_adjacent_root_episodes':int(np.sum(np.diff(line)==0)),'median_root_support_duration_s':float(np.median([e['fundamental_support_end_s']-e['root_onset_s'] for e in episodes]))}
(O/'review/LINE_DESCRIPTORS.json').write_text(json.dumps(diagnostic,indent=2)+'\n');print(json.dumps(diagnostic,indent=2));print('Main PDF pages',len(np.arange(lo,hi,6)),'enlarged examples',len(examples))
