"""Render frozen CED-VAL-006 five-window neutral visualizations."""
from hashlib import sha256
import json, shutil, tempfile
from pathlib import Path

BASE=Path("validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK")
SOURCE=BASE/"run_20260824_183919"; RUN=BASE/"local_visualizations_20260824_185658"
PREREG=BASE/"preregistrations/H-CEDVAL006-FIVE-WINDOW-LOCAL-NEUTRAL-VISUALIZATION-01.md"
STUDY="H-CEDVAL006-FIVE-WINDOW-LOCAL-NEUTRAL-VISUALIZATION-01"
EXECUTION="EXEC-CEDVAL006-LOCAL-VISUALIZATION-20260824-185658"
SOURCE_EXECUTION="EXEC-CEDVAL006-REAL-LIVE-AUDIO-20260824-183919"
SOURCE_FP="8c5723fbeabe2031516b2eeee0c83fb42ad84f46824cf65f5d485c6cf6c82b5c"
SR,HOP,SCOPE=48000,512,11912868
WINDOWS=(("W1",0,1191286,1071286,1311286),("W2",1,3573860,3453860,3693860),
         ("W3",2,5956434,5836434,6076434),("W4",3,8339007,8219007,8459007),
         ("W5",4,10721581,10601581,10841581))
INPUT_HASHES={"elementary_metric_events.json":"64db95d8feeb6ab7ca22aa8081e177c57d6ab57c9f0aaf3bb4a5650db28329f5",
 "drum_relative_localizations.json":"a1f401a8c26f894ee36fa68f924008393410048da64ebb874b415611c796c51a",
 "rhythm_section_timing_profile.json":"32c599c5a14f12577a8b7562aeff19b7ef0507b6e348a82a6093461e246dc008",
 "artifact_manifest.json":"53abec045bb26beb29c123fa564c740cef6c6da82298c91f8718679108e25ba0"}
AUTHORITY_HASHES={str(PREREG):"ceab140853db3f7d6aaa7e06dfbdcdad7fb7b23ff5040c5ab60df726b0ca1e4c"}

def canonical(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def checksum(path):
 h=sha256()
 with Path(path).open("rb") as f:
  for block in iter(lambda:f.read(1048576),b""): h.update(block)
 return h.hexdigest()
def write(path,x): Path(path).write_text(json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+"\n")

def load():
 for name,expected in INPUT_HASHES.items():
  if checksum(SOURCE/name)!=expected: raise RuntimeError(f"FROZEN_INPUT_CONFLICT:{name}")
 for name,expected in AUTHORITY_HASHES.items():
  if checksum(name)!=expected: raise RuntimeError(f"PREREGISTRATION_CONFLICT:{name}")
 manifest=json.loads((SOURCE/"artifact_manifest.json").read_text())
 if manifest["execution_id"]!=SOURCE_EXECUTION or manifest["scientific_fingerprint"]!=SOURCE_FP:
  raise RuntimeError("SOURCE_AUTHORITY_CONFLICT")
 events=json.loads((SOURCE/"elementary_metric_events.json").read_text())
 locs=json.loads((SOURCE/"drum_relative_localizations.json").read_text())
 profile=json.loads((SOURCE/"rhythm_section_timing_profile.json").read_text())
 if (len(events["Drums"]),len(events["Double Bass"]),len(locs))!=(909,1055,1055): raise RuntimeError("POPULATION_CONFLICT")
 for records in events.values():
  for e in records:
   sample=e["producer_sample_coordinate"]
   if sample!=HOP*e["producer_frame"] or e["timestamp_seconds"]!=sample/SR or e["timestamp_seconds"].hex()!=e["timestamp_hex"]:
    raise RuntimeError(f"COORDINATE_CONFLICT:{e['eme_id']}")
 for _,_,_,start,end in WINDOWS:
  if not (0<=start<end<=SCOPE and end-start==240000): raise RuntimeError("WINDOW_CONFLICT")
 return events,locs,profile

def build(events,locs,profile):
 by_target={x["target_eme_id"]:x for x in locs}; windows=[]
 for wid,stratum,center,start,end in WINDOWS:
  drums=[x for x in events["Drums"] if start<=x["producer_sample_coordinate"]<end]
  bass=[x for x in events["Double Bass"] if start<=x["producer_sample_coordinate"]<end]
  drum_ids={x["eme_id"] for x in drums}; included=[]; connectors=[]; censored=[]; ties=[]
  for event in bass:
   loc=by_target.get(event["eme_id"])
   if loc is None: raise RuntimeError(f"LOCALIZATION_MISSING:{event['eme_id']}")
   included.append(loc)
   if loc["nearest_selection_status"]=="EQUAL_DISTANCE_TIE": ties.append(loc["localization_id"])
   ref=loc["nearest_drum_reference"]
   if ref is None: raise RuntimeError(f"FROZEN_REFERENCE_MISSING:{event['eme_id']}")
   decision={"localization_id":loc["localization_id"],"bass_eme_id":event["eme_id"],"drum_eme_id":ref["eme_id"],
             "bass_timestamp_seconds":event["timestamp_seconds"],"drum_timestamp_seconds":ref["timestamp_seconds"]}
   (connectors if ref["eme_id"] in drum_ids else censored).append(decision)
  record={"window_id":wid,"stratum_index":stratum,"center_sample_frame":center,"center_time_seconds":center/SR,
   "start_sample_frame":start,"end_sample_frame_exclusive":end,"start_time_seconds":start/SR,
   "end_time_seconds_exclusive":end/SR,"duration_sample_frames":end-start,"duration_seconds":(end-start)/SR,
   "drums_eme_count":len(drums),"double_bass_eme_count":len(bass),"total_eme_count":len(drums)+len(bass),
   "eligible_frozen_localization_count":len(included),"connectors_rendered_count":len(connectors),
   "display_boundary_censoring_count":len(censored),"nearest_tie_count":len(ties),
   "included_drums_eme_ids":[x["eme_id"] for x in drums],"included_double_bass_eme_ids":[x["eme_id"] for x in bass],
   "included_localization_ids":[x["localization_id"] for x in included],"nearest_tie_localization_ids":ties,
   "connectors":connectors,"display_boundary_censoring":censored,"drums_events":drums,"double_bass_events":bass,
   "source_execution_id":SOURCE_EXECUTION,"source_scientific_fingerprint":SOURCE_FP,"profile_id":profile["profile_id"],
   "correspondence_status":"GEOMETRIC_ONLY","calibration_applicability":"UNESTABLISHED",
   "acquisition_authority":{"live_performance":"SUPPORTED_BY_LEWITT_PROVIDER_DECLARATION",
   "raw_no_editing_no_tuning":"SUPPORTED_TO_THE_EXTENT_DECLARED","shared_hardware_clock":"UNESTABLISHED",
   "common_session_time_origin":"UNESTABLISHED","physical_onset":"NOT_ESTABLISHED"}}
  basis={k:v for k,v in record.items() if k not in {"scientific_content_fingerprint","drums_events","double_bass_events"}}
  record["scientific_content_fingerprint"]=sha256(canonical(basis)).hexdigest(); windows.append(record)
 return {"schema":"JGA-CEDVAL006-LOCAL-NEUTRAL-VISUALIZATION/v1","study_id":STUDY,"execution_id":EXECUTION,
  "source_execution_id":SOURCE_EXECUTION,"source_scientific_fingerprint":SOURCE_FP,"membership_coordinate":"producer_sample_coordinate",
  "membership_rule":"start_sample_frame <= producer_sample_coordinate < end_sample_frame",
  "frame_lattice":{"hop_samples":HOP,"sample_rate_hz":SR,"seconds":HOP/SR},"windows":windows,
  "acquisition_authority_status":"PARTIAL_STRICTLY_BOUNDED_AS_RECORDED","correspondence_status":"GEOMETRIC_ONLY",
  "calibration_applicability":"UNESTABLISHED","firewalls":{"jga_rerun":False,"external_tracker_used":False,"bpm_used":False,
  "h02_used":False,"strength_accessed":False,"musical_interpretation_performed":False,"raw_assets_changed":False,
  "historical_authorities_changed":False,"production_code_changed":False}}

def render(content,directory):
 import matplotlib; matplotlib.use("Agg")
 import matplotlib.pyplot as plt
 directory.mkdir(parents=True,exist_ok=True); hashes={}
 for item in content["windows"]:
  fig,ax=plt.subplots(figsize=(14,4.5),constrained_layout=True)
  for e in item["drums_events"]: ax.scatter(e["timestamp_seconds"],1.0,s=22,marker="|",linewidths=1.2,color="#242424",zorder=3)
  for e in item["double_bass_events"]: ax.scatter(e["timestamp_seconds"],0.0,s=22,marker="|",linewidths=1.2,color="#1769aa",zorder=3)
  for c in item["connectors"]: ax.plot([c["bass_timestamp_seconds"],c["drum_timestamp_seconds"]],[0,1],color="#8d99a6",alpha=.42,linewidth=.65,zorder=1)
  ax.set_xlim(item["start_time_seconds"],item["end_time_seconds_exclusive"]); ax.set_ylim(-.45,1.45)
  ax.set_yticks([0,1],["Double Bass","Drums"]); ax.set_xlabel("Absolute distributed-file time (seconds)")
  ax.set_title(f"CED-VAL-006 {item['window_id']} — OBSERVATIONAL / FRAME-RESOLVED\nGEOMETRIC_ONLY — 512-sample JGA frame lattice")
  ax.grid(axis="x",color="#dddddd",linewidth=.45)
  ax.text(.995,.02,"Not physical-onset or musical-correspondence authority",transform=ax.transAxes,ha="right",va="bottom",fontsize=8,color="#555555")
  path=directory/f"cedval006_{item['window_id'].lower()}_observational.png"
  fig.savefig(path,dpi=180,metadata={"Software":"JGA frozen scientific visualization"}); plt.close(fig); hashes[item["window_id"]]=checksum(path)
 return hashes

def main():
 events,locs,profile=load(); first=build(events,locs,profile); second=build(events,locs,profile)
 if canonical(first)!=canonical(second): raise RuntimeError("SCIENTIFIC_CONTENT_REPLAY_FAILURE")
 with tempfile.TemporaryDirectory(prefix="cedval006-vis-a-") as a,tempfile.TemporaryDirectory(prefix="cedval006-vis-b-") as b:
  ah,bh=render(first,Path(a)),render(second,Path(b))
  if ah!=bh: raise RuntimeError("PNG_BYTE_REPLAY_FAILURE")
  for wid,*_ in WINDOWS: shutil.copyfile(Path(a)/f"cedval006_{wid.lower()}_observational.png",RUN/f"cedval006_{wid.lower()}_observational.png")
 compact=[{k:v for k,v in x.items() if k not in {"drums_events","double_bass_events"}} for x in first["windows"]]
 scientific={**first,"windows":compact}; png={wid:checksum(RUN/f"cedval006_{wid.lower()}_observational.png") for wid,*_ in WINDOWS}
 basis={"scientific_record":scientific,"per_window_scientific_content_fingerprints":{x["window_id"]:x["scientific_content_fingerprint"] for x in compact},
        "png_sha256":png,"scientific_content_replay":True,"png_byte_replay":True}
 aggregate=sha256(canonical(basis)).hexdigest(); result={"status":"PASS_FROZEN_FIVE_WINDOW_LOCAL_NEUTRAL_VISUALIZATIONS",**basis,
  "aggregate_visualization_fingerprint":aggregate,"artifact_paths":[str(RUN/f"cedval006_{wid.lower()}_observational.png") for wid,*_ in WINDOWS]}
 write(RUN/"scientific_content.json",scientific); write(RUN/"result.json",result)
 write(RUN/"input_manifest.json",{"study_id":STUDY,"execution_id":EXECUTION,"source_execution_id":SOURCE_EXECUTION,
  "source_scientific_fingerprint":SOURCE_FP,"input_checksums":INPUT_HASHES,"authority_checksums":AUTHORITY_HASHES,"authority_gate":"PASS"})
 write(RUN/"completion_protocol.json",{"status":result["status"],"scientific_content_replay":"PASS_EXACT_TWO_COMPLETE_EXECUTIONS",
  "png_byte_replay":"PASS_BYTE_IDENTICAL_TWO_COMPLETE_EXECUTIONS","aggregate_visualization_fingerprint":aggregate,
  **first["firewalls"]})
 (RUN/"report.md").write_text(f"# {STUDY} Frozen Visualization Result\n\nExecution: `{EXECUTION}`\n\nAggregate visualization fingerprint: `{aggregate}`.\n\n"
  "Status: **PASS_FROZEN_FIVE_WINDOW_LOCAL_NEUTRAL_VISUALIZATIONS**\n\nFive systematic windows were rendered only from frozen EME and AD-038 records. Scientific-content and PNG-byte replay passed. Correspondence remains `GEOMETRIC_ONLY`; calibration remains `UNESTABLISHED`.\n")
 names=["execute.py","verify.py","input_manifest.json","scientific_content.json","result.json","completion_protocol.json","report.md",*[f"cedval006_{wid.lower()}_observational.png" for wid,*_ in WINDOWS]]
 write(RUN/"artifact_manifest.json",{"study_id":STUDY,"execution_id":EXECUTION,"aggregate_visualization_fingerprint":aggregate,"artifacts":{n:checksum(RUN/n) for n in names}})
 print(json.dumps({"execution_id":EXECUTION,"windows":[{"window_id":x["window_id"],"bounds":[x["start_sample_frame"],x["end_sample_frame_exclusive"]],
  "counts":[x["drums_eme_count"],x["double_bass_eme_count"],x["total_eme_count"]],"connectors":x["connectors_rendered_count"],
  "censoring":x["display_boundary_censoring_count"],"ties":x["nearest_tie_count"],"fingerprint":x["scientific_content_fingerprint"],
  "png_sha256":png[x["window_id"]]} for x in compact],"aggregate_visualization_fingerprint":aggregate,
  "scientific_content_replay":True,"png_byte_replay":True},indent=2,sort_keys=True))

if __name__=="__main__": main()
