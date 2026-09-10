#!/usr/bin/env python3
"""Execute the frozen controlled millisecond-report acceptance."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from jga.engines.pulse_candidate_builder import PulseCandidateBuilder
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.representation.builders.drum_relative_eme_localization_builder import (
    DrumRelativeEMELocalizationBuilder,
)


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SOURCES = (
    ("Drums", "TEMPORAL_REFERENCE", ROOT / "recordings/validation/stems/drums.wav",
     "d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd", 63),
    ("Piano", "ACCOMPANIMENT", ROOT / "recordings/validation/stems/piano.wav",
     "26fa1158f375598cc7c01e04379c00547ef1787f6862eb2f29a36aafd9007c7e", 49),
    ("Double Bass", "ACCOMPANIMENT",
     ROOT / "recordings/validation/stems/double_bass.wav",
     "31d6f2e34d360c6f8f75362187433f2a2c1f5eb5cbbfe627305e99d07d8be6c5", 27),
)
EXECUTION_ID = "EXEC-VAL001-CANONICAL-TIMING-REPORT-MILLISECOND-ACCEPTANCE-01"
PROVENANCE_ID = "VAL-001-CONTROLLED-STEMS"
ROLE_AUTHORITY_ID = "AD-040-CONTROLLED-ROLE-AUTHORITY"
ROLE_AUTHORITY_FINGERPRINT = "b8983e8"
CALIBRATION_AUTHORITY_ID = "VAL-001-CALIBRATION-CONTEXT"
CALIBRATION_AUTHORITY_FINGERPRINT = "UNAPPLIED-CONTROLLED-CONTEXT"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run_cli(destination: Path) -> None:
    command = [
        sys.executable,
        str(ROOT / "tools/run_rhythm_section_timing_report.py"),
    ]
    for label, role, path, _, _ in SOURCES:
        command.extend(("--source", f"{role}={label}={path}"))
    for label, _, _, expected, _ in SOURCES:
        command.extend(("--expected-sha256", f"{label}={expected}"))
    command.extend((
        "--execution-id", EXECUTION_ID,
        "--provenance-id", PROVENANCE_ID,
        "--role-authority-id", ROLE_AUTHORITY_ID,
        "--role-authority-fingerprint", ROLE_AUTHORITY_FINGERPRINT,
        "--calibration-applicability", "UNESTABLISHED",
        "--calibration-authority-id", CALIBRATION_AUTHORITY_ID,
        "--calibration-authority-fingerprint", CALIBRATION_AUTHORITY_FINGERPRINT,
        "--jga-revision", "MILLISECOND-ACCEPTANCE-SCHEMA-V2",
        "--output", str(destination),
    ))
    subprocess.run(command, cwd=ROOT, check=True)


def direct_authority():
    analyses = {
        label: AnalysisPipeline().analyze(str(path))
        for label, _, path, _, _ in SOURCES
    }
    events = {
        label: tuple(context.elementary_metric_events)
        for label, context in analyses.items()
    }
    candidates = tuple(
        candidate
        for context in analyses.values()
        for candidate in context.domain_pulse_candidates
    )
    localizations = DrumRelativeEMELocalizationBuilder().build(
        events["Piano"] + events["Double Bass"],
        events["Drums"],
        candidates,
        temporal_origin_seconds=0.0,
        analysis_execution_id=EXECUTION_ID,
    )
    return analyses, events, {str(item.target_eme_id): item for item in localizations}


def verify(document: dict) -> dict:
    assert document["schema"] == {
        "id": "JGA_RHYTHM_SECTION_TIMING_REPORT_V1", "version": 2,
    }
    analyses, events, direct = direct_authority()
    assert {label: len(events[label]) for label, *_ in SOURCES} == {
        "Drums": 63, "Piano": 49, "Double Bass": 27,
    }
    source_ids = {
        item["source_identity"]: item["label"]
        for item in document["source_authorities"]
    }
    serialized = document["ad038_localizations"]
    assert len(serialized) == len(direct) == 76
    counts = Counter(source_ids[item["target_source_identity"]] for item in serialized)
    assert counts == {"Piano": 49, "Double Bass": 27}

    def reference(item):
        if item is None:
            return None
        return (str(item.eme_id), item.timestamp_seconds)

    ties = 0
    boundary_nulls = 0
    for record in serialized:
        expected = direct[record["target_eme_id"]]
        assert record["target_timestamp_seconds"] == expected.target_timestamp_seconds
        assert (
            None if record["preceding_reference"] is None else (
                record["preceding_reference"]["eme_id"],
                record["preceding_reference"]["timestamp_seconds"],
            )
        ) == reference(expected.preceding_drum_eme)
        assert (
            None if record["following_reference"] is None else (
                record["following_reference"]["eme_id"],
                record["following_reference"]["timestamp_seconds"],
            )
        ) == reference(expected.following_drum_eme)
        assert (
            None if record["nearest_reference"] is None else (
                record["nearest_reference"]["eme_id"],
                record["nearest_reference"]["timestamp_seconds"],
            )
        ) == reference(expected.nearest_drum_eme)
        assert record["distance_from_preceding_seconds"] == expected.distance_from_preceding_seconds
        assert record["distance_from_following_seconds"] == expected.distance_from_following_seconds
        assert record["nearest_displacement_seconds"] == expected.nearest_displacement_seconds
        assert record["distance_from_preceding_ms"] == expected.distance_from_preceding_ms
        assert record["distance_from_following_ms"] == expected.distance_from_following_ms
        assert record["nearest_displacement_ms"] == expected.nearest_displacement_ms
        assert record["nearest_selection_status"] == expected.nearest_selection_status
        assert record["localization_rule"] == expected.localization_rule
        assert record["analysis_execution_id"] == EXECUTION_ID
        assert record["correspondence_status"] == "GEOMETRIC_ONLY"
        assert record["calibration_status"] == "NOT_APPLIED"
        ties += record["nearest_selection_status"] == "EQUAL_DISTANCE_TIE"
        boundary_nulls += (
            record["distance_from_preceding_seconds"] is None
            or record["distance_from_following_seconds"] is None
        )

    observations = document["observations"]
    for label, context in analyses.items():
        assert len(observations[label]) == len(context.domain_pulse_candidates)
        assert all(
            item["producer_sample_coordinate"]
            == item["producer_frame"] * PulseCandidateBuilder.FRAME_LENGTH_SAMPLES
            and item["timestamp_seconds"]
            == item["producer_sample_coordinate"] / context.audio.sample_rate
            for item in observations[label]
        )
    profile = document["ad040_profile"]
    assert profile["temporal_origin_seconds"] == 0.0
    assert profile["temporal_reference_eme_count"] == 63
    assert profile["accompaniment_relationship_count"] == 76
    assert profile["correspondence_status_counts"] == {"GEOMETRIC_ONLY": 76}
    assert len(profile["relationships"]) == 76
    assert all(item["correspondence_status"] == "GEOMETRIC_ONLY" for item in profile["relationships"])
    assert document["invocation_authority"]["execution_id"] == EXECUTION_ID
    assert document["invocation_authority"]["provenance_id"] == PROVENANCE_ID
    return {"tie_count": ties, "one_sided_boundary_count": boundary_nulls}


def main() -> int:
    outputs = (HERE / "canonical_report_run_1.json", HERE / "canonical_report_run_2.json")
    if any(path.exists() for path in outputs):
        raise RuntimeError("acceptance output already exists")
    for path in outputs:
        run_cli(path)
    first_bytes = outputs[0].read_bytes()
    second_bytes = outputs[1].read_bytes()
    assert first_bytes == second_bytes
    first = json.loads(first_bytes)
    second = json.loads(second_bytes)
    summary = verify(first)
    assert verify(second) == summary
    assert first["scientific_fingerprint"] == second["scientific_fingerprint"]
    result = {
        "protocol_id": "H-VAL001-CANONICAL-TIMING-REPORT-MILLISECOND-ACCEPTANCE-01",
        "classification": "PASS_CANONICAL_MILLISECOND_REPORT_ACCEPTED",
        "schema": first["schema"],
        "population": {"Drums": 63, "Piano": 49, "Double Bass": 27,
                       "accompaniment_total": 76},
        "millisecond_rule": "authoritative_seconds * 1000.0",
        "millisecond_fields_verified": 3 * 76,
        "absolute_timeline_coordinates_verified": 76,
        "reference_identity_and_timestamp_verified": 76,
        "producer_frame_sample_roundtrip_verified": sum(map(len, first["observations"].values())),
        "temporal_origin_seconds": 0.0,
        "geometric_only_relationships": 76,
        "tie_count": summary["tie_count"],
        "one_sided_boundary_count": summary["one_sided_boundary_count"],
        "canonical_replay": "BYTE_IDENTICAL",
        "scientific_fingerprint": first["scientific_fingerprint"],
        "canonical_result_sha256": digest(outputs[0]),
        "symbolic_ground_truth_accessed": False,
        "production_scientific_behavior_changed": False,
    }
    encoded = json.dumps(result, ensure_ascii=True, allow_nan=False, sort_keys=True,
                         separators=(",", ":")) + "\n"
    (HERE / "result.json").write_text(encoded, encoding="ascii", newline="\n")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
