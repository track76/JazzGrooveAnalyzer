"""Fresh-process Essentia raw-output constructor; no GT access."""
from hashlib import sha256
from importlib import metadata
import json, platform, sys
from pathlib import Path
import essentia, essentia.standard as es, numpy as np

mono_path, mono_hash, output = map(Path,sys.argv[1:])
if metadata.version("essentia")!="2.1b6.dev1389": raise RuntimeError("VERSION_CONFLICT")
mono=np.load(mono_path,allow_pickle=False); actual=sha256(mono.tobytes(order="C")).hexdigest()
if actual!=mono_hash.name or mono.dtype!=np.float32 or mono.shape!=(1463433,): raise RuntimeError("MONO_AUTHORITY_CONFLICT")
bpm,ticks,confidence,estimates,intervals=es.RhythmExtractor2013(method="multifeature",minTempo=40,maxTempo=208)(mono)
ticks=np.asarray(ticks)
if not np.all(np.isfinite(ticks)) or np.any(np.diff(ticks)<0): raise RuntimeError("OUTPUT_CONFLICT")
def fr(v):
    x=float(v); return {"decimal":x,"binary64_hex":x.hex()}
outputs=[{"frozen_native_index":i,"output_id":f"ESSENTIA-BEAT-{i:04d}","timestamp_seconds":float(v),"timestamp_binary64_hex":float(v).hex()} for i,v in enumerate(ticks)]
record={"system":"ESSENTIA","epistemic_status":"BEAT_TRACKER_OUTPUT","input_mono_raw_bytes_sha256":actual,"outputs":outputs,"raw_output_count":len(outputs),"reported_bpm":fr(bpm),"confidence":{"semantics":"TRACK_LEVEL_MULTIFEATURE_CONFIDENCE",**fr(confidence)},"intervals":[fr(v) for v in np.asarray(intervals)],"estimates":[fr(v) for v in np.asarray(estimates)],"configuration":{"algorithm":"RhythmExtractor2013","method":"multifeature","minTempo":40,"maxTempo":208,"sample_rate_hz":44100,"resampling":False,"cpu":True,"declared_thread_limits":1},"package_authority":{"distribution":"essentia==2.1b6.dev1389","imported_version":essentia.__version__,"wheel_sha256":"84e5167b95d9e74b2ddd928555d5a1e11997a458dae25e653544a953bc3068b9"},"environment":{"python":sys.version,"platform":platform.platform(),"numpy":np.__version__,"pyyaml":metadata.version("pyyaml"),"six":metadata.version("six"),"thread_limits":1},"ground_truth_accessed":False,"known_bpm_supplied":False}
record["scientific_fingerprint"]=sha256(json.dumps(record,sort_keys=True,separators=(",",":")).encode()).hexdigest(); output.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
