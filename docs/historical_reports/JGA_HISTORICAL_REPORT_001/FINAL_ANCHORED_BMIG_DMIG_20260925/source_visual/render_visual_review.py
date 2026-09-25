from pathlib import Path
from decimal import Decimal as D
import csv,json,hashlib,io,sys,os,datetime,subprocess
os.environ['MPLCONFIGDIR']='/private/tmp/jga_visual_mpl'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MultipleLocator,FuncFormatter
from matplotlib.lines import Line2D
sys.path.insert(0,'tools')
from continuous_backup import atomic_write_and_backup,preflight
O=Path('docs/scientific/rfc/JGA_BMIG_DMIG_FINAL_SCORE_REVIEW_20260925');S=Path('docs/scientific/rfc/JGA_MEASURE_INTERNAL_PULSE_GRID_20260925');F=Path('docs/historical_reports/JGA_HISTORICAL_REPORT_001/FINAL_SCORE_V1');V=F.parent/'SCORE_V1_1_REVIEW/COMPLETE_POPULATION_REVIEW'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open()))
def put(n,b):atomic_write_and_backup(O/n,b.encode() if isinstance(b,str) else b)
def js(n,x):put(n,json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def table(n,rr):
 b=io.StringIO();w=csv.DictWriter(b,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr);put(n,b.getvalue())
preflight()
assert json.loads((O/'PHASE_A_VERIFICATION.json').read_text())['status']=='PASS'
for e in json.loads((S/'MANIFEST.json').read_text())['entries']:assert sha(S/e['relative_path'])==e['sha256']
g=rows(S/'MEASURE_INTERNAL_GRID_M33_M48.csv');ev=rows(S/'EVENT_PROVENANCE_127.csv');summ=json.loads((S/'MEASURE_INTERNAL_GRID_SUMMARY.json').read_text())
refs=rows(F/'METRIC_REFERENCE.csv');tt=[float(r['reference_time']) for r in refs];win=rows(F/'BPM_EVOLUTION.csv');central=json.loads((F/'PROFILE.json').read_text())['tempo']['central_bpm']
inputs=[O/'PHASE_A_VERIFICATION.json',O/'BPM_ANNOTATION_PROTOCOL.json',F/'build_score.py',F.parent/'SUMMARY.json',F.parent/'build_report.py',F.parent/'validate_report.py',S/'MANIFEST.json',S/'MEASURE_INTERNAL_GRID_M33_M48.csv',S/'MEASURE_INTERNAL_GRID_RESULTS.csv',S/'MEASURE_INTERNAL_GRID_SUMMARY.json',S/'EVENT_PROVENANCE_127.csv',F/'METRIC_REFERENCE.csv',F/'BPM_EVOLUTION.csv',F/'PROFILE.json',V/'render_saved_population.py',V/'JGA_MICROTIMING_SCORE_V1_1_REVIEW.pdf',Path('JGA_BOOTSTRAP.md')]
hashes={str(p):sha(p) for p in inputs}
assert hashes[str(V/'JGA_MICROTIMING_SCORE_V1_1_REVIEW.pdf')]=='eef9ea779eb0fe6ec7d892149d7aa2f6683be1d27e4e0a792af86580e3b0a56e'
dis=[]
for r in g:
 if r['measure_comparison_eligible']!='YES':continue
 b,d=D(r['BMIG_time_s']),D(r['DMIG_time_s']);mid=(b+d)/2;bd=(b-mid)*1000;dd=(d-mid)*1000
 assert bd==-dd and abs((bd-dd)-D(r['GRID_DELTA_ms']))<D('0.00000001')
 dis.append(dict(measure=r['measure'],beat=r['beat'],quarter_ID=r['quarter_ID'],BMIG_time_s=r['BMIG_time_s'],DMIG_time_s=r['DMIG_time_s'],GRID_DELTA_ms=r['GRID_DELTA_ms'],MIDPOINT_time_s=str(mid),B_DISPLAY_ms=str(bd),D_DISPLAY_ms=str(dd),Bass_observed_support=r['Bass_observed_support'],Drum_observed_support=r['Drum_observed_support'],Bass_grid_point_reconstructed='YES' if r['Bass_observed_support']=='NO' else 'NO',Drum_grid_point_reconstructed='YES' if r['Drum_observed_support']=='NO' else 'NO',notes='Midpoint decomposition only; not independent measurements or PLP offsets.'))
assert len(dis)==40
# Finished files are synchronously backed up before the next output.
table('DISPLAY_GRID_VALUES.csv',dis)
grammar="""# Revisione finale BMIG/DMIG — metodologia tecnica

Fase A: riproduzione esatta dello stimatore originale Theil–Sen con intercetto mediano congiunto, poi A+n*T per tutti i punti. Nessun dato modificato. Tutte le coordinate sono FITTED_MATHEMATICAL_GRID_POINT; OBSERVED_SUPPORT rimane proprietà separata. Le colonne storiche reconstructed nei CSV antecedenti significano soltanto assenza di supporto osservato, non un diverso tipo di griglia. Nessun quadrato speciale o categoria Ricostruito nel nuovo score.

Midpoint=(BMIG+DMIG)/2; B_DISPLAY=1000*(BMIG−midpoint); D_DISPLAY=1000*(DMIG−midpoint); B_DISPLAY=−D_DISPLAY; GRID_DELTA=B_DISPLAY−D_DISPLAY. Una sola quantità decomposta, non due misure indipendenti e non offset PLP. Etichette font5.5pt e marcatori15/8 punti quadrati come revisione precedente. Asse temporale e pannelli invariati. Linea Bass1.15pt continua; Drum1.5pt tratteggio2.1/1.7 sopra Bass. Nessuna separazione artificiale.

BPM interno è la nuova etichetta reader-facing dei medesimi valori BPM locali PLP salvati; NON BPM implicito di BMIG o DMIG. Linea orizzontale = mediana dei904 BPM elementari60/diff,161.49902343750287. La curva resta la serie salvata su32 intervalli, senza nuova elaborazione. Tracciabilità: build_score.py, PROFILE.json, SUMMARY.json, build_report.py, validate_report.py. Le annotazioni estremali sono display-only, definite nel protocollo salvato prima della selezione.

63 coordinate Bass preservate:17 A,27 B,19 C.19 BP approximate non sono onset fisici validati;27 Targeted Pitch CLEAR non hanno GT storico.64 Drum exclusive diagnostici, inclusa anticipazioneQ195 conservata. Nessuna superiore autorità storica attribuita dai simboli. La frase reader-facing «strettamente correlate» è descrittiva della rappresentazione, non un coefficiente di correlazione misurato o un test inferenziale. Supporto4/4:6misure,mediana1.578ms,3ahead3behind; primario>=3:10misure,8.413ms. Nessuna conclusione generale sul musicista. Assenza di GT storico, eterogeneità temporale e campione limitato restano limiti.

Formato base: A4 pagina3 dello score v1.1, stessi pannelli e geometria x. Punti BMIG/DMIG di beat1 possono anticipare visivamente una stanghetta pur appartenendo alla misura seguente; nessuna griglia attribuita alla precedente misura ineleggibile. Nessun evento spostato, ΔBD fra attacchi o inferenza audio. Nessun freeze, bootstrap, commit/push o overwrite.
"""
put('VISUAL_GRAMMAR.md',grammar)
plt.rcParams.update({'font.size':7,'axes.spines.top':False,'axes.spines.right':False,'font.family':'DejaVu Sans'})
blue='#286ea8';orange='#c66a16';rendered=[];gridlog=[];localbp=[];bpmcheck=[]
mem=io.BytesIO()
with PdfPages(mem) as pdf:
 fig=plt.figure(figsize=(210/25.4,297/25.4))
 fig.text(.07,.975,'JGA Microtiming Score · BMIG / DMIG — REVIEW',fontsize=11,weight='bold')
 fig.text(.07,.956,'Ray Brown Trio — Exactly Like You · M33–M48',fontsize=8)
 fig.text(.07,.939,'Pulsazioni interne e attacchi musicali',fontsize=8,weight='bold')
 fig.text(.07,.925,'Pulsazioni interne · valori B / D in millisecondi',fontsize=7)
 top=fig.add_axes([.08,.848,.89,.068]);line,=top.plot([float(x['center_s']) for x in win],[float(x['BPM']) for x in win],c='#546875',lw=.6);top.axhline(central,c='#999',ls='--',lw=.5);top.set(xlim=(0,330),ylabel='BPM');top.xaxis.set_major_locator(MultipleLocator(30));top.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{int(x)//60:02}:{int(x)%60:02}'));top.tick_params(labelsize=6)
 assert list(line.get_ydata())==[float(x['BPM']) for x in win]
 from scipy.signal import find_peaks
 import numpy as np
 protocol=json.loads((O/'BPM_ANNOTATION_PROTOCOL.json').read_text())
 vals=np.array([float(x['BPM']) for x in win]);times=np.array([float(x['center_s']) for x in win]);candidates=[]
 for kind,sign in [('MAX',1),('MIN',-1)]:
  idx,prop=find_peaks(vals*sign,prominence=protocol['min_prominence_BPM'])
  candidates += [{'kind':kind,'index':int(i),'time_s':float(times[i]),'BPM':float(vals[i]),'prominence_BPM':float(pr)} for i,pr in zip(idx,prop['prominences'])]
 selected=[]
 for c in sorted(candidates,key=lambda x:(-x['prominence_BPM'],x['time_s'],x['kind'])):
  if all(abs(c['time_s']-d['time_s'])>=protocol['min_separation_seconds'] for d in selected):selected.append(c)
  if len(selected)==protocol['maximum_labels']:break
 boxes=[]
 for c in selected:
  above=c['kind']=='MAX';a=top.annotate(f"{c['BPM']:.1f}",(c['time_s'],c['BPM']),xytext=(0,2 if above else -3),textcoords='offset points',ha='center',va='bottom' if above else 'top',fontsize=5.2,color='#34434b',bbox={'facecolor':'white','edgecolor':'none','pad':.15})
  fig.canvas.draw();box=a.get_window_extent(fig.canvas.get_renderer())
  c['label_visible']=not any(box.overlaps(v) for v in boxes)
  if c['label_visible']:boxes.append(box)
  else:a.set_visible(False)
 top.annotate(f'Mediana BPM: {central:.1f}',(329,central),xytext=(0,2),textcoords='offset points',ha='right',va='bottom',fontsize=5.2,color='#555',bbox={'facecolor':'white','edgecolor':'none','pad':.5})
 js('BPM_EXTREMA_ANNOTATIONS.json',{'preregistered_protocol_sha256':sha(O/'BPM_ANNOTATION_PROTOCOL.json'),'selected':selected,'central_line_definition':'Median of 904 raw inter-reference BPM = median(60/diff(reference_seconds)); not median or mean of plotted 32-quarter BPM curve.','central_BPM':central,'curve_values_unchanged':True})
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
 fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.52,.023),ncol=5,fontsize=6,frameon=False,handlelength=1.4,columnspacing=1)
 fig.text(.08,.012,'BMIG = Bass Measure Internal Grid · DMIG = Drum Measure Internal Grid',fontsize=6)
 pdf.savefig(fig);fig.savefig('/private/tmp/jga_bmig_final_page1.png',dpi=200);plt.close(fig)
 fig=plt.figure(figsize=(210/25.4,297/25.4));fig.text(.07,.955,'Lettura e limiti · BMIG / DMIG',fontsize=15,weight='bold')
 sections=[
 ('COME LEGGERE B E D',"I valori B (contrabbasso) e D (batteria) indicano la posizione\nrelativa delle rispettive pulsazioni.\n\n− = avanti\n+ = dietro\n\nLa distanza complessiva tra B e D esprime, in millisecondi, lo scarto\ntemporale tra le due pulsazioni."),
 ('RELAZIONE TRA CONTRABBASSO E BATTERIA',"Le griglie interne di contrabbasso e batteria risultano strettamente\ncorrelate nella selezione analizzata.\n\nLa mediana esprime lo scarto temporale complessivo tra le due\npulsazioni; valori negativi indicano il contrabbasso in anticipo,\nvalori positivi il contrabbasso in ritardo.\n\nNelle sei misure con supporto completo, contrabbasso e batteria\nmostrano una pulsazione interna sostanzialmente coincidente:\nla differenza mediana tra le due griglie è prossima allo zero\n(+1,6 ms), con tre misure in anticipo e tre in ritardo.\n\nEstendendo l’analisi alle dieci misure ricostruibili con almeno tre\nquarti osservati per strumento, su sedici analizzate, la mediana è\n+8,4 ms. Questi valori descrivono la selezione, non una caratteristica\ngenerale del modo di suonare di Ray Brown."),
 ('GLI EVENTI MUSICALI',"Gli attacchi di contrabbasso e batteria costituiscono la base per la\nricostruzione delle rispettive pulsazioni interne.\n\nGli eventi aggiuntivi vengono conservati nel grafico, ma non\nmodificano la scansione dei quattro quarti utilizzata per ricostruire\nla pulsazione della misura."),
 ('CONTINUITÀ DELL’ANALISI',"La griglia viene rappresentata soltanto nelle misure in cui gli\neventi disponibili consentono di ricostruire con sufficiente chiarezza\nla pulsazione dei due strumenti.\n\nNelle altre misure gli attacchi rimangono visibili, senza attribuire\nuna relazione temporale non sufficientemente sostenuta dai dati.")]
 y=.90
 for title,txt in sections:
  fig.text(.08,y,title,fontsize=9.5,weight='bold');y-=.024
  fig.text(.08,y,txt,fontsize=8.2,va='top',linespacing=1.35);y-=.0144*len(txt.splitlines())+.032
 fig.text(.08,.07,"L’analisi descrive il rapporto temporale tra le pulsazioni di\ncontrabbasso e batteria e le oscillazioni degli attacchi intorno ad esse.",fontsize=8.2,linespacing=1.4)
 fig.text(.92,.019,'2/2',fontsize=7,ha='right')
 pdf.savefig(fig);fig.savefig('/private/tmp/jga_bmig_final_page2.png',dpi=160);plt.close(fig)
assert len(rendered)==127 and len({e['event_ID'] for e in rendered})==127
assert len(gridlog)==80
put('JGA_BMIG_DMIG_FINAL_SCORE_REVIEW.pdf',mem.getvalue());table('RENDERED_EVENTS.csv',rendered);table('RENDERED_GRIDS.csv',gridlog)
for p,h in hashes.items():assert sha(Path(p))==h
js('REPORT_PROVENANCE.json',{'timestamp_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'git_HEAD':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'input_hashes':hashes,'visual_authority_page':3,'scientific_data_recomputed':False,'display_only_midpoint_arithmetic':True,'fits_rerun':False,'global_BPM_panel_same_data_axes_and_styles':True,'local_BPM_saved_values':localbp,'events_rendered':127,'grid_lines':80,'eligible_quarters':40,'ineligible_measures':summ['ineligible_measures'],'source_manifest_verified':True,'no_freeze':True})
put('RESULT.md',"# Revisione finale BMIG/DMIG\n\nFase A PASS: normalizzazione esclusivamente semantica/visiva; zero coordinate, eleggibilità o valori scientifici cambiati.10misure eleggibili; mediana primaria+8.412698412698205ms,completa4/4+1.5783824640962507ms, identiche alle autorità.\n\nFase B: A4, quattro sistemi da quattro misure, coordinate e dimensioni conservate. Tutti i punti di griglia sono matematici; nessun quadrato selettivo. BPM interno sostituisce la sola dicitura, annotazioni estremali preregistrate e linea Mediana BPM161.5 identificata da autorità. Pagina2 musicologica secondo PI.127eventi originali,80linee griglia,40coppie di display. Nessun ΔBD fra eventi.\n\nVedere PHASE_A_VERIFICATION.json e VISUAL_GRAMMAR.md per definizioni e limiti; no freeze, commit, push, bootstrap, modifica delle autorità. STOP per PI review.\n")
put('render_visual_review.py',Path(__file__).read_bytes())
print('CREATED',len(dis),'display rows;',len(rendered),'events; local BPM',localbp)
