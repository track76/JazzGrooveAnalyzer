"""Execute frozen H-CEDVAL007-RENDERED-RESPONSE-MEASUREMENT-01."""
from __future__ import annotations

import argparse
from decimal import Decimal, getcontext
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import platform
import statistics
import wave

getcontext().prec = 50
BASE = Path("validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK")
DATASET = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK/raw")
MANIFEST = BASE / "input_authority_manifest.json"
SCHEDULE = BASE / "symbolic_beat_reference.json"
PREREG = BASE / "preregistrations/H-CEDVAL007-RENDERED-RESPONSE-MEASUREMENT-01.md"
RULE_ID = "H-CEDVAL007-RENDERED-RESPONSE-MEASUREMENT-01"
EXECUTION_ID = "EXEC-CEDVAL007-RENDERED-RESPONSE-20260824-210717"
DATASET_FINGERPRINT = "cd93455778d1484067f9a3caa3037b6467d27c7e8d5a8c0df694658bad2484e9"
PREREG_COMMIT = "c10d4c1fb505649a3b214df69ba24911b7517bc2"
EXPECTED_REPOSITORY_SHA = {
    str(PREREG): "1fe15d7d97538cf612ec0d9bba0f00474b89803f8b1f12e926c2d5a9c6b7f6fc",
    str(MANIFEST): "cf000d00929d15ada638e28159cffd4abdcae231bf4f04c55986078504899cd1",
    str(SCHEDULE): "c2035145967dc436e08210d57a8ecdbe0ad39c309d253a06cb3c700a99405431",
}
ASSETS = {
    "MARKER": {
        "filename": "CED-VAL-007-CONTROLLED-BEAT-BENCHMARK-v0.1 MARKER GT.wav",
        "sha256": "7c8c8534944e3d901b0de47f97fab03816f47e6ab62225e63ee3ba12e1c2206f",
        "epistemic_status": "RENDERED_MARKER_RESPONSE",
    },
    "DRUM": {
        "filename": "CED-VAL-007-CONTROLLED-BEAT-BENCHMARK-v0.1 DRUM GT.wav",
        "sha256": "c673d2c104eb3eb31012154f1bd84ee81313b4fd36b61bf3913686f43e19bb0c",
        "epistemic_status": "RENDERED_DRUM_RESPONSE",
    },
}
SAMPLE_RATE = 44100
FRAME_COUNT = 1411200
PERIOD = 22050
HALF = 11025


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def exact(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def decimal(value: Fraction, places: int = 15) -> str:
    number = Decimal(value.numerator) / Decimal(value.denominator)
    return f"{number:.{places}f}"


def sample(data: bytes, frame: int, channel: int) -> int:
    offset = (frame * 2 + channel) * 3
    return int.from_bytes(data[offset:offset + 3], "little", signed=True)


def first_nonzero(data: bytes, start: int, end: int, channel: int | None = None):
    for frame in range(start, end):
        left = sample(data, frame, 0)
        right = sample(data, frame, 1)
        if channel == 0 and left != 0:
            return frame, left
        if channel == 1 and right != 0:
            return frame, right
        if channel is None and (left != 0 or right != 0):
            return frame, left, right
    return None


def cell(index: int) -> tuple[int, int]:
    symbolic = PERIOD * index
    if index == 0:
        return 0, HALF
    if index == 63:
        return symbolic - HALF, FRAME_COUNT
    return symbolic - HALF, symbolic + HALF


def linear_quantile(values: list[int], p: Fraction) -> Fraction:
    ordered = sorted(values)
    position = Fraction(len(ordered) - 1) * p
    lower = position.numerator // position.denominator
    upper = lower if position.denominator == 1 else lower + 1
    if lower == upper:
        return Fraction(ordered[lower])
    weight = position - lower
    return Fraction(ordered[lower]) * (1 - weight) + Fraction(ordered[upper]) * weight


def describe(values: list[int]) -> dict:
    if not values:
        return {"count": 0, "samples": "UNDEFINED", "milliseconds": "UNDEFINED"}
    stats = {
        "minimum": Fraction(min(values)),
        "q1_linear": linear_quantile(values, Fraction(1, 4)),
        "median_linear": linear_quantile(values, Fraction(1, 2)),
        "q3_linear": linear_quantile(values, Fraction(3, 4)),
        "maximum": Fraction(max(values)),
        "mean": Fraction(sum(values), len(values)),
    }
    mean_decimal = Decimal(sum(values)) / Decimal(len(values))
    variance = sum((Decimal(value) - mean_decimal) ** 2 for value in values) / Decimal(len(values))
    sd = variance.sqrt()
    output = {"count": len(values), "quartile_method": "linear_interpolation_at_(n-1)*p", "samples": {}, "milliseconds": {}}
    for name, value in stats.items():
        ms = value * Fraction(1000, SAMPLE_RATE)
        output["samples"][name] = {"exact": exact(value), "decimal": decimal(value)}
        output["milliseconds"][name] = {"exact": exact(ms), "decimal": decimal(ms)}
    output["samples"]["population_standard_deviation"] = f"{sd:.15f}"
    output["milliseconds"]["population_standard_deviation"] = f"{sd * Decimal(1000) / Decimal(SAMPLE_RATE):.15f}"
    return output


def verify_inputs() -> tuple[dict, dict, dict[str, bytes], dict]:
    for name, expected in EXPECTED_REPOSITORY_SHA.items():
        if checksum(Path(name)) != expected:
            raise RuntimeError(f"AUTHORITY_CONFLICT repository artifact: {name}")
    manifest = json.loads(MANIFEST.read_text())
    fingerprint = sha256(canonical(manifest["manifest_basis"])).hexdigest()
    if fingerprint != manifest["dataset_fingerprint"] or fingerprint != DATASET_FINGERPRINT:
        raise RuntimeError("AUTHORITY_CONFLICT dataset fingerprint")
    schedule = json.loads(SCHEDULE.read_text())
    expected_events = [[i, PERIOD * i, f"{i}/2" if i % 2 else f"{i // 2}/1"] for i in range(64)]
    if schedule["authority"] != "SYMBOLIC_BEAT_GROUND_TRUTH" or schedule["events"] != expected_events:
        raise RuntimeError("AUTHORITY_CONFLICT symbolic schedule")
    data = {}
    verified_assets = {}
    for source, ref in ASSETS.items():
        path = DATASET / ref["filename"]
        if checksum(path) != ref["sha256"]:
            raise RuntimeError(f"AUTHORITY_CONFLICT asset checksum: {source}")
        with wave.open(str(path), "rb") as stream:
            props = {"channels": stream.getnchannels(), "sample_width_bytes": stream.getsampwidth(), "sample_rate_hz": stream.getframerate(), "frame_count": stream.getnframes(), "compression": stream.getcomptype()}
            data[source] = stream.readframes(stream.getnframes())
        expected = {"channels": 2, "sample_width_bytes": 3, "sample_rate_hz": SAMPLE_RATE, "frame_count": FRAME_COUNT, "compression": "NONE"}
        if props != expected or len(data[source]) != FRAME_COUNT * 6:
            raise RuntimeError(f"AUTHORITY_CONFLICT asset format: {source}")
        verified_assets[source] = {**ref, "properties": props}
    return manifest, schedule, data, verified_assets


def analyze_source(source: str, data: bytes) -> dict:
    records = []
    for index in range(64):
        symbolic = PERIOD * index
        start, end = cell(index)
        guard = None if index == 0 else first_nonzero(data, start, symbolic)
        record = {
            "source": source,
            "symbolic_beat_id": f"BEAT-{index:02d}",
            "beat_index": index,
            "symbolic_sample_coordinate": symbolic,
            "symbolic_time_seconds_exact": exact(Fraction(symbolic, SAMPLE_RATE)),
            "cell": {"start": start, "end_exclusive": end},
            "guard": {"start": None if index == 0 else start, "end_exclusive": None if index == 0 else symbolic, "exact_digital_silence": None if index == 0 else guard is None},
            "search": {"start": symbolic, "end_exclusive": end},
        }
        if guard is not None:
            record["guard"]["first_nonzero_frame"] = guard[0]
            record["guard"]["signed_values"] = {"left": guard[1], "right": guard[2]}
            record.update({"status": "UNRESOLVED_PRE_EVENT_ACTIVITY", "rendered_response": None, "displacement": None, "channel_relation": None})
            records.append(record)
            continue
        left = first_nonzero(data, symbolic, end, 0)
        right = first_nonzero(data, symbolic, end, 1)
        present = [item[0] for item in (left, right) if item is not None]
        if not present:
            status = "UNRESOLVED_INITIAL_FILE_BOUNDARY_NO_RESPONSE" if index == 0 else "UNRESOLVED_NO_RESPONSE_IN_SEARCH"
            record.update({"status": status, "rendered_response": None, "displacement": None, "channel_relation": None})
            records.append(record)
            continue
        rendered = min(present)
        signed = rendered - symbolic
        channel_relation = "STEREO_FIRST_RESPONSE_TIE" if left is not None and right is not None and left[0] == right[0] else "CHANNEL_FIRST_RESPONSE_DIFFERENCE"
        status = "LOCALIZED_INITIAL_FILE_BOUNDARY" if index == 0 else "LOCALIZED_EXACT_ZERO_GUARD"
        record.update({
            "status": status,
            "initial_boundary_limitation": index == 0,
            "rendered_response": {
                "sample_coordinate": rendered,
                "time_seconds_exact": exact(Fraction(rendered, SAMPLE_RATE)),
                "left": {"present": left is not None, "coordinate": None if left is None else left[0], "signed_value": None if left is None else left[1]},
                "right": {"present": right is not None, "coordinate": None if right is None else right[0], "signed_value": None if right is None else right[1]},
                "continuous_time_uncertainty": "((n_rendered-1)/44100,n_rendered/44100] when preceding exact-zero sample exists",
            },
            "displacement": {
                "signed_samples": signed,
                "absolute_samples": abs(signed),
                "signed_milliseconds_exact": exact(Fraction(signed * 1000, SAMPLE_RATE)),
                "signed_milliseconds_decimal": decimal(Fraction(signed * 1000, SAMPLE_RATE)),
                "absolute_milliseconds_exact": exact(Fraction(abs(signed) * 1000, SAMPLE_RATE)),
                "absolute_milliseconds_decimal": decimal(Fraction(abs(signed) * 1000, SAMPLE_RATE)),
            },
            "channel_relation": channel_relation,
        })
        records.append(record)
    signed_values = [record["displacement"]["signed_samples"] for record in records if record["displacement"]]
    absolute_values = [abs(value) for value in signed_values]
    status_counts = {status: sum(record["status"] == status for record in records) for status in sorted({record["status"] for record in records})}
    content = {
        "source": source,
        "epistemic_status": ASSETS[source]["epistemic_status"],
        "expected_event_count": 64,
        "localized_count": len(signed_values),
        "unresolved_count": 64 - len(signed_values),
        "ambiguous_count": 0,
        "authority_conflict_count": 0,
        "status_counts": status_counts,
        "channel_relation_counts": {name: sum(record.get("channel_relation") == name for record in records) for name in ("STEREO_FIRST_RESPONSE_TIE", "CHANNEL_FIRST_RESPONSE_DIFFERENCE")},
        "signed_displacement_samples": signed_values,
        "absolute_displacement_samples": absolute_values,
        "signed_displacement_statistics": describe(signed_values),
        "absolute_displacement_statistics": describe(absolute_values),
        "events": records,
    }
    content["scientific_fingerprint"] = sha256(canonical(content)).hexdigest()
    return content


def main(output: Path) -> None:
    manifest, schedule, data, verified_assets = verify_inputs()
    sources = {source: analyze_source(source, data[source]) for source in ("MARKER", "DRUM")}
    combined_basis = {
        "rule_id": RULE_ID,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "symbolic_authority": "SYMBOLIC_BEAT_GROUND_TRUTH",
        "source_fingerprints": {source: sources[source]["scientific_fingerprint"] for source in ("MARKER", "DRUM")},
    }
    combined_fingerprint = sha256(canonical(combined_basis)).hexdigest()
    scientific = {
        "execution_id": EXECUTION_ID,
        "rule_id": RULE_ID,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "symbolic_ground_truth_changed": False,
        "sources": sources,
        "combined_fingerprint_basis": combined_basis,
        "combined_response_measurement_fingerprint": combined_fingerprint,
        "epistemic_separation": {"symbolic": "SYMBOLIC_BEAT_GROUND_TRUTH", "MARKER": "RENDERED_MARKER_RESPONSE", "DRUM": "RENDERED_DRUM_RESPONSE"},
        "firewalls": {"latency_correction": False, "cedval004_latency_transfer": False, "jga_executed": False, "essentia_executed": False, "librosa_executed": False, "h02_used": False, "strength_accessed": False, "musical_interpretation": False, "production_code_changed": False, "raw_assets_changed": False, "historical_authorities_changed": False},
    }
    input_manifest = {"execution_id": EXECUTION_ID, "preregistration": {"id": RULE_ID, "commit": PREREG_COMMIT, "sha256": EXPECTED_REPOSITORY_SHA[str(PREREG)]}, "dataset_authority": manifest["authority_id"], "dataset_fingerprint": DATASET_FINGERPRINT, "symbolic_reference_sha256": EXPECTED_REPOSITORY_SHA[str(SCHEDULE)], "assets": verified_assets, "environment": {"python": platform.python_version(), "platform": platform.platform(), "byteorder": __import__("sys").byteorder}}
    result = {"execution_id": EXECUTION_ID, "status": "PASS_DETERMINISTIC_RESPONSE_MEASUREMENT", "combined_response_measurement_fingerprint": combined_fingerprint, "source_results": {source: {key: sources[source][key] for key in ("expected_event_count", "localized_count", "unresolved_count", "ambiguous_count", "authority_conflict_count", "status_counts", "scientific_fingerprint")} for source in ("MARKER", "DRUM")}}
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "input_manifest.json", input_manifest)
    write_json(output / "event_level_responses.json", {"execution_id": EXECUTION_ID, "sources": {source: sources[source]["events"] for source in ("MARKER", "DRUM")}})
    write_json(output / "source_summary.json", {"execution_id": EXECUTION_ID, "sources": {source: {key: value for key, value in sources[source].items() if key != "events"} for source in ("MARKER", "DRUM")}})
    write_json(output / "scientific_content.json", scientific)
    write_json(output / "result.json", result)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    main(args.output)
