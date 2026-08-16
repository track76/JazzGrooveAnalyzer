"""Blind execution of H-VAL001-RHYTHM-TEMPO-01."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import platform
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


EXPERIMENT_ID = "H-VAL001-RHYTHM-TEMPO-01"
INPUT_SHA256 = "25ee4d610f6a3130f0b4f001b1908c8dad443d34ee30413905f6fd377202c9e8"
PREREG_SHA256 = "6750651e756e2533a58cd4a3cba357f874e56855d21416321ee5596f6a678925"
SAMPLE_RATE = 44100
FRAME_LENGTH = 512
MINIMUM_RECURRENCE = 2
RUN_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
INPUT = RUN_DIR / "blind_input.json"
PREREG = ROOT / "validation/VAL-001/preregistrations/H-VAL001-RHYTHM-TEMPO-01.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def candidate_identity(contributor: str, frames: int, occurrences: list[dict[str, Any]]) -> str:
    evidence = {
        "contributor": contributor,
        "duration_frames": frames,
        "occurrences": [
            [item["start_eme_id"], item["end_eme_id"]] for item in occurrences
        ],
    }
    return f"CP-{fingerprint(evidence)}"


def source_candidates(contributor: str, population: dict[str, Any]) -> dict[str, Any]:
    events = sorted(
        population["events"],
        key=lambda item: (item["absolute_timestamp_seconds"], item["eme_id"]),
    )
    projected = []
    for event in events:
        exact_frame = event["absolute_timestamp_seconds"] * SAMPLE_RATE / FRAME_LENGTH
        frame = round(exact_frame)
        projected.append(
            {
                **event,
                "frame_index": frame,
                "frame_quantization_residual": exact_frame - frame,
            }
        )
    first_time = projected[0]["absolute_timestamp_seconds"]
    last_time = projected[-1]["absolute_timestamp_seconds"]
    midpoint = (first_time + last_time) / 2.0
    occurrences_by_frames: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for index, (start, end) in enumerate(zip(projected, projected[1:])):
        duration = end["frame_index"] - start["frame_index"]
        if duration <= 0:
            continue
        occurrence_midpoint = (
            start["absolute_timestamp_seconds"] + end["absolute_timestamp_seconds"]
        ) / 2.0
        occurrences_by_frames[duration].append(
            {
                "start_index": index,
                "end_index": index + 1,
                "start_eme_id": start["eme_id"],
                "end_eme_id": end["eme_id"],
                "start_seconds": start["absolute_timestamp_seconds"],
                "end_seconds": end["absolute_timestamp_seconds"],
                "midpoint_seconds": occurrence_midpoint,
                "scope_half": "EARLY" if occurrence_midpoint < midpoint else "LATE",
            }
        )
    candidates = []
    for frames, occurrences in sorted(occurrences_by_frames.items()):
        if len(occurrences) < MINIMUM_RECURRENCE:
            continue
        half_counts = {
            "EARLY": sum(item["scope_half"] == "EARLY" for item in occurrences),
            "LATE": sum(item["scope_half"] == "LATE" for item in occurrences),
        }
        persistent = all(half_counts.values())
        candidate = {
            "candidate_id": candidate_identity(contributor, frames, occurrences),
            "duration_frames": frames,
            "duration_seconds": frames * FRAME_LENGTH / SAMPLE_RATE,
            "measurement_interval_frames": [frames - 1, frames + 1],
            "measurement_interval_seconds": [
                (frames - 1) * FRAME_LENGTH / SAMPLE_RATE,
                (frames + 1) * FRAME_LENGTH / SAMPLE_RATE,
            ],
            "recurrence_count": len(occurrences),
            "occurrences": occurrences,
            "half_counts": half_counts,
            "first_occurrence_midpoint": min(item["midpoint_seconds"] for item in occurrences),
            "last_occurrence_midpoint": max(item["midpoint_seconds"] for item in occurrences),
            "support_span_seconds": (
                max(item["midpoint_seconds"] for item in occurrences)
                - min(item["midpoint_seconds"] for item in occurrences)
            ),
            "persistence": "PERSISTENT" if persistent else "LIMITED_SCOPE",
            "eligible_for_consensus": persistent,
        }
        candidate["candidate_fingerprint"] = fingerprint(candidate)
        candidates.append(candidate)
    result = {
        "contributor": contributor,
        "input_fingerprint": population["input_fingerprint"],
        "eme_count": len(events),
        "observed_scope_seconds": [first_time, last_time],
        "scope_midpoint_seconds": midpoint,
        "projected_events": projected,
        "candidate_count": len(candidates),
        "persistent_candidate_count": sum(item["eligible_for_consensus"] for item in candidates),
        "candidates": candidates,
    }
    result["source_candidate_population_fingerprint"] = fingerprint(result)
    return result


def common_intersection(candidates: tuple[dict[str, Any], ...]) -> list[int] | None:
    lower = max(item["measurement_interval_frames"][0] for item in candidates)
    upper = min(item["measurement_interval_frames"][1] for item in candidates)
    return [lower, upper] if lower <= upper else None


def consensus_candidates(source_results: dict[str, Any]) -> list[dict[str, Any]]:
    eligible = {
        contributor: [item for item in result["candidates"] if item["eligible_for_consensus"]]
        for contributor, result in source_results.items()
    }
    triples = []
    contributors = tuple(source_results)
    for candidates in itertools.product(*(eligible[name] for name in contributors)):
        intersection = common_intersection(candidates)
        if intersection is not None:
            triples.append((tuple(zip(contributors, candidates, strict=True)), intersection))
    pairs = []
    for left_name, right_name in itertools.combinations(contributors, 2):
        for left, right in itertools.product(eligible[left_name], eligible[right_name]):
            pair_ids = {left["candidate_id"], right["candidate_id"]}
            if any(pair_ids.issubset({item[1]["candidate_id"] for item in triple}) for triple, _ in triples):
                continue
            intersection = common_intersection((left, right))
            if intersection is not None:
                pairs.append((((left_name, left), (right_name, right)), intersection))
    tuples = triples + pairs
    output = []
    for members, intersection in tuples:
        frame_values = [candidate["duration_frames"] for _, candidate in members]
        estimate_frames = sum(frame_values) / len(frame_values)
        period_seconds = estimate_frames * FRAME_LENGTH / SAMPLE_RATE
        identity_members = sorted(
            [
                {"contributor": contributor, "candidate_id": candidate["candidate_id"]}
                for contributor, candidate in members
            ],
            key=lambda item: (item["contributor"], item["candidate_id"]),
        )
        item = {
            "common_period_id": f"RCP-{fingerprint(identity_members)}",
            "supporting_sources": [contributor for contributor, _ in members],
            "source_candidates": identity_members,
            "source_duration_frames": frame_values,
            "equal_source_estimate_frames": estimate_frames,
            "period_seconds": period_seconds,
            "corresponding_rate": 60.0 / period_seconds,
            "common_measurement_intersection_frames": intersection,
            "common_measurement_intersection_seconds": [
                intersection[0] * FRAME_LENGTH / SAMPLE_RATE,
                intersection[1] * FRAME_LENGTH / SAMPLE_RATE,
            ],
            "corresponding_rate_interval": [
                60.0 / (intersection[1] * FRAME_LENGTH / SAMPLE_RATE),
                60.0 / (intersection[0] * FRAME_LENGTH / SAMPLE_RATE),
            ],
            "temporal_stability": "FULL_SCOPE_PERSISTENT",
            "source_persistence": {
                contributor: {
                    "half_counts": candidate["half_counts"],
                    "first_occurrence_midpoint": candidate["first_occurrence_midpoint"],
                    "last_occurrence_midpoint": candidate["last_occurrence_midpoint"],
                    "support_span_seconds": candidate["support_span_seconds"],
                }
                for contributor, candidate in members
            },
        }
        item["common_period_fingerprint"] = fingerprint(item)
        output.append(item)
    return sorted(output, key=lambda item: (item["equal_source_estimate_frames"], item["common_period_id"]))


def hierarchy(common: list[dict[str, Any]]) -> list[dict[str, Any]]:
    relationships = []
    for left, right in itertools.combinations(common, 2):
        shorter, longer = sorted((left, right), key=lambda item: item["equal_source_estimate_frames"])
        short_interval = shorter["common_measurement_intersection_frames"]
        long_interval = longer["common_measurement_intersection_frames"]
        overlap = [max(2 * short_interval[0], long_interval[0]), min(2 * short_interval[1], long_interval[1])]
        if overlap[0] <= overlap[1]:
            relationships.append(
                {
                    "relationship": "1:2_MEASUREMENT_INTERVAL_OVERLAP",
                    "shorter_candidate_id": shorter["common_period_id"],
                    "longer_candidate_id": longer["common_period_id"],
                    "overlap_frames": overlap,
                    "metric_role": "UNASSIGNED",
                }
            )
    return relationships


def classify(source_results: dict[str, Any], common: list[dict[str, Any]]) -> str:
    if len(common) == 1:
        return "UNIQUE_COMMON_PERIOD"
    if len(common) > 1:
        return "MULTIPLE_COMMON_PERIODS"
    stable_sources = sum(result["persistent_candidate_count"] > 0 for result in source_results.values())
    any_candidates = any(result["candidate_count"] > 0 for result in source_results.values())
    if stable_sources >= 2:
        return "SOURCE_DISAGREEMENT"
    if any_candidates:
        return "NO_COMMON_PERIOD"
    return "NO_COMMON_PERIOD"


def execute() -> dict[str, Any]:
    if sha256(INPUT) != INPUT_SHA256 or sha256(PREREG) != PREREG_SHA256:
        raise RuntimeError("Frozen input or preregistration checksum mismatch")
    blind_input = json.loads(INPUT.read_text())
    source_results = {
        contributor: source_candidates(contributor, population)
        for contributor, population in blind_input["populations"].items()
    }
    common = consensus_candidates(source_results)
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "BLIND_FROZEN",
        "epistemic_status": "DERIVED_EVIDENCE",
        "input_sha256": INPUT_SHA256,
        "preregistration_sha256": PREREG_SHA256,
        "ground_truth_accessed": False,
        "declared_bpm_accessed": False,
        "declared_meter_accessed": False,
        "declared_timeline_accessed": False,
        "normalized_phase_accessed": False,
        "musical_role_assigned": False,
        "configuration": {
            "sample_rate": SAMPLE_RATE,
            "frame_length_samples": FRAME_LENGTH,
            "minimum_recurrence": MINIMUM_RECURRENCE,
            "interval_uncertainty_frames": 1,
            "cross_source_maximum_frame_difference": 2,
            "minimum_supporting_sources": 2,
            "source_weighting": "one_equal_vote_per_contributor",
        },
        "environment": {"python": sys.version, "platform": platform.platform()},
        "source_results": source_results,
        "common_period_candidates": common,
        "hierarchical_relationships": hierarchy(common),
        "consensus_classification": classify(source_results, common),
        "voice_status": "DEFERRED",
    }
    result["scientific_fingerprint"] = fingerprint(result)
    return result


def main() -> None:
    first = execute()
    second = execute()
    first_bytes = canonical(first)
    second_bytes = canonical(second)
    replay = first_bytes == second_bytes
    if not replay:
        raise RuntimeError("Deterministic blind replay failed")
    (RUN_DIR / "blind_result.json").write_bytes(first_bytes + b"\n")
    freeze = {
        "experiment_id": EXPERIMENT_ID,
        "blind_result_sha256": hashlib.sha256(first_bytes + b"\n").hexdigest(),
        "scientific_fingerprint": first["scientific_fingerprint"],
        "deterministic_replay": replay,
        "ground_truth_accessed": False,
        "consensus_classification": first["consensus_classification"],
        "common_period_candidate_ids": [
            item["common_period_id"] for item in first["common_period_candidates"]
        ],
    }
    (RUN_DIR / "blind_freeze.json").write_bytes(canonical(freeze) + b"\n")


if __name__ == "__main__":
    main()
