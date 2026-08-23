"""Execute frozen H-CEDVAL003-CALIBRATION-ZERO-01 exactly once per replay."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
import platform
from pathlib import Path
from statistics import median
import sys

import numpy as np

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.engines.pulse_candidate_builder import PulseCandidateBuilder


BASE = Path("validation/CED-VAL-003-SWING-3-4/run_20260823_203324")
EXTERNAL = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-003-SWING")
AUTHORITY = BASE / "calibration_symbolic_events.json"
PAIR_AUTHORITY = BASE / "symbolic_pair_authority.json"
PREREG = Path("validation/CED-VAL-003-SWING-3-4/preregistrations/H-CEDVAL003-CALIBRATION-ZERO-01.md")
DATASET_MANIFEST = Path("validation/CED-VAL-003-SWING-3-4/input_authority_manifest.json")
INPUT_MANIFEST = BASE / "input_manifest.json"
EVENT_RESULTS = BASE / "event_level_results.json"
PAIR_RESULTS = BASE / "event_pair_results.json"
RESULT = BASE / "result.json"
SCOPE_END = Fraction(1024, 21)
SCOPE_MID = Fraction(512, 21)
FRAME = Fraction(512, 44100)
SOURCES = {
    "Drums": EXTERNAL / "steams/CED-VAL-003-SWING-3-4_drums.wav",
    "Double Bass": EXTERNAL / "steams/CED-VAL-003-SWING-3-4_bass.wav",
    "Piano": EXTERNAL / "steams/CED-VAL-003-SWING-3-4_piano.wav",
}
EXPECTED = {
    str(AUTHORITY): "fcb56adb0dfd6361ab6173107fc2f90d293caf8ca87d3fbc2e6b36e393f6a199",
    str(PAIR_AUTHORITY): "10cee0e96fc21b854714f426ca27543b94a63071b19861c7e28832f7e790fbf7",
    str(PREREG): "2f62d18830ed87cd210ac31f89310a9130e1b0bf29cacce62b6eefe873ff792b",
    str(DATASET_MANIFEST): "f53ce38c5324981753310736e47dd2620364e9a1a71848af50b4d5fb35d5e085",
    str(SOURCES["Drums"]): "11bd51037126608d7052ae0bb2b01d77b86eccae46d60ca088d3d5f57cccc44d",
    str(SOURCES["Double Bass"]): "bd702128f0b6e9887ccfae104ee0af6b2b4307c2021bb826fd85fec669322429",
    str(SOURCES["Piano"]): "64b95f5c41bb2bc102c68ffb2fa9b0215a2397e749f671ba2891378533302065",
    str(EXTERNAL / "symbolic/CED-VAL-003-SWING-3-4.musicxml"): "f74856b2766db824536bdbab0b3ab62dbcf8460c780272b88df13dec8620f4c2",
    str(EXTERNAL / "symbolic/CED-VAL-003-SWING-3-4.sib"): "f5d67d5e612e820ee8213ed02bf0d3303056ae5101d08f7c6e881b8e4252c477",
}


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_legacy():
    path = Path("validation/VAL-001/run_20260823_070702/experiment.py")
    spec = importlib.util.spec_from_file_location("frozen_calibration_methods", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    module.SCOPE_END = SCOPE_END
    module.SCOPE_MIDPOINT = SCOPE_MID
    module.FRAME_SPACING = FRAME
    return module


def frac(record: dict) -> Fraction:
    return Fraction(record["numerator"], record["denominator"])


def frecord(value: Fraction) -> dict:
    return {"exact": f"{value.numerator}/{value.denominator}", "numerator": value.numerator, "denominator": value.denominator, "decimal": str(float(value))}


def input_manifest() -> str:
    for path, expected in EXPECTED.items():
        if checksum(Path(path)) != expected:
            raise RuntimeError(f"frozen input checksum mismatch: {path}")
    payload = {
        "experiment_id": "H-CEDVAL003-CALIBRATION-ZERO-01",
        "source_revision": "6a373b9edd04758a3ca85534ccb6f3713707e93b",
        "dataset_id": "CED-VAL-003-SWING-3-4",
        "provenance_revision": "PR-CED-VAL-003-SWING-3-4-001",
        "dataset_fingerprint": "9345f5923055a7ed1c953eee4b8613f2b2262c55cd2e5f094d489d097c37f790",
        "frozen_inputs": EXPECTED,
        "origin": "DECLARED_SIBELIUS_EXPORT_FROM_BEGINNING",
        "scope_seconds": frecord(SCOPE_END),
        "midpoint_seconds": frecord(SCOPE_MID),
        "observation": {"hop_samples": PulseCandidateBuilder.FRAME_LENGTH_SAMPLES, "sample_rate_hz": 44100, "frame_spacing_seconds": frecord(FRAME), "pipeline": "jga.pipeline.default_analysis_pipeline.AnalysisPipeline", "declared_metric_reference": None, "declared_meter": None, "beat_reference_consumed": False},
        "execution": {"python": sys.version, "platform": platform.platform(), "numpy": np.__version__},
        "h02_executed": False,
    }
    INPUT_MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return checksum(INPUT_MANIFEST)


def analyze_all() -> dict:
    return {source: AnalysisPipeline().analyze(str(path)) for source, path in SOURCES.items()}


def partitions(records: list[dict], signed_key: str, time_key: str, label: str, legacy) -> dict:
    groups = {
        "full": records,
        "first_partition": [record for record in records if frac(record[time_key]) < SCOPE_MID],
        "second_partition": [record for record in records if frac(record[time_key]) >= SCOPE_MID],
    }
    return {name: {"signed_error_ms": legacy.descriptive(tuple(record[signed_key] for record in group)), "bootstrap_median_95": legacy.bootstrap_median_ci(tuple(record[signed_key] for record in group), f"partition:{label}:{signed_key}:{time_key}:{name}")} for name, group in groups.items()}


def build_pairs(pair_authority: dict, correspondences: dict) -> dict:
    lookup = {source: {record["calibration_symbolic_event_id"]: record for record in payload["event_results"]} for source, payload in correspondences.items()}
    output = {"Piano": [], "Double Bass": []}
    for pair in pair_authority["records"]:
        record = dict(pair)
        if pair["status"] != "VALID_SYMBOLIC_PAIR":
            record["jga_pair_status"] = pair["status"]
            output[pair["source"]].append(record)
            continue
        source_record = lookup[pair["source"]][pair["source_symbolic_event_id"]]
        drum_record = lookup["Drums"][pair["drum_symbolic_event_id"]]
        record["source_absolute_correspondence_status"] = source_record["correspondence_status"]
        record["drum_absolute_correspondence_status"] = drum_record["correspondence_status"]
        if source_record["correspondence_status"] != "VALID" or drum_record["correspondence_status"] != "VALID":
            record["jga_pair_status"] = "UNRESOLVED_JGA_PAIR"
            output[pair["source"]].append(record)
            continue
        source_gt, drum_gt = frac(source_record["t_gt_seconds"]), frac(drum_record["t_gt_seconds"])
        source_jga, drum_jga = frac(source_record["t_jga_seconds"]), frac(drum_record["t_jga_seconds"])
        delta_gt, delta_jga = source_gt - drum_gt, source_jga - drum_jga
        error = delta_jga - delta_gt
        ratio = error / FRAME
        lower = ratio.numerator // ratio.denominator
        frame_offset = min((lower, lower + 1), key=lambda value: (abs(ratio - value), abs(value), value))
        residual = error - frame_offset * FRAME
        record.update({"jga_pair_status": "VALID_JGA_PAIR", "source_eme_id": source_record["eme_id"], "drum_eme_id": drum_record["eme_id"], "source_t_gt_seconds": source_record["t_gt_seconds"], "drum_t_gt_seconds": drum_record["t_gt_seconds"], "source_t_jga_seconds": source_record["t_jga_seconds"], "drum_t_jga_seconds": drum_record["t_jga_seconds"], "delta_gt_seconds": frecord(delta_gt), "delta_jga_seconds": frecord(delta_jga), "signed_e_pair_seconds": frecord(error), "absolute_e_pair_seconds": frecord(abs(error)), "signed_e_pair_ms": float(error * 1000), "absolute_e_pair_ms": float(abs(error) * 1000), "frame_offset": frame_offset, "frame_residual_seconds": frecord(residual), "frame_residual_ms": float(residual * 1000), "normalized_frame_residual": float(residual / FRAME), "adjacent_to_unmatched_or_ambiguous_cell": bool(source_record["adjacent_to_unmatched_or_ambiguous_cell"] or drum_record["adjacent_to_unmatched_or_ambiguous_cell"]), "source_lineage": {key: source_record[key] for key in ("supporting_pulse_candidate_ids", "target_contributor_id", "target_sound_source_id", "source_asset_sha256", "materialization_rule", "temporal_scope")}, "drum_lineage": {key: drum_record[key] for key in ("supporting_pulse_candidate_ids", "target_contributor_id", "target_sound_source_id", "source_asset_sha256", "materialization_rule", "temporal_scope")}})
        output[pair["source"]].append(record)
    return output


def pair_classification(records: list[dict], source: str, legacy) -> dict:
    valid = [record for record in records if record["jga_pair_status"] == "VALID_JGA_PAIR"]
    sensitivity = [record for record in valid if not record["adjacent_to_unmatched_or_ambiguous_cell"]]
    def assess(items: list[dict], prefix: str) -> dict:
        groups = {"full": items, "first_partition": [r for r in items if frac(r["source_t_gt_seconds"]) < SCOPE_MID], "second_partition": [r for r in items if frac(r["source_t_gt_seconds"]) >= SCOPE_MID]}
        intervals = {name: legacy.bootstrap_median_ci(tuple(r["signed_e_pair_ms"] for r in group), f"pair:{source}:{prefix}:{name}") for name, group in groups.items()}
        support = len(groups["full"]) >= 10 and len(groups["first_partition"]) >= 5 and len(groups["second_partition"]) >= 5
        medians = [intervals[name]["median"] for name in groups]
        candidate = support and all(legacy.excludes_zero(intervals[name]) for name in groups) and all(value is not None and value != 0 for value in medians) and (all(value > 0 for value in medians) or all(value < 0 for value in medians)) and all(legacy.intervals_overlap(intervals[name], intervals["full"]) for name in ("first_partition", "second_partition"))
        no_detectable = support and not legacy.excludes_zero(intervals["full"]) and all(legacy.intervals_overlap(intervals[name], intervals["full"]) for name in ("first_partition", "second_partition"))
        return {"counts": {name: len(group) for name, group in groups.items()}, "bootstrap_intervals": intervals, "support": support, "candidate": candidate, "no_detectable": no_detectable}
    primary, sensitive = assess(valid, "primary"), assess(sensitivity, "sensitivity")
    if not primary["support"] or not sensitive["support"]:
        classification = "INSUFFICIENT_EVIDENCE"
    elif primary["candidate"] and sensitive["candidate"]:
        classification = "CANDIDATE_PAIRWISE_BIAS"
    elif primary["no_detectable"] and sensitive["no_detectable"]:
        classification = "NO_DETECTABLE_PAIRWISE_BIAS"
    else:
        classification = "UNSTABLE_PAIRWISE_MEASUREMENT"
    return {"classification": classification, "primary": primary, "sensitivity": sensitive, "sensitivity_conclusion_stable": primary["candidate"] == sensitive["candidate"] and primary["no_detectable"] == sensitive["no_detectable"]}


def main() -> None:
    manifest_sha = input_manifest()
    legacy = load_legacy()
    legacy.MANIFEST_SHA256 = manifest_sha
    authority = json.loads(AUTHORITY.read_text(encoding="utf-8"))
    pair_authority = json.loads(PAIR_AUTHORITY.read_text(encoding="utf-8"))
    first, second = analyze_all(), analyze_all()
    symbols = {source: tuple(event for event in authority["events"] if event["source"] == source) for source in SOURCES}
    first_corr = {source: legacy.correspondence_for_source(source, symbols[source], first[source].elementary_metric_events) for source in SOURCES}
    second_corr = {source: legacy.correspondence_for_source(source, symbols[source], second[source].elementary_metric_events) for source in SOURCES}
    replay = first_corr == second_corr
    if not replay:
        raise RuntimeError("deterministic absolute replay mismatch")
    first_pairs, second_pairs = build_pairs(pair_authority, first_corr), build_pairs(pair_authority, second_corr)
    if first_pairs != second_pairs:
        raise RuntimeError("deterministic pairwise replay mismatch")
    valid_by_source = {source: first_corr[source]["valid_records"] for source in SOURCES}
    statistics, temporal, frames, bias = {}, {}, {}, {}
    for source, records in valid_by_source.items():
        signed = tuple(record["signed_error_ms"] for record in records)
        absolute = tuple(record["absolute_error_ms"] for record in records)
        residual = tuple(record["frame_residual_ms"] for record in records)
        statistics[source] = {"signed_error_ms": legacy.descriptive(signed), "absolute_error_ms": legacy.descriptive(absolute)}
        temporal[source] = partitions(records, "signed_error_ms", "t_gt_seconds", source, legacy)
        frames[source] = {"frame_offsets": dict(sorted(Counter(record["frame_offset"] for record in records).items())), "frame_residual_ms": legacy.descriptive(residual), "normalized_frame_residual": legacy.descriptive(tuple(record["normalized_frame_residual"] for record in records)), "exact_frame_multiple_count": sum(value == 0 for value in residual)}
        bias[source] = legacy.candidate_bias(tuple(records), source)
        if not bias[source]["primary"]["support_requirement"] or not bias[source]["sensitivity"]["support_requirement"]:
            bias[source]["absolute_classification"] = "INSUFFICIENT_EVIDENCE"
        elif bias[source]["candidate_systematic_bias"]:
            bias[source]["absolute_classification"] = "CANDIDATE_SYSTEMATIC_BIAS"
        else:
            bias[source]["absolute_classification"] = "NO_DETECTABLE_SYSTEMATIC_BIAS"
    all_records = [record for source in SOURCES for record in valid_by_source[source]]
    statistics["Overall"] = {"signed_error_ms": legacy.descriptive(tuple(r["signed_error_ms"] for r in all_records)), "absolute_error_ms": legacy.descriptive(tuple(r["absolute_error_ms"] for r in all_records))}
    frames["Overall"] = {"frame_offsets": dict(sorted(Counter(r["frame_offset"] for r in all_records).items())), "frame_residual_ms": legacy.descriptive(tuple(r["frame_residual_ms"] for r in all_records)), "normalized_frame_residual": legacy.descriptive(tuple(r["normalized_frame_residual"] for r in all_records)), "exact_frame_multiple_count": sum(r["frame_residual_ms"] == 0 for r in all_records)}
    qualifying = tuple(source for source in SOURCES if bias[source]["candidate_systematic_bias"])
    differences = {}
    for index, first_source in enumerate(SOURCES):
        for second_source in tuple(SOURCES)[index + 1:]:
            differences[f"{first_source} - {second_source}"] = legacy.bootstrap_median_difference_ci(tuple(r["signed_error_ms"] for r in valid_by_source[first_source]), tuple(r["signed_error_ms"] for r in valid_by_source[second_source]), f"bias-difference:{first_source}:{second_source}")
    qualifying_intervals = [differences[f"{first_source} - {second_source}"] for index, first_source in enumerate(qualifying) for second_source in qualifying[index + 1:]]
    source_specific = bool(qualifying_intervals) and any(legacy.excludes_zero(interval) for interval in qualifying_intervals)
    pooled = tuple(r["signed_error_ms"] for source in qualifying for r in valid_by_source[source])
    pooled_ci = legacy.bootstrap_median_ci(pooled, "bias:pooled-qualifying")
    source_independent = len(qualifying) >= 2 and all(not legacy.excludes_zero(interval) for interval in qualifying_intervals) and legacy.excludes_zero(pooled_ci)
    absolute_outcome = "SOURCE_SPECIFIC_CANDIDATE_BIAS" if source_specific else "SOURCE_INDEPENDENT_CANDIDATE_BIAS" if source_independent else "NO_DETECTABLE_SYSTEMATIC_BIAS"
    pair_summaries = {}
    for source, records in first_pairs.items():
        valid = [record for record in records if record["jga_pair_status"] == "VALID_JGA_PAIR"]
        pair_summaries[source] = {"symbolic_pair_count": len(records), "valid_jga_pair_count": len(valid), "unmatched_symbolic_pair_count": sum(r["status"] == "UNMATCHED_SYMBOLIC_PAIR" for r in records), "ambiguous_symbolic_pair_count": sum(r["status"] == "AMBIGUOUS_SYMBOLIC_PAIR" for r in records), "unresolved_jga_pair_count": sum(r["jga_pair_status"] == "UNRESOLVED_JGA_PAIR" for r in records), "signed_e_pair_ms": legacy.descriptive(tuple(r["signed_e_pair_ms"] for r in valid)), "absolute_e_pair_ms": legacy.descriptive(tuple(r["absolute_e_pair_ms"] for r in valid)), "temporal": partitions(valid, "signed_e_pair_ms", "source_t_gt_seconds", f"{source}-Drums", legacy), "frame_offsets": dict(sorted(Counter(r["frame_offset"] for r in valid).items())), "frame_residual_ms": legacy.descriptive(tuple(r["frame_residual_ms"] for r in valid)), **pair_classification(records, source, legacy)}
    measurement_outcome = "MIXED_MEASUREMENT_BEHAVIOUR" if any(bias[source]["candidate_systematic_bias"] for source in SOURCES) and frames["Overall"]["exact_frame_multiple_count"] != len(all_records) else "QUANTIZATION_DOMINATED_MEASUREMENT" if frames["Overall"]["exact_frame_multiple_count"] == len(all_records) else "RESIDUAL_OR_UNSTABLE_MEASUREMENT_VARIABILITY"
    scientific = {"experiment_id": "H-CEDVAL003-CALIBRATION-ZERO-01", "dataset_fingerprint": "9345f5923055a7ed1c953eee4b8613f2b2262c55cd2e5f094d489d097c37f790", "symbolic_authority_fingerprint": authority["scientific_fingerprint"], "pair_authority_fingerprint": pair_authority["scientific_fingerprint"], "correspondence": first_corr, "pairs": first_pairs, "statistics": statistics, "temporal": temporal, "frames": frames, "bias": bias, "absolute_outcome": absolute_outcome, "pair_summaries": pair_summaries, "measurement_outcome": measurement_outcome}
    scientific = json.loads(json.dumps(scientific))
    fingerprint = sha256(json.dumps(scientific, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    EVENT_RESULTS.write_text(json.dumps({"experiment_id": scientific["experiment_id"], "input_manifest_sha256": manifest_sha, "correspondence_by_source": first_corr}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PAIR_RESULTS.write_text(json.dumps({"experiment_id": scientific["experiment_id"], "symbolic_pair_authority_fingerprint": pair_authority["scientific_fingerprint"], "pairs_by_source": first_pairs}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {"experiment_id": scientific["experiment_id"], "status": "PASS", "dataset_fingerprint": scientific["dataset_fingerprint"], "symbolic_authority_fingerprint": authority["scientific_fingerprint"], "pair_authority_fingerprint": pair_authority["scientific_fingerprint"], "input_manifest_sha256": manifest_sha, "population_summary": {source: {key: value for key, value in first_corr[source].items() if key.endswith("_count")} for source in SOURCES}, "statistics": statistics, "temporal_partitions": temporal, "frame_distributions": frames, "candidate_bias": bias, "source_median_difference_bootstrap": differences, "pooled_qualifying_bootstrap": pooled_ci, "absolute_bias_outcome": absolute_outcome, "measurement_structure_outcome": measurement_outcome, "pairwise": pair_summaries, "deterministic_replay": replay, "raw_observations_modified": False, "correction_authorized": False, "h02_executed": False, "declared_bpm_supplied_to_jga": False, "declared_meter_supplied_to_jga": False, "beat_reference_consumed_by_calibration": False, "rendering_detection_decomposition": "NOT_SUPPORTED_COMBINED_BEHAVIOUR_ONLY", "scientific_fingerprint": fingerprint}
    RESULT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "populations": summary["population_summary"], "absolute_outcome": absolute_outcome, "measurement_outcome": measurement_outcome, "pairwise": {source: {key: value for key, value in payload.items() if key in ("symbolic_pair_count", "valid_jga_pair_count", "classification")} for source, payload in pair_summaries.items()}, "scientific_fingerprint": fingerprint}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
