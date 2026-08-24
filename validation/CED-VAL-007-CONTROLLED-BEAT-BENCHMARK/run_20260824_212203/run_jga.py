"""Fresh-process frozen JGA raw-output constructor; no Ground Truth access."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import platform
import sys

import librosa

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            digest.update(chunk)
    return digest.hexdigest()


input_path, expected_sha, output_path = map(Path, sys.argv[1:])
if checksum(input_path) != expected_sha.name:
    raise RuntimeError("INPUT_AUTHORITY_CONFLICT")
analysis = AnalysisPipeline().analyze(str(input_path))
candidates = tuple(analysis.domain_pulse_candidates)
events = tuple(analysis.elementary_metric_events)
candidate_by_id = {str(item.id): item for item in candidates}
if len(candidate_by_id) != len(candidates) or len(events) != len(candidates):
    raise RuntimeError("AD037_CARDINALITY_CONFLICT")


def coordinate(timestamp: float) -> tuple[int, int]:
    frame = round(timestamp * 44100 / 512)
    sample = frame * 512
    if float(librosa.frames_to_time(frame, sr=44100, hop_length=512)).hex() != timestamp.hex():
        raise RuntimeError("TEMPORAL_MAPPING_CONFLICT")
    return frame, sample


candidate_records = []
for index, item in enumerate(candidates):
    frame, sample = coordinate(item.timestamp)
    candidate_records.append({
        "native_output_index": index,
        "output_id": str(item.id),
        "sound_source_id": str(item.sound_source_id),
        "producer_frame": frame,
        "producer_sample_coordinate": sample,
        "timestamp_seconds": item.timestamp,
        "timestamp_binary64_hex": item.timestamp.hex(),
        "observation_index": item.observation_index,
        "observation_provenance_id": item.observation_provenance_id,
    })

eme_records = []
for index, item in enumerate(events):
    lineage = [str(value) for value in item.supporting_pulse_candidate_ids]
    if len(lineage) != 1 or lineage[0] not in candidate_by_id:
        raise RuntimeError("AD037_LINEAGE_CONFLICT")
    candidate = candidate_by_id[lineage[0]]
    if item.timestamp.hex() != candidate.timestamp.hex() or item.source_asset_sha256 != expected_sha.name:
        raise RuntimeError("AD037_LINEAGE_CONFLICT")
    frame, sample = coordinate(item.timestamp)
    eme_records.append({
        "native_output_index": index,
        "output_id": str(item.id),
        "contributor_id": str(item.contributor_id),
        "sound_source_id": str(item.sound_source_id),
        "producer_frame": frame,
        "producer_sample_coordinate": sample,
        "timestamp_seconds": item.timestamp,
        "timestamp_binary64_hex": item.timestamp.hex(),
        "supporting_pulse_candidate_ids": lineage,
        "association_rule": item.association_rule,
        "association_outcome": item.association_outcome,
        "evidence_status": item.evidence_status,
        "materialization_rule": item.materialization_rule,
        "temporal_scope": item.temporal_scope,
        "source_asset_sha256": item.source_asset_sha256,
    })
candidate_records.sort(key=lambda value: (value["producer_frame"], value["output_id"]))
eme_records.sort(key=lambda value: (value["producer_frame"], value["output_id"]))
for index, record in enumerate(candidate_records):
    record["frozen_output_index"] = index
for index, record in enumerate(eme_records):
    record["frozen_output_index"] = index

record = {
    "system": "JGA",
    "epistemic_status": "FRAME_RESOLVED_JGA_OBSERVATION",
    "execution_call": "AnalysisPipeline().analyze(str(DRUM_GT_PATH))",
    "input_sha256": expected_sha.name,
    "pulse_candidates_without_strength_or_confidence": candidate_records,
    "ad037_elementary_metric_events": eme_records,
    "raw_output_count": len(eme_records),
    "frame_lattice": {"hop_samples": 512, "sample_rate_hz": 44100},
    "environment": {"python": sys.version, "platform": platform.platform(), "librosa": librosa.__version__},
    "ground_truth_accessed": False,
    "strength_or_confidence_accessed": False,
    "known_bpm_supplied": False,
}
record["scientific_fingerprint"] = sha256(canonical(record)).hexdigest()
output_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
