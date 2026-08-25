"""Require exact independent scoring replay and freeze the result."""
from hashlib import sha256
import json,sys
from pathlib import Path
a,b,frozen,proof=map(Path,sys.argv[1:]); x=json.loads(a.read_text()); y=json.loads(b.read_text())
if x!=y or x["combined_benchmark_fingerprint"]!=y["combined_benchmark_fingerprint"]: raise RuntimeError("SCORING_REPLAY_CONFLICT")
frozen.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
r={"status":"PASS","exact_assignment_replay":True,"exact_metric_replay":True,"exact_fingerprint_replay":True,"run_1_sha256":sha256(a.read_bytes()).hexdigest(),"run_2_sha256":sha256(b.read_bytes()).hexdigest(),"result_sha256":sha256(frozen.read_bytes()).hexdigest(),"combined_benchmark_fingerprint":x["combined_benchmark_fingerprint"]}
proof.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n"); print(json.dumps(r,sort_keys=True))
