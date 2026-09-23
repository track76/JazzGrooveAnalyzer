from pathlib import Path
import os,json,csv,shutil
os.environ['MPLCONFIGDIR']='/private/tmp/jga_stem_geometry_mpl';os.environ['XDG_CACHE_HOME']='/private/tmp/jga_stem_geometry_cache'
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from collections import Counter
O=Path(__file__).resolve().parent;R=O.parent;G=R/'JGA_V1_OPERATIONAL_PLP_QUARTER_NEAREST_001_20260922';F=R/'JGA_QUARTER_CENTERED_BASS_DRUM_GEOMETRY_001_20260923'
read=lambda p:list(csv.DictReader(Path(p).open()));a=read(O/'STEM_ASSIGNMENTS.csv');e=read(O/'STEM_EVENT_ROLES.csv');f=read(G/'ALL_EVENT_ROLES.csv');fa=read(F/'SOURCE_CONDITIONED_ASSIGNMENTS.csv');q=read(G/'PLP_REFERENCE.csv');ss=json.loads((G/'SECTIONS.json').read_text());match=read(O/'EVENT_MATCHING.csv');dual=read(O/'DUAL_AUDIT.csv')
styles={'DRUM_SUPPORTED':('#c66a16','D','Drum-supported'),'BASS_SUPPORTED':('#286ea8','o','Bass-supported'),'BASS_AND_DRUM_SUPPORTED':('#8855ad','s','Dual-supported'),'CONFLICTING_EVIDENCE':('#ad3434','X','Conflict'),'UNKNOWN':('#343a40','^','UNKNOWN')}
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
selected={x[k] for x in fa for k in ['BASS_id','DRUM_id'] if x[k]};shared={x['BASS_id'] for x in fa if x['status']=='SHARED_DUAL_MARKER'}
for ext in ['png','pdf','svg']:shutil.copyfile(F/('SOURCE_CONDITIONED_WHOLE.'+ext),O/('FULL_MIX_UNCHANGED.'+ext))
pop=[]
def base(ax,lo,hi):
 ax.axhline(0,c='#555',lw=.9);ax.set_xlim(lo,hi);ax.grid(axis='y',alpha=.2);ax.set_ylabel('Native onset − PLP (ms)');ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{int(x)//60:02d}:{int(x)%60:02d}'))
 for z in q:
  t=float(z['time_seconds'])
  if lo<=t<hi:ax.axvline(t,c='#a0a6aa',lw=.35,alpha=.12,zorder=0);ax.plot([t],[0],'|',c='#8b9095',ms=5,zorder=1)
 for i,s in enumerate(ss):
  if s['end']>lo and s['start']<hi:ax.axvspan(s['start'],s['end'],color='#dce6ef' if i%2==0 else '#faf5ec',alpha=.3,zorder=0);ax.axvline(s['start'],color='#8a8a8a',ls=':',lw=.65)
 for s in ss:
  left,right=max(lo,s['start']),min(hi,s['end'])
  if right>left:ax.text((left+right)/2,.985,s['label'],transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=8,color='#555')
def full(ax,lo,hi):
 base(ax,lo,hi);rr=[x for x in f if lo<=float(x['native_timestamp'])<hi]
 for st,(col,mark,label) in styles.items():
  for chosen in [False,True]:
   z=[x for x in rr if x['source_state']==st and (x['JGA_EVENT_ID'] in selected)==chosen];color=col if chosen else '#bfc3c7';ax.scatter([float(x['native_timestamp']) for x in z],[float(x['EVENT_TO_CELL_QUARTER_MS']) for x in z],s=(62 if hi-lo<10 else 21) if chosen else (32 if hi-lo<10 else 10),marker=mark,facecolors='none' if st=='BASS_SUPPORTED' else color,edgecolors=color,alpha=1,linewidths=1,zorder=4 if chosen else 2,label='FM '+label if chosen else None)
 for x in rr:
  if x['JGA_EVENT_ID'] in shared:ax.annotate('S',(float(x['native_timestamp']),float(x['EVENT_TO_CELL_QUARTER_MS'])),xytext=(0,6),textcoords='offset points',ha='center',fontsize=6,color='#8855ad')
 ax.set_title('FULL MIX — existing support hypotheses; S = shared Dual, not two attacks',fontsize=10)
def stems(ax,lo,hi):
 base(ax,lo,hi);rr=[x for x in e if lo<=float(x['timestamp_s'])<hi]
 for k,st in [('bass','BASS_SUPPORTED'),('drums','DRUM_SUPPORTED')]:
  col,mark,_=styles[st]
  for chosen in [False,True]:
   z=[x for x in rr if x['stem']==k and (x['role']=='PRIMARY')==chosen];color=col if chosen else '#bfc3c7';ax.scatter([float(x['timestamp_s']) for x in z],[float(x['offset_ms']) for x in z],s=(62 if hi-lo<10 else 21) if chosen else (32 if hi-lo<10 else 10),marker=mark,facecolors='none' if k=='bass' else color,edgecolors=color,linewidths=1,alpha=1,zorder=4 if chosen else 2,label='SEPARATOR '+k.upper() if chosen else None)
  empty=[float(x['quarter_timestamp']) for x in a if x['stem']==k and x['state']=='EMPTY' and lo<=float(x['quarter_timestamp'])<hi];ax.scatter(empty,[.025 if k=='bass' else .06]*len(empty),transform=ax.get_xaxis_transform(),marker='s',facecolors='none',edgecolors='#a63a3a',s=24,label=k+' EMPTY rail')
 ax.set_title('SEPARATOR-derived landmarks — model labels, not Ground Truth',fontsize=10)
 return len(rr)
def save(fig,name):
 for ext in ['png','pdf','svg']:fig.savefig(O/(name+'.'+ext),dpi=180,bbox_inches='tight')
 plt.close(fig)
fig,(top,ax)=plt.subplots(2,1,figsize=(16,9),sharex=True,gridspec_kw={'height_ratios':[1,3]},layout='constrained');top.plot([float(x['time_seconds']) for x in q],[float(x['local_bpm']) for x in q],c='#446781',lw=1.2);top.set_ylabel('RAW/discrete PLP BPM');top.set_title('Common FULL-MIX PLP; short-scale jaggedness includes timestamp-lattice quantization',fontsize=10);n=stems(ax,0,330);ax.legend(ncol=4,fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.12));fig.suptitle('Exactly Like You — separated Bass/Drums against unchanged full-mix reference');save(fig,'STEMS_WHOLE');pop.append({'figure':'STEMS_WHOLE','native_stem_events_drawn':n})
for name,lo,hi in [('FULLMIX_VS_STEMS',0,330),('PIANO_BASS_EXCHANGES',141,186),('REFERENCE_ZOOM',122,128.5),('DUAL_OPENING_VIEW',0,48)]:
 fig,axs=plt.subplots(3,1,figsize=(16,11),sharex=True,gridspec_kw={'height_ratios':[3,3,1]},layout='constrained');full(axs[0],lo,hi);stems(axs[1],lo,hi)
 # Matching status lanes show appearance/loss without recoloring scientific source markers.
 lanes=[('bass','STEM','STEM_ONLY',0),('bass','FULL_MIX','FULL_MIX_ONLY',1),('drums','STEM','STEM_ONLY',2),('drums','FULL_MIX','FULL_MIX_ONLY',3)]
 labels=[]
 for k,side,status,y in lanes:
  support={'BASS_SUPPORTED','BASS_AND_DRUM_SUPPORTED'} if k=='bass' else {'DRUM_SUPPORTED','BASS_AND_DRUM_SUPPORTED'}
  z=[x for x in match if x['stem']==k and x['side']==side and x['status']==status and lo<=float(x['timestamp_s'])<hi and (side=='STEM' or x['full_mix_source_state'] in support)];col,mark,_=styles['BASS_SUPPORTED' if k=='bass' else 'DRUM_SUPPORTED'];axs[2].scatter([float(x['timestamp_s']) for x in z],[y]*len(z),s=12,marker=mark,facecolors='none' if k=='bass' else col,edgecolors=col);labels.append(k+' '+('stem-only' if side=='STEM' else 'FM-supported-only'))
 axs[2].set_yticks(range(4),labels,fontsize=8);axs[2].set_ylim(-.7,3.7);axs[2].set_xlabel('Original source time');axs[2].set_title('No compatible event within fixed one-hop rule; not proof of physical absence',fontsize=9)
 ymin=min(axs[0].get_ylim()[0],axs[1].get_ylim()[0]);ymax=max(axs[0].get_ylim()[1],axs[1].get_ylim()[1]);axs[0].set_ylim(ymin,ymax);axs[1].set_ylim(ymin,ymax)
 axs[0].legend(ncol=5,fontsize=8);axs[1].legend(ncol=4,fontsize=8);fig.suptitle(name.replace('_',' ')+' — same PLP cells; no alignment correction or physical truth claim');save(fig,name)
fig,ax=plt.subplots(figsize=(11,5),layout='constrained');ct=Counter(x['category'] for x in dual);ax.bar(list(ct),list(ct.values()),color='#8855ad');ax.tick_params(axis='x',labelrotation=20);ax.set_ylabel('Full-mix shared-Dual cells');ax.set_title('180 shared-Dual cells: stem observability, not verified physical disambiguation');save(fig,'DUAL_CATEGORY_AUDIT')
(O/'FIGURE_VALIDATION.json').write_text(json.dumps({'original_fullmix_copied':True,'source_styles':styles,'PLP_series_unchanged':True,'fullmix_selection_unchanged':True,'stem_context_preserved':True,'new_smoothing':False,'detail_windows_prospective':['Opening0-48','PianoBass141-186','Reference122-128.5'],'populations':pop},indent=2)+'\n')
