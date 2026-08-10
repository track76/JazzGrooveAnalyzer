"""Execute H-VAL001-C1-09 with a strict blind/post-blind boundary."""

from __future__ import annotations

from collections import Counter
from dataclasses import fields, is_dataclass
from decimal import Decimal
from enum import Enum
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.null_separator import NullSeparator


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
SOURCE_RUN = ROOT / "validation/VAL-001/run_20260809_171404"
INPUTS = {
    "BLIND-AUDIO-01": SOURCE_RUN / "controlled_dataset/audio/condition_a.wav",
    "BLIND-AUDIO-02": SOURCE_RUN / "controlled_dataset/audio/condition_a_repeat.wav",
    "BLIND-AUDIO-03": SOURCE_RUN / "controlled_dataset/audio/condition_b.wav",
    "BLIND-AUDIO-04": SOURCE_RUN / "controlled_dataset/audio/condition_b_repeat.wav",
}
PAIRS = {
    "PAIR-01": ("BLIND-AUDIO-01", "BLIND-AUDIO-02"),
    "PAIR-02": ("BLIND-AUDIO-03", "BLIND-AUDIO-04"),
}
EXPERIMENT_ID = "H-VAL001-C1-09"


def canonical(value: object) -> object:
    if is_dataclass(value):
        return {
            field.name: canonical(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (tuple, list)):
        return [canonical(item) for item in value]
    if isinstance(value, dict):
        return {str(key): canonical(item) for key, item in value.items()}
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(type(value).__name__)


def encoded(value: object) -> bytes:
    return json.dumps(
        canonical(value), sort_keys=True, separators=(",", ":")
    ).encode()


def fingerprint(value: object) -> str:
    return sha256(encoded(value)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(canonical(value), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def analyze(path: Path) -> dict[str, object]:
    context = AnalysisPipeline(separator=NullSeparator()).analyze(str(path))
    observations = tuple(context.pulse_candidates or ())
    population = context.candidate_period_population
    evidence = {
        "input_sha256": sha256_file(path),
        "sample_rate_hz": context.audio.sample_rate,
        "duration_seconds": context.audio.duration,
        "pulse_candidate_count": len(observations),
        "pulse_candidate_timestamps_seconds": [item.time for item in observations],
        "pulse_candidate_strengths": [item.strength for item in observations],
        "pulse_candidate_confidences": [item.confidence for item in observations],
        "measurement_unit": population.measurement_unit,
        "discovery_configuration": list(
            population.provenance.discovery_configuration
        ),
        "candidate_periods": [
            {
                "duration_seconds": str(candidate.duration_seconds),
                "occurrence_count": len(candidate.recurrence_evidence),
                "occurrences": [
                    {
                        "start_observation_index": item.start_observation_index,
                        "end_observation_index": item.end_observation_index,
                        "start_seconds": str(item.start_seconds),
                        "end_seconds": str(item.end_seconds),
                    }
                    for item in candidate.recurrence_evidence
                ],
            }
            for candidate in population.candidates
        ],
    }
    evidence["scientific_content_fingerprint"] = fingerprint(evidence)
    return evidence


def make_blind_record() -> dict[str, object]:
    record = {
        "experiment_id": EXPERIMENT_ID,
        "source_revision": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "analysis_configuration": {
            "pipeline": "AnalysisPipeline",
            "separator": "NullSeparator",
            "candidate_discovery": "CandidatePeriodDiscovery",
            "frame_length_samples": 512,
            "recurrence_definition": (
                "exact consecutive positive frame interval occurring at least twice"
            ),
        },
        "blind_exclusions": [
            "input condition relationship",
            "rendering lineage",
            "MusicXML",
            "Ground Truth",
            "tempo",
            "beat",
            "meter",
            "metric level",
        ],
        "executions": {
            identity: analyze(path) for identity, path in INPUTS.items()
        },
    }
    record["blind_record_fingerprint"] = fingerprint(record)
    return record


def candidate_map(execution: dict[str, object]) -> dict[str, set[tuple[str, str]]]:
    return {
        candidate["duration_seconds"]: {
            (occurrence["start_seconds"], occurrence["end_seconds"])
            for occurrence in candidate["occurrences"]
        }
        for candidate in execution["candidate_periods"]
    }


def evaluate_pair(
    left: dict[str, object], right: dict[str, object]
) -> dict[str, object]:
    left_times = left["pulse_candidate_timestamps_seconds"]
    right_times = right["pulse_candidate_timestamps_seconds"]
    exact_times = sorted(set(left_times) & set(right_times))
    left_candidates = candidate_map(left)
    right_candidates = candidate_map(right)
    correspondences = []
    for left_duration, left_support in left_candidates.items():
        for right_duration, right_support in right_candidates.items():
            shared = sorted(left_support & right_support)
            if len(shared) >= 2:
                correspondences.append(
                    {
                        "left_duration_seconds": left_duration,
                        "right_duration_seconds": right_duration,
                        "shared_exact_support_count": len(shared),
                        "shared_exact_supporting_timestamp_pairs": shared,
                    }
                )
    frame_seconds = 512 / 44100
    offsets = Counter(
        round((right_time - left_time) / frame_seconds)
        for left_time, right_time in zip(left_times, right_times)
    )
    return {
        "left_observation_count": len(left_times),
        "right_observation_count": len(right_times),
        "exact_timestamp_intersection_count": len(exact_times),
        "exact_timestamp_intersection": exact_times,
        "indexwise_offset_frames_distribution": dict(sorted(offsets.items())),
        "left_candidate_count": len(left_candidates),
        "right_candidate_count": len(right_candidates),
        "lineage_supported_correspondence_count": len(correspondences),
        "lineage_supported_correspondences": correspondences,
    }


def blind() -> None:
    first = make_blind_record()
    second = make_blind_record()
    if encoded(first) != encoded(second):
        raise RuntimeError("Blind deterministic replay differs")
    write_json(RUN / "blind_results.json", first)
    write_json(
        RUN / "reproducibility.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "deterministic_replay_identical": True,
            "first_fingerprint": first["blind_record_fingerprint"],
            "second_fingerprint": second["blind_record_fingerprint"],
            "blind_results_sha256": sha256_file(RUN / "blind_results.json"),
        },
    )


def post_blind() -> None:
    blind_path = RUN / "blind_results.json"
    source = json.loads(blind_path.read_text(encoding="utf-8"))
    package_manifest = SOURCE_RUN / "controlled_dataset/controlled_ab_manifest.json"
    generation_record = (
        SOURCE_RUN / "controlled_dataset/provenance/dataset_generation_record.md"
    )
    result = {
        "experiment_id": EXPERIMENT_ID,
        "source_blind_record_sha256": sha256_file(blind_path),
        "source_blind_record_fingerprint": source["blind_record_fingerprint"],
        "post_blind_authority": {
            "controlled_dataset_manifest_sha256": sha256_file(package_manifest),
            "dataset_generation_record_sha256": sha256_file(generation_record),
        },
        "post_blind_condition_assignment": {
            "PAIR-01": "CED-VAL-001-RD-001-A canonical and repeated render",
            "PAIR-02": "CED-VAL-001-RD-001-B canonical and repeated render",
        },
        "criterion": (
            "Under identical declared observation conditions and authoritatively "
            "shared symbolic/render lineage, Candidate Periods have experiment-local "
            "independent-audio lineage support only when at least two independently "
            "detected adjacent observation pairs have exactly identical start and "
            "end timestamps."
        ),
        "criterion_limitations": [
            "No numerical tolerance or event-order substitution is used.",
            "Non-identical detected timestamps remain indeterminate.",
            "The criterion is sufficient within this experiment and is not claimed necessary generally.",
        ],
        "pairs": {
            pair_id: evaluate_pair(
                source["executions"][left], source["executions"][right]
            )
            for pair_id, (left, right) in PAIRS.items()
        },
    }
    result["post_blind_fingerprint"] = fingerprint(result)
    write_json(RUN / "post_blind_evaluation.json", result)


if __name__ == "__main__":
    if sys.argv[1:] == ["blind"]:
        blind()
    elif sys.argv[1:] == ["post-blind"]:
        post_blind()
    else:
        raise SystemExit("usage: experiment.py {blind|post-blind}")
