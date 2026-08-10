"""Execute H-VAL001-C1-10 measurement-perturbation invariance audit."""

from __future__ import annotations

from collections import Counter
from dataclasses import fields, is_dataclass
from decimal import Decimal
from enum import Enum
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import wave

import numpy as np
import soundfile as sf

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.null_separator import NullSeparator


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
SOURCE = ROOT / (
    "validation/VAL-001/run_20260809_171404/controlled_dataset/"
    "audio/condition_a.wav"
)
EXPERIMENT_ID = "H-VAL001-C1-10"
SHIFT_SAMPLES = 256
SAMPLE_RATE = 44100
FRAME_LENGTH = 512


def external_asset() -> Path:
    root = os.environ.get("JGA_EXTERNAL_ROOT", "").strip()
    if not root:
        raise RuntimeError("JGA_EXTERNAL_ROOT is required")
    destination = Path(root) / "experiments" / EXPERIMENT_ID / "audio"
    destination.mkdir(parents=True, exist_ok=True)
    return destination / "blind_audio_02.wav"


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


def wav_metadata(path: Path) -> dict[str, object]:
    with wave.open(str(path), "rb") as stream:
        frames = stream.readframes(stream.getnframes())
        return {
            "codec": "PCM" if stream.getcomptype() == "NONE" else stream.getcomptype(),
            "sample_rate_hz": stream.getframerate(),
            "bit_depth": stream.getsampwidth() * 8,
            "channel_count": stream.getnchannels(),
            "sample_count_per_channel": stream.getnframes(),
            "sample_data_sha256": sha256(frames).hexdigest(),
            "file_sha256": sha256_file(path),
        }


def prepare() -> None:
    destination = external_asset()
    samples, sample_rate = sf.read(SOURCE, dtype="int32", always_2d=True)
    if sample_rate != SAMPLE_RATE:
        raise RuntimeError("Unexpected source sample rate")
    if np.count_nonzero(samples[-SHIFT_SAMPLES:]) != 0:
        raise RuntimeError("Tail truncation would remove nonzero source samples")
    shifted = np.concatenate(
        (
            np.zeros((SHIFT_SAMPLES, samples.shape[1]), dtype=samples.dtype),
            samples[:-SHIFT_SAMPLES],
        )
    )
    sf.write(destination, shifted, sample_rate, subtype="PCM_24")
    recovered, recovered_rate = sf.read(
        destination, dtype="int32", always_2d=True
    )
    if recovered_rate != sample_rate:
        raise RuntimeError("Perturbed sample rate differs")
    if not np.array_equal(recovered[SHIFT_SAMPLES:], samples[:-SHIFT_SAMPLES]):
        raise RuntimeError("Perturbation did not preserve shifted source samples")
    record = {
        "experiment_id": EXPERIMENT_ID,
        "classification": "Declared Experimental Procedure",
        "perturbation": "prepend 256 zero samples and remove 256 verified-zero trailing samples",
        "changed_measurement_condition": "audio origin relative to the 512-sample observation grid",
        "unchanged": [
            "source sample ordering",
            "all nonzero sample values",
            "sample rate",
            "bit depth",
            "channel count",
            "sample count",
            "duration",
            "analysis configuration",
        ],
        "source": wav_metadata(SOURCE),
        "perturbed": wav_metadata(destination),
        "source_repository_path": str(SOURCE.relative_to(ROOT)),
        "perturbed_external_root_relative_path": str(
            destination.relative_to(Path(os.environ["JGA_EXTERNAL_ROOT"]))
        ),
        "shift_samples": SHIFT_SAMPLES,
        "truncated_tail_nonzero_scalar_count": 0,
        "shifted_sample_identity_verified": True,
    }
    write_json(RUN / "measurement_generation_record.json", record)


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
        "measurement_unit": population.measurement_unit,
        "discovery_configuration": list(
            population.provenance.discovery_configuration
        ),
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
            "frame_length_samples": FRAME_LENGTH,
            "sample_rate_hz": SAMPLE_RATE,
            "recurrence_definition": (
                "exact consecutive positive frame interval occurring at least twice"
            ),
        },
        "blind_exclusions": [
            "perturbation identity",
            "condition relationship",
            "MusicXML",
            "Ground Truth",
            "tempo",
            "beat",
            "meter",
            "metric level",
        ],
        "executions": {
            "BLIND-AUDIO-01": analyze(SOURCE),
            "BLIND-AUDIO-02": analyze(external_asset()),
        },
    }
    record["blind_record_fingerprint"] = fingerprint(record)
    return record


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


def candidate_map(execution: dict[str, object]) -> dict[str, set[tuple[str, str]]]:
    return {
        candidate["duration_seconds"]: {
            (occurrence["start_seconds"], occurrence["end_seconds"])
            for occurrence in candidate["occurrences"]
        }
        for candidate in execution["candidate_periods"]
    }


def post_blind() -> None:
    blind_path = RUN / "blind_results.json"
    source = json.loads(blind_path.read_text(encoding="utf-8"))
    generation_path = RUN / "measurement_generation_record.json"
    generation = json.loads(generation_path.read_text(encoding="utf-8"))
    left = source["executions"]["BLIND-AUDIO-01"]
    right = source["executions"]["BLIND-AUDIO-02"]
    shift_seconds = generation["shift_samples"] / SAMPLE_RATE
    left_times = left["pulse_candidate_timestamps_seconds"]
    right_times = right["pulse_candidate_timestamps_seconds"]
    aligned_right_times = [value - shift_seconds for value in right_times]
    aligned_offsets_samples = [
        round((right_time - shift_seconds - left_time) * SAMPLE_RATE)
        for left_time, right_time in zip(left_times, right_times)
    ]
    left_candidates = candidate_map(left)
    right_candidates = candidate_map(right)
    exact_candidate_durations = sorted(
        set(left_candidates) & set(right_candidates), key=Decimal
    )
    shift_decimal = Decimal(SHIFT_SAMPLES) / Decimal(SAMPLE_RATE)
    lineage_correspondences = []
    for duration in exact_candidate_durations:
        left_support = left_candidates[duration]
        aligned_right_support = {
            (
                str(Decimal(start) - shift_decimal),
                str(Decimal(end) - shift_decimal),
            )
            for start, end in right_candidates[duration]
        }
        shared_support = sorted(left_support & aligned_right_support)
        if len(shared_support) >= 2:
            lineage_correspondences.append(
                {
                    "duration_seconds": duration,
                    "shared_exact_aligned_support_count": len(shared_support),
                    "shared_exact_aligned_supporting_timestamp_pairs": shared_support,
                }
            )
    exact_aligned_observations = sorted(set(left_times) & set(aligned_right_times))
    result = {
        "experiment_id": EXPERIMENT_ID,
        "source_blind_record_sha256": sha256_file(blind_path),
        "source_blind_record_fingerprint": source["blind_record_fingerprint"],
        "measurement_generation_record_sha256": sha256_file(generation_path),
        "revealed_perturbation_samples": generation["shift_samples"],
        "revealed_perturbation_seconds": str(Decimal(SHIFT_SAMPLES) / Decimal(SAMPLE_RATE)),
        "observation_comparison": {
            "left_count": len(left_times),
            "right_count": len(right_times),
            "exact_aligned_timestamp_count": len(exact_aligned_observations),
            "aligned_indexwise_offset_samples_distribution": dict(
                sorted(Counter(aligned_offsets_samples).items())
            ),
            "strength_sequences_identical": left["pulse_candidate_strengths"]
            == right["pulse_candidate_strengths"],
            "confidence_sequences_identical": left["pulse_candidate_confidences"]
            == right["pulse_candidate_confidences"],
        },
        "candidate_comparison": {
            "left_count": len(left_candidates),
            "right_count": len(right_candidates),
            "exact_shared_duration_count": len(exact_candidate_durations),
            "exact_shared_durations_seconds": exact_candidate_durations,
            "left_only_durations_seconds": sorted(
                set(left_candidates) - set(right_candidates), key=Decimal
            ),
            "right_only_durations_seconds": sorted(
                set(right_candidates) - set(left_candidates), key=Decimal
            ),
            "lineage_supported_correspondence_count": len(
                lineage_correspondences
            ),
            "lineage_supported_correspondences": lineage_correspondences,
            "complete_populations_identical": left["candidate_periods"]
            == right["candidate_periods"],
        },
        "classification_rules": {
            "preserved_observation": "exact equality after reversing the declared sample shift",
            "preserved_candidate_period_correspondence": "at least two exactly aligned supporting timestamp pairs",
            "broken_correspondence": "requires established source-observation identity and is not inferred from absence",
            "observational_instability": "identical-input deterministic replay differs",
        },
        "limitations": [
            "Indexwise offsets are descriptive and do not establish event identity.",
            "No tolerance, nearest-neighbour rule or ordering substitution is used.",
            "Absence of exact aligned support is indeterminate, not unrelatedness.",
        ],
    }
    result["post_blind_fingerprint"] = fingerprint(result)
    write_json(RUN / "post_blind_evaluation.json", result)


if __name__ == "__main__":
    if sys.argv[1:] == ["prepare"]:
        prepare()
    elif sys.argv[1:] == ["blind"]:
        blind()
    elif sys.argv[1:] == ["post-blind"]:
        post_blind()
    else:
        raise SystemExit("usage: experiment.py {prepare|blind|post-blind}")
