"""Require exact two-run scientific replay and freeze one raw authority."""
from hashlib import sha256
import json,sys
from pathlib import Path
a,b,frozen,proof=map(Path,sys.argv[1:])
x=json.loads(a.read_text()); y=json.loads(b.read_text())
if x!=y or x["scientific_fingerprint"]!=y["scientific_fingerprint"]: raise RuntimeError("RAW_REPLAY_CONFLICT")
frozen.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
r={"status":"PASS","system":x["system"],"run_1_sha256":sha256(a.read_bytes()).hexdigest(),"run_2_sha256":sha256(b.read_bytes()).hexdigest(),"frozen_sha256":sha256(frozen.read_bytes()).hexdigest(),"scientific_fingerprint":x["scientific_fingerprint"],"raw_output_count":x["raw_output_count"],"exact_scientific_content_replay":True,"exact_population_replay":True,"exact_coordinate_replay":True,"ground_truth_accessed":False}
proof.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n"); print(json.dumps(r,sort_keys=True))
