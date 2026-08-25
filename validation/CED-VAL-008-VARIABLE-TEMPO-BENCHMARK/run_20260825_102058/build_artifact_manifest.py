"""Freeze checksums for bounded execution artifacts."""
from hashlib import sha256
import json,sys
from pathlib import Path
here=Path(__file__).resolve().parent; out=here/"artifact_manifest.json"
files=sorted(p for p in here.iterdir() if p.is_file() and p.name not in {"artifact_manifest.json"})
assets=[{"file":p.name,"byte_size":p.stat().st_size,"sha256":sha256(p.read_bytes()).hexdigest()} for p in files]
r=json.loads((here/"result.json").read_text())
m={"execution_id":r["execution_id"],"study_id":r["study_id"],"dataset_fingerprint":r["dataset_fingerprint"],"combined_benchmark_fingerprint":r["combined_benchmark_fingerprint"],"assets":assets}
m["manifest_fingerprint"]=sha256(json.dumps(m,sort_keys=True,separators=(",",":")).encode()).hexdigest(); out.write_text(json.dumps(m,indent=2,sort_keys=True)+"\n"); print(json.dumps({"asset_count":len(assets),"manifest_fingerprint":m["manifest_fingerprint"]},sort_keys=True))
