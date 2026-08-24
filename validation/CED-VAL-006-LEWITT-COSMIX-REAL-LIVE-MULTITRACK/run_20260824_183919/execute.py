"""Execute the frozen CED-VAL-006 AD-037/AD-038/AD-040 protocol."""
from __future__ import annotations
from collections import Counter
from hashlib import sha256
import json, math, platform, subprocess, sys, tempfile, wave
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5
import librosa
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.representation.builders.drum_relative_eme_localization_builder import DrumRelativeEMELocalizationBuilder
from jga.representation.builders.rhythm_section_timing_profile_builder import RhythmSectionTimingProfileBuilder
from jga.representation.rhythm_section_timing_profile import AnalyticalRoleAssignment

BASE = Path("validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK")
RUN = BASE / "run_20260824_183919"
STUDY = "H-CEDVAL006-REAL-LIVE-AUDIO-RHYTHM-SECTION-TIMING-PROFILE-01"
EXECUTION = "EXEC-CEDVAL006-REAL-LIVE-AUDIO-20260824-183919"
DATASET_FP = "9d837f710fbf3292c80490d499bc96df0a8fe1140bc9139b65de8a553c4c2eca"
INPUT_FP = "cf89598f0f198cb14ee4f455b4094cffe3e4b4597da4fd92d2fffba41a233bae"
SR, HOP, NFRAMES = 48000, 512, 11912868
DATASET = BASE / "input_authority_manifest.json"
INPUTS = BASE / "analytical_input_authority.json"
PREREG = BASE / "preregistrations/H-CEDVAL006-REAL-LIVE-AUDIO-RHYTHM-SECTION-TIMING-PROFILE-01.md"
CLARIFICATION = BASE / "clarifications/CL-PR-CEDVAL006-DATASET-FINGERPRINT-BASIS-01.md"
SOURCES = (
    ("Drums", "TEMPORAL_REFERENCE", "Dums Overheads LCT 640 TS-Dual Output Mode.wav", "dbfc4c3c59cac2c42cb2bbd33f1e55dbb1ec8c2fe6c6d095e30efc791dd57b8d", 2),
    ("Double Bass", "ACCOMPANIMENT", "BASS - DI.wav", "c0a99f65158d12a69e062cc990e86631a0d29d7e83f30537d34eb301516855a9", 1),
)
REPO_HASHES = {
    str(PREREG): "44f94167bd3c90e6bee824dbc6f1dc038f252f11d5ff402194499875bce33b78",
    str(CLARIFICATION): "b80eb53bb920428aad4dd5c7806f4919caacebe8c0ccbf47c67c9f03675e6315",
    str(DATASET): "c96ad3bac2b8dbc9e5a949ae13c5a0a65a47c89bd09f8a9c369551bada12e72b",
    str(INPUTS): "3f041b70ecf12c538f024a57aeb8c28a598e1ce65090e5c016b9e8c51289cde0",
    "src/jga/audio/file_audio_source.py": "3441cdf4feb8fc98280c005e1e806bdd4c34861cb33b94fd58023a8e050f0d69",
    "src/jga/engines/audio_preprocessor.py": "83ef6157f9b320e6f4bd659adad4f085883f1142244c47b159261e40ea33ca5f",
    "src/jga/separation/null_separator.py": "148292b92efb88c2992c828a73f569dc30d71925c2df3945b75cfe3daa5162b1",
    "src/jga/engines/source_pulse_candidate_builder.py": "5b270f352483dde91448b0958a299c08e51d064ab867bc872ef1cdde37a81c32",
    "src/jga/engines/domain_pulse_candidate_adapter.py": "6a3d276bf50534bc6823075a26787c624ab7a8d2ecca58628579fb86658a9330",
    "src/jga/pipeline/default_analysis_pipeline.py": "04ecdfee536717b977276b91b7e9416701e7a89ce9aa7bc4339917263725ef17",
    "src/jga/domain/services/elementary_metric_event_builder.py": "137e390a69c9361d5cbfd66908256b2417d76c95d503e7ad2c409cd2e1b66cc2",
    "src/jga/representation/builders/drum_relative_eme_localization_builder.py": "bf6d61bf3c2be644047fd81553e68a73bb0b4f95e67535acc010d30e1fc465fd",
    "src/jga/representation/builders/rhythm_section_timing_profile_builder.py": "92c63c2d19045553b09a3ca36ad2321eba348adac4cfd35cde9e3115f5f720c4",
}

def canonical(x): return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
def write(path, x): Path(path).write_text(json.dumps(x, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
def digest(path):
    h = sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1048576), b""): h.update(block)
    return h.hexdigest()

def verify_authority():
    for path, expected in REPO_HASHES.items():
        if digest(path) != expected: raise RuntimeError(f"AUTHORITY_CONFLICT:{path}")
    dataset = json.loads(DATASET.read_text())
    keys = ("schema", "dataset_id", "external_root", "directory_structure", "scientifically_relevant_assets", "filesystem_metadata_sidecars")
    basis = {key: dataset[key] for key in keys}
    if sha256(canonical(basis)).hexdigest() != DATASET_FP or dataset["dataset_fingerprint"] != DATASET_FP:
        raise RuntimeError("DATASET_FINGERPRINT_CONFLICT")
    inputs = json.loads(INPUTS.read_text()); frozen = dict(inputs); frozen.pop("analytical_input_fingerprint")
    if inputs["analytical_input_fingerprint"] != INPUT_FP or sha256(canonical(frozen)).hexdigest() != INPUT_FP:
        raise RuntimeError("ANALYTICAL_INPUT_CONFLICT")
    selected = {x["analytical_source"]: x for x in inputs["selected_inputs"]}; paths = {}
    for source, role, filename, expected, channels in SOURCES:
        item = selected[source]; path = Path(item["absolute_path"])
        if (item["filename"], item["analytical_role"], item["sha256"]) != (filename, role, expected) or digest(path) != expected:
            raise RuntimeError(f"INPUT_CONFLICT:{source}")
        with wave.open(str(path), "rb") as w: props = (w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes(), w.getcomptype())
        if props != (channels, 3, SR, NFRAMES, "NONE"): raise RuntimeError(f"FORMAT_CONFLICT:{source}:{props}")
        paths[source] = path
    return dataset, inputs, paths

def coordinate(timestamp):
    frame = round(timestamp * SR / HOP); sample = HOP * frame
    if float(librosa.frames_to_time(frame, sr=SR, hop_length=HOP)).hex() != timestamp.hex():
        raise RuntimeError("TEMPORAL_MAPPING_CONFLICT")
    return frame, sample

def candidate(x):
    frame, sample = coordinate(x.timestamp)
    return {"pulse_candidate_id": str(x.id), "sound_source_id": str(x.sound_source_id), "producer_frame": frame,
            "producer_sample_coordinate": sample, "timestamp_seconds": x.timestamp, "timestamp_hex": x.timestamp.hex(),
            "observation_index": x.observation_index, "observation_provenance_id": x.observation_provenance_id}

def eme(x):
    frame, sample = coordinate(x.timestamp)
    return {"eme_id": str(x.id), "contributor_id": str(x.contributor_id), "sound_source_id": str(x.sound_source_id),
            "producer_frame": frame, "producer_sample_coordinate": sample, "timestamp_seconds": x.timestamp,
            "timestamp_hex": x.timestamp.hex(), "supporting_pulse_candidate_ids": [str(i) for i in x.supporting_pulse_candidate_ids],
            "association_rule": x.association_rule, "association_outcome": x.association_outcome,
            "evidence_status": x.evidence_status, "materialization_rule": x.materialization_rule,
            "temporal_scope": x.temporal_scope, "source_asset_sha256": x.source_asset_sha256}

def reference(x):
    if x is None: return None
    frame, sample = coordinate(x.timestamp_seconds)
    return {"eme_id": str(x.eme_id), "contributor_id": str(x.contributor_id), "sound_source_id": str(x.sound_source_id),
            "producer_frame": frame, "producer_sample_coordinate": sample, "timestamp_seconds": x.timestamp_seconds,
            "timestamp_hex": x.timestamp_seconds.hex(), "supporting_observations": [{"pulse_candidate_id": str(o.pulse_candidate_id),
            "sound_source_id": str(o.sound_source_id), "observation_index": o.observation_index,
            "observation_provenance_id": o.observation_provenance_id} for o in x.supporting_observations],
            "source_asset_sha256": x.source_asset_sha256, "temporal_scope": x.temporal_scope,
            "materialization_rule": x.materialization_rule}

def localization(x):
    frame, sample = coordinate(x.target_timestamp_seconds)
    key = f"{x.target_eme_id}:{x.localization_rule}:{x.analysis_execution_id}"
    return {"localization_id": str(uuid5(NAMESPACE_URL, f"jga:ad038:{key}")), "target_eme_id": str(x.target_eme_id),
            "target_timestamp_seconds": x.target_timestamp_seconds, "target_timestamp_hex": x.target_timestamp_seconds.hex(),
            "target_producer_frame": frame, "target_producer_sample_coordinate": sample,
            "target_contributor_id": str(x.target_contributor_id), "target_sound_source_id": str(x.target_sound_source_id),
            "target_source_asset_sha256": x.target_source_asset_sha256, "target_temporal_scope": x.target_temporal_scope,
            "target_materialization_rule": x.target_materialization_rule, "preceding_drum_reference": reference(x.preceding_drum_eme),
            "following_drum_reference": reference(x.following_drum_eme), "nearest_drum_reference": reference(x.nearest_drum_eme),
            "distance_from_preceding_seconds": x.distance_from_preceding_seconds,
            "distance_from_following_seconds": x.distance_from_following_seconds,
            "nearest_signed_displacement_seconds": x.nearest_displacement_seconds,
            "nearest_absolute_displacement_seconds": None if x.nearest_displacement_seconds is None else abs(x.nearest_displacement_seconds),
            "nearest_selection_status": x.nearest_selection_status,
            "relationship_status": "GEOMETRIC_ONLY" if x.nearest_drum_eme is not None else "UNRESOLVED",
            "observed_interval_fraction": x.observed_interval_fraction, "temporal_origin_seconds": x.temporal_origin_seconds,
            "localization_rule": x.localization_rule, "analysis_execution_id": x.analysis_execution_id}

def quantile(v, p):
    pos = (len(v) - 1) * p; lo, hi = math.floor(pos), math.ceil(pos)
    return v[lo] if lo == hi else v[lo] * (hi - pos) + v[hi] * (pos - lo)
def describe(values):
    if not values: return {"n": 0, "statistics": "NOT_AVAILABLE"}
    v = sorted(values); mean = math.fsum(v) / len(v)
    s = {"minimum": v[0], "q1": quantile(v,.25), "median": quantile(v,.5), "q3": quantile(v,.75), "maximum": v[-1],
         "mean": mean, "population_standard_deviation": math.sqrt(math.fsum((x-mean)**2 for x in v)/len(v))}
    return {"n": len(v), "quantile_method": "linear_empirical_interpolation_at_(n-1)*p", "seconds": s,
            "milliseconds": {k: x*1000 for k,x in s.items()}}

def run_once(paths):
    analyses = {source: AnalysisPipeline().analyze(str(path)) for source,path in paths.items()}
    candidates, events, runtime = {}, {}, []
    for source, _role, _filename, asset_sha, _channels in SOURCES:
        cs = tuple(analyses[source].domain_pulse_candidates); es = tuple(analyses[source].elementary_metric_events); by_id = {str(x.id): x for x in cs}
        if len(by_id) != len(cs) or len(es) != len(cs): raise RuntimeError("AD037_CARDINALITY_CONFLICT")
        for event in es:
            lineage = [str(x) for x in event.supporting_pulse_candidate_ids]
            if len(lineage)!=1 or lineage[0] not in by_id or event.timestamp.hex()!=by_id[lineage[0]].timestamp.hex() or event.source_asset_sha256!=asset_sha:
                raise RuntimeError("AD037_LINEAGE_CONFLICT")
        candidates[source] = sorted((candidate(x) for x in cs), key=lambda x:(x["producer_frame"],x["pulse_candidate_id"]))
        events[source] = sorted((eme(x) for x in es), key=lambda x:(x["producer_frame"],x["eme_id"])); runtime.extend(cs)
    drums = tuple(analyses["Drums"].elementary_metric_events); bass = tuple(analyses["Double Bass"].elementary_metric_events)
    locs_runtime = DrumRelativeEMELocalizationBuilder().build(bass, drums, tuple(runtime), temporal_origin_seconds=0.0, analysis_execution_id=EXECUTION)
    locs = sorted((localization(x) for x in locs_runtime), key=lambda x:(x["target_timestamp_seconds"],x["target_eme_id"]))
    assignments=[]
    for source, role, _filename, asset_sha, _channels in SOURCES:
        sample=tuple(analyses[source].elementary_metric_events)[0]
        assignments.append(AnalyticalRoleAssignment(assignment_id=uuid5(NAMESPACE_URL,f"{STUDY}:role:{source}:{asset_sha}"),
            source_id=sample.sound_source_id,asset_id=asset_sha,temporal_scope="analysis_input",temporal_origin_seconds=0.0,
            role=role,assignment_rule="cedval006-pi-approved-analytical-role/v1",execution_id=EXECUTION,
            scientific_authority_id="PR-CEDVAL006-ANALYTICAL-INPUTS-001",scientific_authority_fingerprint=INPUT_FP))
    p=RhythmSectionTimingProfileBuilder().build(drums+bass,locs_runtime,assignments,temporal_scope="analysis_input",temporal_origin_seconds=0.0,
        execution_id=EXECUTION,provenance_id="PR-CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK-001",
        scientific_authority_ids=("AD-037","AD-038","AD-040",STUDY))
    profile={"profile_id":str(p.profile_id),"scientific_fingerprint":p.scientific_fingerprint,"projection_rule":p.projection_rule,
        "temporal_scope":p.temporal_scope,"temporal_origin_seconds":p.temporal_origin_seconds,"execution_id":p.execution_id,
        "provenance_id":p.provenance_id,"scientific_authority_ids":list(p.scientific_authority_ids),
        "role_assignments":[{"assignment_id":str(x.assignment_id),"source_id":str(x.source_id),"asset_id":x.asset_id,"role":x.role,
        "temporal_scope":x.temporal_scope,"temporal_origin_seconds":x.temporal_origin_seconds,"assignment_rule":x.assignment_rule,
        "execution_id":x.execution_id,"scientific_authority_id":x.scientific_authority_id,
        "scientific_authority_fingerprint":x.scientific_authority_fingerprint} for x in p.role_assignments],
        "temporal_reference_eme_ids":[str(x.id) for x in p.temporal_reference_events],
        "accompaniment_relationship_target_eme_ids":[str(x.target_eme.id) for x in p.accompaniment_relationships],
        "represented_observation_count":len(p.temporal_reference_events)+len(p.accompaniment_relationships),
        "source_counts":{"Drums":len(p.temporal_reference_events),"Double Bass":len(p.accompaniment_relationships)},
        "relationship_status_counts":dict(sorted(Counter(x.correspondence.status for x in p.accompaniment_relationships).items())),
        "calibration_applicability":"UNESTABLISHED"}
    summary={}
    for source in ("Drums","Double Bass"):
        es=events[source]; summary[source]={"pulse_candidate_count":len(candidates[source]),"eme_count":len(es),
        "producer_frame_scope":None if not es else [es[0]["producer_frame"],es[-1]["producer_frame"]],
        "producer_sample_scope":None if not es else [es[0]["producer_sample_coordinate"],es[-1]["producer_sample_coordinate"]],
        "timestamp_scope_seconds":None if not es else [es[0]["timestamp_seconds"],es[-1]["timestamp_seconds"]],
        "timestamp_scope_hex":None if not es else [es[0]["timestamp_hex"],es[-1]["timestamp_hex"]]}
    signed=[x["nearest_signed_displacement_seconds"] for x in locs if x["nearest_signed_displacement_seconds"] is not None]; absolute=[abs(x) for x in signed]
    geometry={"eligible_count":len(bass),"localized_count":sum(x["nearest_drum_reference"] is not None for x in locs),
      "unresolved_count":sum(x["nearest_drum_reference"] is None for x in locs),
      "preceding_available_count":sum(x["preceding_drum_reference"] is not None for x in locs),
      "following_available_count":sum(x["following_drum_reference"] is not None for x in locs),
      "nearest_available_count":sum(x["nearest_drum_reference"] is not None for x in locs),
      "nearest_tie_count":sum(x["nearest_selection_status"]=="EQUAL_DISTANCE_TIE" for x in locs),
      "nearest_selection_status_counts":dict(sorted(Counter(x["nearest_selection_status"] for x in locs).items())),
      "relationship_status_counts":dict(sorted(Counter(x["relationship_status"] for x in locs).items())),
      "signed_displacement_seconds":signed,"absolute_displacement_seconds":absolute,
      "signed_displacement_descriptive":describe(signed),"absolute_displacement_descriptive":describe(absolute)}
    return {"pulse_candidates_without_strength_or_confidence":candidates,"elementary_metric_events":events,
      "drum_relative_localizations":locs,"rhythm_section_timing_profile":profile,"source_summary":summary,"geometry_summary":geometry}

def child(path):
    _d,_i,paths=verify_authority(); write(path,run_once(paths))

def freeze():
    dataset,inputs,paths=verify_authority()
    with tempfile.TemporaryDirectory(prefix="cedval006_replay_") as td:
        a,b=Path(td)/"a.json",Path(td)/"b.json"; command=[sys.executable,str(Path(__file__).resolve()),"run-once"]
        subprocess.run(command+[str(a)],check=True); subprocess.run(command+[str(b)],check=True)
        if a.read_bytes()!=b.read_bytes(): raise RuntimeError("DETERMINISTIC_REPLAY_FAILURE")
        result_once=json.loads(a.read_text())
    content={"schema":"JGA-CEDVAL006-REAL-LIVE-AUDIO-OBSERVATIONAL-RESULT/v1","study_id":STUDY,"execution_id":EXECUTION,
      "dataset_authority_id":dataset["authority_id"],"dataset_fingerprint":DATASET_FP,
      "analytical_input_authority_id":inputs["authority_id"],"analytical_input_fingerprint":INPUT_FP,
      "common_distributed_file_scope":{"sample_rate_hz":SR,"first_frame":0,"last_frame":NFRAMES-1,"frame_count":NFRAMES},
      "temporal_mapping":{"native_sample_rate_hz":SR,"resampling":False,"hop_samples":HOP,
      "producer_sample_coordinate_rule":"512 * producer_frame","timestamp_rule":"producer_sample_coordinate / 48000"},**result_once,
      "firewalls":{"correspondence_status":"GEOMETRIC_ONLY","calibration_applicability":"UNESTABLISHED","external_tracker_used":False,
      "bpm_used":False,"h02_used":False,"strength_accessed_by_scientific_execution":False,"symbolic_input_used":False,
      "musical_interpretation_performed":False,"jga_tuned":False,"raw_assets_changed":False,"production_code_changed":False,
      "historical_authorities_changed":False},"acquisition_authority":{"live_performance":"SUPPORTED_BY_PRIMARY_PROVIDER_DECLARATION",
      "raw_no_editing_no_tuning":"SUPPORTED_TO_THE_EXTENT_DECLARED_BY_LEWITT","shared_hardware_clock":"UNESTABLISHED_NOT_EXPLICITLY_DOCUMENTED",
      "common_session_time_origin":"UNESTABLISHED_NOT_EXPLICITLY_DOCUMENTED","physical_onset_ground_truth":"NOT_ESTABLISHED"},
      "deterministic_replay":"PASS_EXACT_TWO_FRESH_PROCESS_EXECUTIONS"}
    fp=sha256(canonical(content)).hexdigest()
    write(RUN/"input_manifest.json",{"study_id":STUDY,"execution_id":EXECUTION,"preregistration_commit":"8d0435a1184c89e31907960fc3c4a95628af679d",
      "clarification_commit":"ea967a153b3f561efc53c5277a18b729adc97af2","dataset_fingerprint":DATASET_FP,"analytical_input_fingerprint":INPUT_FP,
      "repository_checksums":REPO_HASHES,"raw_asset_checksums":{s:digest(p) for s,p in paths.items()},
      "environment":{"python":sys.version,"platform":platform.platform(),"librosa":librosa.__version__},
      "authority_gate":"PASS_RECOVERED_SIX_FIELD_BASIS","temporal_mapping_gate":"PASS_NATIVE_48000_HZ_NO_RESAMPLING"})
    mapping=(("pulse_candidates.json","pulse_candidates_without_strength_or_confidence"),("elementary_metric_events.json","elementary_metric_events"),
      ("drum_relative_localizations.json","drum_relative_localizations"),("rhythm_section_timing_profile.json","rhythm_section_timing_profile"),
      ("source_summary.json","source_summary"),("geometry_summary.json","geometry_summary"))
    for filename,key in mapping: write(RUN/filename,result_once[key])
    write(RUN/"scientific_content.json",content)
    result={"status":"PASS_FROZEN_REAL_LIVE_AUDIO_OBSERVATIONAL_PROFILE","study_id":STUDY,"execution_id":EXECUTION,
      "scientific_fingerprint":fp,"profile_id":result_once["rhythm_section_timing_profile"]["profile_id"],
      "profile_fingerprint":result_once["rhythm_section_timing_profile"]["scientific_fingerprint"],
      "source_summary":result_once["source_summary"],"geometry_summary":result_once["geometry_summary"],
      "deterministic_replay":content["deterministic_replay"],"firewalls":content["firewalls"]}; write(RUN/"result.json",result)
    write(RUN/"completion_protocol.json",{"study_id":STUDY,"status":result["status"],"dataset_fingerprint_basis":"PASS_RECOVERED_SIX_FIELD_BASIS",
      "temporal_mapping_gate":"PASS","ad037_cardinality_and_lineage":"PASS","ad038_geometry":"PASS","ad040_profile":"PASS",
      "deterministic_replay":result["deterministic_replay"],"scientific_fingerprint":fp})
    (RUN/"report.md").write_text(f"# {STUDY} Frozen Result\n\nStatus: **{result['status']}**\n\nScientific fingerprint: `{fp}`.\n\n"
      "The unchanged AD-037/AD-038/AD-040 stack produced an observational, frame-resolved profile on the native 48 kHz distributed-file coordinate. Correspondence remains `GEOMETRIC_ONLY`; calibration remains `UNESTABLISHED`.\n\n"
      "No external tracker, BPM, H02, strength analysis, symbolic input, correction or musical interpretation was used.\n")
    names=["execute.py","input_manifest.json","pulse_candidates.json","elementary_metric_events.json","drum_relative_localizations.json",
      "rhythm_section_timing_profile.json","source_summary.json","geometry_summary.json","scientific_content.json","result.json","completion_protocol.json","report.md"]
    write(RUN/"artifact_manifest.json",{"study_id":STUDY,"execution_id":EXECUTION,"scientific_fingerprint":fp,"artifacts":{n:digest(RUN/n) for n in names}})
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    if len(sys.argv)==3 and sys.argv[1]=="run-once": child(Path(sys.argv[2]))
    elif len(sys.argv)==1: freeze()
    else: raise SystemExit("usage: execute.py [run-once OUTPUT]")
