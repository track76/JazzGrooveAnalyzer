"""Execute frozen H-CEDVAL004-PHYSICAL-ONSET-MEASUREMENT-01."""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
from hashlib import sha256
import json
import platform
from pathlib import Path
import wave


getcontext().prec = 40
BASE = Path("validation/CED-VAL-004-PHYSICAL-ONSET")
RUN = BASE / "run_20260824_110800"
EXTERNAL = Path("/Volumes/SSD Track/JGA")
AUTHORITY = BASE / "input_authority_manifest.json"
SCHEDULE = BASE / "event_schedule.json"
PREREG = BASE / "preregistrations/H-CEDVAL004-PHYSICAL-ONSET-MEASUREMENT-01.md"
RULE_ID = "H-CEDVAL004-PHYSICAL-ONSET-MEASUREMENT-01"
EXECUTION_ID = "EXEC-CEDVAL004-PHYSICAL-ONSET-20260824-110800"
DATASET_FINGERPRINT = "704ce5926852a2ff62d9794dbee48156f875016979214cf7ef3ab93aa35ec772"
PREREG_COMMIT = "6c6ccde0de597b4e9c818d92eb88e814b8d9328e"
EXPECTED_REPOSITORY_SHA = {
    str(PREREG): "b9f845a94d917449e9615a46a298807d48da98b3ee1e2083259887b85b86f053",
    str(AUTHORITY): "823893f86f5d8a8b68e5ef57dce47739454897e93321dac1b815c735330d429a",
    str(SCHEDULE): "458227636da615278d5334039630f916d1b8be200587c37ae16a4673e8afe2dc",
}
SAMPLE_RATE = 44100
FRAME_COUNT = 8820000
SEARCH_LENGTH = 352800
BASELINE_LENGTH = 88200


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def decimal(value: Fraction, places: int = 15) -> str:
    raw = Decimal(value.numerator) / Decimal(value.denominator)
    return f"{raw:.{places}f}"


def read_pcm(path: Path) -> tuple[dict, bytes]:
    with wave.open(str(path), "rb") as stream:
        properties = {
            "channels": stream.getnchannels(),
            "sample_width_bytes": stream.getsampwidth(),
            "sample_rate_hz": stream.getframerate(),
            "frame_count": stream.getnframes(),
            "compression": stream.getcomptype(),
        }
        data = stream.readframes(stream.getnframes())
    if properties != {
        "channels": 2,
        "sample_width_bytes": 3,
        "sample_rate_hz": SAMPLE_RATE,
        "frame_count": FRAME_COUNT,
        "compression": "NONE",
    }:
        raise RuntimeError(f"AUTHORITY_CONFLICT WAV properties: {path}: {properties}")
    return properties, data


def sample(data: bytes, frame: int, channel: int) -> int:
    offset = (frame * 2 + channel) * 3
    return int.from_bytes(data[offset : offset + 3], "little", signed=True)


def first_difference(source: bytes, control: bytes, start: int, end: int, channel: int) -> tuple[int | None, int | None]:
    for frame in range(start, end):
        source_value = sample(source, frame, channel)
        if source_value != sample(control, frame, channel):
            return frame, source_value
    return None, None


def linear_quantile(sorted_values: list[int], proportion: Fraction) -> Fraction:
    position = Fraction(len(sorted_values) - 1) * proportion
    lower = position.numerator // position.denominator
    upper = lower if position.denominator == 1 else lower + 1
    if lower == upper:
        return Fraction(sorted_values[lower])
    weight = position - lower
    return Fraction(sorted_values[lower]) * (1 - weight) + Fraction(sorted_values[upper]) * weight


def describe(values: list[int]) -> dict:
    if not values:
        return {"n": 0}
    ordered = sorted(values)
    mean = Fraction(sum(ordered), len(ordered))
    variance = sum((Decimal(value) - Decimal(mean.numerator) / Decimal(mean.denominator)) ** 2 for value in ordered) / Decimal(len(ordered))
    sample_stats = {
        "minimum": Fraction(ordered[0]),
        "q1": linear_quantile(ordered, Fraction(1, 4)),
        "median": linear_quantile(ordered, Fraction(1, 2)),
        "q3": linear_quantile(ordered, Fraction(3, 4)),
        "maximum": Fraction(ordered[-1]),
        "mean": mean,
    }
    result = {"n": len(ordered), "quartile_method": "linear_interpolation_at_(n-1)*p", "samples": {}, "milliseconds": {}}
    for name, value in sample_stats.items():
        result["samples"][name] = {"exact": exact(value), "decimal": decimal(value)}
        ms = value * Fraction(1000, SAMPLE_RATE)
        result["milliseconds"][name] = {"exact": exact(ms), "decimal": decimal(ms)}
    sd_samples = variance.sqrt()
    sd_ms = sd_samples * Decimal(1000) / Decimal(SAMPLE_RATE)
    result["samples"]["population_standard_deviation"] = f"{sd_samples:.15f}"
    result["milliseconds"]["population_standard_deviation"] = f"{sd_ms:.15f}"
    return result


def verify_inputs() -> tuple[dict, dict, dict[str, bytes], dict[str, bytes], dict]:
    for path_text, expected in EXPECTED_REPOSITORY_SHA.items():
        if checksum(Path(path_text)) != expected:
            raise RuntimeError(f"AUTHORITY_CONFLICT repository checksum: {path_text}")
    authority = json.loads(AUTHORITY.read_text())
    frozen_dataset_fingerprint = authority.pop("dataset_fingerprint")
    computed_dataset_fingerprint = sha256(canonical(authority)).hexdigest()
    if frozen_dataset_fingerprint != computed_dataset_fingerprint or frozen_dataset_fingerprint != DATASET_FINGERPRINT:
        raise RuntimeError("AUTHORITY_CONFLICT dataset fingerprint")
    schedule = json.loads(SCHEDULE.read_text())
    frozen_schedule_fingerprint = schedule.pop("schedule_fingerprint")
    computed_schedule_fingerprint = sha256(canonical(schedule)).hexdigest()
    if frozen_schedule_fingerprint != computed_schedule_fingerprint:
        raise RuntimeError("AUTHORITY_CONFLICT schedule fingerprint")
    if len(schedule["events"]) != 20 or [item["marker_sample"] for item in schedule["events"]] != [88200 + 441000 * k for k in range(20)]:
        raise RuntimeError("AUTHORITY_CONFLICT event population or marker rule")

    source_data: dict[str, bytes] = {}
    control_data: dict[str, bytes] = {}
    input_assets = {}
    for source in ("Drums", "Double Bass"):
        source_ref = authority["canonical_assets"][source]
        control_ref = authority["control_assets"][source]
        source_path = EXTERNAL / source_ref["path"]
        control_path = EXTERNAL / control_ref["path"]
        if checksum(source_path) != source_ref["sha256"] or checksum(control_path) != control_ref["sha256"]:
            raise RuntimeError(f"AUTHORITY_CONFLICT asset checksum: {source}")
        source_properties, source_data[source] = read_pcm(source_path)
        control_properties, control_data[source] = read_pcm(control_path)
        if any(control_data[source]):
            raise RuntimeError(f"AUTHORITY_CONFLICT nonzero control: {source}")
        input_assets[source] = {
            "source": {**source_ref, "properties": source_properties},
            "control": {**control_ref, "properties": control_properties, "exact_digital_zero": True},
        }
    return authority, schedule, source_data, control_data, {
        "dataset_fingerprint": frozen_dataset_fingerprint,
        "schedule_fingerprint": frozen_schedule_fingerprint,
        "assets": input_assets,
    }


def analyze_once(schedule: dict, source_data: dict[str, bytes], control_data: dict[str, bytes]) -> list[dict]:
    records = []
    for event in schedule["events"]:
        source = event["source"]
        marker = event["marker_sample"]
        search_end = marker + SEARCH_LENGTH
        baseline_start = marker - BASELINE_LENGTH
        baseline_end = marker
        baseline_left = first_difference(source_data[source], control_data[source], baseline_start, baseline_end, 0)
        baseline_right = first_difference(source_data[source], control_data[source], baseline_start, baseline_end, 1)
        baseline_pass = baseline_left[0] is None and baseline_right[0] is None
        if not baseline_pass:
            records.append({
                "event_id": event["event_id"], "source": source, "marker_sample": marker,
                "status": "AUTHORITY_CONFLICT", "reason": "NONZERO_PRE_MARKER_BASELINE",
                "baseline": {"start": baseline_start, "end_exclusive": baseline_end, "exact_zero": False},
            })
            continue
        left_frame, left_value = first_difference(source_data[source], control_data[source], marker, search_end, 0)
        right_frame, right_value = first_difference(source_data[source], control_data[source], marker, search_end, 1)
        present = [value for value in (left_frame, right_frame) if value is not None]
        if not present:
            records.append({
                "event_id": event["event_id"], "source": source, "marker_sample": marker,
                "marker_time_exact": event["time_seconds_exact"],
                "search_window": {"start": marker, "end_exclusive": search_end},
                "baseline": {"start": baseline_start, "end_exclusive": baseline_end, "exact_zero": True},
                "channels": {"left": {"present": False}, "right": {"present": False}},
                "n_physical": None, "t_physical": None, "latency": None,
                "channel_disagreement": False, "channel_spread": None,
                "status": "NO_PHYSICAL_RESPONSE_FOUND", "uncertainty": None,
            })
            continue
        n_physical = min(present)
        latency = n_physical - marker
        disagreement = left_frame != right_frame
        spread = abs(left_frame - right_frame) if left_frame is not None and right_frame is not None else None
        t_physical = Fraction(n_physical, SAMPLE_RATE)
        latency_seconds = Fraction(latency, SAMPLE_RATE)
        uncertainty_lower = Fraction(n_physical - 1, SAMPLE_RATE)
        uncertainty_upper = t_physical
        records.append({
            "event_id": event["event_id"], "source": source, "marker_sample": marker,
            "marker_time_exact": event["time_seconds_exact"],
            "search_window": {"start": marker, "end_exclusive": search_end},
            "baseline": {"start": baseline_start, "end_exclusive": baseline_end, "exact_zero": True},
            "channels": {
                "left": {"present": left_frame is not None, "first_response_sample": left_frame, "signed_value": left_value},
                "right": {"present": right_frame is not None, "first_response_sample": right_frame, "signed_value": right_value},
            },
            "n_physical": n_physical,
            "t_physical": {"seconds_exact": exact(t_physical), "seconds_decimal": decimal(t_physical)},
            "latency": {
                "samples": latency,
                "seconds_exact": exact(latency_seconds),
                "seconds_decimal": decimal(latency_seconds),
                "milliseconds_exact": exact(latency_seconds * 1000),
                "milliseconds_decimal": decimal(latency_seconds * 1000),
            },
            "channel_disagreement": disagreement,
            "channel_disagreement_status": "CHANNEL_DISAGREEMENT" if disagreement else None,
            "channel_spread": None if spread is None else {
                "samples": spread,
                "milliseconds_exact": exact(Fraction(spread * 1000, SAMPLE_RATE)),
                "milliseconds_decimal": decimal(Fraction(spread * 1000, SAMPLE_RATE)),
            },
            "status": "VALID_PHYSICAL_ONSET",
            "uncertainty": {
                "continuous_time_lower_exclusive_seconds_exact": exact(uncertainty_lower),
                "continuous_time_upper_inclusive_seconds_exact": exact(uncertainty_upper),
                "width_seconds_exact": "1/44100",
            },
        })
    return records


def source_summary(records: list[dict]) -> dict:
    output = {}
    for source in ("Drums", "Double Bass"):
        selected = [record for record in records if record["source"] == source]
        valid = [record for record in selected if record["status"] == "VALID_PHYSICAL_ONSET"]
        latencies = [record["latency"]["samples"] for record in valid]
        spreads = [record["channel_spread"]["samples"] for record in valid if record["channel_spread"] is not None]
        output[source] = {
            "event_count": len(selected),
            "valid_onset_count": len(valid),
            "missing_response_count": sum(record["status"] == "NO_PHYSICAL_RESPONSE_FOUND" for record in selected),
            "authority_conflict_count": sum(record["status"] == "AUTHORITY_CONFLICT" for record in selected),
            "channel_disagreement_count": sum(bool(record.get("channel_disagreement")) for record in selected),
            "latency_samples_in_event_order": latencies,
            "latency_milliseconds_in_event_order": [decimal(Fraction(value * 1000, SAMPLE_RATE)) for value in latencies],
            "latency_descriptive": describe(latencies),
            "channel_spread_samples_in_event_order": spreads,
            "channel_spread_milliseconds_in_event_order": [decimal(Fraction(value * 1000, SAMPLE_RATE)) for value in spreads],
            "channel_spread_descriptive": describe(spreads),
        }
    return output


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
    authority, schedule, source_data, control_data, verified_input = verify_inputs()
    first = analyze_once(schedule, source_data, control_data)
    second = analyze_once(schedule, source_data, control_data)
    if canonical(first) != canonical(second):
        raise RuntimeError("AUTHORITY_CONFLICT deterministic replay")
    summary = source_summary(first)
    if len(first) != 20 or any(item["status"] == "AUTHORITY_CONFLICT" for item in first):
        raise RuntimeError("Physical authority freeze criterion failed")
    provenance = {
        "rule_id": RULE_ID,
        "rule_version": "v1",
        "preregistration_commit": PREREG_COMMIT,
        "execution_id": EXECUTION_ID,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "sample_rate_hz": SAMPLE_RATE,
        "search_window_length_samples": SEARCH_LENGTH,
        "pre_marker_baseline_length_samples": BASELINE_LENGTH,
        "threshold_used": False,
        "source_specific_rule_used": False,
        "jga_executed": False,
        "strength_accessed": False,
        "h02_executed": False,
    }
    fingerprint_basis = {
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "schedule_fingerprint": verified_input["schedule_fingerprint"],
        "rule_id": RULE_ID,
        "records": first,
        "summary": summary,
        "provenance": provenance,
    }
    scientific_fingerprint = sha256(canonical(fingerprint_basis)).hexdigest()
    input_manifest = {
        "schema": "JGA-PHYSICAL-ONSET-INPUT-MANIFEST/v1",
        "dataset_authority_id": "PR-CED-VAL-004-PHYSICAL-ONSET-001",
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "preregistration_id": RULE_ID,
        "preregistration_commit": PREREG_COMMIT,
        "repository_checksums": EXPECTED_REPOSITORY_SHA,
        "verified_input": verified_input,
        "authority_gate": "PASS",
    }
    event_authority = {
        "schema": "JGA-PHYSICAL-ONSET-EVENT-AUTHORITY/v1",
        "status": "FROZEN_PHYSICAL_ONSET_AUTHORITY",
        "scientific_fingerprint": scientific_fingerprint,
        "records": first,
        "provenance": provenance,
    }
    result = {
        "schema": "JGA-PHYSICAL-ONSET-RESULT/v1",
        "study_id": RULE_ID,
        "execution_id": EXECUTION_ID,
        "status": "PASS_FROZEN_PHYSICAL_ONSET_AUTHORITY",
        "event_count": len(first),
        "source_summary": summary,
        "deterministic_replay": "PASS_EXACT",
        "scientific_fingerprint": scientific_fingerprint,
        "firewalls": {
            "jga_executed": False, "strength_accessed": False, "h02_executed": False,
            "historical_results_changed": False, "raw_assets_changed": False,
            "production_code_changed": False,
        },
    }
    completion = {
        "study_id": RULE_ID,
        "execution_id": EXECUTION_ID,
        "authority_gate": "PASS",
        "event_population": "20/20",
        "baseline_checks": "20/20 PASS",
        "deterministic_replay": "PASS_EXACT",
        "physical_authority_frozen": True,
        "scientific_fingerprint": scientific_fingerprint,
    }
    if any((RUN / name).exists() for name in ("input_manifest.json", "event_level_physical_onsets.json", "source_summary.json", "result.json", "completion_protocol.json", "report.md", "artifact_manifest.json")):
        raise RuntimeError("Execution artifacts already exist")
    write_json(RUN / "input_manifest.json", input_manifest)
    write_json(RUN / "event_level_physical_onsets.json", event_authority)
    write_json(RUN / "source_summary.json", summary)
    write_json(RUN / "result.json", result)
    write_json(RUN / "completion_protocol.json", completion)
    report_lines = [
        f"# {RULE_ID} frozen execution result", "", "Status: **PASS — FROZEN PHYSICAL-ONSET AUTHORITY**", "",
        f"Scientific fingerprint: `{scientific_fingerprint}`.", "",
        "The exact preregistered first-nonzero rule was applied to 20/20 events. All pre-marker baselines passed; no threshold or source-specific rule was used. Deterministic replay was exact.", "",
    ]
    for source in ("Drums", "Double Bass"):
        item = summary[source]
        report_lines.extend([
            f"## {source}", "",
            f"Events: {item['event_count']}; valid: {item['valid_onset_count']}; missing: {item['missing_response_count']}; conflicts: {item['authority_conflict_count']}.", "",
            f"Latency samples: `{item['latency_samples_in_event_order']}`.", "",
            f"Latency milliseconds: `{item['latency_milliseconds_in_event_order']}`.", "",
            f"Channel spreads in samples: `{item['channel_spread_samples_in_event_order']}`.", "",
        ])
    report_lines.extend(["## Firewalls", "", "JGA, PulseCandidate strength and H02 were not accessed or executed. Raw assets and historical results remain unchanged. This authority does not measure JGA error or predictor correctness.", ""])
    (RUN / "report.md").write_text("\n".join(report_lines))
    artifact_files = [
        "execute.py", "verify.py", "input_manifest.json", "event_level_physical_onsets.json",
        "source_summary.json", "result.json", "completion_protocol.json", "report.md",
    ]
    artifact_manifest = {
        "schema": "JGA-ARTIFACT-MANIFEST/v1",
        "study_id": RULE_ID,
        "scientific_fingerprint": scientific_fingerprint,
        "artifacts": {name: checksum(RUN / name) for name in artifact_files},
    }
    write_json(RUN / "artifact_manifest.json", artifact_manifest)
    print(json.dumps({"status": result["status"], "scientific_fingerprint": scientific_fingerprint, "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
