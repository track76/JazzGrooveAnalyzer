"""Execute frozen CED-VAL-006 external two-tracker benchmark."""
from hashlib import sha256
import inspect, json, os, platform, subprocess, sys, tempfile, wave
from pathlib import Path
import numpy as np, scipy
from scipy.signal import resample_poly

BASE=Path("validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK")
RUN=BASE/"external_beat_benchmark_20260824_191341"
PREREG=BASE/"preregistrations/H-CEDVAL006-EXTERNAL-BEAT-POSITION-FEASIBILITY-01.md"
INPUT=Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw/Dums Overheads LCT 640 TS-Dual Output Mode.wav")
INPUT_SHA="dbfc4c3c59cac2c42cb2bbd33f1e55dbb1ec8c2fe6c6d095e30efc791dd57b8d"
PREREG_SHA="11358b62a021c0f7b70d0297d375d0b24da4971a6540af9196d56afdcb1c5daa"
STUDY="H-CEDVAL006-EXTERNAL-BEAT-POSITION-FEASIBILITY-01"; EXECUTION="EXEC-CEDVAL006-EXTERNAL-BEAT-BENCHMARK-20260824-191341"
ESSENTIA_PYTHON=Path("/tmp/jga-essentia-2.1b6.dev1389/bin/python")
WHEEL=Path("/tmp/essentia-2.1b6.dev1389-cp313-cp313-macosx_15_0_arm64.whl")
WHEEL_SHA="84e5167b95d9e74b2ddd928555d5a1e11997a458dae25e653544a953bc3068b9"
SCIPY_SOURCE_SHA="ae162c8d1c43ee90fae826ab9f9232425bf66042b84d97fcd808b270d9309a51"
THREADS={"OMP_NUM_THREADS":"1","OPENBLAS_NUM_THREADS":"1","MKL_NUM_THREADS":"1","VECLIB_MAXIMUM_THREADS":"1"}

def canonical(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def write(path,x): Path(path).write_text(json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
def checksum(path):
 h=sha256()
 with Path(path).open("rb") as f:
  for block in iter(lambda:f.read(1048576),b""): h.update(block)
 return h.hexdigest()
def fingerprint(record): return sha256(canonical({k:v for k,v in record.items() if k!="scientific_fingerprint"})).hexdigest()
def build_mono():
 with wave.open(str(INPUT),"rb") as w:
  props=(w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes(),w.getcomptype())
  if props!=(2,3,48000,11912868,"NONE"): raise RuntimeError(f"INPUT_FORMAT_CONFLICT:{props}")
  raw=w.readframes(w.getnframes())
 b=np.frombuffer(raw,dtype=np.uint8).reshape(-1,2,3)
 u=b[:,:,0].astype(np.int64)|(b[:,:,1].astype(np.int64)<<8)|(b[:,:,2].astype(np.int64)<<16)
 s=np.where(u&0x800000,u-0x1000000,u)
 mono=((s[:,0]+s[:,1])/(2*8388608)).astype(np.float32)
 if mono.shape!=(11912868,) or mono.dtype!=np.float32: raise RuntimeError("MONO_CONFLICT")
 return np.ascontiguousarray(mono)
def array_value(x): return {"decimal":float(x),"binary32_hex_bytes":np.asarray(x,dtype=np.float32).tobytes().hex()}
def run(python,script,array_path,array_hash,*args):
 env=os.environ.copy(); env.update(THREADS); output=args[-1]
 subprocess.run([str(python),str(script),str(array_path),array_hash,*map(str,args)],check=True,cwd=Path.cwd(),env=env)
 return json.loads(Path(output).read_text())
def describe(records):
 values=np.asarray([x["decimal"] for x in records],dtype=np.float64)
 if not len(values): return None
 return {"count":len(values),"minimum":float(np.min(values)),"maximum":float(np.max(values)),"mean":float(np.mean(values)),
         "median":float(np.median(values)),"population_standard_deviation":float(np.std(values,ddof=0))}

def main():
 if checksum(INPUT)!=INPUT_SHA or checksum(PREREG)!=PREREG_SHA: raise RuntimeError("INPUT_OR_PREREG_CONFLICT")
 if not ESSENTIA_PYTHON.exists() or checksum(WHEEL)!=WHEEL_SHA: raise RuntimeError("ESSENTIA_ENVIRONMENT_CONFLICT")
 scipy_source=Path(inspect.getsourcefile(resample_poly))
 if scipy.__version__!="1.18.0" or checksum(scipy_source)!=SCIPY_SOURCE_SHA: raise RuntimeError("RESAMPLER_IMPLEMENTATION_CONFLICT")
 with tempfile.TemporaryDirectory(prefix="cedval006-external-beat-") as td:
  temp=Path(td); native=build_mono(); native_hash=sha256(native.tobytes(order="C")).hexdigest()
  native_authority={"shape":list(native.shape),"dtype":str(native.dtype),"sample_count":int(native.size),"sample_rate_hz":48000,
   "raw_bytes_sha256":native_hash,"minimum":array_value(np.min(native)),"maximum":array_value(np.max(native)),
   "construction":"float32((int64(L)+int64(R))/(2*8388608))","temporal_origin":"original distributed-file sample zero",
   "scope":"[0,11912868)","normalization":False,"filtering":False,"trimming":False,"gain_modification":False}
  native_authority["scientific_fingerprint"]=fingerprint(native_authority)
  native_path=temp/"native_mono.npy"; np.save(native_path,native,allow_pickle=False)
  resampled=resample_poly(native,up=147,down=160,axis=0,window=("kaiser",5.0),padtype="constant",cval=0.0)
  if resampled.shape!=(10944948,) or resampled.dtype!=np.float32: raise RuntimeError(f"RESAMPLED_INPUT_CONFLICT:{resampled.shape}:{resampled.dtype}")
  resampled=np.ascontiguousarray(resampled); resampled_hash=sha256(resampled.tobytes(order="C")).hexdigest()
  resampled_authority={"shape":list(resampled.shape),"dtype":str(resampled.dtype),"sample_count":int(resampled.size),
   "sample_rate_hz":44100,"raw_bytes_sha256":resampled_hash,"minimum":array_value(np.min(resampled)),"maximum":array_value(np.max(resampled)),
   "implementation":{"distribution":"scipy==1.18.0","source":"scipy/signal/_signaltools.py","source_sha256":SCIPY_SOURCE_SHA,
   "numpy":np.__version__},"call":{"up":147,"down":160,"axis":0,"window":["kaiser",5.0],"padtype":"constant","cval":0.0},
   "native_mono_scientific_fingerprint":native_authority["scientific_fingerprint"],
   "origin_mapping":"output sample zero equals original sample zero; sample m time=m/44100 and nominal original coordinate=m*160/147",
   "duration_seconds":{"exact":"130297/525","decimal":10944948/44100},
   "original_duration_seconds":{"exact":"992739/4000","decimal":248.18475},"ceiling_excess_seconds":{"exact":"1/84000","decimal":1/84000}}
  resampled_authority["scientific_fingerprint"]=fingerprint(resampled_authority)
  resampled_path=temp/"essentia_mono_44100.npy"; np.save(resampled_path,resampled,allow_pickle=False)
  essentia=[run(ESSENTIA_PYTHON,RUN/"run_essentia.py",resampled_path,resampled_hash,
    native_authority["scientific_fingerprint"],resampled_authority["scientific_fingerprint"],temp/f"essentia_{i}.json") for i in (1,2)]
  if canonical(essentia[0])!=canonical(essentia[1]): raise RuntimeError("ESSENTIA_REPLAY_FAILURE")
  essentia_record=essentia[0]; essentia_record["deterministic_replay"]="PASS_EXACT_TWO_FRESH_PROCESS_EXECUTIONS"
  essentia_record["scientific_fingerprint"]=fingerprint(essentia_record)
  librosa=[run(Path(sys.executable),RUN/"run_librosa.py",native_path,native_hash,
    native_authority["scientific_fingerprint"],temp/f"librosa_{i}.json") for i in (1,2)]
  if canonical(librosa[0])!=canonical(librosa[1]): raise RuntimeError("LIBROSA_REPLAY_FAILURE")
  librosa_record=librosa[0]; librosa_record["deterministic_replay"]="PASS_EXACT_TWO_FRESH_PROCESS_EXECUTIONS"
  librosa_record["scientific_fingerprint"]=fingerprint(librosa_record)
 e_ticks=essentia_record["native_outputs"]["ticks"]["seconds"]; e_intervals=essentia_record["native_outputs"]["bpmIntervals"]["seconds"]
 l_frames=librosa_record["native_outputs"]["beat_frames"]["values"]; l_samples=librosa_record["native_outputs"]["beat_samples"]["values"]
 l_times=librosa_record["native_outputs"]["beat_seconds"]["values"]; l_intervals=librosa_record["native_outputs"]["derived_inter_beat_intervals_seconds"]
 combined={"schema":"JGA-CEDVAL006-EXTERNAL-BEAT-POSITION-FEASIBILITY/v1","study_id":STUDY,"execution_id":EXECUTION,
  "preregistration_commit":"7f39c115a3fe8c96d9a8d1cc6ce8dc5496e1a5da","input_sha256":INPUT_SHA,
  "native_mono_scientific_fingerprint":native_authority["scientific_fingerprint"],
  "essentia_resampled_input_scientific_fingerprint":resampled_authority["scientific_fingerprint"],
  "essentia_scientific_fingerprint":essentia_record["scientific_fingerprint"],
  "librosa_scientific_fingerprint":librosa_record["scientific_fingerprint"],"epistemic_status":"CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE",
  "blind_freeze_completed_before_jga_access":True,"firewalls":{"jga_eme_accessed":False,"jga_comparison_performed":False,
  "external_or_manual_bpm_used":False,"lewitt_video_used_for_timing":False,"h02_used":False,"strength_accessed":False,
  "jga_core_changed":False,"production_code_changed":False,"raw_assets_changed":False,"historical_authorities_changed":False,
  "musical_interpretation_performed":False,"constant_bpm_grid_constructed":False}}
 combined_fp=sha256(canonical(combined)).hexdigest()
 result={"status":"PASS_FROZEN_EXTERNAL_TWO_TRACKER_OUTPUTS",**combined,"combined_benchmark_fingerprint":combined_fp,
  "essentia_summary":{"status":essentia_record["status"],"reported_bpm":essentia_record["native_outputs"]["bpm"],"beat_count":len(e_ticks),
  "beat_time_scope_seconds":None if not e_ticks else [e_ticks[0],e_ticks[-1]],"inter_beat_interval_summary_seconds":describe(e_intervals),
  "confidence":essentia_record["native_outputs"]["confidence"]},
  "librosa_summary":{"status":librosa_record["status"],"reported_tempo":librosa_record["native_outputs"]["tempo"],"beat_count":len(l_frames),
  "beat_frame_scope":None if not l_frames else [l_frames[0],l_frames[-1]],"beat_sample_scope":None if not l_samples else [l_samples[0],l_samples[-1]],
  "beat_time_scope_seconds":None if not l_times else [l_times[0],l_times[-1]],"inter_beat_interval_summary_seconds":describe(l_intervals)}}
 write(RUN/"native_mono_authority.json",native_authority); write(RUN/"essentia_resampled_input_authority.json",resampled_authority)
 write(RUN/"essentia_output.json",essentia_record); write(RUN/"librosa_output.json",librosa_record); write(RUN/"result.json",result)
 write(RUN/"input_manifest.json",{"study_id":STUDY,"execution_id":EXECUTION,"preregistration_commit":"7f39c115a3fe8c96d9a8d1cc6ce8dc5496e1a5da",
  "preregistration_sha256":PREREG_SHA,"input_path":str(INPUT),"input_sha256":INPUT_SHA,
  "input_properties":{"channels":2,"sample_width_bytes":3,"sample_rate_hz":48000,"sample_count":11912868},
  "essentia_wheel_sha256":WHEEL_SHA,"orchestrator_environment":{"python":sys.version,"platform":platform.platform(),
  "machine":platform.machine(),"numpy":np.__version__,"scipy":scipy.__version__}})
 write(RUN/"completion_protocol.json",{"status":result["status"],"authority_gate":"PASS","native_mono_gate":"PASS",
  "resampled_input_gate":"PASS","essentia_replay":essentia_record["deterministic_replay"],"librosa_replay":librosa_record["deterministic_replay"],
  "combined_benchmark_fingerprint":combined_fp,**combined["firewalls"]})
 (RUN/"report.md").write_text(f"# {STUDY} Frozen Result\n\nExecution: `{EXECUTION}`\n\nStatus: **{result['status']}**\n\n"
  f"Combined benchmark fingerprint: `{combined_fp}`.\n\nEssentia and librosa replayed exactly across two fresh processes each. Both remain `CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE`. No JGA EME was accessed.\n")
 names=["execute.py","run_essentia.py","run_librosa.py","verify.py","native_mono_authority.json","essentia_resampled_input_authority.json",
  "essentia_output.json","librosa_output.json","result.json","input_manifest.json","completion_protocol.json","report.md"]
 write(RUN/"artifact_manifest.json",{"study_id":STUDY,"execution_id":EXECUTION,"combined_benchmark_fingerprint":combined_fp,
  "artifacts":{name:checksum(RUN/name) for name in names}})
 print(json.dumps({"execution_id":EXECUTION,"native_mono":native_authority,"essentia_resampled_input":resampled_authority,
  "essentia":result["essentia_summary"],"essentia_fingerprint":essentia_record["scientific_fingerprint"],
  "librosa":result["librosa_summary"],"librosa_fingerprint":librosa_record["scientific_fingerprint"],
  "combined_benchmark_fingerprint":combined_fp},indent=2,sort_keys=True))
if __name__=="__main__": main()
