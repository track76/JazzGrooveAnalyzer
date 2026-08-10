"""Execute H-VAL001-C1-08 as an experiment-local measurement audit."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from decimal import Decimal, ROUND_HALF_EVEN
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from jga.core.candidate_period import (
    CandidatePeriod,
    CandidatePeriodObservationScope,
    CandidatePeriodOccurrence,
    CandidatePeriodPopulation,
    CandidatePeriodProvenance,
)


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
SOURCE_RECORD = ROOT / "validation/VAL-001/run_20260809_192908/blind_results.json"
EXPERIMENT_ID = "H-VAL001-C1-08"
SOURCE_REVISION = subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
).strip()
SAMPLE_RATE = 44100
CONTROLLED_SCALE = Decimal(7) / Decimal(10)
MEASUREMENT_REGIMES = (
    ("GRID-512-PHASE-0", 512, 0),
    ("GRID-512-PHASE-256", 512, 256),
    ("GRID-256-PHASE-0", 256, 0),
)
RECURRENCE_DEFINITION = (
    "exact consecutive positive frame interval occurring at least twice"
)
CORRESPONDENCE_CRITERION = (
    "Two Candidate Periods have experiment-local lineage-supported "
    "correspondence when at least two identical adjacent source-observation "
    "pairs support the first period and, after the declared controlled "
    "transformation and measurement operation, support the second period."
)


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fingerprint(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode()
    return sha256(encoded).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )


def quantize(
    sample_positions: tuple[Decimal, ...],
    frame_length_samples: int,
    grid_origin_samples: int,
) -> tuple[int, ...]:
    quantum = Decimal(frame_length_samples)
    origin = Decimal(grid_origin_samples)
    return tuple(
        int(
            ((position - origin) / quantum).to_integral_value(
                rounding=ROUND_HALF_EVEN
            )
        )
        for position in sample_positions
    )


def make_blind_inputs() -> tuple[dict[str, object], dict[str, object]]:
    source = json.loads(SOURCE_RECORD.read_text(encoding="utf-8"))
    source_execution = source["executions"]["BLIND-CONDITION-01"]
    timestamps = tuple(
        Decimal(str(value))
        for value in source_execution["pulse_candidate_timestamps_seconds"]
    )
    sample_positions = tuple(
        timestamp * Decimal(SAMPLE_RATE) for timestamp in timestamps
    )
    transformed_positions = tuple(
        position * CONTROLLED_SCALE for position in sample_positions
    )

    neutral_regimes: dict[str, object] = {}
    for regime_id, frame_length, grid_origin in MEASUREMENT_REGIMES:
        neutral_regimes[regime_id] = {
            "measurement_configuration": {
                "frame_length_samples": frame_length,
                "grid_origin_samples": grid_origin,
                "rounding": "ROUND_HALF_EVEN",
                "sample_rate_hz": SAMPLE_RATE,
            },
            "BLIND-POPULATION-01": {
                "event_ids": list(range(len(sample_positions))),
                "frame_positions": list(
                    quantize(sample_positions, frame_length, grid_origin)
                ),
            },
            "BLIND-POPULATION-02": {
                "event_ids": list(range(len(transformed_positions))),
                "frame_positions": list(
                    quantize(transformed_positions, frame_length, grid_origin)
                ),
            },
        }

    blind_inputs = {
        "experiment_id": EXPERIMENT_ID,
        "source_record_path": str(SOURCE_RECORD.relative_to(ROOT)),
        "source_record_sha256": sha256_file(SOURCE_RECORD),
        "source_blind_record_fingerprint": source["blind_record_fingerprint"],
        "source_observation_count": len(sample_positions),
        "neutral_measurement_regimes": neutral_regimes,
        "blind_exclusions": [
            "controlled transformation identity",
            "condition semantics",
            "Ground Truth",
            "MusicXML",
            "tempo",
            "beat",
            "meter",
            "metric level",
        ],
    }
    generation_record = {
        "experiment_id": EXPERIMENT_ID,
        "classification": "Declared Experimental Procedure",
        "source_population": "H-VAL001-C1-07 BLIND-CONDITION-01",
        "source_event_identity": "stable zero-based observation index",
        "condition_assignment": {
            "BLIND-POPULATION-01": "identity transformation",
            "BLIND-POPULATION-02": "sample position multiplied by 7/10",
        },
        "controlled_temporal_scale": "7/10",
        "musical_semantics": "none",
        "measurement_regimes": [
            {
                "measurement_regime_id": regime_id,
                "frame_length_samples": frame_length,
                "grid_origin_samples": grid_origin,
                "sample_rate_hz": SAMPLE_RATE,
                "rounding": "ROUND_HALF_EVEN",
            }
            for regime_id, frame_length, grid_origin in MEASUREMENT_REGIMES
        ],
        "preregistered_correspondence_criterion": CORRESPONDENCE_CRITERION,
        "criterion_status": "experiment-local scientific hypothesis",
    }
    return blind_inputs, generation_record


def discover_population(
    regime_id: str,
    population_id: str,
    frame_positions: tuple[int, ...],
    configuration: dict[str, object],
    source_record_sha256: str,
) -> CandidatePeriodPopulation:
    occurrences: dict[int, list[CandidatePeriodOccurrence]] = {}
    frame_length = int(configuration["frame_length_samples"])
    grid_origin = int(configuration["grid_origin_samples"])
    for start_index, (start_frame, end_frame) in enumerate(
        zip(frame_positions, frame_positions[1:])
    ):
        interval = end_frame - start_frame
        if interval <= 0:
            continue
        start_seconds = Decimal(
            str((grid_origin + start_frame * frame_length) / SAMPLE_RATE)
        )
        end_seconds = Decimal(
            str((grid_origin + end_frame * frame_length) / SAMPLE_RATE)
        )
        occurrences.setdefault(interval, []).append(
            CandidatePeriodOccurrence(
                start_observation_index=start_index,
                end_observation_index=start_index + 1,
                start_seconds=start_seconds,
                end_seconds=end_seconds,
            )
        )

    candidates = tuple(
        CandidatePeriod(
            duration_seconds=Decimal(interval * frame_length) / Decimal(SAMPLE_RATE),
            recurrence_evidence=tuple(support),
        )
        for interval, support in sorted(occurrences.items())
        if len(support) >= 2
    )
    return CandidatePeriodPopulation(
        observation_scope=CandidatePeriodObservationScope(
            observation_population_id=f"{regime_id}:{population_id}",
            source_identity=str(SOURCE_RECORD.relative_to(ROOT)),
            start_seconds=Decimal("0"),
            end_seconds=max(
                (occurrence.end_seconds for c in candidates for occurrence in c.recurrence_evidence),
                default=Decimal("0"),
            ),
        ),
        provenance=CandidatePeriodProvenance(
            input_asset_path=str(SOURCE_RECORD.relative_to(ROOT)),
            input_asset_sha256=source_record_sha256,
            discovery_configuration=(
                ("frame_length_samples", str(frame_length)),
                ("grid_origin_samples", str(grid_origin)),
                ("sample_rate_hz", str(SAMPLE_RATE)),
                ("rounding", str(configuration["rounding"])),
                ("recurrence_definition", RECURRENCE_DEFINITION),
            ),
            source_revision=SOURCE_REVISION,
        ),
        measurement_unit="seconds",
        candidates=candidates,
    )


def serialize_population(
    population: CandidatePeriodPopulation,
    frame_length: int,
) -> dict[str, object]:
    candidates = []
    for candidate in population.candidates:
        interval_frames = int(
            (
                candidate.duration_seconds
                * Decimal(SAMPLE_RATE)
                / Decimal(frame_length)
            ).to_integral_value(rounding=ROUND_HALF_EVEN)
        )
        candidates.append(
            {
                "duration_frames": interval_frames,
                "duration_seconds": str(candidate.duration_seconds),
                "occurrence_count": len(candidate.recurrence_evidence),
                "supporting_event_pairs": [
                    [
                        occurrence.start_observation_index,
                        occurrence.end_observation_index,
                    ]
                    for occurrence in candidate.recurrence_evidence
                ],
            }
        )
    result = {
        "observation_scope": asdict(population.observation_scope),
        "provenance": asdict(population.provenance),
        "measurement_unit": population.measurement_unit,
        "candidates": candidates,
        "deeply_immutable_runtime_type": True,
    }
    result["scientific_content_fingerprint"] = fingerprint(result)
    return result


def blind_discovery(blind_inputs: dict[str, object]) -> dict[str, object]:
    results: dict[str, object] = {}
    for regime_id, regime in blind_inputs["neutral_measurement_regimes"].items():
        configuration = regime["measurement_configuration"]
        frame_length = int(configuration["frame_length_samples"])
        populations = {}
        for population_id in ("BLIND-POPULATION-01", "BLIND-POPULATION-02"):
            frames = tuple(regime[population_id]["frame_positions"])
            population = discover_population(
                regime_id,
                population_id,
                frames,
                configuration,
                blind_inputs["source_record_sha256"],
            )
            populations[population_id] = serialize_population(
                population, frame_length
            )
        results[regime_id] = {
            "measurement_configuration": configuration,
            "populations": populations,
        }
    result = {
        "experiment_id": EXPERIMENT_ID,
        "source_revision": SOURCE_REVISION,
        "ground_truth_loaded": False,
        "condition_semantics_available": False,
        "measurement_results": results,
    }
    result["blind_scientific_fingerprint"] = fingerprint(result)
    return result


def candidate_support(candidate: dict[str, object]) -> set[tuple[int, int]]:
    return {tuple(pair) for pair in candidate["supporting_event_pairs"]}


def evaluate_correspondence(
    blind: dict[str, object],
    generation_record: dict[str, object],
) -> dict[str, object]:
    evaluations: dict[str, object] = {}
    for regime_id, regime in blind["measurement_results"].items():
        population_a = regime["populations"]["BLIND-POPULATION-01"]
        population_b = regime["populations"]["BLIND-POPULATION-02"]
        correspondences = []
        lineage_distributions = []
        for candidate_a in population_a["candidates"]:
            support_a = candidate_support(candidate_a)
            mapped_counts: Counter[int] = Counter()
            for candidate_b in population_b["candidates"]:
                shared = sorted(support_a & candidate_support(candidate_b))
                if shared:
                    mapped_counts[candidate_b["duration_frames"]] += len(shared)
                if len(shared) >= 2:
                    correspondences.append(
                        {
                            "population_01_duration_frames": candidate_a[
                                "duration_frames"
                            ],
                            "population_02_duration_frames": candidate_b[
                                "duration_frames"
                            ],
                            "shared_supporting_event_pairs": [
                                list(pair) for pair in shared
                            ],
                            "shared_support_count": len(shared),
                            "numerical_identity": (
                                candidate_a["duration_frames"]
                                == candidate_b["duration_frames"]
                            ),
                        }
                    )
            lineage_distributions.append(
                {
                    "population_01_duration_frames": candidate_a[
                        "duration_frames"
                    ],
                    "candidate_support_count": candidate_a["occurrence_count"],
                    "population_02_candidate_support_by_duration": {
                        str(key): value for key, value in sorted(mapped_counts.items())
                    },
                }
            )
        evaluations[regime_id] = {
            "correspondences": correspondences,
            "correspondence_count": len(correspondences),
            "lineage_distributions": lineage_distributions,
        }

    fingerprints = {
        regime_id: {
            population_id: regime["populations"][population_id][
                "scientific_content_fingerprint"
            ]
            for population_id in ("BLIND-POPULATION-01", "BLIND-POPULATION-02")
        }
        for regime_id, regime in blind["measurement_results"].items()
    }
    result = {
        "experiment_id": EXPERIMENT_ID,
        "ground_truth_loaded": False,
        "condition_assignment_revealed_after_blind_freeze": generation_record[
            "condition_assignment"
        ],
        "controlled_temporal_scale": generation_record[
            "controlled_temporal_scale"
        ],
        "correspondence_criterion": generation_record[
            "preregistered_correspondence_criterion"
        ],
        "measurement_evaluations": evaluations,
        "blind_population_fingerprints": fingerprints,
        "limitations": [
            "The second population is an experiment-local deterministic transformation of frozen observations, not an independent audio observation.",
            "The experiment isolates discrete remeasurement and does not validate onset detection or rendering correspondence.",
            "Lineage-supported correspondence does not establish equivalence, musical meaning, beat, tempo, meter, tactus or metric level.",
            "Absence of lineage-supported correspondence does not establish that observations are unrelated.",
        ],
    }
    result["post_blind_fingerprint"] = fingerprint(result)
    return result


def main() -> None:
    blind_inputs, generation_record = make_blind_inputs()
    write_json(RUN / "blind_inputs.json", blind_inputs)
    write_json(RUN / "measurement_generation_record.json", generation_record)

    first = blind_discovery(blind_inputs)
    repeated = blind_discovery(blind_inputs)
    if first["blind_scientific_fingerprint"] != repeated[
        "blind_scientific_fingerprint"
    ]:
        raise RuntimeError("Blind remeasurement was not deterministic")
    write_json(RUN / "blind_results.json", first)
    write_json(
        RUN / "reproducibility.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "first_fingerprint": first["blind_scientific_fingerprint"],
            "repeated_fingerprint": repeated["blind_scientific_fingerprint"],
            "deterministic": True,
        },
    )

    post_blind = evaluate_correspondence(first, generation_record)
    write_json(RUN / "post_blind_evaluation.json", post_blind)
    write_json(
        RUN / "runtime.log.json",
        {
            "execution_order": [
                "load frozen blind source observations",
                "generate neutral controlled measurement inputs",
                "execute blind Candidate Period discovery",
                "repeat blind discovery",
                "freeze blind results",
                "reveal controlled transformation and condition assignment",
                "evaluate preregistered lineage-supported correspondence",
            ],
            "ground_truth_access": "not performed",
            "production_code_modified": False,
        },
    )
    write_json(
        RUN / "artifact_manifest.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "repository_revision": SOURCE_REVISION,
            "artifacts": {
                path.name: sha256_file(path)
                for path in sorted(RUN.iterdir())
                if path.is_file() and path.name != "artifact_manifest.json"
            },
        },
    )


if __name__ == "__main__":
    main()
