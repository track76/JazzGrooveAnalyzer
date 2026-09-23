from pathlib import Path
import json,csv,hashlib,os,math,statistics
from decimal import Decimal as D
os.environ['MPLCONFIGDIR']='/private/tmp/jga_final_mpl'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D
O=Path(__file__).resolve().parent;P=O.parent;R=P.parents[2]
def rows(p):return list(csv.DictReader(p.open()))
def put(n,x):(O/n).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def table(n,x):
 with (O/n).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(x[0]),lineterminator='\n');w.writeheader();w.writerows(x)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((P/'REPORT_FREEZE.json').read_text())
# Historical mutable authority snapshots are checked before any authorized state update.
for n,h in old['files'].items():
 if n.startswith('docs/historical_reports/JGA_HISTORICAL_REPORT_001/') or n.endswith('HISTORICAL_REPORT_TEMPLATE_V1.md'):assert sha(R/n)==h,n
s=json.loads((P/'SUMMARY.json').read_text());assert sha(Path(s['source']['path']))==s['source']['sha256']
refs=rows(P/'data/global__PLP_REFERENCE.csv');ev=rows(P/'data/global__ALL_EVENT_ROLES.csv');a=rows(P/'data/source__SOURCE_CONDITIONED_ASSIGNMENTS.csv');times=[D(x['time_seconds']) for x in refs];assert str(times[2])=='0.8126984126984127';assert round(times[2],9)==D('0.812698413')
metric=[dict(quarter_id=i,quarter_label=f'Q{i+1}',reference_time=str(t),metric_beat=(i-2)%4+1 if i>=2 else '',measure_id=f'M{(i-2)//4+1}' if i>=2 else '',status='VALIDATED_PI_ORIGIN_PROPAGATED' if i>=2 else 'PRE_ANCHOR_UNNUMBERED') for i,t in enumerate(times)];table('METRIC_REFERENCE.csv',metric)
win=[dict(start_index=i,end_index=i+32,start_Q=f'Q{i+1}',end_Q=f'Q{i+33}',start_s=str(times[i]),end_s=str(times[i+32]),center_s=str((times[i]+times[i+32])/2),intervals=32,BPM=float(D(1920)/(times[i+32]-times[i]))) for i in range(2,len(times)-32)];table('BPM_EVOLUTION.csv',win)
central=s['central_internal_bpm']['value'];tempo={'start':win[0],'end':win[-1],'central_bpm':central,'change_bpm':win[-1]['BPM']-win[0]['BPM'],'change_percent':100*(win[-1]['BPM']/win[0]['BPM']-1),'definition':'32 complete intervals / 33 references; 1920 / elapsed seconds; sliding stride one quarter starting Q3; center timestamp; joined observations, no smoothing. Central remains original median of 904 raw interval BPM.'}
obs=[];pairs=[]
for x in a:
 if x['status'] not in ['SHARED_DUAL_MARKER','SAME_TIMESTAMP_UNRESOLVED']:
  for k in ['BASS','DRUM']:
   if x[k+'_id']:obs.append(dict(source=k,quarter_id=int(x['quarter_id']),event_id=x[k+'_id'],timestamp=x[k+'_timestamp'],offset_ms=x[k+'_offset_ms'],original_state=x[k+'_state']))
 if x['status']=='DISTINCT_PAIR':
  i=int(x['quarter_id']);pairs.append(dict(pair_id=f'P{len(pairs)+1:02}',quarter_id=i,quarter_label=f'Q{i+1}',measure_id=metric[i]['measure_id'],metric_beat=metric[i]['metric_beat'],reference_time=x['quarter_timestamp'],bass_event_id=x['BASS_id'],drum_event_id=x['DRUM_id'],bass_time=x['BASS_timestamp'],drum_time=x['DRUM_timestamp'],bass_delta_ms=x['BASS_offset_ms'],drum_delta_ms=x['DRUM_offset_ms'],drum_minus_bass_ms=x['DRUM_MINUS_BASS_MS'],absolute_separation_ms=str(abs(D(x['DRUM_MINUS_BASS_MS']))),absolute_samples=abs(round(D(x['DRUM_timestamp'])*22050)-round(D(x['BASS_timestamp'])*22050)),provenance='Frozen DISTINCT_PAIR; native full-mix coordinates; source support may remain Dual',annotation_flag=False,annotation_note=''))
assert len(pairs)==21
# Stable chronological IDs exactly reproduce preserved 21-pair sequence.
prior=O/'ORIGINAL_PAIRS.csv'
if prior.exists():
 for x,y in zip(pairs,rows(prior)):
  assert x['pair_id']==y['pair_id'] and x['bass_event_id']==y['bass_native_event_id'] and x['drum_event_id']==y['drum_native_event_id'] and x['drum_minus_bass_ms']==y['drum_minus_bass_ms']
table('MICROTIMING_PAIRS.csv',pairs);table('PRIMARY_OBSERVATIONS.csv',obs)
def stats(v):
 v=[float(x) for x in v];n=len(v)
 return dict(N=n,median_ms=statistics.median(v) if n else None,mean_ms=statistics.mean(v) if n else None,before=sum(x<0 for x in v),after=sum(x>0 for x in v),exact=sum(x==0 for x in v),before_pct=100*sum(x<0 for x in v)/n if n else None,after_pct=100*sum(x>0 for x in v)/n if n else None,exact_pct=100*sum(x==0 for x in v)/n if n else None)
primary={k:stats([x['offset_ms'] for x in obs if x['source']==k]) for k in ['BASS','DRUM']};primary['PAIR']=stats([x['drum_minus_bass_ms'] for x in pairs]);assert primary['BASS']['N']==23 and primary['DRUM']['N']==654
beats=[]
for b in range(1,5):
 row={'beat':b,'qualification':'DESCRIPTIVE ONLY; report N; no significance threshold'}
 for k in ['BASS','DRUM']:
  for key,val in stats([x['offset_ms'] for x in obs if x['source']==k and metric[x['quarter_id']]['metric_beat']==b]).items():row[k+'_'+key]=val
 for key,val in stats([x['drum_minus_bass_ms'] for x in pairs if x['metric_beat']==b]).items():row['PAIR_'+key]=val
 beats.append(row)
table('BEAT_MICROTIMING.csv',beats)
low=min(x['absolute_samples'] for x in pairs);high=max(x['absolute_samples'] for x in pairs);mins=[x['pair_id'] for x in pairs if x['absolute_samples']==low];maxs=[x['pair_id'] for x in pairs if x['absolute_samples']==high];assert mins==['P12','P13','P21'] and maxs==['P05','P14']
put('PROFILE.json',dict(tempo=tempo,primary=primary,beats=beats,minimum_pair_ids=mins,maximum_pair_ids=maxs,metric_anchor={'PI_text_seconds':'0.812698413','preserved_exact_seconds':str(times[2]),'quarter':'Q3','measure':'M1','beat':1,'provenance':'PI_METRIC_ANCHOR — explicit final approval, 2026-09-23'},quarters=905,complete_measures=225,final_partial_measure='M226 beats 1–3',pre_anchor=['Q1','Q2'],methodology_changed=False))
styles={'BASS_SUPPORTED':('#286ea8','o'),'DRUM_SUPPORTED':('#c66a16','D'),'BASS_AND_DRUM_SUPPORTED':('#bfc3c7','s'),'UNKNOWN':('#bfc3c7','^'),'CONFLICTING_EVIDENCE':('#bfc3c7','X')};selected={x['event_id'] for x in obs};rowrecords=[];page_records=[]
plt.rcParams.update({'font.size':7,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(8.27,2.6));ax.plot([float(x['center_s']) for x in win],[x['BPM'] for x in win],'-',color='#546875',lw=.8,marker='.',ms=1);ax.axhline(central,color='#999',ls='--',lw=.7);ax.set(xlabel='Recording time (s)',ylabel='BPM',title='PLP 32-quarter elapsed-span tempo · dashed: frozen central statistic');fig.tight_layout();fig.savefig(O/'BPM_EVOLUTION.png',dpi=180);plt.close(fig)
def fmt(t):return f'{int(t)//60:02}:{float(t)%60:05.2f}'
starts=list(range(2,len(times),16))
with PdfPages(O/'JGA_MICROTIMING_SCORE.pdf') as pdf:
 for page in range(math.ceil(len(starts)/4)):
  fig=plt.figure(figsize=(8.2677165354,11.692913386));fig.text(.07,.976,f'JGA MICROTIMING SCORE · Report 001 · {page+1}/15',fontsize=11,weight='bold');fig.text(.07,.955,'Ray Brown Trio — Exactly Like You · 4/4 · observable onset timing',fontsize=8)
  fig.text(.07,.938,f"Tempo {win[0]['BPM']:.2f} → {win[-1]['BPM']:.2f} BPM | central {central:.2f} | change {tempo['change_bpm']:+.2f} ({tempo['change_percent']:+.2f}%)",fontsize=7)
  top=fig.add_axes([.08,.848,.89,.068]);top.plot([float(x['center_s']) for x in win],[x['BPM'] for x in win],color='#546875',lw=.6,marker='.',ms=.7);top.axhline(central,c='#999',ls='--',lw=.5);top.set(xlim=(0,330),ylabel='BPM');top.tick_params(labelsize=6);top.set_xlabel('Recording time (s) · 32-quarter span',fontsize=6,labelpad=1)
  ids_on_page=[]
  for local,start in enumerate(starts[page*4:page*4+4]):
   end=min(start+16,len(times));included=list(range(start,end));qids=([0,1]+included) if start==2 else included
   left=0 if start==2 else float((times[start-1]+times[start])/2);right=330 if end==len(times) else float((times[end-1]+times[end])/2)
   y=.655-local*.194;ax=fig.add_axes([.08,y,.89,.115]);ax.set(xlim=(left,right),ylim=(-210,300),ylabel='Δt (ms)');ax.tick_params(axis='y',labelsize=6);ax.set_xticks([]);ax.axhline(0,c='#555',lw=.6);ax.grid(axis='y',alpha=.15)
   wi=max(2,min(start-8,len(times)-33));w=win[wi-2];m1=(start-2)//4+1;m2=(end-3)//4+1
   fig.text(.08,y+.155,f"Local BPM: {w['BPM']:.2f} · M{m1}–M{m2}"+(' · Q1–Q2 before validated origin' if start==2 else '')+(' · M226 incomplete' if end==len(times) else ''),fontsize=7,weight='bold')
   for i in qids:
    t=float(times[i]);b=metric[i]['metric_beat'];ax.axvline(t,c='#555' if b==1 else '#aaa',lw=1 if b==1 else .35,alpha=.85 if b==1 else .5)
    ax.text(t,1.02,str(b) if b else '—',transform=ax.get_xaxis_transform(),ha='center',fontsize=6)
    if b==1:ax.text(t,1.16,metric[i]['measure_id'],transform=ax.get_xaxis_transform(),ha='left',fontsize=6,weight='bold')
    ax.text(t,-.10,f'Q{i+1}\n{fmt(times[i])}',transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=5.2)
   rr=[x for x in ev if int(x['quarter_id']) in qids];ids_on_page.extend(x['JGA_EVENT_ID'] for x in rr)
   for x in rr:
    state=x['source_state'];col,mark=styles[state];active=x['JGA_EVENT_ID'] in selected and state in ['BASS_SUPPORTED','DRUM_SUPPORTED'];col=col if active else '#bfc3c7';tx=float(x['native_timestamp']);dy=float(x['EVENT_TO_CELL_QUARTER_MS']);ax.scatter(tx,dy,s=14 if active else 8,marker=mark,facecolors='none' if mark=='o' else col,edgecolors=col,linewidths=.6,zorder=4 if active else 2)
    if active:ax.annotate(f'{dy:+.0f}',(tx,dy),xytext=(0,6),textcoords='offset points',ha='center',fontsize=5.7,color=col)
   for p in pairs:
    if p['quarter_id'] not in qids:continue
    xx=[float(p['bass_time']),float(p['drum_time'])];yy=[float(p['bass_delta_ms']),float(p['drum_delta_ms'])];ax.plot(xx,yy,c='#777',lw=.45,zorder=1);label=p['pair_id']+(' MIN' if p['pair_id'] in mins else ' MAX' if p['pair_id'] in maxs else '')+f"\nD−B {float(p['drum_minus_bass_ms']):+.0f}";ax.annotate(label,(sum(xx)/2,max(yy)),xytext=(0,18),textcoords='offset points',ha='center',fontsize=5.5,color='#444')
   rowrecords.append(dict(page=page+1,measure_start=m1,measure_end=m2,quarter_ids=qids,local_bpm_window_start=w['start_Q'],local_bpm_window_end=w['end_Q'],local_bpm=w['BPM'],events=len(rr)))
  handles=[Line2D([],[],marker='o',mfc='none',mec='#286ea8',ls='',label='Bass selected'),Line2D([],[],marker='D',color='#c66a16',ls='',label='Drum selected'),Line2D([],[],marker='s',color='#bfc3c7',ls='',label='Dual unresolved'),Line2D([],[],marker='^',color='#bfc3c7',ls='',label='Unknown / context')]
  fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.023),ncol=4,fontsize=6,frameon=False);fig.text(.08,.018,'0 ms = PLP reference · + after / − before · gray retains source shape · no physical gesture claim',fontsize=6)
  pdf.savefig(fig);fig.savefig(O/f'SCORE_PAGE_{page+1:02}.png',dpi=180);plt.close(fig);page_records.append({'page':page+1,'event_ids':ids_on_page})
assert len([x for p in page_records for x in p['event_ids']])==1606
assert len(set(x for p in page_records for x in p['event_ids']))==1606
put('PAGE_LINEAGE.json',rowrecords);put('PAGE_EVENTS.json',page_records)
put('VALIDATION.json',dict(data='PASS',source=True,quarters_unchanged=True,source_states_unchanged=True,native_events=1606,each_native_event_plotted_once=True,pairs=21,visual='PENDING',pages=15))
print(json.dumps({'tempo':tempo,'beats':beats},indent=2))
