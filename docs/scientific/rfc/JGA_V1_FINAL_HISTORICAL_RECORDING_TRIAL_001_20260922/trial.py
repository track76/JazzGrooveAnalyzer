"""Frozen-evidence historical-recording trial; no inference or audio modification."""
import os
os.environ['MPLCONFIGDIR']='/private/tmp/jga_final_historical_trial_mpl'
import sys,json,csv,hashlib,datetime,subprocess,shutil
from pathlib import Path
from collections import Counter
import numpy as np

O=Path(__file__).resolve().parent; R=O.parent
W=R/'JGA_WHOLE_TRACK_GROOVE_FROZEN_PIPELINE_001_20260921'
P=R/'JGA_NATIVE_TEMPO_AUTHORITY_001_20260922/COHORT_1/B3_PLP'
T=R/'JGA_SOURCE_ASSOCIATED_ATTACK_TIMING_CALIBRATION_001_20260921'
F=R/'JGA_FIRST_COMPLETE_MUSICOLOGICAL_PERFORMANCE_ANALYSIS_001_20260922'
SOURCE=Path('/Volumes/SSD Track/JGA/downloads/Ray Brown Trio - Exactly Like You.m4a')
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(Path(p).read_text())
def rows(p):return list(csv.DictReader(Path(p).open()))
def put(n,x):
 with (O/n).open('x') as f:json.dump(x,f,indent=2,allow_nan=False);f.write('\n')
def doc(n,s):
 with (O/n).open('x') as f:f.write(s)
def table(n,rr):
 keys=list(dict.fromkeys(k for r in rr for k in r))
 with (O/n).open('x',newline='') as f:w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rr)
def verify(d):
 bad=[str(p) for p,h in d.items() if not Path(p).is_file() or sha(p)!=h]
 assert not bad,repr(bad)
def freeze(n,files):put(n,{'utc':now(),'files':{str(p.relative_to(O)):sha(p) for p in files}})
def prepare():
 assert sha(SOURCE)=='aec97cfb67096bd6a7c3d432f025523d1269b6b261e2dd6bc01a33c045acac45'
 assert sha(P/'OUTPUT_FREEZE.json')=='4384911f6086ba8a1a6f9deaa8370ae9ba22f6339ae42b3b0b4a015204efa7ac'
 verify({P/k:v for k,v in load(P/'OUTPUT_FREEZE.json')['files'].items()})
 for parent,names in [(W,['WHOLE_TRACK_SOURCE_STATES.csv','WHOLE_TRACK_NATIVE_EVENTS.csv']), (T,['DRUM_DERIVATION_RESULTS.json','DRUM_VALIDATION_RAW.json']), (F,['MUSICAL_FORM_MARKERS.csv','PI_MUSICAL_FORM_ANNOTATION.json'])]:
  manifest=load(parent/'ARTIFACT_HASHES.json');manifest=manifest.get('files',manifest)
  for name in names:assert sha(parent/name)==manifest[name]
 original_inventory=load(R/'JGA_TEMPO_AUTHORITY_PHASE_CLOSURE_20260922/PRESERVATION_INVENTORY.json')
 verify({k:v if isinstance(v,str) else v['sha256'] for k,v in original_inventory.items()})
 inputs={'NATIVE_EVENTS.csv':W/'WHOLE_TRACK_NATIVE_EVENTS.csv','SOURCE_STATES.csv':W/'WHOLE_TRACK_SOURCE_STATES.csv',
  'SOURCE_PROCEDURE_FREEZE.json':W/'JGA_WHOLE_TRACK_GROOVE_PROCEDURE_FREEZE.json','SOURCE_ADAPTER.py':W/'common.py',
  'PLP_TIMESTAMPS.npy':P/'BEAT_TIMESTAMPS.npy','PLP_OUTPUT_FREEZE.json':P/'OUTPUT_FREEZE.json',
  'PLP_PERIOD_TRAJECTORY.csv':P/'PERIOD_TRAJECTORY.csv','PLP_FRONTEND.json':P.parent/'FRONTEND.json',
  'PLP_EXECUTION_PROVENANCE.json':P.parent/'EXECUTION_PROVENANCE.json',
  'DRUM_DERIVATION_RESULTS.json':T/'DRUM_DERIVATION_RESULTS.json','DRUM_VALIDATION_RAW.json':T/'DRUM_VALIDATION_RAW.json',
  'ATTACK_PREREGISTRATION.json':T/'JGA_SOURCE_ATTACK_ESTIMATOR_PREREGISTRATION.json','ATTACK_ESTIMATOR.py':T/'jga_attack_estimator.py',
  'ATTACK_RESULT.md':T/'RESULT.md','MUSICAL_FORM_MARKERS.csv':F/'MUSICAL_FORM_MARKERS.csv',
  'PI_MUSICAL_FORM_ANNOTATION.json':F/'PI_MUSICAL_FORM_ANNOTATION.json'}
 (O/'INPUT_SNAPSHOTS').mkdir(exist_ok=False)
 receipt=[]
 for name,p in inputs.items():
  out=O/'INPUT_SNAPSHOTS'/name;shutil.copyfile(p,out);assert sha(p)==sha(out)
  receipt.append({'original_path':str(p),'snapshot':str(out.relative_to(O)),'sha256':sha(p),'size':p.stat().st_size,'role':'REUSED_FROZEN_EVIDENCE'})
 table('INPUT_LINEAGE.csv',receipt);put('PARENT_HASHES.json',{str(p):sha(p) for p in inputs.values()}|{str(SOURCE):sha(SOURCE)})
 put('GIT_BEFORE.json',{'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip(),'status':subprocess.check_output(['git','status','--porcelain=v1'],text=True)})
 config={'study':'JGA-V1-FINAL-HISTORICAL-RECORDING-TRIAL-001','utc':now(),'source_sha256':sha(SOURCE),
  'analysis_s':[0,330],'excluded_s':[330,347.8117006802721],'bounds':'half-open; existing PI M7 stop/phrase/ending boundary, approximate whole seconds',
  'PLP':'Frozen B3 maxima/intervals, no inference, interpolation, smoothing, snapping or attack prior',
  'native_and_identity':'Exact frozen F_MIX rows and qualified ADTOF/MuScriptor/Bass-link states. No detector/model execution or selection by proximity.',
  'reference_assignment':'Nearest ORIGINAL frozen PLP maximum to native marker; ties earlier; no extrapolation outside first/last peak. Fixed native assignment reused for that event\'s qualified acoustic estimate to avoid hidden reassignment.',
  'local_BPM':'60/delta of consecutive frozen PLP maxima. Summary duration-weighted over intersecting source-time segments; not stored BPM or a new tracker.',
  'marker_statistics':'All in-scope events; separate disjoint source states and overlapping Bass-inclusive/Drum-inclusive groups. Native offset is marker geometry, not performer attack. Do not replace native markers with refined values.',
  'attack_statistics':'Only preserved non-null exposed-Drum estimates; preserve 2 derivation / 8 historical-validation records and one abstention. Do not apply estimator to new events. No accepted full-mix Bass refinement.',
  'uncertainty':'Provisional categorical source support, numerical marker coordinate, UNKNOWN numerical attack uncertainty. Refined estimates carry original fixed acoustic review interval, not physical confidence interval. No calibrated PLP phase uncertainty. Lattice spacing is not accuracy.',
  'sign':'Numerical sign of coordinate is descriptive. Refined interval relative to fixed peak: AHEAD if upper<peak; BEHIND if lower>peak; otherwise COMPATIBLE_WITH_FIXED_COORDINATE. Performer intended-beat category remains INDETERMINATE because intended-beat assignment/reference uncertainty unestablished.',
  'pairwise':'No independent Bass-Drum physical pair admitted. Count shared-reference distinct Bass-only/Drum-only markers as co-coverage, without selecting an arbitrary event pair or inferring simultaneity from dual support.',
  'sections':['M1:0-48','M2:48-141','M3:141-186','M4:186-232','M56:232-330'],
  'zoom_s':[216,220],'zoom_reason':'Existing PI exposed-Drum form interval and preserved qualified references; fixed before trial statistics, not result-picked.',
  'summary_definition':'N, population coverage, median, mean, Q1/Q3, IQR, median absolute deviation from median, sample SD ddof=1, median absolute offset, min/max. Empty => null; source-marker and refined estimates never pooled.',
  'assessment':'USABLE_WITH_QUALIFICATION requires defensible source-associated attack timing sufficient for intended Bass/Drum microtiming, not sample-perfect truth. PARTIALLY_USABLE if reproducible source-supported geometry and limited acoustic timing exist but transferable source-associated attack qualification remains unavailable. NOT_YET_USABLE if reproducible temporal/source geometry cannot be assembled.',
  'independence':'Development recording reused; not independent validation for future historical corpus. No new human judgments.',
  'historical_results':'Independent PLP FAIL and all prior results unchanged. This is a new additive authorized readout, not historical report regeneration.',
  'code_sha256':sha(__file__)}
 put('TRIAL_CONFIGURATION.json',config)
 freeze('INPUT_CONFIGURATION_FREEZE.json',[p for p in O.rglob('*') if p.is_file()])
 print('INPUT_CONFIGURATION_FREEZE',sha(O/'INPUT_CONFIGURATION_FREEZE.json'))

def stats(x):
 a=np.asarray(x,dtype=float); n=len(a)
 if not n:return {'N':0,**{k:None for k in ['median_ms','mean_ms','Q1_ms','Q3_ms','IQR_ms','MAD_ms','SD_ms','median_abs_ms','min_ms','max_ms']}}
 q1,med,q3=np.quantile(a,[.25,.5,.75]);return {'N':n,'median_ms':float(med),'mean_ms':float(a.mean()),'Q1_ms':float(q1),'Q3_ms':float(q3),'IQR_ms':float(q3-q1),'MAD_ms':float(np.median(abs(a-med))),'SD_ms':float(np.std(a,ddof=1)) if n>1 else None,'median_abs_ms':float(np.median(abs(a))),'min_ms':float(a.min()),'max_ms':float(a.max())}
def weighted_quantile(values,weights,p):
 order=np.argsort(values);v=np.asarray(values)[order];w=np.asarray(weights)[order]
 return float(v[np.searchsorted(np.cumsum(w),sum(w)*p,side='left')])
def analyze():
 verify({O/k:v for k,v in load(O/'INPUT_CONFIGURATION_FREEZE.json')['files'].items()});verify(load(O/'PARENT_HASHES.json'))
 S=O/'INPUT_SNAPSHOTS';beats=np.load(S/'PLP_TIMESTAMPS.npy');native=rows(S/'NATIVE_EVENTS.csv');states={r['JGA_EVENT_ID']:r for r in rows(S/'SOURCE_STATES.csv')}
 assert np.isfinite(beats).all() and np.all(np.diff(beats)>0)
 sections=[('M1','Opening / solo-launch transition',0,48),('M2','Piano solo / walking Bass',48,141),('M3','Piano-Bass exchanges',141,186),('M4','Piano-Drum exchanges',186,232),('M56','Final theme / turnaround / crescendo',232,330)]
 def section(t):return next((i for i,l,a,b in sections if a<=t<b),'EXCLUDED')
 out=[]
 for r in native:
  t=float(r['timestamp_s']);s=states[r['event_id']];assert t==float(s['native_timestamp'])
  included=0<=t<330;covered=beats[0]<=t<=beats[-1];j=int(np.argmin(abs(beats-t))) if covered else None;q=float(beats[j]) if covered else None
  k=int(np.clip(np.searchsorted(beats,t,side='right')-1,0,len(beats)-2));bpm=60/(beats[k+1]-beats[k])
  out.append({'event_id':r['event_id'],'section':section(t),'IN_SCOPE':included,'native_s':t,'source_state':s['source_state'],
   'reference_available':covered,'PLP_peak_index':j,'PLP_s':q,'marker_offset_ms':None if q is None else (t-q)*1000,
   'PLP_interval_BPM':float(bpm) if covered else None,'source_confidence':'PROVISIONAL_QUALIFIED_EVIDENCE' if s['source_state']!='UNKNOWN' else 'UNKNOWN',
   'timing_kind':'SOURCE_ASSOCIATED_NATIVE_MARKER' if s['source_state']!='UNKNOWN' else 'SOURCE_NEUTRAL_NATIVE_MARKER',
   'timing_confidence':'NUMERICAL_MARKER_ONLY_ATTACK_UNCERTAINTY_UNQUANTIFIED','numerical_attack_uncertainty_ms':None,
   'performer_ahead_on_behind':'INDETERMINATE_UNQUANTIFIED_ATTACK_AND_REFERENCE_UNCERTAINTY',
   'coordinate_sign':None if q is None else 'NEGATIVE' if t<q else 'POSITIVE' if t>q else 'ZERO',
   'native_grid_ms':r['timing_grid_ms'],'source_context':s['context'],'source_adapter_sha256':s['adapter_sha256'],
   'ADTOF_event_id':s['ADTOF_DRUM_event_id'],'ADTOF_distance_ms':s['ADTOF_DRUM_distance_ms'],
   'MU_U_BASS_event_id':s['MU_U_BASS_event_id'],'MU_U_DRUM_event_id':s['MU_U_DRUM_event_id'],'MU_C_DRUM_event_id':s['MU_C_DRUM_event_id'],
   'historical_Bass_links':s['frozen_Bass_native_links'],'exclusion_reason':'' if included else 'PI_M7_STOP_PHRASE_FINAL_HIT_DECAY'})
 table('EVENT_READOUT.csv',out);active=[r for r in out if r['IN_SCOPE']];lookup={r['event_id']:r for r in active}
 attack=[]
 for x in load(S/'DRUM_DERIVATION_RESULTS.json')+load(S/'DRUM_VALIDATION_RAW.json'):
  e=x['event'];r=lookup[e['event_id']];q=r['PLP_s'];t=x['result']['estimate_s'];lo=e['review_lo_s'];hi=e['review_hi_s']
  attack.append({'event_id':e['event_id'],'section':r['section'],'native_anchor_s':e['anchor_s'],'PLP_peak_index':r['PLP_peak_index'],'PLP_s':q,'estimate_s':t,
   'attack_offset_ms':None if t is None else (t-q)*1000,'review_lo_s':lo,'review_hi_s':hi,'review_offset_lo_ms':(lo-q)*1000,'review_offset_hi_ms':(hi-q)*1000,
   'status':'ABSTAIN' if t is None else 'QUALIFIED_EXPOSED_DRUM_ACOUSTIC_ESTIMATE','original_split':e['split'],
   'confidence':'PROMISING_EXPOSED_DRUM_ONLY_NOT_PHYSICAL_GT','interval_semantics':'HISTORICAL_BOUNDED_VISUAL_REVIEW_NOT_CALIBRATED_CONFIDENCE_INTERVAL',
   'conditional_fixed_reference_sign':None if t is None else 'AHEAD_OF_FIXED_PLP_COORDINATE' if hi<q else 'BEHIND_FIXED_PLP_COORDINATE' if lo>q else 'COMPATIBLE_WITH_FIXED_PLP_COORDINATE',
   'performer_ahead_on_behind':'INDETERMINATE_INTENDED_BEAT_AND_REFERENCE_UNCERTAINTY','reason':x['result']['reason'],'reference_origin':e['reference_origin'],
   'reference_event_id':e['reference_event_id'],'reference_note':e['review_reason'],'PI_source_note':e['PI_source_evidence']})
 table('QUALIFIED_DRUM_READOUT.csv',attack)
 seg=[]
 for i,(a,b) in enumerate(zip(beats[:-1],beats[1:])):
  aa=max(0,float(a));bb=min(330,float(b))
  if bb>aa:seg.append({'PLP_left_index':i,'source_start_s':float(a),'source_end_s':float(b),'included_start_s':aa,'included_end_s':bb,'weight_s':bb-aa,'period_s':float(b-a),'implied_BPM':float(60/(b-a))})
 table('PLP_REFERENCE_SEGMENTS.csv',seg)
 groups={'ALL_NATIVE':lambda r:True,'BASS_INCLUSIVE':lambda r:'BASS' in r['source_state'],'DRUM_INCLUSIVE':lambda r:'DRUM' in r['source_state']}
 groups.update({s:(lambda r,s=s:r['source_state']==s) for s in ['BASS_SUPPORTED','DRUM_SUPPORTED','BASS_AND_DRUM_SUPPORTED','UNKNOWN']})
 statrows=[]
 for sid,_,a,b in [('WHOLE','whole',0,330)]+sections:
  rr=[r for r in active if a<=r['native_s']<b]
  for label,predicate in groups.items():
   subset=[r for r in rr if predicate(r) and r['reference_available']]
   statrows.append({'section':sid,'category':label,'semantics':'MARKER_GEOMETRY_NOT_PERFORMER_MICROTIMING','population_N':len(rr),'coverage_fraction':len(subset)/len(rr) if rr else None,**stats([r['marker_offset_ms'] for r in subset])})
  ar=[r for r in attack if r['estimate_s'] is not None and a<=r['native_anchor_s']<b]
  statrows.append({'section':sid,'category':'REFINED_DRUM','semantics':'QUALIFIED_ACOUSTIC_ESTIMATE_FIXED_REFERENCE_GEOMETRY','population_N':sum(a<=r['native_anchor_s']<b for r in attack),'coverage_fraction':len(ar)/sum(a<=r['native_anchor_s']<b for r in attack) if any(a<=r['native_anchor_s']<b for r in attack) else None,**stats([r['attack_offset_ms'] for r in ar])})
 table('TIMING_STATISTICS.csv',statrows)
 sectionrows=[]
 for sid,label,a,b in sections:
  rr=[r for r in active if r['section']==sid];counts=Counter(r['source_state'] for r in rr);ss=[r for r in seg if r['included_start_s']<b and r['included_end_s']>a];weights=[min(b,r['included_end_s'])-max(a,r['included_start_s']) for r in ss];bpms=[r['implied_BPM'] for r in ss]
  sectionrows.append({'section':sid,'label':label,'start_s':a,'end_s':b,'boundary_uncertainty':'PI_APPROXIMATE_WHOLE_SECONDS','native_N':len(rr),'Bass_inclusive_N':sum('BASS' in r['source_state'] for r in rr),'Drum_inclusive_N':sum('DRUM' in r['source_state'] for r in rr),'dual_N':counts['BASS_AND_DRUM_SUPPORTED'],'UNKNOWN_N':counts['UNKNOWN'],'refined_Drum_N':sum(r['estimate_s'] is not None and r['section']==sid for r in attack),'PLP_covered_s':sum(weights),'PLP_duration_weighted_median_BPM':weighted_quantile(bpms,weights,.5),'PLP_min_BPM':min(bpms),'PLP_max_BPM':max(bpms)})
 table('SECTION_SUMMARY.csv',sectionrows)
 cells=[]
 for idx in sorted({r['PLP_peak_index'] for r in active if r['reference_available']}):
  rr=[r for r in active if r['PLP_peak_index']==idx];bass=[r['event_id'] for r in rr if r['source_state']=='BASS_SUPPORTED'];drum=[r['event_id'] for r in rr if r['source_state']=='DRUM_SUPPORTED'];dual=[r['event_id'] for r in rr if r['source_state']=='BASS_AND_DRUM_SUPPORTED']
  cells.append({'PLP_peak_index':idx,'Bass_only_marker_ids':';'.join(bass),'Drum_only_marker_ids':';'.join(drum),'dual_marker_ids':';'.join(dual),'distinct_single_support_co_coverage':bool(bass and drum),'physical_pair_status':'NOT_ESTABLISHED','Bass_Drum_attack_delta_ms':None})
 table('PAIRWISE_COVERAGE.csv',cells)
 bpm=[r['implied_BPM'] for r in seg];weights=[r['weight_s'] for r in seg];c=Counter(r['source_state'] for r in active)
 summary={'native_total_frozen':len(native),'native_in_scope':len(active),'excluded_native':len(native)-len(active),'source_states':dict(c),'Bass_inclusive':sum('BASS' in r['source_state'] for r in active),'Drum_inclusive':sum('DRUM' in r['source_state'] for r in active),
  'marker_reference_available':sum(r['reference_available'] for r in active),'qualified_Drum_estimates':sum(r['estimate_s'] is not None for r in attack),'attempted_Drum_refinement':len(attack),'Drum_refinement_abstentions':sum(r['estimate_s'] is None for r in attack),'other_events_refinement_status':'NOT_ESTABLISHED_NOT_EXECUTED; not counted as algorithm abstentions',
  'qualified_Bass_estimates':0,'independent_Bass_Drum_pairs':0,'distinct_single_support_cells':sum(r['distinct_single_support_co_coverage'] for r in cells),
  'PLP_peaks_in_scope':int(np.sum((beats>=0)&(beats<330))),'PLP_segment_covered_s':sum(weights),'PLP_leading_unbracketed_s':max(0,float(beats[0])),'PLP_duration_weighted_Q1_BPM':weighted_quantile(bpm,weights,.25),'PLP_duration_weighted_median_BPM':weighted_quantile(bpm,weights,.5),'PLP_duration_weighted_Q3_BPM':weighted_quantile(bpm,weights,.75),'PLP_min_BPM':min(bpm),'PLP_max_BPM':max(bpm),
  'confidence_distribution':{'marker_only':len(active),'additional_qualified_acoustic_estimate':sum(r['estimate_s'] is not None for r in attack),'numerically_calibrated_physical_attack_uncertainty':0},
  'conditional_refined_signs':dict(Counter(r['conditional_fixed_reference_sign'] for r in attack if r['estimate_s'] is not None)),
  'performer_ahead_on_behind':'INDETERMINATE; no calibrated attack/reference uncertainty or intended-beat assignment',
  'JGA_V1_HISTORICAL_ANALYSIS':'PARTIALLY_USABLE','single_blocker':'Transferable qualification of source-associated full-mix attack timing, most decisively Double Bass; marker coordinates alone do not establish performer microtiming.',
  'scope':'Useful reproducible exploratory temporal/source geometry and limited exposed-Drum acoustic timing; not a completed Bass-Drum attack/microtiming pipeline or independent corpus validation.'}
 put('SUMMARY.json',summary)
 put('NUMERICAL_OUTPUT_FREEZE.json',{'utc':now(),'configuration_freeze_sha256':sha(O/'INPUT_CONFIGURATION_FREEZE.json'),'files':{p.name:sha(p) for p in O.glob('*.csv')}|{'SUMMARY.json':sha(O/'SUMMARY.json')},'historical_results_unchanged':True})
 figures(active,attack,seg,sections)
 report(summary,sectionrows,statrows)
 verify(load(O/'PARENT_HASHES.json'))
 put('VALIDATION.json',{'utc':now(),'source_hash_pass':True,'parent_hashes_unchanged':True,'native_rows_preserved':len(native),'in_scope_rows':len(active),'excluded_rows':len(native)-len(active),'source_states_unchanged':True,'timestamp_changes':0,'PLP_rerun':False,'model_inference':False,'new_attack_estimates':0,'preserved_refinement_outputs_reused':len(attack),'synthetic_uncertainty_bounds':0,'physical_pair_estimates_fabricated':0,'status':'PASS'})
 print(json.dumps(summary,indent=2))

def figures(active,attack,seg,sections):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.size':9,'svg.fonttype':'none','pdf.fonttype':42})
 colors={'BASS_SUPPORTED':'#167d9a','DRUM_SUPPORTED':'#d17917','BASS_AND_DRUM_SUPPORTED':'#8252a1','UNKNOWN':'#999999'}
 fig,axs=plt.subplots(4,1,figsize=(17,11),sharex=True,gridspec_kw={'height_ratios':[1.2,2.2,2.2,.8]})
 axs[0].plot([r['included_start_s'] for r in seg],[r['implied_BPM'] for r in seg],lw=.65,color='#263b59');axs[0].set_ylabel('PLP inter-peak\nBPM (unsmoothed)')
 for ax,fam in [(axs[1],'BASS'),(axs[2],'DRUM')]:
  for state in [fam+'_SUPPORTED','BASS_AND_DRUM_SUPPORTED']:
   rr=[r for r in active if r['source_state']==state and r['reference_available']]
   ax.scatter([r['native_s'] for r in rr],[r['marker_offset_ms'] for r in rr],s=13 if state!= 'BASS_AND_DRUM_SUPPORTED' else 17,marker='o' if state!='BASS_AND_DRUM_SUPPORTED' else 'x',color=colors[state],alpha=.65,label='single-source support' if state!='BASS_AND_DRUM_SUPPORTED' else 'dual-support marker (shared)')
  ax.axhline(0,color='black',lw=.7);ax.set_ylabel(f'{fam} marker minus\nnearest frozen PLP (ms)');ax.legend(loc='upper right',fontsize=7)
 aa=[r for r in attack if r['estimate_s'] is not None]
 axs[2].errorbar([r['estimate_s'] for r in aa],[r['attack_offset_ms'] for r in aa],yerr=[[r['attack_offset_ms']-r['review_offset_lo_ms'] for r in aa],[r['review_offset_hi_ms']-r['attack_offset_ms'] for r in aa]],fmt='D',ms=4,color='black',capsize=3,label='qualified Drum + review interval')
 axs[2].legend(loc='upper right',fontsize=7)
 unknown=[r['native_s'] for r in active if r['source_state']=='UNKNOWN'];axs[3].plot(unknown,np.zeros(len(unknown)),'|',color='#888888',ms=8,label='identity UNKNOWN');ab=[r['native_anchor_s'] for r in attack if r['estimate_s'] is None];axs[3].plot(ab,np.ones(len(ab)),'v',color='red',label='attempted refinement ABSTAIN');axs[3].set_yticks([]);axs[3].legend(loc='upper left',fontsize=7);axs[3].set_ylabel('Uncertainty');axs[3].set_xlabel('Original source time (mm:ss)')
 for ax in axs:
  for sid,label,a,b in sections:ax.axvline(a,color='#555555',ls=':',lw=.6)
  ax.set_xlim(0,330);ax.grid(alpha=.12)
 for sid,label,a,b in sections:axs[0].text((a+b)/2,1.02,sid+'\n'+label,transform=axs[0].get_xaxis_transform(),ha='center',va='bottom',fontsize=8)
 ticks=np.arange(0,331,30);axs[-1].set_xticks(ticks,[f'{int(t)//60:02}:{int(t)%60:02}' for t in ticks])
 fig.suptitle('Exactly Like You — frozen PLP context and source-associated event geometry\nColored markers: provisional identity, unquantified attack uncertainty. Black diamonds: qualified acoustic estimates. Zero is a coordinate, not performer truth.',fontsize=12,y=.995)
 fig.subplots_adjust(top=.83,bottom=.07,left=.09,right=.98,hspace=.17)
 for ext in ['png','pdf','svg']:fig.savefig(O/f'WHOLE_PERFORMANCE.{ext}',dpi=160)
 plt.close(fig)
 fig,ax=plt.subplots(figsize=(13,5))
 for state,color in colors.items():
  rr=[r for r in active if 216<=r['native_s']<220 and r['source_state']==state]
  ax.scatter([r['native_s'] for r in rr],[r['marker_offset_ms'] for r in rr],s=40,color=color,marker='x' if state=='BASS_AND_DRUM_SUPPORTED' else 'o',label=state)
 rr=[r for r in aa if 216<=r['native_anchor_s']<220]
 ax.errorbar([r['estimate_s'] for r in rr],[r['attack_offset_ms'] for r in rr],yerr=[[r['attack_offset_ms']-r['review_offset_lo_ms'] for r in rr],[r['review_offset_hi_ms']-r['attack_offset_ms'] for r in rr]],fmt='D',color='black',capsize=5,label='preserved acoustic estimate + visual review bounds')
 for r in rr:
  parent=next(e for e in active if e['event_id']==r['event_id']);ax.plot([parent['native_s'],r['estimate_s']],[parent['marker_offset_ms'],r['attack_offset_ms']],color='black',lw=.6)
 ax.axhline(0,color='black',lw=.8);ax.set_xlim(216,220);ax.set_xlabel('Original source seconds');ax.set_ylabel('Signed displacement from fixed PLP coordinate (ms)');ax.set_title('03:36–03:40 — existing exposed-Drum evidence\nReview intervals are not physical confidence bounds; marker and acoustic estimates remain separate');ax.legend(fontsize=7,loc='upper left');ax.grid(alpha=.15);fig.tight_layout()
 for ext in ['png','pdf','svg']:fig.savefig(O/f'ZOOM_REFERENCE.{ext}',dpi=160)
 plt.close(fig)

def report(s,sections,statistics):
 lines=['# JGA v1 final historical-recording trial','', '**Target: Ray Brown Trio — Exactly Like You. Engineering assessment: PARTIALLY_USABLE.**','',
 'This completed trial assembles frozen research evidence; it does not deploy a new production runtime. It is scientifically useful for reproducible exploratory source-associated marker geometry and limited exposed-Drum acoustic timing. It does not yet establish general Bass–Drum performer microtiming.','',
 '## Authority and scope','',
 'Source SHA-256 `'+sha(SOURCE)+'`. Original full mix remains signal authority; no new decode, inference, source separation, PLP retuning or attack detector. Analyze [0,330) s; exclude [330,347.8117006802721) s using existing PI M7 stop/phrase/ending annotation. Boundaries are approximate whole seconds, not inferred from offsets.','',
 'PLP B3 output freeze `4384911f6086ba8a1a6f9deaa8370ae9ba22f6339ae42b3b0b4a015204efa7ac` is reused unchanged. Its inter-maximum interval supplies BPM context. Nearest stored maximum is an operational reference coordinate, not independently verified intended beat for every event. No reference extrapolation. Historical independent PLP FAIL remains unchanged; development 5/5 is not independent corpus evidence. The rejected proximity prior is not used.','',
 '## Population and uncertainty','',f'Native frozen {s["native_total_frozen"]}; included {s["native_in_scope"]}; excluded {s["excluded_native"]}. Disjoint source states: {s["source_states"]}. Bass-inclusive {s["Bass_inclusive"]}, Drum-inclusive {s["Drum_inclusive"]}; both include shared dual markers and must not be summed as independent attacks.','',
 f'Qualified acoustic estimates: {s["qualified_Drum_estimates"]} Drum; one abstention among ten historical attempts. Bass: zero qualified full-mix attack estimates. Other markers are not counted as failed estimator trials: refinement was never applied to them. Numerical uncertainty is unquantified for native attacks and PLP phase; no ±hop or fabricated HIGH-confidence bounds. Original Drum visual intervals are shown as qualified acoustic bounds, not calibrated physical confidence intervals.','',
 f'PLP maxima in scope {s["PLP_peaks_in_scope"]}; inter-peak coverage {s["PLP_segment_covered_s"]:.6f} s; leading unbracketed {s["PLP_leading_unbracketed_s"]:.6f} s. Duration-weighted BPM median {s["PLP_duration_weighted_median_BPM"]:.2f}, Q1 {s["PLP_duration_weighted_Q1_BPM"]:.2f}, Q3 {s["PLP_duration_weighted_Q3_BPM"]:.2f}; unsmoothed interval range {s["PLP_min_BPM"]:.2f}–{s["PLP_max_BPM"]:.2f}. Extremes are algorithmic inter-peak observations, not automatically genuine performance accelerations.','',
 '## Section readout','', '| Section | Native | Bass incl. | Drum incl. | Dual | Unknown | Weighted BPM |','|---|---:|---:|---:|---:|---:|---:|']
 for r in sections:lines.append(f'| {r["section"]}: {r["label"]} | {r["native_N"]} | {r["Bass_inclusive_N"]} | {r["Drum_inclusive_N"]} | {r["dual_N"]} | {r["UNKNOWN_N"]} | {r["PLP_duration_weighted_median_BPM"]:.2f} |')
 lines+=['','## Timing distributions','', 'Full N/coverage/median/mean/IQR/MAD/sample SD/median absolute/range are in TIMING_STATISTICS.csv, separately by marker state, overlapping source group, section and refined acoustic estimates. Values below are descriptive offsets, not signed physical performer judgments.','', '| Category | N | Median ms | Mean ms | IQR ms | MAD ms | SD ms | Median abs ms | Range ms |','|---|---:|---:|---:|---:|---:|---:|---:|---|']
 for r in statistics:
  if r['section']=='WHOLE' and r['category'] in ['BASS_INCLUSIVE','DRUM_INCLUSIVE','REFINED_DRUM']:
   lines.append(f'| {r["category"]} | {r["N"]} | {r["median_ms"]:.2f} | {r["mean_ms"]:.2f} | {r["IQR_ms"]:.2f} | {r["MAD_ms"]:.2f} | {r["SD_ms"]:.2f} | {r["median_abs_ms"]:.2f} | {r["min_ms"]:.2f} to {r["max_ms"]:.2f} |')
 lines+=['','## Ahead/on/behind and pairwise boundary','',
 f'Qualified Drum interval signs relative to a fixed numerical PLP coordinate: {s["conditional_refined_signs"]}. This does not establish intended-beat assignment or physical performer ahead/behind. Native markers cannot receive a defensible performer sign from unquantified attack uncertainty. Zero line denotes a reference coordinate, not a target to attract events to.','',
 f'Independent Bass–Drum attack pairs: 0. Distinct single-source-support co-covered reference cells: {s["distinct_single_support_cells"]}; these do not justify an arbitrary one-to-one attack pairing. Dual support is one marker, never evidence for zero Bass–Drum delay. No Ride/Hi-Hat relationships or kit-component accuracy inferred from generic Drum.','',
 '## What the graphs mean','',
 '[Whole performance](WHOLE_PERFORMANCE.png) and [03:36–03:40 zoom](ZOOM_REFERENCE.png) are also provided as PDF/SVG. Colored observations are source-associated markers with categorical, provisional source support. Shared dual markers are crosses. Black diamonds and vertical bounds show the separately preserved Drum acoustic estimates and reviewed intervals. No artificial attack-error bars on native markers; missing confidence remains missing. Large offsets in fills can denote subdivisions or nearest-reference assignment, not performer lateness.','',
 '## Scientific usefulness and single blocker','',
 'Reliable computational measurements: frozen event coordinates, source-evidence provenance, pulse coordinates, their arithmetic relations, coverage and section assignment under the supplied form map. Qualified estimates: provisional Bass/Drum-associated geometry and the nine exposed sharp-Drum acoustic landmarks. These permit auditable musical hypotheses about changing texture and temporal organization, not a causal or physical groove verdict.','',
 'The single material blocker is **transferable source-associated full-mix attack-timing qualification, most decisively Double Bass**. This does not require fictional sample-perfect truth: sufficiently justified categorical or bounded timing evidence would suffice. Current markers lack that qualification. Thus an operational freeze claiming completed historical Bass–Drum microtiming is not justified by this trial. No new detector or model search follows automatically.','',
 'Exactly Like You is heavily exposed development material. Native detection, source associations, acoustic reference reviews and PLP listening all have recorded reuse limitations. Native sampling lattices, model neighborhood support, sparse Bass coverage, review anchoring, unquantified reference phase and nearest-peak assignment limit interpretation. Descriptive means/quantiles are not significance tests, listener validation or corpus generalization.','',
 'Next action: PI review of the completed trial and its single attack-timing qualification blocker. No further experiment executed.','']
 doc('RESULT.md','\n'.join(lines))
 doc('README.md','# Final historical-recording trial\n\n[Result](RESULT.md) · [Whole graph](WHOLE_PERFORMANCE.png) · [Zoom](ZOOM_REFERENCE.png) · [Configuration](TRIAL_CONFIGURATION.json) · [Summary](SUMMARY.json).\n\nINPUT_SNAPSHOTS contains byte-identical lightweight parent evidence; INPUT_LINEAGE.csv maps originals and hashes. Original commercial audio remains externally referenced, not duplicated or redistributed. All readout tables and figures are new derived evidence. Historical scientific records remain unchanged.\n')

if __name__=='__main__':{'prepare':prepare,'analyze':analyze}[sys.argv[1]]()
