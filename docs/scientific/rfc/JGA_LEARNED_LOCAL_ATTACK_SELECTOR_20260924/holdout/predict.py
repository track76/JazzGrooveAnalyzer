from pathlib import Path
import joblib,json,datetime
from selector import *
W=Path(__file__).resolve().parent;O=W/'output';check_isolation(W);model=joblib.load(W/'input/MODEL.joblib');rule=json.loads((W/'input/SELECTOR_RULE.json').read_text());records=generate(W);pred=[]
for r in records:pred.append({'clip_id':r['clip_id'],'BP_id':r['BP']['native_note_id'],**decide(r,model,rule['threshold'])})
save(O/'BLIND_PREDICTIONS.json',pred);save(O/'PREDICTIONS_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{str(p.relative_to(W)):sha(p) for p in [O/'BLIND_PREDICTIONS.json',O/'BLIND_CANDIDATES.json',W/'selector.py',W/'morphology.py',W/'predict.py',W/'input/MODEL.joblib',W/'input/SELECTOR_RULE.json']}});print('All holdout predictions saved and hashed',len(pred),flush=True)
