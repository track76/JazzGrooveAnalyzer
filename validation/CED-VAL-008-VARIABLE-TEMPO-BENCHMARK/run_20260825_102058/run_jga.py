"""Fresh-process JGA raw-output constructor; no GT access or strength read."""
from hashlib import sha256
import json, platform, sys
from pathlib import Path
import librosa
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline

source, output = map(Path, sys.argv[1:])
expected="cfeb385ab00320f654453a1ff64c6dce9d1d0e80c2008dade847df671a744848"
if sha256(source.read_bytes()).hexdigest()!=expected: raise RuntimeError("INPUT_AUTHORITY_CONFLICT")
analysis=AnalysisPipeline().analyze(str(source))
candidates=tuple(analysis.domain_pulse_candidates); emes=tuple(analysis.elementary_metric_events)
by_id={str(x.id):x for x in candidates}
if len(by_id)!=len(candidates) or len(emes)!=len(candidates): raise RuntimeError("AD037_CARDINALITY_CONFLICT")
def coord(t):
    frame=round(t*44100/512); sample=frame*512
    if float(librosa.frames_to_time(frame,sr=44100,hop_length=512)).hex()!=t.hex(): raise RuntimeError("FRAME_MAPPING_CONFLICT")
    return frame,sample
pc=[]
for x in candidates:
    frame,sample=coord(x.timestamp)
    pc.append({"output_id":str(x.id),"sound_source_id":str(x.sound_source_id),"producer_frame":frame,"producer_sample_coordinate":sample,"timestamp_seconds":x.timestamp,"timestamp_binary64_hex":x.timestamp.hex(),"observation_index":x.observation_index,"observation_provenance_id":x.observation_provenance_id})
eme=[]
for x in emes:
    lineage=[str(v) for v in x.supporting_pulse_candidate_ids]
    if len(lineage)!=1 or lineage[0] not in by_id or x.timestamp.hex()!=by_id[lineage[0]].timestamp.hex(): raise RuntimeError("LINEAGE_CONFLICT")
    frame,sample=coord(x.timestamp)
    eme.append({"output_id":str(x.id),"contributor_id":str(x.contributor_id),"sound_source_id":str(x.sound_source_id),"producer_frame":frame,"producer_sample_coordinate":sample,"timestamp_seconds":x.timestamp,"timestamp_binary64_hex":x.timestamp.hex(),"supporting_pulse_candidate_ids":lineage,"association_rule":x.association_rule,"association_outcome":x.association_outcome,"evidence_status":x.evidence_status,"materialization_rule":x.materialization_rule,"temporal_scope":x.temporal_scope,"source_asset_sha256":x.source_asset_sha256})
pc.sort(key=lambda x:(x["producer_frame"],x["output_id"])); eme.sort(key=lambda x:(x["producer_frame"],x["output_id"]))
for i,x in enumerate(pc): x["frozen_native_index"]=i
for i,x in enumerate(eme): x["frozen_native_index"]=i
record={"system":"JGA","epistemic_status":"FRAME_RESOLVED_JGA_OBSERVATION","execution_call":"AnalysisPipeline().analyze(str(DRUM_GT_PATH))","input_sha256":expected,"pulse_candidates_without_strength_or_confidence":pc,"outputs":eme,"raw_output_count":len(eme),"frame_lattice":{"hop_samples":512,"sample_rate_hz":44100},"environment":{"python":sys.version,"platform":platform.platform(),"librosa":librosa.__version__},"ground_truth_accessed":False,"strength_accessed":False,"confidence_used":False,"known_bpm_supplied":False}
record["scientific_fingerprint"]=sha256(json.dumps(record,sort_keys=True,separators=(",",":")).encode()).hexdigest()
output.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
