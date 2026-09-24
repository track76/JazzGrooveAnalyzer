from pathlib import Path
import json,datetime,joblib,collections
from selector import save,sha,decide
W=Path(__file__).resolve().parent;O=W/'output';blocked=[]
for p in [W.parent/'EVALUATION_POPULATIONS.json',W.parent.parent/'JGA_GALLEGATI_CONTINUOUS_FISHMAN_GT_120_20260924/GROUND_TRUTH/GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json',W.parent.parent/'JGA_NATIVE_BP_GT_120_20260924/EVENT_RESULTS.json']:
 try:p.read_bytes();raise RuntimeError('Reference access permitted unexpectedly')
 except PermissionError:blocked.append({'path':str(p),'read_denied':True})
save(O/'ISOLATION_CHECKS.json',blocked)
records=json.loads((W/'input/CANDIDATES.json').read_text());groups=[]
for clip in sorted({r['clip_id'] for r in records}):
 rs=sorted([r for r in records if r['clip_id']==clip],key=lambda r:(r['search_start_s'],r['BP']['native_note_id']));group=None
 for r in rs:
  end=max(r['search_end_s'],r['BP']['offset_local_s'])
  if group is None or r['search_start_s']>group['activity_end_s']:
   group={'group_id':f'RG{len(groups)+1:04d}','clip_id':clip,'activity_start_s':r['search_start_s'],'activity_end_s':end,'BP_ids':[],'search_intervals':[]};groups.append(group)
  group['activity_end_s']=max(group['activity_end_s'],end);group['BP_ids'].append(r['BP']['native_note_id']);group['search_intervals'].append([r['search_start_s'],r['search_end_s']])
 for g in [g for g in groups if g['clip_id']==clip]:
  merged=[]
  for lo,hi in sorted(g['search_intervals']):
   if merged and lo<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],hi)
   else:merged.append([lo,hi])
  g['search_intervals']=merged
save(O/'SEARCH_REGIONS.json',groups);save(O/'REGIONS_HASH.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':sha(O/'SEARCH_REGIONS.json')})
model=joblib.load(W/'input/MODEL.joblib');rule=json.loads((W/'input/SELECTOR_RULE.json').read_text());recordmap={r['BP']['native_note_id']:r for r in records};pred=[];evidence=[]
for g in groups:
 cand=[c for k in g['BP_ids'] for c in recordmap[k]['candidates']];d=decide({'candidates':cand},model,rule['threshold']);status='ATTACK_SELECTED_IDENTITY_UNRESOLVED' if d['status']=='ATTACK_SELECTED' else d['status'];pred.append({**g,'candidate_context_count':len(cand),'unique_candidate_coordinates':len({c['time_s'] for c in cand}),'selector_status':status,'selected_s':d['selected_s'],'selected_id':d.get('selected_id'),'maximum_score':max(d['probabilities']) if d['probabilities'] else None});evidence.append({'group_id':g['group_id'],'candidate_ids':[c['candidate_id'] for c in cand],'probabilities':d['probabilities']})
save(O/'PREDICTIONS.json',pred);save(O/'ALL_CONTEXT_SCORES.json',evidence)
save(O/'RECOVERY_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{str(p.relative_to(W)):sha(p) for p in [O/'SEARCH_REGIONS.json',O/'PREDICTIONS.json',O/'ALL_CONTEXT_SCORES.json',O/'ISOLATION_CHECKS.json',W/'input/CANDIDATES.json',W/'input/MODEL.joblib',W/'input/SELECTOR_RULE.json',W/'run.py',W/'selector.py',W/'morphology.py']}})
print('Frozen operational regions',len(groups),'statuses',dict(collections.Counter(p['selector_status'] for p in pred)),flush=True)
