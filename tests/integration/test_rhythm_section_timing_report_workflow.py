from hashlib import sha256
import json
from pathlib import Path

import pytest

from jga.reporting.rhythm_section_timing_report import AuthorizedSourceInput
from jga.reporting.rhythm_section_timing_report import RhythmSectionTimingReportError
from jga.reporting.rhythm_section_timing_report_service import (
    RhythmSectionTimingReportService,
)
from tools.run_rhythm_section_timing_report import main


DRUMS = Path("recordings/validation/stems/drums.wav")
BASS = Path("recordings/validation/stems/double_bass.wav")
JGA_REVISION = "dfb143a7926582597133d918dde74fcac53402fa"
CALIBRATION_AUTHORITY = {
    "calibration_applicability": "UNESTABLISHED",
    "calibration_authority_id": "TEST-CALIBRATION-AUTHORITY",
    "calibration_authority_fingerprint": "test-calibration-authority-fingerprint",
}


def inputs():
    return (
        AuthorizedSourceInput(DRUMS, "Drums", "TEMPORAL_REFERENCE"),
        AuthorizedSourceInput(BASS, "Double Bass", "ACCOMPANIMENT"),
    )


def build_report(sources=None):
    return RhythmSectionTimingReportService().build(
        inputs() if sources is None else sources,
        execution_id="CONTROLLED-REPORT-REPLAY-001",
        provenance_id="VAL-001-CONTROLLED-STEMS",
        role_authority_id="AD-040-CONTROLLED-ROLE-AUTHORITY",
        role_authority_fingerprint="b8983e8",
        **CALIBRATION_AUTHORITY,
        jga_revision=JGA_REVISION,
    )


def test_complete_workflow_replays_exactly_and_preserves_firewalls():
    first = build_report()
    second = build_report(tuple(reversed(inputs())))
    assert first == second
    assert first.canonical_json == second.canonical_json
    document = json.loads(first.canonical_json)
    fingerprint = document.pop("scientific_fingerprint")
    canonical_content = json.dumps(
        document,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")
    assert fingerprint == sha256(canonical_content).hexdigest()
    assert fingerprint == first.scientific_fingerprint
    assert document["schema"] == {
        "id": "JGA_RHYTHM_SECTION_TIMING_REPORT_V1",
        "version": 1,
    }
    profile = document["ad040_profile"]
    assert profile["temporal_reference_eme_count"] == 63
    assert profile["accompaniment_relationship_count"] == 27
    assert profile["represented_eme_count"] == 90
    assert profile["correspondence_status_counts"]["GEOMETRIC_ONLY"] == 27
    assert len(document["ad038_localizations"]) == 27
    assert all(
        item["correspondence_status"] == "GEOMETRIC_ONLY"
        and item["calibration_status"] == "NOT_APPLIED"
        for item in document["ad038_localizations"]
    )
    calibration = document["scientific_status"]["calibration"]
    assert calibration == {
        "applicability": "UNESTABLISHED",
        "application": "NOT_APPLIED",
        "correction": "NONE",
        "authority_id": "TEST-CALIBRATION-AUTHORITY",
        "authority_fingerprint": "test-calibration-authority-fingerprint",
    }
    assert profile["calibration_status"] == "NOT_APPLIED"
    assert document["scientific_status"]["timestamp_correction"] == "NONE"
    assert document["scientific_status"]["unsupported_claims"] == [
        "beat_identity", "musical_correspondence", "tempo", "bpm", "meter",
        "downbeat", "swing", "groove", "rushing", "dragging", "intention",
        "human_microtiming", "physical_onset_ground_truth",
        "calibrated_timing_correction",
        "ACQUISITION_CLOCK_SYNCHRONY_NOT_ESTABLISHED",
    ]
    assert all(
        item["producer_sample_coordinate"] == item["producer_frame"] * 512
        for records in document["observations"].values()
        for item in records
    )


def test_cli_writes_the_canonical_json_report(tmp_path):
    destination = tmp_path / "timing-report.json"
    result = main(
        [
            "--source", f"TEMPORAL_REFERENCE=Drums={DRUMS}",
            "--source", f"ACCOMPANIMENT=Double Bass={BASS}",
            "--execution-id", "CONTROLLED-REPORT-CLI-001",
            "--provenance-id", "VAL-001-CONTROLLED-STEMS",
            "--role-authority-id", "AD-040-CONTROLLED-ROLE-AUTHORITY",
            "--role-authority-fingerprint", "b8983e8",
            "--calibration-applicability", "UNESTABLISHED",
            "--calibration-authority-id", "TEST-CALIBRATION-AUTHORITY",
            "--calibration-authority-fingerprint", "test-calibration-authority-fingerprint",
            "--jga-revision", JGA_REVISION,
            "--output", str(destination),
        ]
    )
    assert result == 0
    document = json.loads(destination.read_text())
    assert document["schema"]["id"] == "JGA_RHYTHM_SECTION_TIMING_REPORT_V1"
    assert document["ad040_profile"]["accompaniment_relationship_count"] == 27
    assert len(document["ad040_profile"]["relationships"]) == 27
    assert len(document["ad040_profile"]["role_assignments"]) == 2

    assert main(
        [
            "--source", f"TEMPORAL_REFERENCE=Drums={DRUMS}",
            "--source", f"ACCOMPANIMENT=Double Bass={BASS}",
            "--execution-id", "CONTROLLED-REPORT-CLI-001",
            "--provenance-id", "VAL-001-CONTROLLED-STEMS",
            "--role-authority-id", "AD-040-CONTROLLED-ROLE-AUTHORITY",
            "--role-authority-fingerprint", "b8983e8",
            "--calibration-applicability", "UNESTABLISHED",
            "--calibration-authority-id", "TEST-CALIBRATION-AUTHORITY",
            "--calibration-authority-fingerprint", "test-calibration-authority-fingerprint",
            "--jga-revision", JGA_REVISION,
            "--output", str(destination),
        ]
    ) == 2


def test_ad038_and_ad040_failures_are_bounded(monkeypatch):
    service = RhythmSectionTimingReportService()

    def fail_ad038(*args, **kwargs):
        raise ValueError("forced AD-038 failure")

    monkeypatch.setattr(service._localization_builder, "build", fail_ad038)
    with pytest.raises(RhythmSectionTimingReportError, match="AD038_CONSTRUCTION_FAILURE"):
        service.build(
            inputs(), execution_id="FAIL-AD038", provenance_id="TEST",
            role_authority_id="TEST", role_authority_fingerprint="TEST",
            **CALIBRATION_AUTHORITY,
            jga_revision=JGA_REVISION,
        )

    service = RhythmSectionTimingReportService()

    def fail_ad040(*args, **kwargs):
        raise ValueError("forced AD-040 failure")

    monkeypatch.setattr(service._profile_builder, "build", fail_ad040)
    with pytest.raises(RhythmSectionTimingReportError, match="AD040_CONSTRUCTION_FAILURE"):
        service.build(
            inputs(), execution_id="FAIL-AD040", provenance_id="TEST",
            role_authority_id="TEST", role_authority_fingerprint="TEST",
            **CALIBRATION_AUTHORITY,
            jga_revision=JGA_REVISION,
        )
