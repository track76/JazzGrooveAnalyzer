"""Fresh-process librosa runner for frozen CED-VAL-006 external benchmark."""
from hashlib import sha256
from importlib import metadata
import inspect, json, os, platform, sys
from pathlib import Path
import librosa, numba, numpy as np, scipy

def canonical(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def frecord(value):
 n=float(value); return {"decimal":n,"binary64_hex":n.hex()}

array_path,expected_hash,native_fp,output_path=map(Path,sys.argv[1:])
if metadata.version("librosa")!="0.11.0": raise RuntimeError("LIBROSA_DISTRIBUTION_CONFLICT")
signal=np.load(array_path,allow_pickle=False); actual=sha256(signal.tobytes(order="C")).hexdigest()
if actual!=expected_hash.name or signal.dtype!=np.float32 or signal.shape!=(11912868,): raise RuntimeError("NATIVE_MONO_CONFLICT")
tempo,beats=librosa.beat.beat_track(y=signal,sr=48000,onset_envelope=None,hop_length=512,start_bpm=120.0,
 tightness=100,trim=True,bpm=None,prior=None,units="frames",sparse=True)
tempo=np.asarray(tempo); beats=np.asarray(beats)
if not np.issubdtype(beats.dtype,np.integer) or np.any(np.diff(beats)<0): raise RuntimeError("TRACKER_OUTPUT_AUTHORITY_CONFLICT")
samples=beats.astype(np.int64)*512
if np.any(beats<0) or np.any(samples>=11912868): raise RuntimeError("TRACKER_OUTPUT_AUTHORITY_CONFLICT")
seconds=samples.astype(np.float64)/48000; intervals=np.diff(seconds)
record={"tracker_id":"LIBROSA_BEAT_TRACK_0_11_0","epistemic_status":"CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE",
 "status":"VALID_TRACKER_OUTPUT" if len(beats) else "EMPTY_TRACKER_OUTPUT","package_authority":{"distribution":"librosa==0.11.0",
 "imported_version":librosa.__version__,"callable_signature":str(inspect.signature(librosa.beat.beat_track)),
 "callable_source_sha256":sha256(inspect.getsource(librosa.beat.beat_track).encode()).hexdigest()},
 "environment":{"python":sys.version,"executable":sys.executable,"platform":platform.platform(),"machine":platform.machine(),
 "numpy":np.__version__,"scipy":scipy.__version__,"numba":numba.__version__,"thread_environment":{k:os.environ.get(k) for k in
 ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","VECLIB_MAXIMUM_THREADS")},"device":"CPU","random_seed":"NOT_USED",
 "installed_distributions":sorted({f"{x.metadata['Name']}=={x.version}" for x in metadata.distributions()})},
 "configuration":{"api":"librosa.beat.beat_track","y":"frozen_native_float32_mono","sr":48000,"onset_envelope":None,
 "hop_length":512,"start_bpm":120.0,"tightness":100,"trim":True,"bpm":None,"prior":None,"units":"frames","sparse":True},
 "native_mono_scientific_fingerprint":native_fp.name,"native_mono_raw_bytes_sha256":actual,
 "native_outputs":{"tempo":{"native_type":type(tempo).__name__,"dtype":str(tempo.dtype),"shape":list(tempo.shape),
 "values":[frecord(x) for x in tempo.reshape(-1)],"semantics":"TRACKER_REPORTED_GLOBAL_TEMPO_DESCRIPTIVE_ONLY"},
 "beat_frames":{"native_type":type(beats).__name__,"dtype":str(beats.dtype),"shape":list(beats.shape),"values":[int(x) for x in beats]},
 "beat_samples":{"derivation":"512 * beat_frame","values":[int(x) for x in samples]},
 "beat_seconds":{"derivation":"beat_sample / 48000","values":[frecord(x) for x in seconds]},
 "derived_inter_beat_intervals_seconds":[frecord(x) for x in intervals],"confidence":{"status":"NOT_AVAILABLE_FROM_FROZEN_API"}},
 "frame_lattice":{"hop_samples":512,"sample_rate_hz":48000,"seconds":512/48000},
 "licensing":"ISC; no distribution or production decision"}
record["scientific_fingerprint"]=sha256(canonical(record)).hexdigest()
output_path.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
