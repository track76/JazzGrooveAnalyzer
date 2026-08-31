#!/usr/bin/env python3
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def canonical(v): return json.dumps(v,ensure_ascii=True,allow_nan=False,sort_keys=True,separators=(",",":")).encode("ascii")
def digest(p): return sha256(p.read_bytes()).hexdigest()
r1,r2=HERE/"run_1",HERE/"run_2"
names1,names2=sorted(x.name for x in r1.iterdir()),sorted(x.name for x in r2.iterdir())
assert names1==names2
for name in names1: assert (r1/name).read_bytes()==(r2/name).read_bytes()
audit=json.loads((r1/"audit.json").read_text()); fp=audit.pop("audit_fingerprint"); assert sha256(canonical(audit)).hexdigest()==fp
result=json.loads((HERE/"result.json").read_text()); rfp=result.pop("result_record_fingerprint"); assert sha256(canonical(result)).hexdigest()==rfp
assert result["audit_fingerprint"]==fp
assert result["transition_results"]["DISAPPEARING"]["count"]==250
assert result["transition_results"]["NEWLY_OBSERVABLE"]["count"]==538
assert result["prospective_non_ground_truth_principle"]=="INDETERMINATE"
assert result["replay"]["all_corresponding_pngs_byte_identical"] is True
assert all(value is False for value in result["firewall"].values())
manifest=json.loads((HERE/"artifact_manifest.json").read_text())
for name,expected in manifest["artifacts"].items():
    if name not in {"artifact_manifest.json"}: assert digest(HERE/name)==expected
print("PASS",fp,rfp)
