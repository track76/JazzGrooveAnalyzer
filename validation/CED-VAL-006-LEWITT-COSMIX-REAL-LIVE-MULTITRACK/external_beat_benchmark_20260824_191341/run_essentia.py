"""Fresh-process Essentia runner for frozen CED-VAL-006 external benchmark."""
from hashlib import sha256
from importlib import metadata
import json, os, platform, sys
from pathlib import Path
import essentia, essentia.standard as es, numpy as np, six, yaml

def canonical(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def frecord(value):
 n=float(value); return {"decimal":n,"binary64_hex":n.hex()}

array_path,expected_hash,native_fp,resampled_fp,output_path=map(Path,sys.argv[1:])
if metadata.version("essentia")!="2.1b6.dev1389": raise RuntimeError("ESSENTIA_DISTRIBUTION_CONFLICT")
signal=np.load(array_path,allow_pickle=False); actual=sha256(signal.tobytes(order="C")).hexdigest()
if actual!=expected_hash.name or signal.dtype!=np.float32 or signal.shape!=(10944948,): raise RuntimeError("RESAMPLED_INPUT_CONFLICT")
algorithm=es.RhythmExtractor2013(method="multifeature",minTempo=40,maxTempo=208)
bpm,ticks,confidence,estimates,intervals=algorithm(signal)
ticks=np.asarray(ticks); estimates=np.asarray(estimates); intervals=np.asarray(intervals)
if not np.all(np.isfinite(ticks)) or np.any(np.diff(ticks)<0) or np.any(ticks<0) or np.any(ticks>248.18475):
 raise RuntimeError("TRACKER_OUTPUT_AUTHORITY_CONFLICT")
record={"tracker_id":"ESSENTIA_RHYTHMEXTRACTOR2013_MULTIFEATURE","epistemic_status":"CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE",
 "status":"VALID_TRACKER_OUTPUT" if len(ticks) else "EMPTY_TRACKER_OUTPUT","package_authority":{
 "distribution":"essentia==2.1b6.dev1389","imported_version":essentia.__version__,
 "wheel":"essentia-2.1b6.dev1389-cp313-cp313-macosx_15_0_arm64.whl",
 "wheel_sha256":"84e5167b95d9e74b2ddd928555d5a1e11997a458dae25e653544a953bc3068b9"},
 "environment":{"python":sys.version,"executable":sys.executable,"platform":platform.platform(),"machine":platform.machine(),
 "numpy":np.__version__,"pyyaml":yaml.__version__,"six":six.__version__,"thread_environment":{k:os.environ.get(k) for k in
 ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","VECLIB_MAXIMUM_THREADS")},"device":"CPU","random_seed":"NOT_USED",
 "installed_distributions":sorted({f"{x.metadata['Name']}=={x.version}" for x in metadata.distributions()})},
 "configuration":{"algorithm":"RhythmExtractor2013","mode":"standard","method":"multifeature","minTempo":40,"maxTempo":208,
 "sample_rate_hz":44100,"input_loader":"frozen_external_resampled_float32_array","further_resampling":False},
 "native_mono_scientific_fingerprint":native_fp.name,"resampled_input_scientific_fingerprint":resampled_fp.name,
 "resampled_input_raw_bytes_sha256":actual,"original_time_mapping":"returned_seconds_from_common_sample_zero; no rounded sample coordinate",
 "native_outputs":{"bpm":frecord(bpm),"ticks":{"native_type":type(ticks).__name__,"dtype":str(ticks.dtype),"shape":list(ticks.shape),
 "seconds":[frecord(x) for x in ticks]},"confidence":{"semantics":"TRACK_LEVEL_MULTIFEATURE_CONFIDENCE_NOT_PER_BEAT",**frecord(confidence)},
 "estimates":{"native_type":type(estimates).__name__,"dtype":str(estimates.dtype),"shape":list(estimates.shape),
 "bpm_values":[frecord(x) for x in estimates]},"bpmIntervals":{"native_type":type(intervals).__name__,"dtype":str(intervals.dtype),
 "shape":list(intervals.shape),"seconds":[frecord(x) for x in intervals]}},
 "licensing":"AGPLv3/open non-commercial path; no distribution or production authority"}
record["scientific_fingerprint"]=sha256(canonical(record)).hexdigest()
output_path.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
