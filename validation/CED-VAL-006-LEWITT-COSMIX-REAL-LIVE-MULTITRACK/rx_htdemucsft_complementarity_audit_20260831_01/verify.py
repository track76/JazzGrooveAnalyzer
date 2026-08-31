#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
a = HERE / "audit_execution_1.json"
b = HERE / "audit_execution_2.json"
assert a.read_bytes() == b.read_bytes()
r = json.loads(a.read_text())
assert sum(r["partition"][k]["count"] for k in r["partition"]) == 1055
assert r["overlap"]["intersection_count"] == r["partition"]["A_BOTH"]["count"]
assert r["overlap"]["union_count"] == sum(r["partition"][k]["count"] for k in ("A_BOTH", "B_DEMUCS_ONLY", "C_RX_ONLY"))
fingerprint = r.pop("audit_fingerprint")
payload = json.dumps(r, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
assert hashlib.sha256(payload.encode()).hexdigest() == fingerprint
print("PASS: exhaustive partition, identities, fingerprint, and byte-identical replay verified")
manifest_path = HERE / "artifact_manifest.json"
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text())
    for name, expected in manifest.items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected, name
    print("PASS: artifact manifest verified")
