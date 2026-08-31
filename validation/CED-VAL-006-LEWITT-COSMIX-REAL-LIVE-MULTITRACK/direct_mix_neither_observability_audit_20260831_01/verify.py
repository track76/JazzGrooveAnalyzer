#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
r1,r2=HERE/"run_1",HERE/"run_2"
for rel in sorted(p.relative_to(r1) for p in r1.rglob("*") if p.is_file()):
 a,b=r1/rel,r2/rel; assert b.exists() and a.read_bytes()==b.read_bytes(),rel
r=json.loads((r1/"audit.json").read_text()); fp=r.pop("audit_fingerprint"); payload=json.dumps(r,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii"); assert hashlib.sha256(payload).hexdigest()==fp
assert sum(x["count"] for x in r["population_summaries"].values())==1055
print("PASS: complete output byte identity, fingerprint, and population authority verified")
manifest_path=HERE/"artifact_manifest.json"
if manifest_path.exists():
 manifest=json.loads(manifest_path.read_text())
 for rel,expected in manifest.items(): assert hashlib.sha256((HERE/rel).read_bytes()).hexdigest()==expected,rel
 print("PASS: artifact manifest verified")
