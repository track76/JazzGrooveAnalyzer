#!/usr/bin/env python3
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def canonical(v): return json.dumps(v,ensure_ascii=True,allow_nan=False,sort_keys=True,separators=(",",":")).encode("ascii")
def digest(p): return sha256(p.read_bytes()).hexdigest()
r1,r2=HERE/"run_1",HERE/"run_2"; names=sorted(x.name for x in r1.iterdir()); assert names==sorted(x.name for x in r2.iterdir())
for name in names: assert (r1/name).read_bytes()==(r2/name).read_bytes()
a=json.loads((r1/"audit.json").read_text()); afp=a.pop("audit_fingerprint"); assert sha256(canonical(a)).hexdigest()==afp
r=json.loads((HERE/"result.json").read_text()); rfp=r.pop("result_record_fingerprint"); assert sha256(canonical(r)).hexdigest()==rfp
assert r["audit_fingerprint"]==afp and r["spectral_eq_hypothesis"]=="NO"
assert r["population_counts"]=={"A_STABLE":374,"B_RECOVERED":140,"C1_NEVER_MATCHED":296,"C2_LOST":13,"D_PROCESSED_ONLY":188,"E_CHANGED_SELECTION":232}
assert r["replay"]["all_png_and_npy_byte_identical"] and all(v is False for v in r["firewall"].values())
m=json.loads((HERE/"artifact_manifest.json").read_text())
for name,expected in m["artifacts"].items(): assert digest(HERE/name)==expected
print("PASS",afp,rfp)
