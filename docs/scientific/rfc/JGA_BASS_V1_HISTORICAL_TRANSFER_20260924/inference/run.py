from pathlib import Path
import json,joblib,datetime,collections
from selector import generate,decide,save,sha
W=Path(__file__).resolve().parent;O=W/'output';blocked=[]
for p in [W.parent.parent/'JGA_V1_OPERATIONAL_PLP_QUARTER_NEAREST_001_20260922/PLP_REFERENCE.csv',W.parent.parent.parent.parent/'historical_reports/JGA_HISTORICAL_REPORT_001/FINAL_SCORE_V1/METRIC_REFERENCE.csv',W.parent.parent/'JGA_FUNDAMENTALS_NEAREST_RAW_PLP_20260924/FUNDAMENTALS_NEAREST_PLP.csv',W.parent.parent/'JGA_FUNDAMENTAL_GUIDED_BASS_PROTOTYPE_20260924/JGA_BASS_ATTACKS_VS_RAW_PLP.csv']:
 try:p.read_bytes();raise RuntimeError('Isolation failure: timing reference readable')
 except PermissionError:blocked.append({'path':str(p),'read_denied':True})
save(O/'ISOLATION_CHECKS.json',blocked);records=generate(W);model=joblib.load(W/'input/MODEL.joblib');rule=json.loads((W/'input/SELECTOR_RULE.json').read_text());queries={r['BP']['native_note_id']:{'BP_id':r['BP']['native_note_id'],'search_start_s':r['search_start_s'],'search_end_s':r['search_end_s'],'candidate_count':len(r['candidates']),**decide(r,model,rule['threshold'])} for r in records};save(O/'QUERY_DECISIONS.json',queries)
routes=json.loads((W/'input/ROUTING.json').read_text());events=[]
for r in routes:
 qs=[queries[k] for k in r['hypothesis_ids']];sel=[q for q in qs if q['status']=='ATTACK_SELECTED'];coords={round(q['selected_s']*44100) for q in sel}
 if r['route']=='SECURE_ROUTE':status=qs[0]['status']
 else:status=('NO_CANDIDATE' if all(q['status']=='NO_CANDIDATE' for q in qs) else 'ABSTAIN_NO_SELECTED_ATTACK') if not sel else 'ATTACK_SELECTED_IDENTITY_UNRESOLVED' if len(sel)==1 else 'SHARED_ATTACK_IDENTITY_UNRESOLVED' if len(coords)==1 else 'ABSTAIN_MULTIPLE_DISTINCT_ATTACKS'
 selected=sel[0]['selected_s'] if len(coords)==1 else None
 events.append({**r,'status':status,'selected_s':selected,'selected_BP_ids':[q['BP_id'] for q in sel] if selected is not None else [],'successful_window_count':len(sel),'distinct_candidate_coordinates':len(coords),'timing_provenance':'DEMUCS_BASS_STEM_NATIVE_SPECTRAL_FRAME_CENTER','shared_within_episode':status=='SHARED_ATTACK_IDENTITY_UNRESOLVED'})
save(O/'EPISODE_DECISIONS.json',events);bycoord={}
for e in events:
 if e['selected_s'] is not None:bycoord.setdefault(round(e['selected_s']*44100),[]).append(e)
attacks=[]
for i,(sample,es) in enumerate(sorted(bycoord.items()),1):
 attacks.append({'attack_id':f'BASS_V1_{i:03d}','selected_s':es[0]['selected_s'],'native_sample_coordinate':sample,'episode_ids':[e['episode_id'] for e in es],'hypothesis_ids':sorted({k for e in es for k in e['hypothesis_ids']}),'selected_BP_ids':sorted({k for e in es for k in e['selected_BP_ids']}),'routes':sorted({e['route'] for e in es}),'pitch_hypotheses':sorted({e['fundamental_midi'] for e in es}),'shared_attack':len(es)>1 or any(e['shared_within_episode'] for e in es),'timing_provenance':'DEMUCS_BASS_STEM_NATIVE_SPECTRAL_FRAME_CENTER'})
save(O/'UNIQUE_ACOUSTIC_ATTACKS.json',attacks);save(O/'HISTORICAL_ACOUSTIC_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PLP_access':False,'files':{str(p.relative_to(W)):sha(p) for p in [O/'EPISODE_DECISIONS.json',O/'UNIQUE_ACOUSTIC_ATTACKS.json',O/'QUERY_DECISIONS.json',O/'BLIND_CANDIDATES.json',O/'ISOLATION_CHECKS.json',W/'input/ROUTING.json',W/'input/NOTES.json',W/'input/MODEL.joblib',W/'input/SELECTOR_RULE.json',W/'run.py',W/'selector.py',W/'morphology.py']}});print('PRE-PLP',{'episodes':len(events),'unique_attacks':len(attacks),'statuses':dict(collections.Counter(e['status'] for e in events)),'routes':{r:dict(collections.Counter(e['status'] for e in events if e['route']==r)) for r in ['SECURE_ROUTE','AMBIGUOUS_ROUTE']}},flush=True)
