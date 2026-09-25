from pathlib import Path
import sys,json,csv,io,hashlib,datetime,subprocess
import numpy as np
sys.path.insert(0,'tools')
from continuous_backup import preflight,atomic_write_and_backup
O=Path('docs/scientific/rfc/JGA_FINAL_REPORT_CANDIDATE_20260925');S=Path('docs/scientific/rfc/JGA_MEASURE_INTERNAL_PULSE_GRID_20260925');C=Path('docs/scientific/rfc/JGA_CONTINUOUS_BMIG_DMIG_16_MEASURES_20260925');V=Path('docs/scientific/rfc/JGA_BMIG_DMIG_FINAL_SCORE_REVIEW_20260925');F=Path('docs/historical_reports/JGA_HISTORICAL_REPORT_001/FINAL_SCORE_V1')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open()))
def put(n,b):atomic_write_and_backup(O/n,b.encode() if isinstance(b,str) else b)
def js(n,x):put(n,json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def table(n,rr):
 s=io.StringIO();w=csv.DictWriter(s,fieldnames=rr[0]);w.writeheader();w.writerows(rr);put(n,s.getvalue())
preflight();assert not O.exists()
for root in [S,C,V]:
 for e in json.loads((root/'MANIFEST.json').read_text())['entries']:assert sha(root/e['relative_path'])==e['sha256']
protocol='''# Final anchored BMIG / DMIG — prospective candidate protocol

New candidate only, no canonical adoption. Recorded before new grid estimation and before any new cross-instrument differences. Previous results exposed, no investigator blindness. No selection/tuning against old+1.578ms or desired ahead/behind.

Use exactly the frozen same-instrument QUARTER_FIT_OBSERVATION representative at each Q131–Q194 from EVENT_PROVENANCE_127.csv. All additional63Bass/64Drum population events preserved; not additional grid slots. Q195 context preserved but not fitted. No new event/quarter selection. Same algorithm for each instrument, only own n=0..63 and own observed times enter.

Model: soft quarter anchors plus local quarter-duration continuity. Minimize
J(g) = sum_(observed n) (g_n−t_n)^2 + (1/16) sum_(n=1..62) (g_(n−1)−2g_n+g_(n+1))^2.
No equality g_n=t_n, no observation deletion, no robust downweighting of eligible anchors, no external instrument or PLP times. All eligible anchors have equal coefficient1; quarter is reconstruction unit. Additional-event identity/timestamps never changed. No whole-measure eligibility gate.

Why1/16: fixed prospectively to privilege local data. The local continuity stencil has interior diagonal6/16=0.375 and total absolute off-diagonal10/16=0.625, both below the unit data term at an observed slot. Thus anchored normal-equation rows are strictly diagonally dominant with gap1−4/16=0.75. This is a modeling preference, not validated physical calibration or an acceptance threshold. No tuning or sensitivity-based model selection in this task. Continuity couples only adjacent quarter durations, not a globally imposed line or BPM. It may retain local timing fluctuations; every duration and duration-change reported.

Let W have diagonal1 at observed slots and0 elsewhere, D2 be62×64 second-difference operator. Solve (W+(1/16)D2.T D2)g=W t. For conditioning subtract same-instrument median(t) before solution and add back afterward. Matrix positive definite with>=2 distinct observed slots. Missing slots follow the same coupled minimizer, not delta interpolation. Boundary: no exterior evidence, no reflected/synthetic points; natural finite-domain second-difference penalty. Isolated sparse measures are not fitted separately. No measure-boundary reset. Stop if numerical solve fails or any of63 intervals<=0; do not repair/tune after seeing results.

Write/hash own-only input and each independently estimated grid before comparison. Pure solver signature (n,t), no other data. Programmatically test counterpart-input perturbation invariance, verify normal equations, and verify all original event strings preserved. Model does not force strict monotonicity by moving outputs: monotonicity is an integrity gate on its actual solution.

After both output hashes saved: GRID_DELTA=BMIG−DMIG, negativeBass ahead. Each measure contributes median of four deltas, global=median16measure medians. Recalculate six frozen4/4 measures separately. Compare all prior existing grids per instrument (not only mutually eligible), plus previous common10measure subset and continuous Huber trial. No ms acceptance/materiality thresholds. A nonreproduced+1.6ms reader-facing value cannot be printed as current data. If the new result does not support the approved exact paragraph, STOP before candidate-report generation as explicitly required by the conclusion gate. Never tune to pass the paragraph.

Display-only midpoint decomposition retained, no scientific coordinate changes. BPM start/end: select first/last saved local_bpm row of global__PLP_REFERENCE.csv whose native time lies in [Q131,Q195); no mean/block/curve substitution or BPM recomputation. Frozen global32-quarter curve and approved extrema remain distinct saved display authority. 161.49902343750287 reference is median904elementary interval BPM.

No audio inference, canonical score change, freeze, bootstrap, commit/push. Software requirement record only: [TUTTO IL BRANO] or [DA MM:SS.xx]→[A MM:SS.xx]; subsequent analysis/report respects selected interval. No GUI implementation.
'''
put('FINAL_ANCHORED_GRID_PROTOCOL.md',protocol);js('PREREGISTRATION_RECEIPT.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'protocol_sha256':sha(O/'FINAL_ANCHORED_GRID_PROTOCOL.md'),'new_grid_delta_not_computed':True})
ev=rows(S/'EVENT_PROVENANCE_127.csv');oldg=rows(S/'MEASURE_INTERNAL_GRID_M33_M48.csv');oldr=rows(S/'MEASURE_INTERNAL_GRID_RESULTS.csv');cont=rows(C/'CONTINUOUS_BMIG_DMIG_Q131_Q194.csv');refs=rows(F/'METRIC_REFERENCE.csv')
put('EVENT_PROVENANCE_127.csv',(S/'EVENT_PROVENANCE_127.csv').read_bytes())
inputs=[S/'MANIFEST.json',C/'MANIFEST.json',V/'MANIFEST.json',S/'EVENT_PROVENANCE_127.csv',S/'MEASURE_INTERNAL_GRID_M33_M48.csv',S/'MEASURE_INTERNAL_GRID_RESULTS.csv',C/'CONTINUOUS_BMIG_DMIG_Q131_Q194.csv',V/'JGA_BMIG_DMIG_FINAL_SCORE_REVIEW.pdf',F/'METRIC_REFERENCE.csv',F.parent/'data/global__PLP_REFERENCE.csv',Path('JGA_BOOTSTRAP.md')];hashes={str(p):sha(p) for p in inputs}
def solve(n,t):
 n=np.array(n,int);t=np.array(t,float);d=np.diff(np.eye(64),n=2,axis=0);w=np.zeros(64);w[n]=1;origin=float(np.median(t));y=np.zeros(64);y[n]=t-origin;M=np.diag(w)+d.T@d/16;z=np.linalg.solve(M,y);g=z+origin
 assert np.all(np.isfinite(g)) and np.all(np.diff(g)>0),'STOP: nonmonotonic or nonfinite anchored reconstruction'
 assert max(abs(M@z-y))<1e-10
 return g
ind={};owninputs={};instrument_tables={}
for inst,key in [('BASS','BMIG'),('DRUM','DMIG')]:
 own=[e for e in ev if e['instrument']==inst];a=[e for e in own if e['role']=='QUARTER_FIT_OBSERVATION' and 131<=int(e['quarter_ID'][1:])<=194];a.sort(key=lambda e:int(e['quarter_ID'][1:]));n=[int(e['quarter_ID'][1:])-131 for e in a];t=[e['original_time_s'] for e in a]
 owninputs[inst]={'n':n,'t':t};js(inst+'_OWN_ONLY_INPUT.json',owninputs[inst]);g=solve(n,t);ind[inst]=g;rr=[]
 for i in range(64):
  q=f'Q{131+i}';a0=next((e for e in a if e['quarter_ID']==q),None);add=[e['event_ID'] for e in own if e['quarter_ID']==q and e['role']!='QUARTER_FIT_OBSERVATION']
  rr.append({'quarter_ID':q,'measure':f'M{33+i//4}','beat':i%4+1,key+'_time_s':float(g[i]),inst+'_anchor_yes_no':'YES' if a0 else 'NO',inst+'_anchor_event_ID':a0['event_ID'] if a0 else '',inst+'_anchor_time_s':a0['original_time_s'] if a0 else '', 'additional_'+inst+'_event_IDs':'|'.join(add),key+'_minus_anchor_ms':(g[i]-float(a0['original_time_s']))*1000 if a0 else '', 'support_context':'DIRECT_SOFT_ANCHOR' if a0 else ('ONE_SIDED_BOUNDARY' if i<min(n) or i>max(n) else 'SAME_INSTRUMENT_BRIDGE')})
 instrument_tables[inst]=rr;table(inst+'_INDEPENDENT_ANCHORED_GRID.csv',rr)
js('INDEPENDENT_GRID_RECEIPT.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Bass_sha256':sha(O/'BASS_INDEPENDENT_ANCHORED_GRID.csv'),'Drum_sha256':sha(O/'DRUM_INDEPENDENT_ANCHORED_GRID.csv'),'cross_comparison_not_yet_computed':True})
# Verify own-only signature and counterpart perturbation cannot affect solver output.
for inst in ['BASS','DRUM']:
 other='DRUM' if inst=='BASS' else 'BASS';perturbed={k:dict(v) for k,v in owninputs.items()};perturbed[other]={'n':[0,63],'t':['1000','2000']};assert np.array_equal(solve(**perturbed[inst]),ind[inst])
grid=[];audit=[];intervals=[];comparison=[];contcomparison=[];measures=[];six=[]
for i in range(64):
 b,d=ind['BASS'][i],ind['DRUM'][i];half=(b-d)*500;row={'quarter_ID':f'Q{131+i}','measure':f'M{33+i//4}','beat':i%4+1,'PLP_time_s':oldg[i]['PLP_time_s'],'BMIG_time_s':b,'DMIG_time_s':d,'GRID_DELTA_ms':(b-d)*1000,'MIDPOINT_time_s':(b+d)/2,'B_DISPLAY_ms':half,'D_DISPLAY_ms':-half}
 assert row['B_DISPLAY_ms']==-row['D_DISPLAY_ms'] and row['GRID_DELTA_ms']==row['B_DISPLAY_ms']-row['D_DISPLAY_ms'];grid.append(row)
 mixed={'quarter_ID':row['quarter_ID'],'measure':row['measure'],'beat':row['beat'],'BMIG_present':'YES','DMIG_present':'YES','whole_measure_blanking':'NO'}
 for inst,key in [('BASS','BMIG'),('DRUM','DMIG')]:
  x=instrument_tables[inst][i];present=x[inst+'_anchor_yes_no'];mixed[inst+'_anchor_present']=present;mixed[inst+'_anchor_event_ID']=x[inst+'_anchor_event_ID'];mixed[inst+'_anchor_time_s']=x[inst+'_anchor_time_s'];mixed[inst+'_onset_preserved']='YES' if present=='YES' else 'NOT_PRESENT';mixed[inst+'_additional_event_IDs']=x['additional_'+inst+'_event_IDs'];mixed[inst+'_residual_ms']=-x[key+'_minus_anchor_ms'] if present=='YES' else '';mixed[inst+'_support_context']=x['support_context']
  if oldg[i][key+'_time_s']:
   change=(ind[inst][i]-float(oldg[i][key+'_time_s']))*1000;comparison.append({'instrument':inst,'quarter_ID':row['quarter_ID'],'measure':row['measure'],'old_s':oldg[i][key+'_time_s'],'new_s':ind[inst][i],'signed_change_ms':change,'absolute_change_ms':abs(change),'old_common10':oldg[i]['measure_comparison_eligible']})
  contcomparison.append({'instrument':inst,'quarter_ID':row['quarter_ID'],'continuous_s':cont[i][key+'_time_s'],'anchored_s':ind[inst][i],'signed_change_ms':(ind[inst][i]-float(cont[i][key+'_time_s']))*1000})
 audit.append(mixed)
for inst in ['BASS','DRUM']:
 dt=np.diff(ind[inst])*1000
 for i,v in enumerate(dt):intervals.append({'instrument':inst,'from_quarter':f'Q{131+i}','to_quarter':f'Q{132+i}','duration_ms':v,'implied_BPM':60000/v,'change_from_previous_duration_ms':v-dt[i-1] if i else ''})
for k,r in enumerate(oldr):
 med=float(np.median([x['GRID_DELTA_ms'] for x in grid[4*k:4*k+4]]));measures.append({'measure':r['measure'],'measure_grid_delta_ms':med})
 if r['Bass_observed_N']==r['Drum_observed_N']=='4':six.append({'measure':r['measure'],'old_measure_delta_ms':float(r['MEASURE_GRID_DELTA_ms']),'anchored_measure_delta_ms':med,'signed_change_ms':med-float(r['MEASURE_GRID_DELTA_ms'])})
summary={'model':'Quarter soft anchors with local second-difference penalty lambda=1/16; fixed before results','BMIG_coverage':64,'DMIG_coverage':64,'measures_each':16,'integrity_gate':'PASS','independence_counterpart_perturbation_test':'PASS','instruments':{},'comparison_all_existing_old_grids':{},'comparison_previous_common10':{}}
def change_stats(rr):
 v=np.array([x['signed_change_ms'] for x in rr]);a=abs(v);q1,q3=np.quantile(a,[.25,.75]);mx=max(rr,key=lambda x:x['absolute_change_ms']);return {'N':len(v),'median_signed_ms':float(np.median(v)),'median_absolute_ms':float(np.median(a)),'Q1_absolute_ms':float(q1),'Q3_absolute_ms':float(q3),'max_absolute_ms':float(max(a)),'max_measure':mx['measure'],'max_quarter':mx['quarter_ID']}
for inst in ['BASS','DRUM']:
 n=owninputs[inst]['n'];t=np.array(owninputs[inst]['t'],float);res=(t-ind[inst][n])*1000;dt=np.diff(ind[inst])*1000
 summary['instruments'][inst]={'anchors':len(n),'median_signed_residual_ms':float(np.median(res)),'median_absolute_residual_ms':float(np.median(abs(res))),'MAD_ms':float(np.median(abs(res-np.median(res)))),'max_absolute_residual_ms':float(max(abs(res))),'min_quarter_ms':float(min(dt)),'median_quarter_ms':float(np.median(dt)),'max_quarter_ms':float(max(dt)),'implied_BPM_min':float(60000/max(dt)),'implied_BPM_max':float(60000/min(dt)),'max_duration_change_ms':float(max(abs(np.diff(dt)))),'strictly_increasing':True}
 summary['comparison_all_existing_old_grids'][inst]=change_stats([x for x in comparison if x['instrument']==inst]);summary['comparison_previous_common10'][inst]=change_stats([x for x in comparison if x['instrument']==inst and x['old_common10']=='YES'])
oldmedian=float(np.median([x['old_measure_delta_ms'] for x in six]));newmedian=float(np.median([x['anchored_measure_delta_ms'] for x in six]));values=[x['measure_grid_delta_ms'] for x in measures]
summary['six_complete']={'N':6,'old_median_ms':oldmedian,'anchored_median_ms':newmedian,'signed_change_ms':newmedian-oldmedian,'Bass_ahead':sum(x['anchored_measure_delta_ms']<0 for x in six),'Bass_behind':sum(x['anchored_measure_delta_ms']>0 for x in six),'exact':sum(x['anchored_measure_delta_ms']==0 for x in six)}
summary['all16']={'median_ms':float(np.median(values)),'Bass_ahead':sum(x<0 for x in values),'Bass_behind':sum(x>0 for x in values),'exact':sum(x==0 for x in values)}
for name,rr in [('FINAL_ANCHORED_BMIG_DMIG.csv',grid),('FINAL_ANCHOR_AUDIT.csv',audit),('FINAL_GRID_COMPARISON.csv',comparison),('CONTINUOUS_TRIAL_COMPARISON.csv',contcomparison),('CONTINUITY_AUDIT.csv',intervals),('MEASURE_RESULTS.csv',measures),('CLEAN_SIX_SUBSET.csv',six)]:table(name,rr)
raw=rows(F.parent/'data/global__PLP_REFERENCE.csv');start=float(refs[130]['reference_time']);end=float(refs[194]['reference_time']);bp=[x for x in raw if start<=float(x['time_seconds'])<end];first,last=bp[0],bp[-1];v1=float(first['local_bpm']);v2=float(last['local_bpm']);delta=v2-v1
phrase=f'BPM interno: {v1:.2f} → {v2:.2f} · '+(f'aumento +{delta:.2f} BPM' if delta>0 else f'diminuzione {delta:.2f} BPM' if delta<0 else 'invariato')
js('FINAL_BPM_SUMMARY.json',{'source':str(F.parent/'data/global__PLP_REFERENCE.csv'),'field':'local_bpm','selection':'native rows with time_seconds in [Q131,Q195)','start_s':start,'end_exclusive_s':end,'first_native_row':first,'last_native_row':last,'first_BPM':v1,'last_BPM':v2,'delta_BPM':delta,'reader_text':phrase,'global_median_BPM':161.49902343750287,'global_median_definition':'median904elementaryintervalBPM','rolling32interval_BPM_not_substituted':True})
js('FINAL_GRID_SUMMARY.json',summary)
for p,h in hashes.items():assert sha(Path(p))==h
js('REPORT_PROVENANCE.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'git_HEAD':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'input_hashes':hashes,'protocol_sha256':sha(O/'FINAL_ANCHORED_GRID_PROTOCOL.md'),'independent_receipt':'INDEPENDENT_GRID_RECEIPT.json','all_observed_strings_preserved':True,'new_audio_inference':False,'no_final_authority_promotion':True})
put('build_anchored_candidate.py',Path(__file__).read_bytes());print(json.dumps(summary,indent=2));print(phrase)
