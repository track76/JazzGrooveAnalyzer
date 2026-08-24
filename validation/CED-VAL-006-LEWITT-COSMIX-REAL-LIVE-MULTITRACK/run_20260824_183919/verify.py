"""Independently verify the frozen CED-VAL-006 observational result."""
from collections import Counter
from hashlib import sha256
import json, math
from pathlib import Path

RUN = Path(__file__).resolve().parent
SR, HOP = 48000, 512

def canonical(x): return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
def digest(path):
    h=sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1048576),b""): h.update(block)
    return h.hexdigest()
def quantile(v,p):
    pos=(len(v)-1)*p; lo,hi=math.floor(pos),math.ceil(pos)
    return v[lo] if lo==hi else v[lo]*(hi-pos)+v[hi]*(pos-lo)
def stats(values):
    v=sorted(values); mean=math.fsum(v)/len(v)
    return {"minimum":v[0],"q1":quantile(v,.25),"median":quantile(v,.5),"q3":quantile(v,.75),"maximum":v[-1],
            "mean":mean,"population_standard_deviation":math.sqrt(math.fsum((x-mean)**2 for x in v)/len(v))}
def coordinate(item,prefix=""):
    frame=item[prefix+"producer_frame"]; sample=item[prefix+"producer_sample_coordinate"]
    timestamp=item["target_timestamp_seconds"] if prefix else item["timestamp_seconds"]
    assert sample==HOP*frame and timestamp==sample/SR
def reference(x):
    if x is not None: coordinate(x)

def main():
    content=json.loads((RUN/"scientific_content.json").read_text()); result=json.loads((RUN/"result.json").read_text())
    manifest=json.loads((RUN/"artifact_manifest.json").read_text())
    assert sha256(canonical(content)).hexdigest()==result["scientific_fingerprint"]
    for name,expected in manifest["artifacts"].items(): assert digest(RUN/name)==expected,name
    candidates=content["pulse_candidates_without_strength_or_confidence"]; events=content["elementary_metric_events"]
    for source in ("Drums","Double Bass"):
        ids={x["pulse_candidate_id"] for x in candidates[source]}
        assert len(ids)==len(candidates[source])==len(events[source])
        for x in candidates[source]+events[source]: coordinate(x)
        assert all(len(x["supporting_pulse_candidate_ids"])==1 and x["supporting_pulse_candidate_ids"][0] in ids for x in events[source])
    assert (len(events["Drums"]),len(events["Double Bass"]))==(909,1055)
    locs=content["drum_relative_localizations"]
    assert len(locs)==1055==len({x["target_eme_id"] for x in locs})
    for x in locs:
        coordinate(x,"target_")
        for key in ("preceding_drum_reference","following_drum_reference","nearest_drum_reference"): reference(x[key])
    assert Counter(x["relationship_status"] for x in locs)=={"GEOMETRIC_ONLY":1055}
    summary=content["geometry_summary"]
    assert (summary["eligible_count"],summary["localized_count"],summary["unresolved_count"])==(1055,1055,0)
    signed=[x["nearest_signed_displacement_seconds"] for x in locs]; absolute=[abs(x) for x in signed]
    assert signed==summary["signed_displacement_seconds"] and absolute==summary["absolute_displacement_seconds"]
    assert stats(signed)==summary["signed_displacement_descriptive"]["seconds"]
    assert stats(absolute)==summary["absolute_displacement_descriptive"]["seconds"]
    profile=content["rhythm_section_timing_profile"]
    assert profile["represented_observation_count"]==1964
    assert profile["source_counts"]=={"Drums":909,"Double Bass":1055}
    assert profile["relationship_status_counts"]=={"GEOMETRIC_ONLY":1055}
    assert content["temporal_mapping"]=={"native_sample_rate_hz":48000,"resampling":False,"hop_samples":512,
      "producer_sample_coordinate_rule":"512 * producer_frame","timestamp_rule":"producer_sample_coordinate / 48000"}
    assert content["deterministic_replay"]=="PASS_EXACT_TWO_FRESH_PROCESS_EXECUTIONS"
    fw=content["firewalls"]; assert fw["correspondence_status"]=="GEOMETRIC_ONLY" and fw["calibration_applicability"]=="UNESTABLISHED"
    assert all(v is False for k,v in fw.items() if k not in ("correspondence_status","calibration_applicability"))
    assert not list(RUN.rglob("__pycache__"))
    print("PASS: artifacts, fingerprint, 48 kHz mapping, AD-037 lineage, AD-038 geometry/statistics, AD-040 profile, replay, firewalls")

if __name__=="__main__": main()
