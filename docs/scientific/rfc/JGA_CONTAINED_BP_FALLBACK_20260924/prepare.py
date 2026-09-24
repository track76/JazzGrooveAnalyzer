from pathlib import Path
import json,hashlib,shutil,datetime
W=Path(__file__).resolve().parent;U=W.parent/'JGA_BP_AMBIGUITY_ATTACK_RECOVERY_20260924';P=W.parent/'JGA_LEARNED_LOCAL_ATTACK_SELECTOR_20260924';I=W/'inference';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
for base,freeze in [(U/'inference',U/'inference/output/RECOVERY_FREEZE.json'),(P/'development',P/'development/output/SELECTOR_FREEZE.json')]:
 f=json.loads(freeze.read_text());assert all(sha(base/p)==h for p,h in f['files'].items())
for f in ['selector.py','morphology.py','input/CANDIDATES.json','input/MODEL.joblib','input/SELECTOR_RULE.json']:shutil.copyfile(U/'inference'/f,I/f)
# Preserve exactly previous operational hypothesis membership, without region envelopes or GT cohort IDs.
groups=json.loads((U/'inference/output/SEARCH_REGIONS.json').read_text());save(I/'input/HYPOTHESIS_SETS.json',[{'set_id':g['group_id'],'clip_id':g['clip_id'],'BP_ids':g['BP_ids']} for g in groups])
shutil.copyfile(U/'EVALUATION_POPULATIONS.json',W/'EVALUATION_POPULATIONS.json')
save(W/'PROTOCOL.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Same13 natural and35 masked cohort; previously exposed investigator; process-isolated inference. Fishman observable onset, not string release.','hypothesis_membership':'Exact prior BP-only operational membership retained as bookkeeping, NOT a merged search region. No GT-selected narrowing or restoration of secure matched BP ID for masked cohort. Every original window evaluated independently.','decision':'Unchanged frozen decide per native window. Zero successful queries: ABSTAIN_NO_SELECTED_ATTACK (NO_CANDIDATE if every window empty). One successful query: ATTACK_SELECTED_IDENTITY_UNRESOLVED. Multiple successful queries with identical original PCM sample coordinate: SHARED_ATTACK_IDENTITY_UNRESOLVED. Multiple distinct coordinates: ABSTAIN_MULTIPLE_DISTINCT_ATTACKS.','shared_definition':'Exact native PCM sample equality only, round(time*44100) to identify stored coordinate, not to change timestamp. No proximity tolerance, physical-identity certainty or averaging. Retain an actual original candidate timestamp.','scoring':'Same prior >100ms catastrophic threshold. ±10ms useful recovery. Preserve all failures, abstentions and exact cohort membership.'})
save(W/'INPUT_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{str(p.relative_to(W)):sha(p) for p in [W/'PROTOCOL.json',W/'EVALUATION_POPULATIONS.json',I/'input/HYPOTHESIS_SETS.json',I/'input/CANDIDATES.json',I/'input/MODEL.joblib',I/'input/SELECTOR_RULE.json',I/'selector.py',I/'morphology.py']}})
s='(version 1)\n(allow default)\n(deny network*)\n(deny file-read* (subpath "/Users") (subpath "/Volumes") (subpath "/private/tmp"))\n'
for p in [str(I),str(Path('.venv').resolve())]:s+=f'(allow file-read* (subpath "{p}"))\n'
(W/'isolation.sb').write_text(s+'(allow file-read-metadata)\n')
