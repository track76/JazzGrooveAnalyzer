from pathlib import Path
import os,sys,csv,json,io,textwrap
os.environ['MPLCONFIGDIR']='/private/tmp/jga_final_mpl'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MultipleLocator,FuncFormatter
from matplotlib.lines import Line2D
sys.path.insert(0,'tools')
from continuous_backup import atomic_write_and_backup,preflight
O=Path(__file__).resolve().parent
preflight()
def rows(p):return list(csv.DictReader(p.open()))
def put(n,b):atomic_write_and_backup(O/n,b.encode() if isinstance(b,str) else b)
def table(n,rr):
 b=io.StringIO();w=csv.DictWriter(b,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr);put(n,b.getvalue())
dis=rows(O/'FINAL_ANCHORED_BMIG_DMIG.csv');ev=rows(O/'EVENT_PROVENANCE_127.csv')
refs=rows(O/'source_visual/METRIC_REFERENCE.csv');tt=[float(r['reference_time']) for r in refs];win=rows(O/'source_visual/BPM_EVOLUTION.csv');central=json.loads((O/'source_visual/PROFILE.json').read_text())['tempo']['central_bpm']
reader_text='Nella selezione analizzata, contrabbasso e batteria mostrano una pulsazione interna fortemente coesa. Nelle misure con tutti i punti della pulsazione osservati, la differenza mediana tra le due griglie è di circa 8,9 ms, con il contrabbasso leggermente arretrato rispetto alla batteria. Lo scarto rimane contenuto e descrive una relazione temporale complessivamente molto ravvicinata tra i due strumenti.'
bpm_text='BPM interno: 161,50 → 161,50 · invariato'
plt.rcParams.update({'font.size':7,'axes.spines.top':False,'axes.spines.right':False,'font.family':'DejaVu Sans'})
blue='#286ea8';orange='#c66a16';rendered=[];gridlog=[];localbp=[];bpmcheck=[]
mem=io.BytesIO()
with PdfPages(mem) as pdf:
 fig=plt.figure(figsize=(210/25.4,297/25.4))
 fig.text(.07,.975,'JGA Microtiming Score · BMIG / DMIG — FINALE',fontsize=11,weight='bold')
 fig.text(.07,.956,'Ray Brown Trio — Exactly Like You · M33–M48',fontsize=8)
 fig.text(.07,.939,'Pulsazioni interne e attacchi musicali',fontsize=8,weight='bold')
 fig.text(.07,.925,'Pulsazioni interne · valori B / D in millisecondi',fontsize=7)
 top=fig.add_axes([.08,.848,.89,.068]);line,=top.plot([float(x['center_s']) for x in win],[float(x['BPM']) for x in win],c='#546875',lw=.6);top.axhline(central,c='#999',ls='--',lw=.5);top.set(xlim=(0,330),ylabel='BPM');top.xaxis.set_major_locator(MultipleLocator(30));top.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{int(x)//60:02}:{int(x)%60:02}'));top.tick_params(labelsize=6)
 assert list(line.get_ydata())==[float(x['BPM']) for x in win]
 selected=json.loads((O/'source_visual/BPM_EXTREMA_ANNOTATIONS.json').read_text())['selected']
 boxes=[]
 for c in selected:
  above=c['kind']=='MAX';a=top.annotate(f"{c['BPM']:.1f}",(c['time_s'],c['BPM']),xytext=(0,2 if above else -3),textcoords='offset points',ha='center',va='bottom' if above else 'top',fontsize=5.2,color='#34434b',bbox={'facecolor':'white','edgecolor':'none','pad':.15})
  fig.canvas.draw();box=a.get_window_extent(fig.canvas.get_renderer())
  c['label_visible']=not any(box.overlaps(v) for v in boxes)
  if c['label_visible']:boxes.append(box)
  else:a.set_visible(False)
 top.annotate(f'Mediana BPM: {central:.1f}',(329,central),xytext=(0,2),textcoords='offset points',ha='right',va='bottom',fontsize=5.2,color='#555',bbox={'facecolor':'white','edgecolor':'none','pad':.5})
 for local,start in enumerate([130,146,162,178]):
  end=start+16;left,right=tt[start],tt[end];y=.655-local*.194
  ax=fig.add_axes([.08,y,.89,.115]);ax.set(xlim=(left,right),ylim=(0,1));ax.set_xticks([]);ax.set_yticks([])
  ax.text(-.015,.65,'B',transform=ax.transAxes,color=blue,ha='right',fontsize=7)
  ax.text(-.015,.35,'D',transform=ax.transAxes,color=orange,ha='right',fontsize=7)
  wi=max(2,min(start-8,len(tt)-33));bpm=float(win[wi-2]['BPM']);localbp.append(bpm)
  fig.text(.08,y+.155,f'BPM interno: {bpm:.2f} · M{33+local*4}–M{36+local*4}',fontsize=7,weight='bold')
  for i in range(start,end):
   t=tt[i];beat=(i-2)%4+1
   if beat==1:
    ax.axvline(t,c='#777',lw=.8,zorder=1);ax.text(t,1.16,f'M{(i-2)//4+1}',transform=ax.get_xaxis_transform(),fontsize=6,weight='bold')
   ax.text(t,1.02,str(beat),transform=ax.get_xaxis_transform(),fontsize=6,ha='center')
   ax.plot([t],[0],marker=2,ms=4,color='#777',clip_on=False)
   ax.text(t,-.1,f'Q{i+1}\n{int(t)//60:02}:{t%60:05.2f}',transform=ax.get_xaxis_transform(),fontsize=5.2,ha='center',va='top')
  ax.axvline(right,c='#777',lw=.8,zorder=1)
  for r in dis:
   qi=int(r['quarter_ID'][1:])-1
   if not start<=qi<end:continue
   for inst,prefix,color,width,style,z in [('Bass','B',blue,1.15,'-',2),('Drum','D',orange,1.5,(0,(2.1,1.7)),3)]:
    tx=float(r['BMIG_time_s' if inst=='Bass' else 'DMIG_time_s']);ly=.88 if inst=='Bass' else .08
    ln,=ax.plot([tx,tx],[.19,.81],c=color,lw=width,ls=style,zorder=z,clip_on=False)
    assert all(abs(v-tx)<1e-12 for v in ln.get_xdata())
    val=float(r[prefix+'_DISPLAY_ms']);lab=f'{prefix}{val:+.0f}' if abs(val)>=.5 else f'{prefix}0'
    ax.annotate(lab,(tx,ly),xytext=(2,0),textcoords='offset points',fontsize=5.5,color=color,va='center',annotation_clip=False)
    gridlog.append({'instrument':inst,'quarter':r['quarter_ID'],'native_grid_time_s':str(tx),'render_x_s':str(tx)})
  for e in ev:
   t=float(e['original_time_s']);qi=int(e['quarter_ID'][1:])-1
   # Native x preserved; display by native system interval, with leading Bass anticipation included.
   belongs=(left<=t<right) or (local==0 and t<left and qi>=130)
   if not belongs:continue
   bass=e['instrument']=='BASS';add=e['role']!='QUARTER_FIT_OBSERVATION';color=blue if bass else orange;yy=.65 if bass else .35
   sc=ax.scatter([t],[yy],marker='o' if bass else 'D',s=8 if add else 15,facecolors='white' if bass else color,edgecolors=color,linewidths=.65,alpha=.65 if add else 1,zorder=7,clip_on=False)
   assert float(sc.get_offsets()[0,0])==t
   rendered.append({**e,'system':local+1,'render_x_s':e['original_time_s'],'additional_visual':add})
 # Compact bottom legend in original legend region.
 handles=[Line2D([],[],marker='o',mfc='white',mec=blue,ls='',label='Contrabbasso'),Line2D([],[],marker='D',color=orange,ls='',label='Batteria'),Line2D([],[],color=blue,lw=1.15,label='BMIG'),Line2D([],[],color=orange,lw=1.5,ls=(0,(2.1,1.7)),label='DMIG'),Line2D([],[],color='#546875',lw=.6,label='BPM interno')]
 handles[4:4]=[Line2D([],[],ls='',label='B/D − = avanti'),Line2D([],[],ls='',label='B/D + = dietro')]
 fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.52,.023),ncol=7,fontsize=6,frameon=False,handlelength=1.4,columnspacing=1)
 fig.text(.08,.012,'BMIG = Bass Measure Internal Grid · DMIG = Drum Measure Internal Grid',fontsize=6)
 pdf.savefig(fig);fig.savefig('/private/tmp/jga_final_report_page1.png',dpi=200);plt.close(fig)
 fig=plt.figure(figsize=(210/25.4,297/25.4))
 fig.text(.08,.90,'RAPPORTO TRA CONTRABBASSO E BATTERIA',fontsize=10,weight='bold')
 fig.text(.08,.85,'\n'.join(textwrap.wrap(reader_text,width=87)),fontsize=8.2,va='top',linespacing=1.5)
 fig.text(.08,.68,bpm_text,fontsize=8.2)
 pdf.savefig(fig);fig.savefig('/private/tmp/jga_final_report_page2.png',dpi=200);plt.close(fig)
assert len(rendered)==127 and len({e['event_ID'] for e in rendered})==127
assert len(gridlog)==128
put('JGA_FINAL_REPORT.pdf',mem.getvalue());table('RENDERED_EVENTS.csv',rendered);table('RENDERED_GRIDS.csv',gridlog)
