from pathlib import Path
import json,joblib,datetime,collections
from selector import decide,save,sha
W=Path(__file__).resolve().parent;O=W/'output';checks=[]
for p in [W.parent/'EVALUATION_POPULATIONS.json',W.parent.parent/'JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_120_20260924/GROUND_TRUTH/GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json',W.parent.parent/'JGA_BP_AMBIGUITY_ATTACK_RECOVERY_20260924/EVENT_RESULTS.json']:
 try:p.read_bytes();raise RuntimeError('GT isolation failure')
 except PermissionError:checks.append({'path':str(p),'read_denied':True})
save(O/'ISOLATION_CHECKS.json',checks);records=json.loads((W/'input/CANDIDATES.json').read_text());model=joblib.load(W/'input/MODEL.joblib');rule=json.loads((W/'input/SELECTOR_RULE.json').read_text());queries={r['BP']['native_note_id']:{'BP_id':r['BP']['native_note_id'],'window_start_s':r['search_start_s'],'window_end_s':r['search_end_s'],**decide(r,model,rule['threshold'])} for r in records};save(O/'INDEPENDENT_WINDOW_DECISIONS.json',queries);out=[]
for g in json.loads((W/'input/HYPOTHESIS_SETS.json').read_text()):
 qs=[queries[k] for k in g['BP_ids']];sel=[q for q in qs if q['status']=='ATTACK_SELECTED'];coords={round(q['selected_s']*44100) for q in sel}
 status=('NO_CANDIDATE' if all(q['status']=='NO_CANDIDATE' for q in qs) else 'ABSTAIN_NO_SELECTED_ATTACK') if not sel else 'ATTACK_SELECTED_IDENTITY_UNRESOLVED' if len(sel)==1 else 'SHARED_ATTACK_IDENTITY_UNRESOLVED' if len(coords)==1 else 'ABSTAIN_MULTIPLE_DISTINCT_ATTACKS'
 out.append({**g,'status':status,'successful_windows':len(sel),'distinct_selected_coordinates':len(coords),'selected_s':sel[0]['selected_s'] if len(coords)==1 else None,'all_successful_query_ids':[q['BP_id'] for q in sel],'all_selected_coordinates_s':[q['selected_s'] for q in sel]})
save(O/'CONTAINED_PREDICTIONS.json',out);save(O/'PREDICTION_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{str(p.relative_to(W)):sha(p) for p in [O/'CONTAINED_PREDICTIONS.json',O/'INDEPENDENT_WINDOW_DECISIONS.json',O/'ISOLATION_CHECKS.json',W/'run.py',W/'input/HYPOTHESIS_SETS.json',W/'input/CANDIDATES.json',W/'input/MODEL.joblib',W/'selector.py',W/'morphology.py']}});print(dict(collections.Counter(p['status'] for p in out)))
