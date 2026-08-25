"""Seal all raw authorities before any Ground Truth access."""
from hashlib import sha256
import json,sys
from pathlib import Path
out=Path(sys.argv[1]); paths=[Path(x) for x in sys.argv[2:]]
assets=[]
for p in paths:
    x=json.loads(p.read_text())
    if x.get("ground_truth_accessed") is not False: raise RuntimeError("BLINDNESS_CONFLICT")
    assets.append({"file":p.name,"sha256":sha256(p.read_bytes()).hexdigest(),"system":x["system"],"raw_output_count":x["raw_output_count"],"scientific_fingerprint":x["scientific_fingerprint"]})
record={"status":"PASS_FROZEN_BEFORE_GT_ACCESS","ground_truth_accessed":False,"assets":assets}
record["blind_freeze_fingerprint"]=sha256(json.dumps(record,sort_keys=True,separators=(",",":")).encode()).hexdigest()
out.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n"); print(json.dumps(record,sort_keys=True))
