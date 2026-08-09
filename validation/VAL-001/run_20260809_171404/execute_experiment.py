"""Execute H-VAL001-C1-06 with a strict blind/post-blind boundary."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from decimal import Decimal
from enum import Enum
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import wave

import numpy as np
from scipy.io import wavfile

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.dummy_multi_stem_separator import DummyMultiStemSeparator
from tools.validate_controlled_ab_package import validate_package


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
PACKAGE = RUN / "controlled_dataset"
EXPERIMENT_ID = "H-VAL001-C1-06"
SOURCE_REVISION = subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
).strip()


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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
    if isinstance(value, tuple):
        return [canonical(item) for item in value]
    if isinstance(value, list):
        return [canonical(item) for item in value]
    if isinstance(value, dict):
        return {str(key): canonical(item) for key, item in value.items()}
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(f"Unsupported record value: {type(value).__name__}")


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        canonical(value), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def fingerprint(value: object) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


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
            "duration_seconds": stream.getnframes() / stream.getframerate(),
            "sample_data_sha256": sha256(frames).hexdigest(),
            "file_sha256": sha256_file(path),
        }


def repeat_difference(canonical_path: Path, repeated_path: Path) -> dict[str, object]:
    sample_rate_a, samples_a = wavfile.read(canonical_path)
    sample_rate_b, samples_b = wavfile.read(repeated_path)
    if sample_rate_a != sample_rate_b or samples_a.shape != samples_b.shape:
        raise ValueError("Repeated render measurement identity differs")
    # scipy exposes 24-bit PCM left-justified in int32; convert to signed 24-bit units.
    a = samples_a.astype(np.int64) // 256
    b = samples_b.astype(np.int64) // 256
    difference = a - b
    nonzero_a = np.flatnonzero(np.any(a != 0, axis=1))
    nonzero_b = np.flatnonzero(np.any(b != 0, axis=1))
    return {
        "file_bytes_identical": canonical_path.read_bytes() == repeated_path.read_bytes(),
        "sample_values_identical": bool(np.array_equal(a, b)),
        "differing_scalar_sample_count": int(np.count_nonzero(difference)),
        "total_scalar_sample_count": int(difference.size),
        "maximum_absolute_difference_24bit_units": int(np.max(np.abs(difference))),
        "mean_absolute_difference_24bit_units": float(np.mean(np.abs(difference))),
        "rms_difference_24bit_units": float(
            np.sqrt(np.mean(difference.astype(float) ** 2))
        ),
        "first_nonzero_frame_canonical": int(nonzero_a[0]) if len(nonzero_a) else None,
        "first_nonzero_frame_repeated": int(nonzero_b[0]) if len(nonzero_b) else None,
        "last_nonzero_frame_canonical": int(nonzero_a[-1]) if len(nonzero_a) else None,
        "last_nonzero_frame_repeated": int(nonzero_b[-1]) if len(nonzero_b) else None,
    }


def finalize_package_manifest() -> dict[str, object]:
    manifest_path = PACKAGE / "controlled_ab_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    measurements = {}
    for suffix in ("a", "b"):
        condition = manifest[f"condition_{suffix}"]
        for key, filename in (
            ("canonical_wav", f"condition_{suffix}.wav"),
            ("repeated_render_wav", f"condition_{suffix}_repeat.wav"),
            ("catalogue_mp3", f"condition_{suffix}.mp3"),
        ):
            path = PACKAGE / "audio" / filename
            condition[key] = {
                "repository_path": f"audio/{filename}",
                "sha256": sha256_file(path),
            }
        measurements[suffix] = wav_metadata(PACKAGE / "audio" / f"condition_{suffix}.wav")

    a_format = {
        key: measurements["a"][key]
        for key in (
            "sample_rate_hz",
            "bit_depth",
            "channel_count",
            "sample_count_per_channel",
        )
    }
    b_format = {
        key: measurements["b"][key]
        for key in a_format
    }
    if a_format != b_format:
        raise ValueError("Canonical condition WAV formats differ")
    manifest["controlled_audio_format"] = a_format

    dgr_path = PACKAGE / "provenance/dataset_generation_record.md"
    dgr = dgr_path.read_text(encoding="utf-8")
    marker = "\n## Supplied Audio Assets\n"
    if marker in dgr:
        dgr = dgr.split(marker, 1)[0].rstrip() + "\n"
    lines = [marker, "The following file identities and measurements are **Observed Facts**.\n"]
    for filename in (
        "condition_a.wav",
        "condition_a_repeat.wav",
        "condition_b.wav",
        "condition_b_repeat.wav",
        "condition_a.mp3",
        "condition_b.mp3",
    ):
        path = PACKAGE / "audio" / filename
        lines.append(f"- `audio/{filename}` — SHA-256 `{sha256_file(path)}`\n")
    lines.append(
        "\nAll WAV assets are stereo 24-bit PCM at 44.1 kHz with "
        f"{a_format['sample_count_per_channel']} samples per channel. "
        "The generating application, rendering library, generation date, and "
        "MP3 encoder configuration remain `not specified`.\n"
    )
    dgr_path.write_text(dgr + "".join(lines), encoding="utf-8")
    manifest["dataset_generation_record"]["sha256"] = sha256_file(dgr_path)
    write_json(manifest_path, manifest)

    pending_path = PACKAGE / "pending_catalog_items.json"
    pending = json.loads(pending_path.read_text(encoding="utf-8"))
    pending["status"] = "EXECUTION_LOCAL_CATALOGUE_READY"
    for suffix, item in zip(("a", "b"), pending["items"]):
        xml_path = PACKAGE / "symbolic" / f"condition_{suffix}.musicxml"
        mp3_path = PACKAGE / "audio" / f"condition_{suffix}.mp3"
        item["authoritative_musicxml"].update(
            {
                "sha256": sha256_file(xml_path),
                "repository_revision": SOURCE_REVISION,
            }
        )
        item["mp3_recording"].update(
            {
                "sha256": sha256_file(mp3_path),
                # The audio assets are first preserved by the experiment
                # commit prepared after this record is frozen. Do not assign
                # that not-yet-existing repository revision.
                "repository_revision": "not_specified",
            }
        )
    write_json(pending_path, pending)
    return manifest


def population_signature(context: object) -> dict[str, object]:
    population = context.candidate_period_population
    candidates = []
    for candidate in population.candidates:
        candidates.append(
            {
                "duration_seconds": str(candidate.duration_seconds),
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


class FixedIdentities:
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix
        self.index = 0

    def __call__(self) -> str:
        self.index += 1
        return f"{self.prefix}-{self.index:03d}"


def validation_chain(suffix: str, manifest: dict[str, object]) -> dict[str, object]:
    # Imported only after the blind record exists.
    from jga.analysis_representation import (
        CompletedAnalysisMaterializer,
        MaterializationProvenance,
    )
    from jga.comparator import ScientificComparator
    from jga.ground_truth.loaders import MusicXmlGroundTruthLoader
    from jga.scientific_validation_record import ScientificValidationRecordMaterializer
    from jga.validation_catalog.models import (
        ValidationAsset,
        ValidationItem,
        ValidationItemMetadata,
        ValidationItemProvenance,
    )

    condition = manifest[f"condition_{suffix}"]
    xml_path = PACKAGE / condition["authoritative_musicxml"]["repository_path"]
    mp3_path = PACKAGE / condition["catalogue_mp3"]["repository_path"]
    gt_path = PACKAGE / f"ground_truth/condition_{suffix}.ground_truth.json"
    item = ValidationItem(
        validation_item_id=condition["validation_item_id"],
        ground_truth_id=condition["ground_truth_id"],
        authoritative_musicxml=ValidationAsset(
            repository_path=str(xml_path.relative_to(ROOT)),
            sha256=sha256_file(xml_path),
            repository_revision=SOURCE_REVISION,
            licensing_status=condition["licensing_status"],
        ),
        mp3_recording=ValidationAsset(
            repository_path=str(mp3_path.relative_to(ROOT)),
            sha256=sha256_file(mp3_path),
            repository_revision="not_specified",
            licensing_status=condition["licensing_status"],
        ),
        provenance=ValidationItemProvenance(schema_version="1", item_version="1"),
        metadata=ValidationItemMetadata(
            title=f"H-VAL001-C1-06 Condition {suffix.upper()}"
        ),
    )
    ground_truth = MusicXmlGroundTruthLoader(
        repository_root=ROOT,
        definition_path=gt_path.relative_to(ROOT),
    ).load(xml_path.relative_to(ROOT))
    completed = AnalysisPipeline(separator=DummyMultiStemSeparator()).analyze(str(mp3_path))
    analysis = CompletedAnalysisMaterializer().materialize(
        completed,
        MaterializationProvenance(
            analysis_execution_id=f"{EXPERIMENT_ID}-{suffix.upper()}-MP3-ANALYSIS",
            audio_content_id=f"{condition['validation_item_id']}-MP3",
            source_revision=SOURCE_REVISION,
            pipeline_version="JGA-H-VAL001-C1-06",
            effective_configuration=(("separator", "dummy_multi_stem"),),
        ),
    )
    comparison = ScientificComparator(
        identity_factory=FixedIdentities(f"{EXPERIMENT_ID}-{suffix.upper()}")
    ).compare(item, analysis, ground_truth)
    record = ScientificValidationRecordMaterializer().materialize(
        comparison, analysis
    )
    return {
        "validation_item": item,
        "ground_truth": ground_truth,
        "immutable_analysis_representation": analysis,
        "comparison_result": comparison,
        "scientific_validation_record": record,
    }


def refresh_artifact_manifest() -> None:
    artifacts = {}
    for path in sorted(RUN.rglob("*")):
        if (
            not path.is_file()
            or path.name == "artifact_manifest.json"
            or "__pycache__" in path.parts
        ):
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
    manifest = finalize_package_manifest()
    package_validation = validate_package(PACKAGE)

    audio = {}
    for suffix in ("a", "b"):
        canonical_path = PACKAGE / "audio" / f"condition_{suffix}.wav"
        repeat_path = PACKAGE / "audio" / f"condition_{suffix}_repeat.wav"
        audio[suffix] = {
            "canonical": wav_metadata(canonical_path),
            "repeat": wav_metadata(repeat_path),
            "difference": repeat_difference(canonical_path, repeat_path),
        }
    write_json(
        RUN / "audio_asset_validation.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "package_validation": package_validation,
            "conditions": audio,
        },
    )

    # Blind phase: no Ground Truth, symbolic source, or condition interpretation.
    paths = {
        "BLIND-CONDITION-01": PACKAGE / "audio/condition_a.wav",
        "BLIND-CONDITION-01-REPEAT": PACKAGE / "audio/condition_a_repeat.wav",
        "BLIND-CONDITION-02": PACKAGE / "audio/condition_b.wav",
        "BLIND-CONDITION-02-REPEAT": PACKAGE / "audio/condition_b_repeat.wav",
    }
    blind_executions = {
        identity: blind_analysis(path) for identity, path in paths.items()
    }
    deterministic_replays = {
        "BLIND-CONDITION-01": blind_analysis(paths["BLIND-CONDITION-01"]),
        "BLIND-CONDITION-02": blind_analysis(paths["BLIND-CONDITION-02"]),
    }
    blind = {
        "experiment_id": EXPERIMENT_ID,
        "repository_revision": SOURCE_REVISION,
        "ground_truth_available": False,
        "musicxml_available_to_analysis": False,
        "event_removal_inventory_available_to_analysis": False,
        "condition_assignment_revealed": False,
        "executions": blind_executions,
        "deterministic_replay": {
            identity: {
                "first_fingerprint": blind_executions[identity][
                    "scientific_content_fingerprint"
                ],
                "repeated_fingerprint": replay["scientific_content_fingerprint"],
                "identical": (
                    blind_executions[identity]["scientific_content_fingerprint"]
                    == replay["scientific_content_fingerprint"]
                ),
            }
            for identity, replay in deterministic_replays.items()
        },
    }
    blind["blind_record_fingerprint"] = fingerprint(blind)
    write_json(RUN / "blind_results.json", blind)

    # Post-blind phase begins only after blind_results.json exists.
    chains = {
        "condition_a": validation_chain("a", manifest),
        "condition_b": validation_chain("b", manifest),
    }
    for name, chain in chains.items():
        write_json(RUN / f"{name}_immutable_analysis.json", chain["immutable_analysis_representation"])
        write_json(RUN / f"{name}_comparison_result.json", chain["comparison_result"])
        write_json(
            RUN / f"{name}_scientific_validation_record.json",
            chain["scientific_validation_record"],
        )

    first = blind_executions["BLIND-CONDITION-01"]
    second = blind_executions["BLIND-CONDITION-02"]
    repeat_first = blind_executions["BLIND-CONDITION-01-REPEAT"]
    repeat_second = blind_executions["BLIND-CONDITION-02-REPEAT"]

    def duration_counts(evidence: dict[str, object]) -> dict[str, int]:
        return {
            candidate["duration_seconds"]: candidate["occurrence_count"]
            for candidate in evidence["candidates"]
        }

    counts_a = duration_counts(first)
    counts_b = duration_counts(second)
    repeat_counts_a = duration_counts(repeat_first)
    repeat_counts_b = duration_counts(repeat_second)
    shared = sorted(set(counts_a) & set(counts_b), key=Decimal)

    gt_a = chains["condition_a"]["ground_truth"]
    gt_b = chains["condition_b"]["ground_truth"]
    post = {
        "experiment_id": EXPERIMENT_ID,
        "blind_record_fingerprint": blind["blind_record_fingerprint"],
        "condition_assignment": {
            "condition_a": "BLIND-CONDITION-01",
            "condition_b": "BLIND-CONDITION-02",
        },
        "ground_truth": {
            "condition_a_id": gt_a.ground_truth_id,
            "condition_b_id": gt_b.ground_truth_id,
            "shared_tempo": canonical(gt_a.tempo) if gt_a.tempo == gt_b.tempo else None,
            "shared_time_signature": (
                canonical(gt_a.time_signature)
                if gt_a.time_signature == gt_b.time_signature
                else None
            ),
            "shared_instrumentation": gt_a.instruments == gt_b.instruments,
        },
        "candidate_period_counts": {
            "condition_a": counts_a,
            "condition_b": counts_b,
            "condition_a_repeat": repeat_counts_a,
            "condition_b_repeat": repeat_counts_b,
        },
        "exact_shared_candidate_durations_seconds": shared,
        "shared_candidate_occurrence_differences_b_minus_a": {
            duration: counts_b[duration] - counts_a[duration] for duration in shared
        },
        "canonical_repeat_exact_duration_count_equality": {
            "condition_a": counts_a == repeat_counts_a,
            "condition_b": counts_b == repeat_counts_b,
        },
        "scientific_scope": (
            "Descriptive invariance evidence only; no candidate is assigned a "
            "metric level and no Ground Truth participated in discovery."
        ),
    }
    post["post_blind_fingerprint"] = fingerprint(post)
    write_json(RUN / "post_blind_evaluation.json", post)

    chain_results = {
        "experiment_id": EXPERIMENT_ID,
        "blind_record_fingerprint": blind["blind_record_fingerprint"],
    }
    chain_results.update(
        {
            name: {
                "validation_item_id": chain["validation_item"].validation_item_id,
                "analysis_execution_id": chain[
                    "immutable_analysis_representation"
                ].analysis_execution_id,
                "analysis_content_fingerprint": chain[
                    "immutable_analysis_representation"
                ].content_fingerprint,
                "comparison_execution_id": chain[
                    "comparison_result"
                ].comparison_execution_id,
                "comparison_result_id": chain["comparison_result"].comparison_result_id,
                "scientific_validation_record_id": chain[
                    "scientific_validation_record"
                ].record_id,
                "scientific_validation_record_fingerprint": chain[
                    "scientific_validation_record"
                ].record_fingerprint,
                "comparison_states": {
                    quantity: getattr(chain["comparison_result"], quantity).state.value
                    for quantity in (
                        "tempo",
                        "time_signature",
                        "sections",
                        "instrumentation",
                    )
                },
            }
            for name, chain in chains.items()
        },
    )
    write_json(RUN / "validation_chain_results.json", chain_results)

    write_json(
        RUN / "validator_result.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "result": "VALID",
            "package_validation": package_validation,
            "blind_execution_completed": True,
            "post_blind_evaluation_completed": True,
            "scientific_validation_records_completed": True,
        },
    )
    refresh_artifact_manifest()


if __name__ == "__main__":
    main()
