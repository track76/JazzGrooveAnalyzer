"""Execute frozen H-CEDVAL004-PHYSICAL-TO-JGA-COMPARISON-01."""
from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
from hashlib import sha256
import json
import platform
from pathlib import Path
import sys
import wave

import librosa

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline

getcontext().prec = 50
BASE = Path("validation/CED-VAL-004-PHYSICAL-ONSET")
RUN = BASE / "run_20260824_112730"
EXTERNAL = Path("/Volumes/SSD Track/JGA")
AUTHORITY = BASE / "input_authority_manifest.json"
SCHEDULE = BASE / "event_schedule.json"
PHYSICAL = BASE / "run_20260824_110800/event_level_physical_onsets.json"
PREREG = BASE / "preregistrations/H-CEDVAL004-PHYSICAL-TO-JGA-COMPARISON-01.md"
STUDY_ID = "H-CEDVAL004-PHYSICAL-TO-JGA-COMPARISON-01"
EXECUTION_ID = "EXEC-CEDVAL004-PHYSICAL-TO-JGA-20260824-112730"
DATASET_FP = "704ce5926852a2ff62d9794dbee48156f875016979214cf7ef3ab93aa35ec772"
PHYSICAL_FP = "7b2ec48f0ff0afca54849b5847f5ebd637c8d672eb2b88247ea6a1841af99062"
PREREG_COMMIT = "7338985a100d51b0d21de802f8b2befc6acb0bba"
SR, HOP, SCOPE = 44100, 512, 8820000
REPO_HASHES = {
    str(PREREG): "161d60f088462df54b07f1919f01a05c5fbed367ee6e9942a6a850a63299fcd5",
    str(AUTHORITY): "823893f86f5d8a8b68e5ef57dce47739454897e93321dac1b815c735330d429a",
    str(SCHEDULE): "458227636da615278d5334039630f916d1b8be200587c37ae16a4673e8afe2dc",
    str(PHYSICAL): "e8860a248325f5080077f51c833f39884c63cbedaa1671f549a6a7465729d7b2",
    "src/jga/pipeline/default_analysis_pipeline.py": "04ecdfee536717b977276b91b7e9416701e7a89ce9aa7bc4339917263725ef17",
    "src/jga/engines/source_pulse_candidate_builder.py": "5b270f352483dde91448b0958a299c08e51d064ab867bc872ef1cdde37a81c32",
    "src/jga/engines/domain_pulse_candidate_adapter.py": "6a3d276bf50534bc6823075a26787c624ab7a8d2ecca58628579fb86658a9330",
    "src/jga/domain/services/elementary_metric_event_builder.py": "137e390a69c9361d5cbfd66908256b2417d76c95d503e7ad2c409cd2e1b66cc2",
    "src/jga/domain/elementary_metric_event.py": "d9066db4bfe6ca75e2ce8e1d0a2b8a71ab86853f35d0fc04b8414632fab7da7b",
}

def canonical(value): return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
def checksum(path):
    h = sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""): h.update(chunk)
    return h.hexdigest()
def exact(v: Fraction): return f"{v.numerator}/{v.denominator}"
def dec(v: Fraction): return f"{Decimal(v.numerator)/Decimal(v.denominator):.15f}"
def write_json(path, value): Path(path).write_text(json.dumps(value, indent=2, sort_keys=True)+"\n")

def quantile(vals, p):
    pos = Fraction(len(vals)-1)*p; lo = pos.numerator//pos.denominator; hi = lo if pos.denominator == 1 else lo+1
    return Fraction(vals[lo]) if lo == hi else Fraction(vals[lo])*(1-(pos-lo))+Fraction(vals[hi])*(pos-lo)
def describe(values):
    if not values: return {"n": 0}
    vals=sorted(values); mean=Fraction(sum(vals),len(vals)); md=Decimal(mean.numerator)/Decimal(mean.denominator)
    var=sum((Decimal(v)-md)**2 for v in vals)/Decimal(len(vals))
    out={"n":len(vals),"quartile_method":"linear_interpolation_at_(n-1)*p","samples":{},"milliseconds":{}}
    for key,val in (("minimum",Fraction(vals[0])),("q1",quantile(vals,Fraction(1,4))),("median",quantile(vals,Fraction(1,2))),("q3",quantile(vals,Fraction(3,4))),("maximum",Fraction(vals[-1])),("mean",mean)):
        out["samples"][key]={"exact":exact(val),"decimal":dec(val)}
        ms=val*Fraction(1000,SR); out["milliseconds"][key]={"exact":exact(ms),"decimal":dec(ms)}
    sd=var.sqrt(); out["samples"]["population_standard_deviation"]=f"{sd:.15f}"; out["milliseconds"]["population_standard_deviation"]=f"{sd*Decimal(1000)/Decimal(SR):.15f}"
    return out

def verify_inputs():
    for path, expected in REPO_HASHES.items():
        if checksum(path) != expected: raise RuntimeError(f"AUTHORITY_CONFLICT checksum {path}")
    authority=json.loads(AUTHORITY.read_text()); frozen=authority.pop("dataset_fingerprint")
    if frozen != DATASET_FP or sha256(canonical(authority)).hexdigest()!=frozen: raise RuntimeError("AUTHORITY_CONFLICT dataset fingerprint")
    schedule=json.loads(SCHEDULE.read_text()); sfp=schedule.pop("schedule_fingerprint")
    if sha256(canonical(schedule)).hexdigest()!=sfp: raise RuntimeError("AUTHORITY_CONFLICT schedule fingerprint")
    if [x["marker_sample"] for x in schedule["events"]] != [88200+441000*k for k in range(20)]: raise RuntimeError("AUTHORITY_CONFLICT schedule")
    assets={}; paths={}
    for source in ("Drums","Double Bass"):
        ref=authority["canonical_assets"][source]; path=EXTERNAL/ref["path"]
        if checksum(path)!=ref["sha256"]: raise RuntimeError(f"AUTHORITY_CONFLICT asset {source}")
        with wave.open(str(path),"rb") as w: props={"channels":w.getnchannels(),"sample_width_bytes":w.getsampwidth(),"sample_rate_hz":w.getframerate(),"frame_count":w.getnframes(),"compression":w.getcomptype()}
        if props!={"channels":2,"sample_width_bytes":3,"sample_rate_hz":SR,"frame_count":SCOPE,"compression":"NONE"}: raise RuntimeError(f"AUTHORITY_CONFLICT WAV {source}")
        paths[source]=path; assets[source]={**ref,"properties":props}
    ph=json.loads(PHYSICAL.read_text())
    if ph["scientific_fingerprint"]!=PHYSICAL_FP or len(ph["records"])!=20 or any(r["status"]!="VALID_PHYSICAL_ONSET" for r in ph["records"]): raise RuntimeError("AUTHORITY_CONFLICT physical authority")
    return schedule,paths,assets,sfp

def observation_once(paths):
    result={}
    for source,path in paths.items():
        ctx=AnalysisPipeline().analyze(str(path)); candidates={str(x.id):x for x in ctx.domain_pulse_candidates}
        emes=[]
        for eme in ctx.elementary_metric_events:
            ids=[str(x) for x in eme.supporting_pulse_candidate_ids]
            if len(ids)!=1 or ids[0] not in candidates: raise RuntimeError("AUTHORITY_CONFLICT lineage")
            candidate=candidates[ids[0]]
            if candidate.timestamp.hex()!=eme.timestamp.hex(): raise RuntimeError("AUTHORITY_CONFLICT timestamp lineage")
            frame=round(eme.timestamp*SR/HOP); reconstructed=float(librosa.frames_to_time(frame,sr=SR,hop_length=HOP))
            if reconstructed.hex()!=eme.timestamp.hex(): raise RuntimeError(f"AUTHORITY_CONFLICT frame roundtrip {eme.id}")
            emes.append({"eme_id":str(eme.id),"pulse_candidate_id":ids[0],"observation_index":candidate.observation_index,"observation_provenance_id":candidate.observation_provenance_id,"contributor_id":str(eme.contributor_id),"sound_source_id":str(eme.sound_source_id),"source_asset_sha256":eme.source_asset_sha256,"temporal_scope":eme.temporal_scope,"materialization_rule":eme.materialization_rule,"timestamp_binary64":eme.timestamp,"timestamp_hex":eme.timestamp.hex(),"producer_frame":frame,"n_JGA":HOP*frame})
        cand=[{"pulse_candidate_id":str(x.id),"observation_index":x.observation_index,"observation_provenance_id":x.observation_provenance_id,"sound_source_id":str(x.sound_source_id),"timestamp_binary64":x.timestamp,"timestamp_hex":x.timestamp.hex(),"producer_frame":round(x.timestamp*SR/HOP),"n_JGA":HOP*round(x.timestamp*SR/HOP)} for x in ctx.domain_pulse_candidates]
        result[source]={"pulse_candidates":sorted(cand,key=lambda x:(x["n_JGA"],x["pulse_candidate_id"])),"elementary_metric_events":sorted(emes,key=lambda x:(x["n_JGA"],x["eme_id"]))}
    return result

def blind_correspondence(schedule, observed):
    records=[]; consumed={s:set() for s in observed}; boundaries_out={s:[] for s in observed}
    for source in ("Drums","Double Bass"):
        events=[e for e in schedule["events"] if e["source"]==source]; markers=[e["marker_sample"] for e in events]
        boundaries=[Fraction(markers[i]+markers[i+1],2) for i in range(9)]
        emes=observed[source]["elementary_metric_events"]
        for i,event in enumerate(events):
            left=Fraction(0) if i==0 else boundaries[i-1]; right=Fraction(SCOPE) if i==9 else boundaries[i]
            boundary=[e for e in emes if Fraction(e["n_JGA"]) in boundaries]
            inside=[e for e in emes if left <= e["n_JGA"] < right and Fraction(e["n_JGA"]) not in boundaries]
            for e in inside: consumed[source].add(e["eme_id"])
            for e in boundary: boundaries_out[source].append(e["eme_id"])
            status="UNMATCHED_PHYSICAL_EVENT" if len(inside)==0 else "VALID_PHYSICAL_JGA_CORRESPONDENCE" if len(inside)==1 else "AMBIGUOUS_MULTIPLE_OBSERVED"
            records.append({"event_id":event["event_id"],"source":source,"marker_sample":event["marker_sample"],"cell":{"left_exact":exact(left),"right_exact":exact(right),"left_closed":True,"right_open":True},"status":status,"observed_count":len(inside),"eme_ids":[e["eme_id"] for e in inside],"observations":inside})
    unmatched={}
    for source in observed:
        all_ids={e["eme_id"] for e in observed[source]["elementary_metric_events"]}; b=set(boundaries_out[source]); unmatched[source]=sorted(all_ids-consumed[source]-b)
    return {"records":records,"boundary_eme_ids":{s:sorted(set(v)) for s,v in boundaries_out.items()},"unmatched_observed_eme_ids":unmatched}

def measure(blind):
    ph={r["event_id"]:r for r in json.loads(PHYSICAL.read_text())["records"]}; records=[]
    for r in blind["records"]:
        out={k:v for k,v in r.items() if k!="observations"}; out["physical_authority_id"]=r["event_id"]
        if r["status"]=="VALID_PHYSICAL_JGA_CORRESPONDENCE":
            obs=r["observations"][0]; p=ph[r["event_id"]]; n=obs["n_JGA"]-p["n_physical"]
            marker_phys=p["n_physical"]-p["marker_sample"]; marker_jga=obs["n_JGA"]-p["marker_sample"]
            if marker_jga != marker_phys+n: raise RuntimeError("decomposition failure")
            out.update({"selected_eme_id":obs["eme_id"],"producer_frame":obs["producer_frame"],"n_JGA":obs["n_JGA"],"n_physical":p["n_physical"],"t_JGA_exact":exact(Fraction(obs["n_JGA"],SR)),"t_physical_exact":p["t_physical"]["seconds_exact"],"e_samples":n,"e_seconds_exact":exact(Fraction(n,SR)),"e_ms_exact":exact(Fraction(1000*n,SR)),"e_ms_decimal":dec(Fraction(1000*n,SR)),"abs_e_samples":abs(n),"abs_e_seconds_exact":exact(Fraction(abs(n),SR)),"abs_e_ms_exact":exact(Fraction(1000*abs(n),SR)),"abs_e_ms_decimal":dec(Fraction(1000*abs(n),SR)),"marker_to_physical_samples":marker_phys,"marker_to_JGA_samples":marker_jga,"physical_to_JGA_samples":n,"decomposition_verified":True})
        records.append(out)
    return records

def summarize(source, observed, records, blind):
    selected=[r for r in records if r["source"]==source]; valid=[r for r in selected if r["status"]=="VALID_PHYSICAL_JGA_CORRESPONDENCE"]
    errors=[r["e_samples"] for r in valid]; absolute=[abs(x) for x in errors]
    return {"physical_event_count":len(selected),"observed_eme_count":len(observed[source]["elementary_metric_events"]),"observed_pulse_candidate_count":len(observed[source]["pulse_candidates"]),"valid_correspondence_count":len(valid),"unmatched_physical_event_count":sum(r["status"]=="UNMATCHED_PHYSICAL_EVENT" for r in selected),"ambiguous_multiple_observed_count":sum(r["status"]=="AMBIGUOUS_MULTIPLE_OBSERVED" for r in selected),"ambiguous_boundary_count":len(blind["boundary_eme_ids"][source]),"unmatched_observed_count":len(blind["unmatched_observed_eme_ids"][source]),"signed_error_samples_in_event_order":errors,"signed_error_ms_in_event_order":[dec(Fraction(1000*x,SR)) for x in errors],"absolute_error_samples_in_event_order":absolute,"absolute_error_ms_in_event_order":[dec(Fraction(1000*x,SR)) for x in absolute],"signed_error_descriptive":describe(errors),"absolute_error_descriptive":describe(absolute),"exact_zero_count":sum(x==0 for x in errors),"negative_early_count":sum(x<0 for x in errors),"positive_late_count":sum(x>0 for x in errors)}

def main():
    schedule,paths,assets,schedule_fp=verify_inputs()
    first_obs=observation_once(paths); first_blind=blind_correspondence(schedule,first_obs)
    blind_basis={"study_id":STUDY_ID,"dataset_fingerprint":DATASET_FP,"schedule_fingerprint":schedule_fp,"observed":first_obs,"correspondence":first_blind,"strength_accessed":False}
    blind_fp=sha256(canonical(blind_basis)).hexdigest()
    first_records=measure(first_blind); first_summary={s:summarize(s,first_obs,first_records,first_blind) for s in ("Drums","Double Bass")}
    second_obs=observation_once(paths); second_blind=blind_correspondence(schedule,second_obs); second_records=measure(second_blind); second_summary={s:summarize(s,second_obs,second_records,second_blind) for s in ("Drums","Double Bass")}
    if canonical((first_obs,first_blind,first_records,first_summary)) != canonical((second_obs,second_blind,second_records,second_summary)): raise RuntimeError("deterministic replay failure")
    scientific={"study_id":STUDY_ID,"dataset_fingerprint":DATASET_FP,"physical_authority_fingerprint":PHYSICAL_FP,"blind_fingerprint":blind_fp,"observed":first_obs,"blind_correspondence":first_blind,"event_level_results":first_records,"source_summary":first_summary,"frame_authority":{"sample_rate_hz":SR,"hop_samples":HOP,"spacing_seconds_exact":"512/44100","spacing_ms_decimal":dec(Fraction(512000,SR)),"all_n_JGA_on_lattice":all(e["n_JGA"]%HOP==0 for s in first_obs.values() for e in s["elementary_metric_events"])},"firewalls":{"strength_accessed":False,"confidence_used":False,"jga_tuned":False,"h02_changed":False,"h03_created":False,"historical_results_changed":False,"raw_assets_changed":False,"production_code_changed":False},"deterministic_replay":"PASS_EXACT"}
    fp=sha256(canonical(scientific)).hexdigest()
    manifest={"dataset_authority_id":"PR-CED-VAL-004-PHYSICAL-ONSET-001","dataset_fingerprint":DATASET_FP,"physical_authority_fingerprint":PHYSICAL_FP,"preregistration_id":STUDY_ID,"preregistration_commit":PREREG_COMMIT,"repository_and_authority_checksums":REPO_HASHES,"canonical_assets":assets,"environment":{"python":sys.version,"platform":platform.platform(),"librosa":librosa.__version__},"authority_gate":"PASS"}
    result={"schema":"JGA-PHYSICAL-TO-JGA-RESULT/v1","status":"PASS_FROZEN_MEASUREMENT_RESULT","scientific_fingerprint":fp,"blind_fingerprint":blind_fp,"source_summary":first_summary,"deterministic_replay":"PASS_EXACT","firewalls":scientific["firewalls"]}
    write_json(RUN/"input_manifest.json",manifest); write_json(RUN/"observed_populations.json",first_obs); write_json(RUN/"blind_correspondence.json",{"blind_fingerprint":blind_fp,**first_blind}); write_json(RUN/"event_level_results.json",first_records); write_json(RUN/"source_summary.json",first_summary); write_json(RUN/"scientific_content.json",scientific); write_json(RUN/"result.json",result)
    write_json(RUN/"completion_protocol.json",{"study_id":STUDY_ID,"status":result["status"],"authority_gate":"PASS","deterministic_replay":"PASS_EXACT","producer_frame_roundtrip":"PASS_ALL","marker_decomposition":"PASS_ALL_VALID","scientific_fingerprint":fp})
    lines=[f"# {STUDY_ID} frozen result","",f"Status: **{result['status']}**","",f"Scientific fingerprint: `{fp}`.","",f"Blind fingerprint: `{blind_fp}`.",""]
    for s in ("Drums","Double Bass"):
        x=first_summary[s]; lines += [f"## {s}","",f"Physical/EME: {x['physical_event_count']}/{x['observed_eme_count']}; valid {x['valid_correspondence_count']}; unmatched physical {x['unmatched_physical_event_count']}; ambiguous multiple {x['ambiguous_multiple_observed_count']}; ambiguous boundary {x['ambiguous_boundary_count']}; unmatched observed {x['unmatched_observed_count']}.","",f"Signed samples: `{x['signed_error_samples_in_event_order']}`.","",f"Signed ms: `{x['signed_error_ms_in_event_order']}`.",""]
    lines += ["## Firewalls","","Strength and confidence were not used or emitted. JGA was not tuned. H02, historical results, raw assets, architecture, and production code remain unchanged.",""]
    (RUN/"report.md").write_text("\n".join(lines))
    artifacts=["execute.py","input_manifest.json","observed_populations.json","blind_correspondence.json","event_level_results.json","source_summary.json","scientific_content.json","result.json","completion_protocol.json","report.md"]
    write_json(RUN/"artifact_manifest.json",{"study_id":STUDY_ID,"scientific_fingerprint":fp,"artifacts":{n:checksum(RUN/n) for n in artifacts}})
    print(json.dumps({"status":result["status"],"fingerprint":fp,"blind_fingerprint":blind_fp,"summary":first_summary},indent=2))

if __name__ == "__main__": main()
