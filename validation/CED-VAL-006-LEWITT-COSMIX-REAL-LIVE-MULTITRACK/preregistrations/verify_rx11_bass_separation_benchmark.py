#!/usr/bin/env python3
"""Verify the RX benchmark preregistration without requiring an RX output."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
P=HERE/"H-CEDVAL006-RX11-BASS-SEPARATION-BENCHMARK-01.json"
def canonical(v): return json.dumps(v,ensure_ascii=True,allow_nan=False,sort_keys=True,separators=(",",":")).encode("ascii")
d=json.loads(P.read_text()); fp=d.pop("preregistration_fingerprint"); assert sha256(canonical(d)).hexdigest()==fp
assert d["status"]=="PREREGISTERED_AWAITING_MANUAL_RX_EXPORT"
assert d["input_authority"]["sha256"]=="32845a5d05538524b19c8f857b0a908f6618cc4b95110a14169f1e450ddfe6e0"
assert d["rx_authority"]["version"]=="11.2.0" and d["rx_authority"]["build"]=="11.2.0.4231"
assert d["rx_configuration"]["stems"]["Bass"]["solo"] is True
assert sum(x["solo"] for x in d["rx_configuration"]["stems"].values())==1
assert all(v is False for v in d["scientific_firewalls"].values())
print("PASS",fp)
