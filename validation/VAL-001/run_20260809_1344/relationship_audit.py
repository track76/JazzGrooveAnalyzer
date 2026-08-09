"""Experiment-local H-VAL001-C1-04 relationship evidence audit.

This program analyzes an already frozen observation record. It is not a
production Candidate Period discovery implementation.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
RUN_DIRECTORY = Path(__file__).resolve().parent
INPUT_RECORD = (
    REPOSITORY_ROOT
    / "validation/VAL-001/run_20260809_100843/blind_candidate_discovery.json"
)
BLIND_OUTPUT = RUN_DIRECTORY / "blind_relationship_audit.json"
POST_BLIND_OUTPUT = RUN_DIRECTORY / "post_blind_comparison.json"
TARGET_FRAME_INTERVALS = (33, 66, 132)


def canonical_fingerprint(value: object) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def circular_residual(value: int, reference: int, period: int) -> int:
    forward = (value - reference) % period
    if forward > period / 2:
        return forward - period
    return forward


def candidate_by_interval(population: dict[str, Any]) -> dict[int, Any]:
    return {
        candidate["frame_interval"]: candidate
        for candidate in population[
            "recurrent_candidates_minimum_two_occurrences"
        ]
    }


def all_pair_evidence(
    frames: list[int],
    target: int,
) -> tuple[list[dict[str, int]], list[dict[str, Any]]]:
    adjacent: list[dict[str, int]] = []
    non_consecutive: list[dict[str, Any]] = []
    for start_index, start_frame in enumerate(frames):
        for end_index in range(start_index + 1, len(frames)):
            end_frame = frames[end_index]
            lag = end_frame - start_frame
            if lag > target:
                break
            if lag != target:
                continue
            pair = {
                "start_event_index": start_index,
                "end_event_index": end_index,
                "start_frame": start_frame,
                "end_frame": end_frame,
            }
            if end_index == start_index + 1:
                adjacent.append(pair)
            else:
                non_consecutive.append(
                    {
                        **pair,
                        "intervening_event_count": end_index - start_index - 1,
                        "constituent_consecutive_gaps": [
                            frames[index + 1] - frames[index]
                            for index in range(start_index, end_index)
                        ],
                    }
                )
    return adjacent, non_consecutive


def phase_evidence(
    candidate: dict[str, Any],
    event_frames: list[int],
) -> dict[str, Any]:
    period = candidate["frame_interval"]
    start_frames = [
        event_frames[occurrence["start_event_index"]]
        for occurrence in candidate["occurrences"]
    ]
    residues = [frame % period for frame in start_frames]
    frequencies = Counter(residues)
    modal_count = max(frequencies.values())
    modal_residues = sorted(
        residue for residue, count in frequencies.items() if count == modal_count
    )
    reference = modal_residues[0]
    return {
        "period_frames": period,
        "supporting_occurrence_count": len(start_frames),
        "start_frame_residue_frequency": {
            str(residue): frequencies[residue] for residue in sorted(frequencies)
        },
        "modal_residues_frames": modal_residues,
        "modal_residue_count": modal_count,
        "residual_reference_frames": reference,
        "circular_residuals_frames": [
            circular_residual(residue, reference, period) for residue in residues
        ],
        "residual_definition": (
            "signed shortest circular frame distance from the smallest modal "
            "start residue; descriptive only, with no threshold"
        ),
    }


def temporal_distribution(
    candidate: dict[str, Any],
    event_frames: list[int],
    observation_end_frame: int,
) -> dict[str, Any]:
    occurrences = candidate["occurrences"]
    start_frames = [
        event_frames[item["start_event_index"]] for item in occurrences
    ]
    end_frames = [event_frames[item["end_event_index"]] for item in occurrences]
    quartile_counts = [0, 0, 0, 0]
    for start_frame in start_frames:
        quartile = min(3, (4 * start_frame) // max(observation_end_frame, 1))
        quartile_counts[quartile] += 1
    sorted_starts = sorted(start_frames)
    gaps = [
        later - earlier for earlier, later in zip(sorted_starts, sorted_starts[1:])
    ]
    return {
        "period_frames": candidate["frame_interval"],
        "supporting_occurrence_count": len(occurrences),
        "first_occurrence_start_frame": min(start_frames),
        "last_occurrence_end_frame": max(end_frames),
        "support_span_frames": max(end_frames) - min(start_frames),
        "observation_span_frames": observation_end_frame,
        "support_span_fraction": (
            (max(end_frames) - min(start_frames)) / observation_end_frame
            if observation_end_frame
            else None
        ),
        "occurrence_start_counts_by_observation_quarter": quartile_counts,
        "consecutive_support_start_gaps_frames": gaps,
        "largest_support_start_gap_frames": max(gaps) if gaps else None,
    }


def analyze_source(source_name: str, source: dict[str, Any]) -> dict[str, Any]:
    population = source["elementary_metric_event_distinct_population"]
    frames = population["event_frames"]
    candidates = candidate_by_interval(population)
    observation_end_frame = round(
        source["audio_duration_seconds"] * source["sample_rate"] / source["hop_length"]
    )

    lag_audit: dict[str, Any] = {}
    phase_audit: dict[str, Any] = {}
    distribution_audit: dict[str, Any] = {}
    for target in TARGET_FRAME_INTERVALS:
        adjacent, non_consecutive = all_pair_evidence(frames, target)
        lag_audit[str(target)] = {
            "duration_seconds": target * source["frame_duration_seconds"],
            "all_supporting_pair_count": len(adjacent) + len(non_consecutive),
            "consecutive_pair_count": len(adjacent),
            "non_consecutive_pair_count": len(non_consecutive),
            "non_consecutive_pairs": non_consecutive,
            "additional_to_consecutive_inventory": bool(non_consecutive),
            "independence_from_existing_event_population": "not_established",
        }
        candidate = candidates.get(target)
        if candidate is not None:
            phase_audit[str(target)] = phase_evidence(candidate, frames)
            distribution_audit[str(target)] = temporal_distribution(
                candidate,
                frames,
                observation_end_frame,
            )

    return {
        "source_identity": source["source_identity"],
        "asset_path": source["asset_path"],
        "asset_sha256": source["asset_sha256"],
        "sample_rate": source["sample_rate"],
        "frame_length_samples": source["hop_length"],
        "frame_duration_seconds": source["frame_duration_seconds"],
        "event_count": len(frames),
        "observation_end_frame": observation_end_frame,
        "consecutive_candidate_baseline": [
            {
                "frame_interval": candidate["frame_interval"],
                "duration_seconds": candidate["duration_seconds"],
                "occurrence_count": candidate["occurrence_count"],
                "relative_frequency": candidate["relative_frequency"],
            }
            for candidate in population[
                "recurrent_candidates_minimum_two_occurrences"
            ]
        ],
        "target_non_consecutive_lag_audit": lag_audit,
        "target_phase_audit": phase_audit,
        "target_temporal_distribution_audit": distribution_audit,
    }


def cross_source_evidence(results: dict[str, Any]) -> dict[str, Any]:
    target_results: dict[str, Any] = {}
    for target in TARGET_FRAME_INTERVALS:
        rows: dict[str, Any] = {}
        for source_name, result in results.items():
            candidates = result["consecutive_candidate_baseline"]
            exact = next(
                (item for item in candidates if item["frame_interval"] == target),
                None,
            )
            nearest = min(
                candidates,
                key=lambda item: (
                    abs(item["frame_interval"] - target),
                    item["frame_interval"],
                ),
            )
            rows[source_name] = {
                "exact_consecutive_occurrence_count": (
                    exact["occurrence_count"] if exact else 0
                ),
                "all_pair_support_count": result[
                    "target_non_consecutive_lag_audit"
                ][str(target)]["all_supporting_pair_count"],
                "nearest_recurrent_frame_interval": nearest["frame_interval"],
                "nearest_difference_frames": nearest["frame_interval"] - target,
            }
        target_results[str(target)] = rows
    return {
        "targets": target_results,
        "independence_note": (
            "Each controlled WAV source is a distinct authoritative generated "
            "asset. Full-mix DummyMultiStemSeparator duplicates are excluded; "
            "only the distinct full-mix event population is used."
        ),
        "closeness_note": (
            "Nearest numerical differences are reported without a closeness "
            "threshold or equivalence classification."
        ),
    }


def build_blind_analysis(input_record: dict[str, Any]) -> dict[str, Any]:
    sources = {
        source_name: analyze_source(source_name, source)
        for source_name, source in input_record["first_execution"].items()
    }
    return {
        "experiment_id": "H-VAL001-C1-04",
        "scientific_protocol": "SVP-001",
        "source_experiment_id": input_record["experiment_id"],
        "source_blind_record_fingerprint": input_record[
            "blind_record_fingerprint"
        ],
        "repository_revision": "ea31e03fd4837491723d4f8a80b6d16dfa892bea",
        "bootstrap_revision": "ea31e03",
        "configuration": {
            "input_population": (
                "frozen distinct ElementaryMetricEvent frame populations from "
                "H-VAL001-C1-03 first blind execution"
            ),
            "target_frame_intervals": list(TARGET_FRAME_INTERVALS),
            "non_consecutive_lag_operation": (
                "exact positive differences for all event pairs with index "
                "distance greater than one"
            ),
            "phase_operation": (
                "supporting consecutive-occurrence start frame modulo exact "
                "candidate frame interval"
            ),
            "temporal_distribution_operation": (
                "raw support span, start counts in four equal observation-span "
                "partitions, and consecutive support-start gaps"
            ),
            "ground_truth_available": False,
            "metric_interpretation": "none",
            "thresholds": "none",
        },
        "sources": sources,
        "cross_source_evidence": cross_source_evidence(sources),
        "limitations": [
            "The audit uses already frozen observations and does not repeat audio analysis.",
            "All non-consecutive lags are mathematical relations within the same event population; statistical independence is not established.",
            "Modulo-phase descriptions use an experiment-local operation and no phase threshold.",
            "Four equal temporal partitions are descriptive coordinates, not canonical locality or persistence concepts.",
            "Nearest cross-source frame differences do not define equivalence or closeness.",
        ],
    }


def verify_assets(analysis: dict[str, Any]) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for source in analysis["sources"].values():
        path = REPOSITORY_ROOT / source["asset_path"]
        checksum = file_sha256(path)
        if checksum != source["asset_sha256"]:
            raise RuntimeError(f"Asset checksum mismatch: {source['asset_path']}")
        checksums[source["asset_path"]] = checksum
    return checksums


def run_blind() -> None:
    if BLIND_OUTPUT.exists():
        raise RuntimeError(f"Refusing to overwrite {BLIND_OUTPUT}")
    input_record = json.loads(INPUT_RECORD.read_text(encoding="utf-8"))
    first = build_blind_analysis(input_record)
    second = build_blind_analysis(input_record)
    first_fingerprint = canonical_fingerprint(first)
    second_fingerprint = canonical_fingerprint(second)
    output = {
        "blind_frozen_utc": datetime.now(timezone.utc).isoformat(),
        "first_execution_fingerprint": first_fingerprint,
        "repeated_execution_fingerprint": second_fingerprint,
        "deterministic_reproduction": first_fingerprint == second_fingerprint,
        "verified_asset_checksums": verify_assets(first),
        "analysis": first,
    }
    output["blind_record_fingerprint"] = canonical_fingerprint(output)
    BLIND_OUTPUT.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run_post_blind() -> None:
    if not BLIND_OUTPUT.exists():
        raise RuntimeError("Blind record must be frozen before Ground Truth loading.")
    if POST_BLIND_OUTPUT.exists():
        raise RuntimeError(f"Refusing to overwrite {POST_BLIND_OUTPUT}")

    from jga.ground_truth.loaders.musicxml_ground_truth_loader import (
        MusicXmlGroundTruthLoader,
    )

    getcontext().prec = 28
    loader = MusicXmlGroundTruthLoader()
    ground_truth = loader.load(Path(loader.SOURCE_PATH))
    quarter_duration = Decimal(60) / ground_truth.tempo.beats_per_minute
    references = {
        "half_quarter_duration_seconds": quarter_duration / 2,
        "quarter_duration_seconds": quarter_duration,
        "double_quarter_duration_seconds": quarter_duration * 2,
    }
    blind = json.loads(BLIND_OUTPUT.read_text(encoding="utf-8"))
    comparisons: dict[str, Any] = {}
    for source_name, source in blind["analysis"]["sources"].items():
        frame_duration = Decimal(str(source["frame_duration_seconds"]))
        comparisons[source_name] = {}
        for candidate in source["consecutive_candidate_baseline"]:
            frames = candidate["frame_interval"]
            duration = frame_duration * frames
            comparisons[source_name][str(frames)] = {
                "candidate_duration_seconds": str(duration),
                "reference_differences_seconds": {
                    name: str(duration - reference)
                    for name, reference in references.items()
                },
            }

    output = {
        "experiment_id": "H-VAL001-C1-04",
        "blind_record_sha256": file_sha256(BLIND_OUTPUT),
        "blind_record_fingerprint": blind["blind_record_fingerprint"],
        "ground_truth_loaded_after_blind_freeze": True,
        "ground_truth": {
            "ground_truth_id": ground_truth.ground_truth_id,
            "source_path": ground_truth.provenance.source.repository_path,
            "source_sha256": ground_truth.provenance.source.sha256,
            "tempo_beats_per_minute": str(
                ground_truth.tempo.beats_per_minute
            ),
            "tempo_beat_unit": ground_truth.tempo.beat_unit,
        },
        "derived_reference_durations_seconds": {
            name: str(value) for name, value in references.items()
        },
        "candidate_comparisons": comparisons,
        "epistemic_classification": {
            "ground_truth_tempo": "Observed Fact",
            "derived_reference_durations": "Logical Inference",
            "candidate_reference_differences": "Logical Inference",
        },
    }
    output["post_blind_record_fingerprint"] = canonical_fingerprint(output)
    POST_BLIND_OUTPUT.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    if sys.argv[1:] == ["blind"]:
        run_blind()
    elif sys.argv[1:] == ["post-blind"]:
        run_post_blind()
    else:
        raise SystemExit("usage: relationship_audit.py blind|post-blind")
