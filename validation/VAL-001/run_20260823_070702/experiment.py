"""Execute frozen H-VAL001-CALIBRATION-ZERO-01 without changing inputs."""

from bisect import bisect_left, bisect_right
from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
from statistics import fmean, median, pstdev

import numpy as np

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline


getcontext().prec = 50
RUN_ID = "run_20260823_070702"
BASE = Path(f"validation/VAL-001/{RUN_ID}")
AUTHORITY_PATH = BASE / "calibration_symbolic_events.json"
AUTHORITY_SHA256 = "038a970994dcb42961d115c6b5c7dd2a05c714b52f5fec3a1756133b5cdedd9f"
MANIFEST_PATH = BASE / "input_manifest.json"
MANIFEST_SHA256 = "71bc3439eddf781c6fed531d29e67340616ca3ab8352904dfa53b68e38c02600"
OUTPUT_PATH = BASE / "result.json"
EVENTS_PATH = BASE / "event_level_results.json"
SOURCES = (
    ("Drums", "drums.wav"),
    ("Piano", "piano.wav"),
    ("Double Bass", "double_bass.wav"),
    ("Tenor Sax", "tenor_sax.wav"),
)
SCOPE_START = Fraction(0, 1)
SCOPE_END = Fraction(1865728, 44100)
SCOPE_MIDPOINT = (SCOPE_START + SCOPE_END) / 2
FRAME_SPACING = Fraction(512, 44100)
BOOTSTRAP_RESAMPLES = 10_000
MEASUREMENT_STRUCTURE_OUTCOME = "MIXED_MEASUREMENT_BEHAVIOUR"
QUANTIZATION_STRUCTURE_EVIDENCE = "PARTIAL"


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fraction_from_record(record: dict) -> Fraction:
    return Fraction(record["numerator"], record["denominator"])


def fraction_record(value: Fraction) -> dict[str, int | str]:
    decimal_value = Decimal(value.numerator) / Decimal(value.denominator)
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": str(decimal_value),
    }


def milliseconds(value: Fraction) -> float:
    return float(value * 1000)


def descriptive(values: tuple[float, ...]) -> dict:
    if not values:
        return {
            "n": 0,
            "minimum": None,
            "maximum": None,
            "mean": None,
            "median": None,
            "population_standard_deviation": None,
            "q1": None,
            "q2": None,
            "q3": None,
        }
    quartiles = np.quantile(np.asarray(values), (0.25, 0.5, 0.75), method="linear")
    return {
        "n": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": fmean(values),
        "median": median(values),
        "population_standard_deviation": pstdev(values),
        "q1": float(quartiles[0]),
        "q2": float(quartiles[1]),
        "q3": float(quartiles[2]),
    }


def seed_for(label: str) -> int:
    digest = sha256(f"{MANIFEST_SHA256}:{label}".encode()).hexdigest()
    return int(digest[:16], 16)


def bootstrap_median_ci(values: tuple[float, ...], label: str) -> dict:
    if not values:
        return {"n": 0, "lower_95": None, "median": None, "upper_95": None}
    population = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed_for(label))
    samples = rng.choice(
        population,
        size=(BOOTSTRAP_RESAMPLES, len(population)),
        replace=True,
    )
    medians = np.median(samples, axis=1)
    lower, upper = np.quantile(medians, (0.025, 0.975), method="linear")
    return {
        "n": len(values),
        "lower_95": float(lower),
        "median": median(values),
        "upper_95": float(upper),
        "resamples": BOOTSTRAP_RESAMPLES,
        "seed": seed_for(label),
    }


def bootstrap_median_difference_ci(
    first: tuple[float, ...], second: tuple[float, ...], label: str
) -> dict:
    if not first or not second:
        return {"lower_95": None, "median_difference": None, "upper_95": None}
    first_array = np.asarray(first, dtype=float)
    second_array = np.asarray(second, dtype=float)
    rng = np.random.default_rng(seed_for(label))
    first_samples = rng.choice(
        first_array, size=(BOOTSTRAP_RESAMPLES, len(first_array)), replace=True
    )
    second_samples = rng.choice(
        second_array, size=(BOOTSTRAP_RESAMPLES, len(second_array)), replace=True
    )
    differences = np.median(first_samples, axis=1) - np.median(second_samples, axis=1)
    lower, upper = np.quantile(differences, (0.025, 0.975), method="linear")
    return {
        "lower_95": float(lower),
        "median_difference": median(first) - median(second),
        "upper_95": float(upper),
        "resamples": BOOTSTRAP_RESAMPLES,
        "seed": seed_for(label),
    }


def excludes_zero(interval: dict) -> bool:
    lower = interval["lower_95"]
    upper = interval["upper_95"]
    return lower is not None and (lower > 0.0 or upper < 0.0)


def intervals_overlap(first: dict, second: dict) -> bool:
    return max(first["lower_95"], second["lower_95"]) <= min(
        first["upper_95"], second["upper_95"]
    )


def nearest_frame_offset(error: Fraction) -> int:
    ratio = error / FRAME_SPACING
    lower = ratio.numerator // ratio.denominator
    candidates = (lower, lower + 1)
    return min(
        candidates,
        key=lambda integer: (
            abs(ratio - integer),
            abs(integer),
            integer,
        ),
    )


def analyze_sources() -> dict:
    return {
        name: AnalysisPipeline().analyze(
            f"recordings/validation/stems/{filename}"
        )
        for name, filename in SOURCES
    }


def correspondence_for_source(source: str, symbolic_events: tuple, emes: tuple) -> dict:
    ordered_symbols = tuple(
        sorted(symbolic_events, key=lambda item: fraction_from_record(item["t_gt_seconds"]))
    )
    times = tuple(fraction_from_record(item["t_gt_seconds"]) for item in ordered_symbols)
    if len(times) != len(set(times)):
        raise RuntimeError(f"Symbolic grouping left duplicate times for {source}")
    boundaries = tuple((left + right) / 2 for left, right in zip(times, times[1:]))
    by_cell: dict[int, list] = {index: [] for index in range(len(ordered_symbols))}
    boundary_emes: dict[int, list] = {index: [] for index in range(len(boundaries))}
    unmatched_out_of_scope = []

    for eme in sorted(emes, key=lambda item: (item.timestamp, str(item.id))):
        observed_time = Fraction(str(eme.timestamp))
        if observed_time < SCOPE_START or observed_time >= SCOPE_END:
            unmatched_out_of_scope.append(eme)
            continue
        boundary_index = bisect_left(boundaries, observed_time)
        if boundary_index < len(boundaries) and boundaries[boundary_index] == observed_time:
            boundary_emes[boundary_index].append(eme)
            continue
        cell_index = bisect_right(boundaries, observed_time)
        by_cell[cell_index].append(eme)

    event_results = []
    valid_records = []
    invalid_cells = set()
    ambiguous_observed_ids = set()
    for index, symbol in enumerate(ordered_symbols):
        cell_emes = tuple(by_cell[index])
        if len(cell_emes) == 1:
            status = "VALID"
            eme = cell_emes[0]
            t_gt = times[index]
            t_jga = Fraction(str(eme.timestamp))
            error = t_jga - t_gt
            frame_offset = nearest_frame_offset(error)
            frame_residual = error - frame_offset * FRAME_SPACING
            record = {
                "source": source,
                "cell_index": index,
                "calibration_symbolic_event_id": symbol[
                    "calibration_symbolic_event_id"
                ],
                "t_gt_seconds": fraction_record(t_gt),
                "eme_id": str(eme.id),
                "t_jga_seconds": fraction_record(t_jga),
                "signed_error_seconds": fraction_record(error),
                "signed_error_ms": milliseconds(error),
                "absolute_error_seconds": fraction_record(abs(error)),
                "absolute_error_ms": milliseconds(abs(error)),
                "frame_offset": frame_offset,
                "frame_residual_seconds": fraction_record(frame_residual),
                "frame_residual_ms": milliseconds(frame_residual),
                "normalized_frame_residual": float(frame_residual / FRAME_SPACING),
                "target_contributor_id": str(eme.contributor_id),
                "target_sound_source_id": str(eme.sound_source_id),
                "supporting_pulse_candidate_ids": [
                    str(item) for item in eme.supporting_pulse_candidate_ids
                ],
                "source_asset_sha256": eme.source_asset_sha256,
                "temporal_scope": eme.temporal_scope,
                "materialization_rule": eme.materialization_rule,
                "correspondence_status": status,
            }
            valid_records.append(record)
            event_results.append(record)
        elif len(cell_emes) == 0:
            status = "UNMATCHED_SYMBOLIC"
            invalid_cells.add(index)
            event_results.append(
                {
                    "source": source,
                    "cell_index": index,
                    "calibration_symbolic_event_id": symbol[
                        "calibration_symbolic_event_id"
                    ],
                    "t_gt_seconds": symbol["t_gt_seconds"],
                    "correspondence_status": status,
                }
            )
        else:
            status = "AMBIGUOUS_MULTIPLE_OBSERVED"
            invalid_cells.add(index)
            ambiguous_observed_ids.update(str(eme.id) for eme in cell_emes)
            event_results.append(
                {
                    "source": source,
                    "cell_index": index,
                    "calibration_symbolic_event_id": symbol[
                        "calibration_symbolic_event_id"
                    ],
                    "t_gt_seconds": symbol["t_gt_seconds"],
                    "candidate_emes": [
                        {
                            "eme_id": str(eme.id),
                            "t_jga_seconds": fraction_record(Fraction(str(eme.timestamp))),
                            "supporting_pulse_candidate_ids": [
                                str(item) for item in eme.supporting_pulse_candidate_ids
                            ],
                        }
                        for eme in cell_emes
                    ],
                    "correspondence_status": status,
                }
            )

    boundary_records = []
    for boundary_index, boundary_items in boundary_emes.items():
        if not boundary_items:
            continue
        invalid_cells.update((boundary_index, boundary_index + 1))
        ambiguous_observed_ids.update(str(eme.id) for eme in boundary_items)
        for eme in boundary_items:
            boundary_records.append(
                {
                    "source": source,
                    "boundary_index": boundary_index,
                    "boundary_seconds": fraction_record(boundaries[boundary_index]),
                    "eme_id": str(eme.id),
                    "t_jga_seconds": fraction_record(Fraction(str(eme.timestamp))),
                    "correspondence_status": "AMBIGUOUS_BOUNDARY",
                }
            )

    adjacent_cells = {
        candidate
        for invalid in invalid_cells
        for candidate in (invalid - 1, invalid + 1)
        if 0 <= candidate < len(ordered_symbols)
    }
    for record in valid_records:
        record["adjacent_to_unmatched_or_ambiguous_cell"] = (
            record["cell_index"] in adjacent_cells
        )

    valid_ids = {record["eme_id"] for record in valid_records}
    unmatched_observed = [
        {
            "eme_id": str(eme.id),
            "t_jga_seconds": fraction_record(Fraction(str(eme.timestamp))),
            "reason": "OUTSIDE_DECLARED_SCOPE",
        }
        for eme in unmatched_out_of_scope
    ]
    accounted = valid_ids | ambiguous_observed_ids | {
        record["eme_id"] for record in unmatched_observed
    }
    all_ids = {str(eme.id) for eme in emes}
    if accounted != all_ids:
        missing = sorted(all_ids - accounted)
        raise RuntimeError(f"Unaccounted observed EME for {source}: {missing}")

    return {
        "source": source,
        "symbolic_event_count": len(ordered_symbols),
        "observed_eme_count": len(emes),
        "valid_correspondence_count": len(valid_records),
        "unmatched_symbolic_count": sum(
            item["correspondence_status"] == "UNMATCHED_SYMBOLIC"
            for item in event_results
        ),
        "unmatched_observed_count": len(unmatched_observed),
        "ambiguous_multiple_cell_count": sum(
            item["correspondence_status"] == "AMBIGUOUS_MULTIPLE_OBSERVED"
            for item in event_results
        ),
        "ambiguous_boundary_eme_count": len(boundary_records),
        "event_results": event_results,
        "boundary_results": boundary_records,
        "unmatched_observed": unmatched_observed,
        "valid_records": valid_records,
    }


def core_candidate_bias(records: tuple[dict, ...], label: str) -> dict:
    signed = tuple(record["signed_error_ms"] for record in records)
    first_half = tuple(
        record["signed_error_ms"]
        for record in records
        if fraction_from_record(record["t_gt_seconds"]) < SCOPE_MIDPOINT
    )
    second_half = tuple(
        record["signed_error_ms"]
        for record in records
        if fraction_from_record(record["t_gt_seconds"]) >= SCOPE_MIDPOINT
    )
    intervals = {
        "full": bootstrap_median_ci(signed, f"{label}:full"),
        "first_partition": bootstrap_median_ci(first_half, f"{label}:first"),
        "second_partition": bootstrap_median_ci(second_half, f"{label}:second"),
    }
    medians = tuple(intervals[name]["median"] for name in intervals)
    nonzero_medians = all(value is not None and value != 0.0 for value in medians)
    same_sign = nonzero_medians and (
        all(value > 0.0 for value in medians)
        or all(value < 0.0 for value in medians)
    )
    support = len(signed) >= 10 and len(first_half) >= 5 and len(second_half) >= 5
    intervals_exclude_zero = all(excludes_zero(value) for value in intervals.values())
    temporal_overlap = (
        support
        and intervals_overlap(intervals["first_partition"], intervals["full"])
        and intervals_overlap(intervals["second_partition"], intervals["full"])
    )
    passed = support and intervals_exclude_zero and same_sign and temporal_overlap
    return {
        "n": len(signed),
        "first_partition_n": len(first_half),
        "second_partition_n": len(second_half),
        "bootstrap_intervals": intervals,
        "support_requirement": support,
        "all_intervals_exclude_zero": intervals_exclude_zero,
        "same_sign": same_sign,
        "temporal_interval_overlap": temporal_overlap,
        "core_criterion_passed": passed,
    }


def candidate_bias(records: tuple[dict, ...], source: str) -> dict:
    primary = core_candidate_bias(records, f"bias:{source}:primary")
    sensitivity_records = tuple(
        record
        for record in records
        if not record["adjacent_to_unmatched_or_ambiguous_cell"]
    )
    sensitivity = core_candidate_bias(
        sensitivity_records, f"bias:{source}:sensitivity"
    )
    conclusion_stable = (
        primary["core_criterion_passed"] == sensitivity["core_criterion_passed"]
    )
    final_pass = primary["core_criterion_passed"] and conclusion_stable
    return {
        "source": source,
        "primary": primary,
        "sensitivity": sensitivity,
        "sensitivity_conclusion_stable": conclusion_stable,
        "authority_conflict": False,
        "candidate_systematic_bias": final_pass,
    }


def execute() -> tuple[dict, dict]:
    if checksum(AUTHORITY_PATH) != AUTHORITY_SHA256:
        raise RuntimeError("Frozen symbolic authority checksum mismatch")
    if checksum(MANIFEST_PATH) != MANIFEST_SHA256:
        raise RuntimeError("Frozen input manifest checksum mismatch")
    authority = load_json(AUTHORITY_PATH)
    if authority["authority_status"] != "SUFFICIENT":
        raise RuntimeError("Symbolic authority is not sufficient")

    first_analyses = analyze_sources()
    second_analyses = analyze_sources()
    symbolic_by_source = {
        source: tuple(
            event for event in authority["events"] if event["source"] == source
        )
        for source, _filename in SOURCES
    }
    first_correspondence = {
        source: correspondence_for_source(
            source,
            symbolic_by_source[source],
            first_analyses[source].elementary_metric_events,
        )
        for source, _filename in SOURCES
    }
    second_correspondence = {
        source: correspondence_for_source(
            source,
            symbolic_by_source[source],
            second_analyses[source].elementary_metric_events,
        )
        for source, _filename in SOURCES
    }
    deterministic_replay = first_correspondence == second_correspondence
    if not deterministic_replay:
        raise RuntimeError("Deterministic correspondence replay mismatch")

    valid_by_source = {
        source: tuple(first_correspondence[source]["valid_records"])
        for source, _filename in SOURCES
    }
    statistics = {}
    frame_distributions = {}
    for source, _filename in SOURCES:
        records = valid_by_source[source]
        signed = tuple(record["signed_error_ms"] for record in records)
        absolute = tuple(record["absolute_error_ms"] for record in records)
        residual = tuple(record["frame_residual_ms"] for record in records)
        normalized = tuple(record["normalized_frame_residual"] for record in records)
        statistics[source] = {
            "signed_error_ms": descriptive(signed),
            "absolute_error_ms": descriptive(absolute),
        }
        frame_distributions[source] = {
            "frame_offsets": dict(
                sorted(Counter(record["frame_offset"] for record in records).items())
            ),
            "frame_residual_ms": descriptive(residual),
            "normalized_frame_residual": descriptive(normalized),
            "exact_frame_multiple_count": sum(value == 0.0 for value in residual),
        }

    all_valid = tuple(
        record
        for source, _filename in SOURCES
        for record in valid_by_source[source]
    )
    overall_signed = tuple(record["signed_error_ms"] for record in all_valid)
    overall_absolute = tuple(record["absolute_error_ms"] for record in all_valid)
    overall_residual = tuple(record["frame_residual_ms"] for record in all_valid)
    overall_normalized = tuple(
        record["normalized_frame_residual"] for record in all_valid
    )
    statistics["Overall"] = {
        "signed_error_ms": descriptive(overall_signed),
        "absolute_error_ms": descriptive(overall_absolute),
    }
    frame_distributions["Overall"] = {
        "frame_offsets": dict(
            sorted(Counter(record["frame_offset"] for record in all_valid).items())
        ),
        "frame_residual_ms": descriptive(overall_residual),
        "normalized_frame_residual": descriptive(overall_normalized),
        "exact_frame_multiple_count": sum(value == 0.0 for value in overall_residual),
    }

    bias_results = {
        source: candidate_bias(valid_by_source[source], source)
        for source, _filename in SOURCES
    }
    qualifying = tuple(
        source
        for source, _filename in SOURCES
        if bias_results[source]["candidate_systematic_bias"]
    )
    pairwise = {}
    for index, first_source in enumerate(source for source, _filename in SOURCES):
        for second_source in tuple(source for source, _filename in SOURCES)[index + 1 :]:
            label = f"pairwise:{first_source}:{second_source}"
            pairwise[f"{first_source} - {second_source}"] = (
                bootstrap_median_difference_ci(
                    tuple(
                        record["signed_error_ms"]
                        for record in valid_by_source[first_source]
                    ),
                    tuple(
                        record["signed_error_ms"]
                        for record in valid_by_source[second_source]
                    ),
                    label,
                )
            )

    qualifying_pair_intervals = tuple(
        pairwise[f"{first_source} - {second_source}"]
        for index, first_source in enumerate(qualifying)
        for second_source in qualifying[index + 1 :]
    )
    source_specific = bool(qualifying_pair_intervals) and any(
        excludes_zero(interval) for interval in qualifying_pair_intervals
    )
    pooled_qualifying = tuple(
        record["signed_error_ms"]
        for source in qualifying
        for record in valid_by_source[source]
    )
    pooled_interval = bootstrap_median_ci(
        pooled_qualifying, "bias:pooled-qualifying"
    )
    source_independent = (
        len(qualifying) >= 2
        and all(not excludes_zero(interval) for interval in qualifying_pair_intervals)
        and excludes_zero(pooled_interval)
    )
    if source_specific:
        bias_outcome = "SOURCE_SPECIFIC_CANDIDATE_BIAS"
    elif source_independent:
        bias_outcome = "SOURCE_INDEPENDENT_CANDIDATE_BIAS"
    else:
        bias_outcome = "NO_DETECTABLE_SYSTEMATIC_BIAS"

    scientific_content = {
        "experiment_id": "H-VAL001-CALIBRATION-ZERO-01",
        "authority_fingerprint": authority["scientific_fingerprint"],
        "correspondence": first_correspondence,
        "statistics": statistics,
        "frame_distributions": frame_distributions,
        "candidate_bias": bias_results,
        "pairwise": pairwise,
        "bias_outcome": bias_outcome,
        "measurement_structure_outcome": MEASUREMENT_STRUCTURE_OUTCOME,
        "quantization_structure_evidence": QUANTIZATION_STRUCTURE_EVIDENCE,
    }
    fingerprint = sha256(
        json.dumps(scientific_content, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    event_payload = {
        "experiment_id": "H-VAL001-CALIBRATION-ZERO-01",
        "input_manifest_sha256": MANIFEST_SHA256,
        "authority_sha256": AUTHORITY_SHA256,
        "correspondence_by_source": first_correspondence,
    }
    summary = {
        "experiment_id": "H-VAL001-CALIBRATION-ZERO-01",
        "run_id": RUN_ID,
        "status": "PASS",
        "voice_status": "DEFERRED",
        "authority_status": authority["authority_status"],
        "authority_fingerprint": authority["scientific_fingerprint"],
        "input_manifest_sha256": MANIFEST_SHA256,
        "population_summary": {
            source: {
                key: value
                for key, value in first_correspondence[source].items()
                if key.endswith("_count")
            }
            for source, _filename in SOURCES
        },
        "statistics": statistics,
        "frame_distributions": frame_distributions,
        "candidate_bias": bias_results,
        "qualifying_candidate_bias_sources": qualifying,
        "pairwise_median_signed_error_difference_ms": pairwise,
        "pooled_qualifying_source_interval": pooled_interval,
        "bias_evidence_outcome": bias_outcome,
        "measurement_structure_outcome": MEASUREMENT_STRUCTURE_OUTCOME,
        "quantization_structure_evidence": QUANTIZATION_STRUCTURE_EVIDENCE,
        "deterministic_replay": deterministic_replay,
        "rendering_detection_decomposition": "NOT_SUPPORTED",
        "measured_behaviour": "COMBINED_RENDERING_MEASUREMENT",
        "correction_authorized": False,
        "raw_observations_modified": False,
        "declared_bpm_supplied_to_jga": False,
        "declared_meter_supplied_to_jga": False,
        "beat_reference_consumed_by_calibration": False,
        "scientific_fingerprint": fingerprint,
    }
    return event_payload, summary


def main() -> None:
    events, summary = execute()
    EVENTS_PATH.write_text(
        json.dumps(events, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    OUTPUT_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
