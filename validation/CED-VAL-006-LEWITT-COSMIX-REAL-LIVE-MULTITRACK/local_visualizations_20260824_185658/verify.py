"""Verify the frozen CED-VAL-006 local visualization authority."""
from hashlib import sha256
import json
from pathlib import Path
RUN=Path(__file__).resolve().parent
def canonical(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def checksum(path):
 h=sha256()
 with Path(path).open("rb") as f:
  for block in iter(lambda:f.read(1048576),b""): h.update(block)
 return h.hexdigest()
def main():
 result=json.loads((RUN/"result.json").read_text()); manifest=json.loads((RUN/"artifact_manifest.json").read_text())
 for name,expected in manifest["artifacts"].items(): assert checksum(RUN/name)==expected,name
 for w in result["scientific_record"]["windows"]:
  basis={k:v for k,v in w.items() if k!="scientific_content_fingerprint"}
  assert sha256(canonical(basis)).hexdigest()==w["scientific_content_fingerprint"]
  assert w["duration_sample_frames"]==240000==w["end_sample_frame_exclusive"]-w["start_sample_frame"]
  assert w["total_eme_count"]==w["drums_eme_count"]+w["double_bass_eme_count"]
  assert w["eligible_frozen_localization_count"]==w["double_bass_eme_count"]
  assert w["connectors_rendered_count"]+w["display_boundary_censoring_count"]==w["eligible_frozen_localization_count"]
 basis={k:result[k] for k in ("scientific_record","per_window_scientific_content_fingerprints","png_sha256","scientific_content_replay","png_byte_replay")}
 assert sha256(canonical(basis)).hexdigest()==result["aggregate_visualization_fingerprint"]
 assert result["scientific_content_replay"] is True and result["png_byte_replay"] is True
 fw=result["scientific_record"]["firewalls"]; assert all(v is False for v in fw.values())
 assert not list(RUN.rglob("__pycache__")) and not list(RUN.rglob("*.pyc"))
 print("PASS_FROZEN_CEDVAL006_FIVE_WINDOW_LOCAL_NEUTRAL_VISUALIZATIONS")
 print(result["aggregate_visualization_fingerprint"])
if __name__=="__main__": main()
