"""Blind drum observation freeze followed by post-blind symbolic audit."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import statistics
from xml.etree import ElementTree

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.null_separator import NullSeparator


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
MANIFEST_PATH = RUN / "manifest.json"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, indent=2, sort_keys=True).encode() + b"\n"


def write_json(path: Path, value: object) -> None:
    path.write_bytes(canonical_bytes(value))


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def freeze_blind(manifest: dict) -> dict:
    asset = ROOT / manifest["blind_asset"]["path"]
    if checksum(asset) != manifest["blind_asset"]["sha256"]:
        raise RuntimeError("Drum asset checksum mismatch")
    context = AnalysisPipeline(separator=NullSeparator()).analyze(str(asset))
    observations = [
        {
            "index": index,
            "timestamp_seconds": candidate.time,
            "strength": candidate.strength,
            "confidence": candidate.confidence,
        }
        for index, candidate in enumerate(context.pulse_candidates)
    ]
    return {
        "experiment_id": manifest["experiment_id"],
        "ground_truth_loaded": False,
        "asset_path": manifest["blind_asset"]["path"],
        "asset_sha256": manifest["blind_asset"]["sha256"],
        "sample_rate_hz": context.audio.sample_rate,
        "pulse_candidate_count": len(observations),
        "pulse_candidates": observations,
    }


def drum_onsets(musicxml: Path) -> list[float]:
    root = ElementTree.parse(musicxml).getroot()
    names = {
        item.attrib["id"]: item.findtext("part-name")
        for item in root.findall("./part-list/score-part")
    }
    part = next(
        item for item in root.findall("part")
        if names[item.attrib["id"]] == "Set di batteria"
    )
    position = 0.0
    divisions = 1
    last_start = 0.0
    onsets = []
    for measure in part.findall("measure"):
        declared_divisions = measure.find("attributes/divisions")
        if declared_divisions is not None:
            divisions = int(declared_divisions.text)
        for item in list(measure):
            if item.tag == "backup":
                position -= int(item.findtext("duration")) / divisions
            elif item.tag == "forward":
                position += int(item.findtext("duration")) / divisions
            elif item.tag == "note":
                duration = int(item.findtext("duration", "0")) / divisions
                chord = item.find("chord") is not None
                grace = item.find("grace") is not None
                start = last_start if chord else position
                if not chord:
                    last_start = start
                ties = {tie.attrib.get("type") for tie in item.findall("tie")}
                continuation = "stop" in ties and "start" not in ties
                if item.find("rest") is None and not continuation:
                    onsets.append(start)
                if not chord and not grace:
                    position += duration
    return sorted(set(onsets))


def evaluate(manifest: dict, blind: dict) -> dict:
    source = ROOT / manifest["ground_truth_asset"]["path"]
    if checksum(source) != manifest["ground_truth_asset"]["sha256"]:
        raise RuntimeError("Ground Truth checksum mismatch")
    positions = drum_onsets(source)
    expected = [position * 60.0 / 78.0 for position in positions]
    detected = [item["timestamp_seconds"] for item in blind["pulse_candidates"]]
    bound = manifest["measurement"]["correspondence_bound_seconds"]
    symbolic_edges = [
        [j for j, candidate in enumerate(detected) if abs(candidate - target) <= bound]
        for target in expected
    ]
    candidate_edges = [
        [i for i, target in enumerate(expected) if abs(candidate - target) <= bound]
        for candidate in detected
    ]
    matched = [
        (i, edges[0]) for i, edges in enumerate(symbolic_edges)
        if len(edges) == 1 and len(candidate_edges[edges[0]]) == 1
    ]
    errors = [detected[j] - expected[i] for i, j in matched]
    missed = [i for i, edges in enumerate(symbolic_edges) if len(edges) != 1]
    extra = [j for j, edges in enumerate(candidate_edges) if len(edges) != 1]
    duplicates = {
        "symbolic_with_multiple_candidates": sum(len(x) > 1 for x in symbolic_edges),
        "candidates_with_multiple_symbolic_onsets": sum(len(x) > 1 for x in candidate_edges),
    }
    if len(matched) == len(expected) == len(detected):
        result = "COMPLETE"
    elif matched:
        result = "PARTIAL"
    else:
        result = "FAILED"
    absolute = [abs(value) for value in errors]
    return {
        "ground_truth_loaded_after_blind_freeze": True,
        "symbolic_unique_onset_count": len(expected),
        "detected_pulse_candidate_count": len(detected),
        "score_positions_quarters": positions,
        "expected_timestamps_seconds": expected,
        "exact_match_count": int(
            sum(detected[j] == expected[i] for i, j in matched)
        ),
        "correspondence_match_count": len(matched),
        "missed_symbolic_indices": missed,
        "extra_candidate_indices": extra,
        "duplicate_assignments": duplicates,
        "matched_pairs": [
            {
                "symbolic_index": i,
                "candidate_index": j,
                "score_position_quarters": positions[i],
                "expected_seconds": expected[i],
                "detected_seconds": detected[j],
                "signed_error_seconds": detected[j] - expected[i],
            }
            for i, j in matched
        ],
        "timing_error_seconds": {
            "minimum_signed": min(errors) if errors else None,
            "maximum_signed": max(errors) if errors else None,
            "median_absolute": statistics.median(absolute) if absolute else None,
            "mean_absolute": statistics.fmean(absolute) if absolute else None,
        },
        "event_correspondence_result": result,
    }


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    if manifest["status"] != "PREREGISTERED":
        raise RuntimeError("Experiment is not preregistered")
    first = freeze_blind(manifest)
    second = freeze_blind(manifest)
    if canonical_bytes(first) != canonical_bytes(second):
        raise RuntimeError("Blind replay is not deterministic")
    write_json(RUN / "blind_observations.json", first)
    frozen_sha256 = checksum(RUN / "blind_observations.json")
    result = evaluate(manifest, first)
    result["blind_observations_sha256_before_ground_truth"] = frozen_sha256
    result["blind_replay_byte_identical"] = True
    write_json(RUN / "post_blind_correspondence.json", result)


if __name__ == "__main__":
    main()
