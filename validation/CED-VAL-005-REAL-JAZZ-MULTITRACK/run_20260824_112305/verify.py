"""Independent integrity verification for the frozen CED-VAL-005 result."""
from collections import Counter
from hashlib import sha256
import json
import math
from pathlib import Path

RUN = Path(__file__).resolve().parent
SR = 44100


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(path):
    h = sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def quantile(values, p):
    position = (len(values) - 1) * p
    low, high = math.floor(position), math.ceil(position)
    return values[low] if low == high else values[low] * (high - position) + values[high] * (position - low)


def statistics(values):
    values = sorted(values)
    mean = math.fsum(values) / len(values)
    return {
        "minimum": values[0], "q1": quantile(values, .25),
        "median": quantile(values, .5), "q3": quantile(values, .75),
        "maximum": values[-1], "mean": mean,
        "population_standard_deviation": math.sqrt(math.fsum((x - mean) ** 2 for x in values) / len(values)),
    }


def main():
    content = json.loads((RUN / "scientific_content.json").read_text())
    result = json.loads((RUN / "result.json").read_text())
    manifest = json.loads((RUN / "artifact_manifest.json").read_text())
    assert sha256(canonical(content)).hexdigest() == result["scientific_fingerprint"]
    for name, expected in manifest["artifacts"].items():
        assert digest(RUN / name) == expected, name
    candidates = content["pulse_candidates_without_strength_or_confidence"]
    events = content["elementary_metric_events"]
    for source in ("Drums", "Double Bass"):
        candidate_ids = {item["pulse_candidate_id"] for item in candidates[source]}
        assert len(candidate_ids) == len(candidates[source]) == len(events[source])
        assert all(len(item["supporting_pulse_candidate_ids"]) == 1 for item in events[source])
        assert all(item["supporting_pulse_candidate_ids"][0] in candidate_ids for item in events[source])
        assert all(item["producer_sample_coordinate"] == 512 * item["producer_frame"] for item in candidates[source] + events[source])
    assert (len(events["Drums"]), len(events["Double Bass"])) == (907, 1138)
    localizations = content["drum_relative_localizations"]
    assert len(localizations) == len(events["Double Bass"]) == 1138
    assert len({item["target_eme_id"] for item in localizations}) == 1138
    assert Counter(item["relationship_status"] for item in localizations) == {"GEOMETRIC_ONLY": 1138}
    assert Counter(item["nearest_selection_status"] for item in localizations) == {"UNIQUE": 1132, "EQUAL_DISTANCE_TIE": 6}
    assert sum(item["preceding_drum_reference"] is not None for item in localizations) == 1138
    assert sum(item["following_drum_reference"] is not None for item in localizations) == 1136
    assert sum(item["nearest_drum_reference"] is not None for item in localizations) == 1138
    signed = [item["nearest_signed_displacement_seconds"] for item in localizations]
    absolute = [abs(item) for item in signed]
    summary = content["geometry_summary"]
    assert signed == summary["signed_displacement_seconds"]
    assert absolute == summary["absolute_displacement_seconds"]
    for key, value in statistics(signed).items():
        assert value == summary["signed_displacement_descriptive"]["seconds"][key]
    for key, value in statistics(absolute).items():
        assert value == summary["absolute_displacement_descriptive"]["seconds"][key]
    profile = content["rhythm_section_timing_profile"]
    assert profile["represented_observation_count"] == 2045
    assert profile["source_counts"] == {"Drums": 907, "Double Bass": 1138}
    assert profile["relationship_status_counts"] == {"GEOMETRIC_ONLY": 1138}
    assert profile["calibration_applicability"] == "UNESTABLISHED"
    firewalls = content["firewalls"]
    assert firewalls == {
        "correspondence_status": "GEOMETRIC_ONLY",
        "calibration_applicability": "UNESTABLISHED",
        "h02_used": False,
        "strength_accessed_by_scientific_execution": False,
        "bpm_meter_symbolic_input_used": False,
        "musical_interpretation_performed": False,
        "jga_tuned": False,
        "raw_assets_changed": False,
        "production_code_changed": False,
        "historical_authorities_changed": False,
    }
    assert not list(RUN.rglob("__pycache__"))
    print("PASS: fingerprint, artifacts, cardinality, lineage, frame lattice, AD-038, AD-040, statistics, firewalls")


if __name__ == "__main__":
    main()
