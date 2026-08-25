"""Fresh-process librosa raw-output constructor; no GT access."""
from hashlib import sha256
from importlib import metadata
import inspect, json, platform, sys
from pathlib import Path
import librosa, numpy as np

mono_path, mono_hash, output = map(Path,sys.argv[1:])
if metadata.version("librosa")!="0.11.0": raise RuntimeError("VERSION_CONFLICT")
mono=np.load(mono_path,allow_pickle=False); actual=sha256(mono.tobytes(order="C")).hexdigest()
if actual!=mono_hash.name or mono.dtype!=np.float32 or mono.shape!=(1463433,): raise RuntimeError("MONO_AUTHORITY_CONFLICT")
tempo,beats=librosa.beat.beat_track(y=mono,sr=44100,onset_envelope=None,hop_length=512,tightness=100,trim=True,bpm=None,prior=None,units="frames",sparse=True)
beats=np.asarray(beats)
if not np.issubdtype(beats.dtype,np.integer) or np.any(np.diff(beats)<0): raise RuntimeError("OUTPUT_CONFLICT")
outputs=[]
for i,frame in enumerate(beats):
    sample=int(frame)*512; t=sample/44100
    outputs.append({"frozen_native_index":i,"output_id":f"LIBROSA-BEAT-{i:04d}","beat_frame":int(frame),"beat_sample":sample,"timestamp_seconds":t,"timestamp_binary64_hex":t.hex()})
record={"system":"LIBROSA","epistemic_status":"BEAT_TRACKER_OUTPUT","input_mono_raw_bytes_sha256":actual,"outputs":outputs,"raw_output_count":len(outputs),"reported_tempo":[{"decimal":float(v),"binary64_hex":float(v).hex()} for v in np.asarray(tempo).reshape(-1)],"configuration":{"api":"librosa.beat.beat_track","sr":44100,"onset_envelope":None,"hop_length":512,"start_bpm":"OMITTED_LIBRARY_DEFAULT_NOT_GROUND_TRUTH_INPUT","tightness":100,"trim":True,"bpm":None,"prior":None,"units":"frames","sparse":True},"package_authority":{"distribution":"librosa==0.11.0","imported_version":librosa.__version__,"callable_signature":str(inspect.signature(librosa.beat.beat_track)),"callable_source_sha256":sha256(inspect.getsource(librosa.beat.beat_track).encode()).hexdigest()},"environment":{"python":sys.version,"platform":platform.platform(),"numpy":np.__version__},"ground_truth_accessed":False,"known_bpm_supplied":False}
record["scientific_fingerprint"]=sha256(json.dumps(record,sort_keys=True,separators=(",",":")).encode()).hexdigest(); output.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
