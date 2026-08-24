"""Independent integrity checks for frozen physical-to-JGA result."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

RUN=Path("validation/CED-VAL-004-PHYSICAL-ONSET/run_20260824_112730")
SR=44100

def checksum(path):
    h=sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

result=json.loads((RUN/"result.json").read_text())
observed=json.loads((RUN/"observed_populations.json").read_text())
blind=json.loads((RUN/"blind_correspondence.json").read_text())
records=json.loads((RUN/"event_level_results.json").read_text())
summary=json.loads((RUN/"source_summary.json").read_text())
scientific=json.loads((RUN/"scientific_content.json").read_text())
artifacts=json.loads((RUN/"artifact_manifest.json").read_text())

assert result["status"]=="PASS_FROZEN_MEASUREMENT_RESULT"
assert result["scientific_fingerprint"]==sha256(json.dumps(scientific,sort_keys=True,separators=(",",":")).encode()).hexdigest()
assert len(records)==20 and len(blind["records"])==20
for source in ("Drums","Double Bass"):
    assert len(observed[source]["pulse_candidates"])==10
    assert len(observed[source]["elementary_metric_events"])==10
    assert summary[source]["physical_event_count"]==10
    assert summary[source]["valid_correspondence_count"]==10
    assert sum(summary[source][k] for k in ("unmatched_physical_event_count","ambiguous_multiple_observed_count","ambiguous_boundary_count","unmatched_observed_count"))==0
for source in observed.values():
    candidates={x["pulse_candidate_id"]:x for x in source["pulse_candidates"]}
    for eme in source["elementary_metric_events"]:
        assert eme["pulse_candidate_id"] in candidates
        assert eme["n_JGA"]==512*eme["producer_frame"]
        assert eme["timestamp_hex"]==candidates[eme["pulse_candidate_id"]]["timestamp_hex"]
for record in records:
    assert record["status"]=="VALID_PHYSICAL_JGA_CORRESPONDENCE"
    assert record["e_samples"]==record["n_JGA"]-record["n_physical"]
    assert record["abs_e_samples"]==abs(record["e_samples"])
    assert record["marker_to_JGA_samples"]==record["marker_to_physical_samples"]+record["physical_to_JGA_samples"]
    assert Fraction(record["e_seconds_exact"])==Fraction(record["e_samples"],SR)
    assert Fraction(record["e_ms_exact"])==Fraction(1000*record["e_samples"],SR)
assert result["firewalls"]=={"confidence_used":False,"h02_changed":False,"h03_created":False,"historical_results_changed":False,"jga_tuned":False,"production_code_changed":False,"raw_assets_changed":False,"strength_accessed":False}
for name, expected in artifacts["artifacts"].items():
    if name != "verify.py": assert checksum(RUN/name)==expected
print(json.dumps({"status":"PASS","cardinality":"20/20 VALID","frame_roundtrip":"PASS","decomposition":"PASS","firewalls":"PASS","scientific_fingerprint":result["scientific_fingerprint"]},indent=2))
