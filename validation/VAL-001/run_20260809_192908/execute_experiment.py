"""Execute H-VAL001-C1-07 without changing production scientific logic."""

from __future__ import annotations

from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import wave

import numpy as np
from scipy.io import wavfile

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.dummy_multi_stem_separator import DummyMultiStemSeparator


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
PACKAGE = RUN / "controlled_dataset"
MANIFEST_PATH = PACKAGE / "controlled_dataset_manifest.json"
EXPERIMENT_ID = "H-VAL001-C1-07"
SOURCE_REVISION = subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
).strip()
PREVIOUS_B_HASHES = {
    "474b2e46ad2216f3d2d2446086c46bb2bcb93561effcf1c86e5bc6700e901b2e",
    "8081c634bcc6017c19d7d27068b9084ba5ada20246c585fa5c958c5db1fec71a",
}


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fingerprint(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def wav_identity(path: Path) -> dict[str, object]:
    with wave.open(str(path), "rb") as stream:
        if stream.getcomptype() != "NONE":
            raise ValueError(f"WAV is not PCM: {path.name}")
        result: dict[str, object] = {
            "codec": "PCM",
            "sample_rate_hz": stream.getframerate(),
            "bit_depth": stream.getsampwidth() * 8,
            "channel_count": stream.getnchannels(),
            "sample_count_per_channel": stream.getnframes(),
            "duration_seconds": stream.getnframes() / stream.getframerate(),
            "file_sha256": sha256_file(path),
        }
    if (
        result["sample_rate_hz"] != 44100
        or result["bit_depth"] != 24
        or result["channel_count"] != 2
    ):
        raise ValueError(f"Invalid controlled WAV format: {path.name}")
    return result


def first_last_nonzero(samples: np.ndarray) -> tuple[int | None, int | None]:
    active = np.any(samples != 0, axis=1) if samples.ndim == 2 else samples != 0
    indices = np.flatnonzero(active)
    if not len(indices):
        return None, None
    return int(indices[0]), int(indices[-1])


def compare_renders(canonical_path: Path, repeat_path: Path) -> dict[str, object]:
    rate_a, samples_a = wavfile.read(canonical_path)
    rate_b, samples_b = wavfile.read(repeat_path)
    if rate_a != rate_b or samples_a.shape != samples_b.shape:
        raise ValueError(
            f"Within-condition render extent differs: {canonical_path.name}"
        )
    first_a, last_a = first_last_nonzero(samples_a)
    first_b, last_b = first_last_nonzero(samples_b)
    # scipy represents 24-bit PCM left-justified in int32. Convert the exact
    # sample difference back to native 24-bit integer units.
    difference = (
        samples_a.astype(np.int64) - samples_b.astype(np.int64)
    ) // 256
    return {
        "sample_values_identical": bool(np.array_equal(samples_a, samples_b)),
        "differing_scalar_sample_count": int(np.count_nonzero(difference)),
        "total_scalar_sample_count": int(samples_a.size),
        "maximum_absolute_difference_24bit_units": int(
            np.max(np.abs(difference))
        ),
        "mean_absolute_difference_24bit_units": float(
            np.mean(np.abs(difference))
        ),
        "rms_difference_24bit_units": float(
            np.sqrt(np.mean(difference.astype(np.float64) ** 2))
        ),
        "first_nonzero_frame_canonical": first_a,
        "first_nonzero_frame_repeated": first_b,
        "last_nonzero_frame_canonical": last_a,
        "last_nonzero_frame_repeated": last_b,
    }


def finalize_and_validate_package() -> tuple[dict[str, object], dict[str, object]]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    measurements: dict[str, object] = {}
    for suffix in ("a", "b"):
        condition = manifest[f"condition_{suffix}"]
        for asset_name, filename in (
            ("canonical_wav", f"condition_{suffix}.wav"),
            ("repeated_render_wav", f"condition_{suffix}_repeat.wav"),
            ("catalogue_mp3", f"condition_{suffix}.mp3"),
        ):
            path = PACKAGE / "audio" / filename
            if not path.is_file():
                raise ValueError(f"Missing required asset: {filename}")
            condition[asset_name]["sha256"] = sha256_file(path)

        canonical = PACKAGE / "audio" / f"condition_{suffix}.wav"
        repeated = PACKAGE / "audio" / f"condition_{suffix}_repeat.wav"
        canonical_identity = wav_identity(canonical)
        repeat_identity = wav_identity(repeated)
        if canonical_identity["sample_count_per_channel"] != repeat_identity[
            "sample_count_per_channel"
        ]:
            raise ValueError(f"Condition {suffix} repeat length differs")
        measurements[suffix] = {
            "canonical": canonical_identity,
            "repeat": repeat_identity,
            "difference": compare_renders(canonical, repeated),
        }

    b_hashes = {
        measurements["b"]["canonical"]["file_sha256"],
        measurements["b"]["repeat"]["file_sha256"],
    }
    if b_hashes & PREVIOUS_B_HASHES:
        raise ValueError("Condition B reuses an H-VAL001-C1-06 WAV asset")
    if measurements["a"]["canonical"]["sample_count_per_channel"] == measurements[
        "b"
    ]["canonical"]["sample_count_per_channel"]:
        raise ValueError("Tempo contrast did not change physical render extent")

    observed_first_frames = {
        measurements[suffix]["difference"]["first_nonzero_frame_canonical"]
        for suffix in ("a", "b")
    }
    if len(observed_first_frames) != 1:
        raise ValueError("Conditions do not share the same first acoustic frame")

    dgr_path = PACKAGE / manifest["dataset_generation_record"]["repository_path"]
    manifest["dataset_generation_record"]["sha256"] = sha256_file(dgr_path)
    write_json(MANIFEST_PATH, manifest)

    pending_path = PACKAGE / "pending_catalog_items.json"
    pending = json.loads(pending_path.read_text(encoding="utf-8"))
    pending["status"] = "EXECUTION_LOCAL_CATALOGUE_READY"
    for suffix, item in zip(("a", "b"), pending["items"]):
        xml_path = PACKAGE / "symbolic" / f"condition_{suffix}.musicxml"
        mp3_path = PACKAGE / "audio" / f"condition_{suffix}.mp3"
        item["authoritative_musicxml"].update(
            {"sha256": sha256_file(xml_path), "repository_revision": SOURCE_REVISION}
        )
        item["mp3_recording"].update(
            {"sha256": sha256_file(mp3_path), "repository_revision": None}
        )
    write_json(pending_path, pending)

    package_evidence = {
        "experiment_id": EXPERIMENT_ID,
        "controlled_dataset_id": manifest["controlled_dataset_id"],
        "result": "VALID",
        "wav_measurements": measurements,
        "condition_b_distinct_from_c1_06": True,
        "temporal_origin": {
            "declared_procedure": "MusicXML score time zero = WAV sample zero",
            "observed_common_first_acoustic_frame": next(iter(observed_first_frames)),
            "classification": "Declared Experimental Procedure with supporting physical observation",
        },
        "limitations": [
            "A and B were not generated in one repository-controlled renderer.",
            "No audio-to-symbolic correspondence tolerance is defined.",
        ],
    }
    package_evidence["package_fingerprint"] = fingerprint(package_evidence)
    return manifest, package_evidence


def population_signature(context: object) -> dict[str, object]:
    population = context.candidate_period_population
    candidates = []
    for candidate in population.candidates:
        # M92 defines candidature by an exact integer frame interval. Recover
        # that already-authorized measurement identity from the preserved
        # duration and explicit discovery configuration.
        duration_frames = round(
            candidate.duration_seconds * Decimal(44100) / Decimal(512)
        )
        candidates.append(
            {
                "duration_seconds": str(candidate.duration_seconds),
                "duration_frames": duration_frames,
                "occurrence_count": len(candidate.recurrence_evidence),
                "occurrences": [
                    {
                        "start_observation_index": occurrence.start_observation_index,
                        "end_observation_index": occurrence.end_observation_index,
                        "start_seconds": str(occurrence.start_seconds),
                        "end_seconds": str(occurrence.end_seconds),
                    }
                    for occurrence in candidate.recurrence_evidence
                ],
            }
        )
    evidence = {
        "pulse_candidate_count": len(context.pulse_candidates or ()),
        "pulse_candidate_timestamps_seconds": [
            candidate.time for candidate in context.pulse_candidates or ()
        ],
        "pulse_candidate_strengths": [
            candidate.strength for candidate in context.pulse_candidates or ()
        ],
        "pulse_candidate_confidences": [
            candidate.confidence for candidate in context.pulse_candidates or ()
        ],
        "candidate_period_count": len(candidates),
        "candidates": candidates,
        "measurement_unit": population.measurement_unit,
        "discovery_configuration": list(population.provenance.discovery_configuration),
    }
    evidence["scientific_content_fingerprint"] = fingerprint(evidence)
    return evidence


def blind_analysis(path: Path) -> dict[str, object]:
    context = AnalysisPipeline(separator=DummyMultiStemSeparator()).analyze(str(path))
    return population_signature(context)


def duration_counts(execution: dict[str, object]) -> dict[str, int]:
    return {
        candidate["duration_seconds"]: candidate["occurrence_count"]
        for candidate in execution["candidates"]
    }


def post_blind(blind: dict[str, object]) -> dict[str, object]:
    from jga.ground_truth.loaders import MusicXmlGroundTruthLoader

    ground_truth = {}
    for suffix in ("a", "b"):
        gt_path = PACKAGE / "ground_truth" / f"condition_{suffix}.ground_truth.json"
        xml_path = PACKAGE / "symbolic" / f"condition_{suffix}.musicxml"
        ground_truth[suffix] = MusicXmlGroundTruthLoader(
            repository_root=ROOT,
            definition_path=gt_path.relative_to(ROOT),
        ).load(xml_path.relative_to(ROOT))

    a = blind["executions"]["BLIND-CONDITION-01"]
    b = blind["executions"]["BLIND-CONDITION-02"]
    a_candidates = {Decimal(c["duration_frames"]): c for c in a["candidates"]}
    b_candidates = {Decimal(c["duration_frames"]): c for c in b["candidates"]}
    expected_scale = (
        ground_truth["a"].tempo.beats_per_minute
        / ground_truth["b"].tempo.beats_per_minute
    )
    exact_pairs = []
    nearest_descriptions = []
    for a_frames, candidate_a in sorted(a_candidates.items()):
        target = a_frames * expected_scale
        if target in b_candidates:
            exact_pairs.append(
                {
                    "condition_a_frames": str(a_frames),
                    "condition_b_frames": str(target),
                    "condition_a_seconds": candidate_a["duration_seconds"],
                    "condition_b_seconds": b_candidates[target]["duration_seconds"],
                }
            )
        if b_candidates:
            nearest = min(b_candidates, key=lambda value: abs(value - target))
            nearest_descriptions.append(
                {
                    "condition_a_frames": str(a_frames),
                    "expected_scaled_frames": str(target),
                    "nearest_condition_b_frames": str(nearest),
                    "signed_frame_difference": str(nearest - target),
                }
            )

    result = {
        "experiment_id": EXPERIMENT_ID,
        "blind_record_fingerprint": blind["blind_record_fingerprint"],
        "condition_assignment": {
            "condition_a": "BLIND-CONDITION-01",
            "condition_b": "BLIND-CONDITION-02",
        },
        "ground_truth": {
            "condition_a_id": ground_truth["a"].ground_truth_id,
            "condition_b_id": ground_truth["b"].ground_truth_id,
            "condition_a_tempo": {
                "beats_per_minute": str(
                    ground_truth["a"].tempo.beats_per_minute
                ),
                "beat_unit": ground_truth["a"].tempo.beat_unit,
            },
            "condition_b_tempo": {
                "beats_per_minute": str(
                    ground_truth["b"].tempo.beats_per_minute
                ),
                "beat_unit": ground_truth["b"].tempo.beat_unit,
            },
            "derived_temporal_scale_b_over_a": str(expected_scale),
        },
        "candidate_period_counts": {
            "condition_a": duration_counts(a),
            "condition_b": duration_counts(b),
        },
        "exact_authoritative_scale_pairs": exact_pairs,
        "nearest_pair_descriptions_without_equivalence_claim": nearest_descriptions,
        "classification_rule": (
            "Without an authorized tolerance, only exact frame-domain scaling "
            "relationships support the scaling proposition."
        ),
        "scientific_classification": (
            "TEMPORAL SCALING EVIDENCE SUPPORTED"
            if exact_pairs
            else "EVIDENCE INSUFFICIENT"
        ),
        "limitations": [
            "No tolerance or equivalence threshold is authorized.",
            "Integer-frame observation quantization may prevent exact scaled equality.",
            "No candidate is assigned beat, tempo, tactus, subdivision or metric level.",
        ],
    }
    result["post_blind_fingerprint"] = fingerprint(result)
    return result


def refresh_artifact_manifest() -> None:
    artifacts = {}
    for path in sorted(RUN.rglob("*")):
        if not path.is_file() or path.name == "artifact_manifest.json":
            continue
        artifacts[str(path.relative_to(RUN))] = sha256_file(path)
    write_json(
        RUN / "artifact_manifest.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "repository_revision": SOURCE_REVISION,
            "artifacts": artifacts,
        },
    )


def main() -> None:
    _, package_evidence = finalize_and_validate_package()
    write_json(RUN / "audio_asset_validation.json", package_evidence)

    paths = {
        "BLIND-CONDITION-01": PACKAGE / "audio/condition_a.wav",
        "BLIND-CONDITION-01-REPEAT": PACKAGE / "audio/condition_a_repeat.wav",
        "BLIND-CONDITION-02": PACKAGE / "audio/condition_b.wav",
        "BLIND-CONDITION-02-REPEAT": PACKAGE / "audio/condition_b_repeat.wav",
    }
    executions = {identity: blind_analysis(path) for identity, path in paths.items()}
    replay_a = blind_analysis(paths["BLIND-CONDITION-01"])
    replay_b = blind_analysis(paths["BLIND-CONDITION-02"])
    blind = {
        "experiment_id": EXPERIMENT_ID,
        "repository_revision": SOURCE_REVISION,
        "ground_truth_available": False,
        "musicxml_available_to_analysis": False,
        "condition_tempo_available_to_analysis": False,
        "condition_assignment_revealed": False,
        "executions": executions,
        "deterministic_replay": {
            "BLIND-CONDITION-01": {
                "identical": replay_a == executions["BLIND-CONDITION-01"],
                "first_fingerprint": executions["BLIND-CONDITION-01"][
                    "scientific_content_fingerprint"
                ],
                "repeated_fingerprint": replay_a["scientific_content_fingerprint"],
            },
            "BLIND-CONDITION-02": {
                "identical": replay_b == executions["BLIND-CONDITION-02"],
                "first_fingerprint": executions["BLIND-CONDITION-02"][
                    "scientific_content_fingerprint"
                ],
                "repeated_fingerprint": replay_b["scientific_content_fingerprint"],
            },
        },
        "independent_render_population_equality": {
            "BLIND-CONDITION-01": duration_counts(executions["BLIND-CONDITION-01"])
            == duration_counts(executions["BLIND-CONDITION-01-REPEAT"]),
            "BLIND-CONDITION-02": duration_counts(executions["BLIND-CONDITION-02"])
            == duration_counts(executions["BLIND-CONDITION-02-REPEAT"]),
        },
    }
    blind["blind_record_fingerprint"] = fingerprint(blind)
    write_json(RUN / "blind_results.json", blind)

    post = post_blind(blind)
    write_json(RUN / "post_blind_evaluation.json", post)
    write_json(
        RUN / "validator_result.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "result": "VALID",
            "asset_validation_fingerprint": package_evidence["package_fingerprint"],
            "blind_record_fingerprint": blind["blind_record_fingerprint"],
            "post_blind_fingerprint": post["post_blind_fingerprint"],
            "scientific_classification": post["scientific_classification"],
        },
    )
    refresh_artifact_manifest()


if __name__ == "__main__":
    main()
