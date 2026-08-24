"""Independent verifier for the frozen CED-VAL-006 external benchmark."""
from hashlib import sha256
import json, math
from pathlib import Path

RUN=Path(__file__).resolve().parent

def canonical(value):
 return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def load(name): return json.loads((RUN/name).read_text())
def digest(path):
 h=sha256()
 with path.open("rb") as stream:
  for block in iter(lambda:stream.read(1048576),b""): h.update(block)
 return h.hexdigest()
def fingerprint(record):
 return sha256(canonical({k:v for k,v in record.items() if k!="scientific_fingerprint"})).hexdigest()
def require(condition,message):
 if not condition: raise RuntimeError(message)

def main():
 native=load("native_mono_authority.json")
 resampled=load("essentia_resampled_input_authority.json")
 essentia=load("essentia_output.json")
 librosa=load("librosa_output.json")
 result=load("result.json")
 manifest=load("artifact_manifest.json")

 for name,expected in manifest["artifacts"].items():
  require(digest(RUN/name)==expected,f"ARTIFACT_CHECKSUM_CONFLICT:{name}")
 require(fingerprint(native)==native["scientific_fingerprint"],"NATIVE_MONO_FINGERPRINT_CONFLICT")
 require(fingerprint(resampled)==resampled["scientific_fingerprint"],"RESAMPLED_INPUT_FINGERPRINT_CONFLICT")
 require(fingerprint(essentia)==essentia["scientific_fingerprint"],"ESSENTIA_FINGERPRINT_CONFLICT")
 require(fingerprint(librosa)==librosa["scientific_fingerprint"],"LIBROSA_FINGERPRINT_CONFLICT")

 require(native["shape"]==[11912868] and native["dtype"]=="float32","NATIVE_MONO_SHAPE_CONFLICT")
 require(native["sample_rate_hz"]==48000 and native["scope"]=="[0,11912868)","NATIVE_MONO_COORDINATE_CONFLICT")
 require(resampled["shape"]==[10944948] and resampled["dtype"]=="float32","RESAMPLED_SHAPE_CONFLICT")
 require(resampled["sample_rate_hz"]==44100,"RESAMPLED_RATE_CONFLICT")
 require(resampled["call"]=={"axis":0,"cval":0.0,"down":160,"padtype":"constant","up":147,"window":["kaiser",5.0]},"RESAMPLING_CALL_CONFLICT")
 require(resampled["native_mono_scientific_fingerprint"]==native["scientific_fingerprint"],"RESAMPLED_LINEAGE_CONFLICT")

 require(essentia["deterministic_replay"]=="PASS_EXACT_TWO_FRESH_PROCESS_EXECUTIONS","ESSENTIA_REPLAY_CONFLICT")
 require(librosa["deterministic_replay"]=="PASS_EXACT_TWO_FRESH_PROCESS_EXECUTIONS","LIBROSA_REPLAY_CONFLICT")
 require(essentia["epistemic_status"]==librosa["epistemic_status"]=="CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE","EPISTEMIC_STATUS_CONFLICT")
 ticks=[x["decimal"] for x in essentia["native_outputs"]["ticks"]["seconds"]]
 require(all(math.isfinite(x) for x in ticks) and ticks==sorted(ticks),"ESSENTIA_TICK_ORDER_CONFLICT")
 require(not ticks or (ticks[0]>=0 and ticks[-1]<=248.18475),"ESSENTIA_SCOPE_CONFLICT")
 frames=librosa["native_outputs"]["beat_frames"]["values"]
 samples=librosa["native_outputs"]["beat_samples"]["values"]
 times=[x["decimal"] for x in librosa["native_outputs"]["beat_seconds"]["values"]]
 require(frames==sorted(frames),"LIBROSA_FRAME_ORDER_CONFLICT")
 require(samples==[512*x for x in frames],"LIBROSA_SAMPLE_MAPPING_CONFLICT")
 require(all(t==s/48000 for t,s in zip(times,samples)),"LIBROSA_TIME_MAPPING_CONFLICT")

 combined={k:v for k,v in result.items() if k not in {"status","combined_benchmark_fingerprint","essentia_summary","librosa_summary"}}
 combined_fp=sha256(canonical(combined)).hexdigest()
 require(combined_fp==result["combined_benchmark_fingerprint"]==manifest["combined_benchmark_fingerprint"],"COMBINED_FINGERPRINT_CONFLICT")
 require(result["essentia_summary"]["beat_count"]==len(ticks),"ESSENTIA_COUNT_CONFLICT")
 require(result["librosa_summary"]["beat_count"]==len(frames),"LIBROSA_COUNT_CONFLICT")
 require(all(value is False for value in result["firewalls"].values()),"FIREWALL_CONFLICT")
 forbidden=list(RUN.rglob("__pycache__"))+list(RUN.rglob("*.pyc"))
 require(not forbidden,"TRANSIENT_ARTIFACT_CONFLICT")
 print(json.dumps({"status":"PASS_INDEPENDENT_AUTHORITY_VERIFICATION","combined_benchmark_fingerprint":combined_fp},sort_keys=True))

if __name__=="__main__": main()
