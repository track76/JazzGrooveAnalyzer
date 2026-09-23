from pathlib import Path
import os,csv,json
os.environ['MPLCONFIGDIR']='/private/tmp/jga_quarter_nearest_mpl';os.environ['XDG_CACHE_HOME']='/private/tmp/jga_quarter_nearest_cache'
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
O=Path(__file__).resolve().parent;read=lambda n:list(csv.DictReader((O/n).open()));r=read('ALL_EVENT_ROLES.csv');q=read('QUARTER_NEAREST_ONSETS.csv');cells=read('QUARTER_CELLS.csv');source={'acoustic_end_s':330};sections=json.loads((O/'SECTIONS.json').read_text())
styles={'DRUM_SUPPORTED':('#c66a16','D','Drum-supported'),'BASS_SUPPORTED':('#286ea8','o','Bass-supported'),'BASS_AND_DRUM_SUPPORTED':('#8855ad','s','Dual-supported'),'CONFLICTING_EVIDENCE':('#ad3434','X','Conflict'),'UNKNOWN':('#343a40','^','UNKNOWN primary')}
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
def draw(name,detail=False):
 if detail:
  qq=[x for x,c in zip(q,cells) if float(c['RIGHT_BOUNDARY'])>=122 and float(c['LEFT_BOUNDARY'])<=128.5];ids={x['quarter_id'] for x in qq};rr=[x for x in r if x['quarter_id'] in ids];xs=[float(x['native_timestamp']) for x in rr]+[float(x['quarter_timestamp']) for x in qq];lo=min(122,min(xs))-.06;hi=max(128.5,max(xs))+.06
 else:qq=q;rr=r;lo=0;hi=source['acoustic_end_s']
 fig,(a,b)=plt.subplots(2,1,figsize=(16,8 if detail else 9),sharex=True,gridspec_kw={'height_ratios':[1,3]},layout='constrained');qt=np.array([float(x['quarter_timestamp']) for x in qq]);bp=np.array([float(x['stored_BPM']) for x in qq]);a.plot(qt,bp,c='#446781',lw=1.2);a.set_ylabel('Frozen PLP inter-peak BPM')
 for t in qt:
  for ax in [a,b]:ax.axvline(t,c='#a0a6aa',lw=.5 if detail else .35,alpha=.35 if detail else .12,zorder=0)
 context=[x for x in rr if x['role']=='CONTEXT'];b.scatter([float(x['native_timestamp']) for x in context],[float(x['EVENT_TO_CELL_QUARTER_MS']) for x in context],c='#bfc3c7',s=32 if detail else 10,marker='o',alpha=1,label='Context (all sources)',zorder=2)
 for st,(color,marker,label) in styles.items():
  z=[x for x in rr if x['role']=='PRIMARY' and x['source_state']==st];xx=[float(x['native_timestamp']) for x in z];yy=[float(x['EVENT_TO_CELL_QUARTER_MS']) for x in z]
  b.scatter(xx,yy,s=62 if detail else 21,marker=marker,facecolors='none' if st=='BASS_SUPPORTED' else color,edgecolors=color,linewidths=1,label=label,zorder=4)
  if detail:
   for n,(tx,yy0) in enumerate(zip(xx,yy)):
    dy=[12,25,-20,35,-31][n%5];b.annotate(f'{yy0:+.0f} ms',(tx,yy0),xytext=(0,dy),textcoords='offset points',ha='center',fontsize=8,color=color,arrowprops={'arrowstyle':'-','lw':.4,'color':color})
 b.axhline(0,c='#555',lw=.9,label='Quarter zero');b.plot(qt,np.zeros(len(qt)),'|',c='#8b9095',ms=5,zorder=1)
 empty=[float(x['quarter_timestamp']) for x in qq if x['QUARTER_STATE']=='EMPTY'];b.scatter(empty,[.025]*len(empty),transform=b.get_xaxis_transform(),marker='s',facecolors='none',edgecolors='#a63a3a',s=24,label='EMPTY quarter (rail)',zorder=5)
 b.set_ylabel('JGA-native marker − cell quarter (ms)');b.set_xlabel('Recording time');b.set_xlim(lo,hi);yyall=[float(x['EVENT_TO_CELL_QUARTER_MS']) for x in rr];b.set_ylim(min(yyall)-30,max(yyall)+45 if detail else max(yyall)+30);b.grid(axis='y',alpha=.2);b.legend(loc='upper center',bbox_to_anchor=(.5,-.15),ncol=4,fontsize=9)
 b.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{int(x)//60:02d}:{x%60:04.1f}' if detail else f'{int(x)//60:02d}:{int(x)%60:02d}'))
 if detail:
  for ax in [a,b]:ax.axvline(122,c='#444',ls='--',lw=.8);ax.axvline(128.5,c='#444',ls='--',lw=.8)
  for n,(tx,b0) in enumerate(zip(qt,bp)):
   if n%4==0:a.annotate(f'{b0:.2f}',(tx,b0),xytext=(0,7),textcoords='offset points',ha='center',fontsize=8)
  fig.suptitle('Quarter-nearest onset | reference 02:02–02:08.5 (dashed bounds)\nOriginal event timestamps; neighboring cell context included at edges; no source-stream continuation')
 else:fig.suptitle(f'Exactly Like You | operational PLP quarter-nearest onset geometry\n{sum(x["role"]=="PRIMARY" for x in rr)} colored selected landmarks + {len(context)} gray context events; {len(empty)} EMPTY; no physical attack-time claim')
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
counts=[draw('QUARTER_NEAREST_GROOVE_WHOLE_TRACK'),draw('QUARTER_NEAREST_REFERENCE_WINDOW',True)]
(O/'FIGURE_POPULATION_COUNTS.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
