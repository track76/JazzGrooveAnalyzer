#!/usr/bin/env python3
import hashlib,json,statistics
from pathlib import Path
HERE=Path(__file__).resolve().parent
r=json.loads((HERE/"run_1/audit.json").read_text())
bands=["30_80_hz","80_160_hz","160_320_hz","320_500_hz","500_1000_hz","1000_2000_hz"]
summary={}
for pop,rows in r["complete_records"].items():
 summary[pop]={b:{"controlled_mix_attack_baseline_contrast_db_median":statistics.median(x["descriptors"]["controlled_mix"]["bands"][b]["attack_baseline_contrast_db"] for x in rows),"original_bass_attack_baseline_contrast_db_median":statistics.median(x["descriptors"]["original_bass"]["bands"][b]["attack_baseline_contrast_db"] for x in rows)} for b in bands}
(HERE/"fixed_band_summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
(HERE/"result.json").write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
manifest={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob("*")) if p.is_file() and p.name!="artifact_manifest.json"}
(HERE/"artifact_manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
