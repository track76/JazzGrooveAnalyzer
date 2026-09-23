from pathlib import Path
import os,csv,json
os.environ['MPLCONFIGDIR']='/private/tmp/jga_quarter_nearest_mpl';os.environ['XDG_CACHE_HOME']='/private/tmp/jga_quarter_nearest_cache'
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
O=Path(__file__).resolve().parent;read=lambda n:list(csv.DictReader((O/'INPUT_SNAPSHOTS'/n).open()));original_r=read('ALL_EVENT_ROLES.csv');original_q=read('QUARTER_NEAREST_ONSETS.csv');cells=read('QUARTER_CELLS.csv');source={'acoustic_end_s':330};sections=json.loads((O/'INPUT_SNAPSHOTS/SECTIONS.json').read_text())
assign=list(csv.DictReader((O/'SOURCE_CONDITIONED_ASSIGNMENTS.csv').open()))
selected_ids={x[k] for x in assign for k in ['BASS_id','DRUM_id'] if x[k]}
shared_ids={x['BASS_id'] for x in assign if x['status']=='SHARED_DUAL_MARKER'}
source_view=False
r=original_r;q=original_q
styles={'DRUM_SUPPORTED':('#c66a16','D','Drum-supported'),'BASS_SUPPORTED':('#286ea8','o','Bass-supported'),'BASS_AND_DRUM_SUPPORTED':('#8855ad','s','Dual-supported'),'CONFLICTING_EVIDENCE':('#ad3434','X','Conflict'),'UNKNOWN':('#343a40','^','UNKNOWN primary')}
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
def draw(name,detail=False):
 if detail:
  qq=[x for x,c in zip(q,cells) if float(c['RIGHT_BOUNDARY'])>=122 and float(c['LEFT_BOUNDARY'])<=128.5];ids={x['quarter_id'] for x in qq};rr=[x for x in r if x['quarter_id'] in ids];xs=[float(x['native_timestamp']) for x in rr]+[float(x['quarter_timestamp']) for x in qq];lo=min(122,min(xs))-.06;hi=max(128.5,max(xs))+.06
 else:qq=q;rr=r;lo=0;hi=source['acoustic_end_s']
 fig,(a,b)=plt.subplots(2,1,figsize=(16,8 if detail else 9),sharex=True,gridspec_kw={'height_ratios':[1,3]},layout='constrained');qt=np.array([float(x['quarter_timestamp']) for x in qq]);bp=np.array([float(x['stored_BPM']) for x in qq]);a.plot(qt,bp,c='#446781',lw=1.2);a.set_ylabel('RAW / discrete PLP\ninter-peak BPM');a.set_title('Short-scale jaggedness includes timestamp-lattice quantization; not inferred performer tempo changes',fontsize=9,pad=23)
 for t in qt:
  for ax in [a,b]:ax.axvline(t,c='#a0a6aa',lw=.5 if detail else .35,alpha=.35 if detail else .12,zorder=0)
 context=[x for x in rr if x['role']=='CONTEXT']
 for st,(color,marker,label) in styles.items():
  z=[x for x in context if x['source_state']==st]
  b.scatter([float(x['native_timestamp']) for x in z],[float(x['EVENT_TO_CELL_QUARTER_MS']) for x in z],facecolors='none' if st=='BASS_SUPPORTED' else '#bfc3c7',edgecolors='#bfc3c7',s=32 if detail else 10,marker=marker,alpha=1,label='Gray context: '+label,zorder=2)

 for st,(color,marker,label) in styles.items():
  z=[x for x in rr if x['role']=='PRIMARY' and x['source_state']==st];xx=[float(x['native_timestamp']) for x in z];yy=[float(x['EVENT_TO_CELL_QUARTER_MS']) for x in z]
  b.scatter(xx,yy,s=62 if detail else 21,marker=marker,facecolors='none' if st=='BASS_SUPPORTED' else color,edgecolors=color,linewidths=1,label=label,zorder=4)
  if detail:
   for n,(tx,yy0) in enumerate(zip(xx,yy)):
    dy=[12,25,-20,35,-31][n%5];b.annotate(f'{yy0:+.0f} ms',(tx,yy0),xytext=(0,dy),textcoords='offset points',ha='center',fontsize=8,color=color,arrowprops={'arrowstyle':'-','lw':.4,'color':color})
 if source_view:
  for x in rr:
   if x['JGA_EVENT_ID'] in shared_ids:
    b.annotate('S',(float(x['native_timestamp']),float(x['EVENT_TO_CELL_QUARTER_MS'])),xytext=(0,7),textcoords='offset points',ha='center',fontsize=7 if detail else 5,color='#8855ad',zorder=6)
  for pair in assign:
   if pair['status']=='DISTINCT_PAIR' and pair['quarter_id'] in {x['quarter_id'] for x in qq}:
    xx=[float(pair['BASS_timestamp']),float(pair['DRUM_timestamp'])];yy=[float(pair['BASS_offset_ms']),float(pair['DRUM_offset_ms'])]
    b.plot(xx,yy,c='#555',lw=.6,zorder=3)
    if detail:b.annotate('D−B '+format(float(pair['DRUM_MINUS_BASS_MS']),'+.1f')+' ms',((xx[0]+xx[1])/2,(yy[0]+yy[1])/2),xytext=(4,4),textcoords='offset points',fontsize=8,color='#555')
 b.axhline(0,c='#555',lw=.9,label='Quarter zero');b.plot(qt,np.zeros(len(qt)),'|',c='#8b9095',ms=5,zorder=1)
 empty=[float(x['quarter_timestamp']) for x in qq if x['QUARTER_STATE']=='EMPTY'];b.scatter(empty,[.025]*len(empty),transform=b.get_xaxis_transform(),marker='s',facecolors='none',edgecolors='#a63a3a',s=24,label='Neither source support (rail)' if source_view else 'EMPTY quarter (rail)',zorder=5)
 b.set_ylabel('JGA-native marker − cell quarter (ms)');b.set_xlabel('Recording time');b.set_xlim(lo,hi);yyall=[float(x['EVENT_TO_CELL_QUARTER_MS']) for x in rr];b.set_ylim(min(yyall)-30,max(yyall)+45 if detail else max(yyall)+30);b.grid(axis='y',alpha=.2);b.legend(loc='upper center',bbox_to_anchor=(.5,-.15),ncol=4,fontsize=9)
 b.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{int(x)//60:02d}:{x%60:04.1f}' if detail else f'{int(x)//60:02d}:{int(x)%60:02d}'))
 if detail:
  for ax in [a,b]:ax.axvline(122,c='#444',ls='--',lw=.8);ax.axvline(128.5,c='#444',ls='--',lw=.8)
  for n,(tx,b0) in enumerate(zip(qt,bp)):
   if n%4==0:a.annotate(f'{b0:.2f}',(tx,b0),xytext=(0,7),textcoords='offset points',ha='center',fontsize=8)
  fig.suptitle('Quarter-centered Bass / Drum | reference 02:02–02:08.5\nS = shared Dual, ONE marker; line = distinct observable pair, not a physical attack claim')
 else:fig.suptitle(('Exactly Like You | source-conditioned Bass / Drum geometry; S = shared Dual, not a pair' if source_view else 'Exactly Like You | unchanged global selection; gray context retains source shape')+f'\n{sum(x["role"]=="PRIMARY" for x in rr)} unique selected landmarks + {len(context)} gray context events; no physical attack-time claim')
 if not detail:
  for k,section in enumerate(sections):
   l,u=section['start'],section['end']
   for ax in [a,b]:
    ax.axvspan(l,u,color='#dce6ef' if k%2==0 else '#faf5ec',alpha=.3,zorder=0)
    ax.axvline(l,color='#8a8a8a',ls=':',lw=.65)
   a.text((l+u)/2,1.01,section['id']+' '+section['label'],transform=a.get_xaxis_transform(),ha='center',fontsize=8)
 for ext in ['png','svg','pdf']:fig.savefig(O/(name+'.'+ext),dpi=190,bbox_inches='tight')
 plt.close(fig)
 return {'figure':name,'quarters_drawn':len(qq),'primary_markers_drawn':sum(x['role']=='PRIMARY' for x in rr),'context_markers_drawn':len(context),'empty_quarters_drawn':len(empty),'all_requested_context_retained':True,'x_limits':[lo,hi]}
counts=[draw('REVISED_GLOBAL_SOURCE_SHAPED_CONTEXT')]
source_view=True
r=[dict(e,role='PRIMARY' if e['JGA_EVENT_ID'] in selected_ids else 'CONTEXT') for e in original_r]
status={a['quarter_id']:a['status'] for a in assign}
q=[dict(e,QUARTER_STATE='EMPTY' if status[e['quarter_id']]=='NEITHER' else 'SELECTED') for e in original_q]
counts.append(draw('SOURCE_CONDITIONED_WHOLE'))
counts.append(draw('SOURCE_CONDITIONED_ZOOM',True))
(O/'FIGURE_POPULATIONS.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
