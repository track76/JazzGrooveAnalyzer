#!/usr/bin/env python3
"""Verify the prospective RX sensitivity-scale correction."""
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
P=HERE/"H-CEDVAL006-RX11-BASS-SEPARATION-BENCHMARK-01-R1.json"
ORIGINAL=HERE/"H-CEDVAL006-RX11-BASS-SEPARATION-BENCHMARK-01.json"
def canonical(v): return json.dumps(v,ensure_ascii=True,allow_nan=False,sort_keys=True,separators=(",",":")).encode("ascii")
d=json.loads(P.read_text()); fp=d.pop("preregistration_fingerprint"); assert sha256(canonical(d)).hexdigest()==fp
assert d["evidence_conflict_resolution"]["render_performed"] is False
assert d["evidence_conflict_resolution"]["other_protocol_fields_changed"] is False
stems=d["rx_configuration"]["stems"]
assert set(stems)=={"Vocal","Bass","Drums","Other"}
assert all(x["sensitivity_ui_value"]==50 and x["sensitivity_ui_scale"]==[0,100] and x["sensitivity_state"]=="RESET_DEFAULT_MIDPOINT" for x in stems.values())
assert sum(x["solo"] for x in stems.values())==1 and stems["Bass"]["solo"]
original=json.loads(ORIGINAL.read_text())
for key in original:
    if key not in {"preregistration_id","status","rx_configuration","preregistration_fingerprint"}:
        assert original[key]==d[key]
old_config=dict(original["rx_configuration"]); old_stems=old_config.pop("stems")
new_config=dict(d["rx_configuration"]); new_stems=new_config.pop("stems")
assert old_config==new_config
for old,new in (("Vocals","Vocal"),("Bass","Bass"),("Percussion","Drums"),("Other","Other")):
    for field in ("gain_db","solo","mute"):
        assert old_stems[old][field]==new_stems[new][field]
print("PASS",fp)
