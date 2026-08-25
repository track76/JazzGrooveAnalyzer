"""Read-only verifier for the frozen CED-VAL-008 execution."""
from hashlib import sha256
import json,subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent; base=here.parent
subprocess.run([sys.executable,str(base/"verify.py")],check=True)
m=json.loads((here/"artifact_manifest.json").read_text())
for a in m["assets"]:
    p=here/a["file"]
    if p.stat().st_size!=a["byte_size"] or sha256(p.read_bytes()).hexdigest()!=a["sha256"]: raise RuntimeError(f"ARTIFACT_CONFLICT: {p}")
copy=dict(m); fingerprint=copy.pop("manifest_fingerprint")
if sha256(json.dumps(copy,sort_keys=True,separators=(",",":")).encode()).hexdigest()!=fingerprint: raise RuntimeError("MANIFEST_FINGERPRINT_CONFLICT")
r=json.loads((here/"result.json").read_text()); s=json.loads((here/"scoring_replay.json").read_text()); b=json.loads((here/"blind_raw_freeze_manifest.json").read_text())
if r["combined_benchmark_fingerprint"]!=m["combined_benchmark_fingerprint"] or s["status"]!="PASS" or b["status"]!="PASS_FROZEN_BEFORE_GT_ACCESS": raise RuntimeError("RESULT_AUTHORITY_CONFLICT")
if not r["ground_truth_accessed_after_raw_freeze"] or r["latency_correction"] or r["marker_correction"] or r["weighted_composite_score"] or r["universal_superiority_claim"]: raise RuntimeError("FIREWALL_CONFLICT")
for system in ("jga","librosa","essentia"):
    replay=json.loads((here/f"{system}_replay.json").read_text())
    if replay["status"]!="PASS" or replay["ground_truth_accessed"] is not False: raise RuntimeError("RAW_REPLAY_CONFLICT")
print(json.dumps({"execution_id":r["execution_id"],"combined_benchmark_fingerprint":r["combined_benchmark_fingerprint"],"manifest_fingerprint":fingerprint,"raw_replay":"PASS","scoring_replay":"PASS","status":"PASS"},sort_keys=True))
