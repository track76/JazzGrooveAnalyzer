from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).resolve().parent;D=W/'development';H=W/'holdout';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=json.loads((D/'output/SELECTOR_FREEZE.json').read_text());assert all(sha(D/p)==h for p,h in f['files'].items())
for src,dest in [(D/'selector.py',H/'selector.py'),(D/'output/MODEL.joblib',H/'input/MODEL.joblib'),(D/'output/SELECTOR_RULE.json',H/'input/SELECTOR_RULE.json'),(D/'output/SELECTOR_FREEZE.json',H/'input/SELECTOR_FREEZE.json')]:shutil.copyfile(src,dest)
print('Frozen model verified and copied; no GT copied.')
