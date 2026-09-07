from pathlib import Path

import pytest

from jga.reporting.rhythm_section_timing_report import (
    AuthorizedSourceInput,
    RhythmSectionTimingReportError,
)
from jga.reporting.rhythm_section_timing_report_service import (
    RhythmSectionTimingReportService,
)


DRUMS = Path("recordings/validation/stems/drums.wav")
BASS = Path("recordings/validation/stems/double_bass.wav")
AUTHORITY = {
    "execution_id": "TEST-EXECUTION",
    "provenance_id": "TEST-PROVENANCE",
    "role_authority_id": "TEST-ROLE-AUTHORITY",
    "role_authority_fingerprint": "test-role-authority-fingerprint",
    "calibration_applicability": "UNESTABLISHED",
    "calibration_authority_id": "TEST-CALIBRATION-AUTHORITY",
    "calibration_authority_fingerprint": "test-calibration-authority-fingerprint",
    "jga_revision": "test-jga-revision",
}


def source(path, label, role, expected_sha256=None):
    # Explicit fixture bindings; label is not an identity input.
    digest, key = (
        ("31d6f2e34d360c6f8f75362187433f2a2c1f5eb5cbbfe627305e99d07d8be6c5", "VAL001_SOURCE_003")
        if path == BASS else
        ("d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd", "VAL001_SOURCE_001")
    )
    return AuthorizedSourceInput(path, label, role, expected_sha256 or digest,
                                 "VAL-001-DIRECT-INPUT-SOURCE-AUTHORITY-V1", key)


@pytest.mark.parametrize(
    ("sources", "message"),
    (
        ((), "MISSING_SOURCE_AUTHORITY"),
        ((source(DRUMS, "Drums", "ACCOMPANIMENT"),),
         "ROLE_AUTHORITY_REQUIRES_EXACTLY_ONE_TEMPORAL_REFERENCE"),
        ((source(DRUMS, "Drums", "TEMPORAL_REFERENCE"),
          source(BASS, "Bass", "TEMPORAL_REFERENCE")),
         "ROLE_AUTHORITY_REQUIRES_EXACTLY_ONE_TEMPORAL_REFERENCE"),
        ((source(DRUMS, "Drums", "TEMPORAL_REFERENCE"),),
         "MISSING_ACCOMPANIMENT_AUTHORITY"),
        ((source(DRUMS, "Same", "TEMPORAL_REFERENCE"),
          source(BASS, "Same", "ACCOMPANIMENT")), "DUPLICATE_SOURCE_LABEL"),
        ((source(DRUMS, "Drums", "AUTOMATIC"),
          source(BASS, "Bass", "ACCOMPANIMENT")),
         "UNSUPPORTED_ANALYTICAL_ROLE:AUTOMATIC"),
    ),
)
def test_role_authority_failures_are_bounded(sources, message):
    with pytest.raises(RhythmSectionTimingReportError, match=message):
        RhythmSectionTimingReportService().build(sources, **AUTHORITY)


def test_missing_source_and_checksum_failure_are_bounded():
    service = RhythmSectionTimingReportService()
    missing = (
        source(Path("does-not-exist.wav"), "Drums", "TEMPORAL_REFERENCE"),
        source(BASS, "Bass", "ACCOMPANIMENT"),
    )
    with pytest.raises(RhythmSectionTimingReportError, match="MISSING_SOURCE:Drums"):
        service.build(missing, **AUTHORITY)

    mismatch = (
        source(DRUMS, "Drums", "TEMPORAL_REFERENCE", "0" * 64),
        source(BASS, "Bass", "ACCOMPANIMENT"),
    )
    with pytest.raises(
        RhythmSectionTimingReportError, match="SOURCE_CHECKSUM_MISMATCH:Drums"
    ):
        service.build(mismatch, **AUTHORITY)


def test_missing_provenance_authority_fails_before_analysis():
    sources = (
        source(DRUMS, "Drums", "TEMPORAL_REFERENCE"),
        source(BASS, "Bass", "ACCOMPANIMENT"),
    )
    with pytest.raises(
        RhythmSectionTimingReportError, match="MISSING_PROVENANCE_AUTHORITY"
    ):
        RhythmSectionTimingReportService().build(
            sources,
            **{**AUTHORITY, "jga_revision": ""},
        )


def test_calibration_applicability_requires_explicit_supported_authority():
    sources = (
        source(DRUMS, "Drums", "TEMPORAL_REFERENCE"),
        source(BASS, "Bass", "ACCOMPANIMENT"),
    )
    service = RhythmSectionTimingReportService()
    with pytest.raises(
        RhythmSectionTimingReportError,
        match="UNSUPPORTED_CALIBRATION_APPLICABILITY:INFERRED",
    ):
        service.build(
            sources,
            **{**AUTHORITY, "calibration_applicability": "INFERRED"},
        )
    with pytest.raises(
        RhythmSectionTimingReportError, match="MISSING_PROVENANCE_AUTHORITY"
    ):
        service.build(
            sources,
            **{**AUTHORITY, "calibration_authority_id": ""},
        )


def test_empty_eme_population_is_a_bounded_failure():
    class EmptyContext:
        elementary_metric_events = ()

    class EmptyPipeline:
        def analyze(self, _, **kwargs):
            return EmptyContext()

    sources = (
        source(DRUMS, "Drums", "TEMPORAL_REFERENCE"),
        source(BASS, "Bass", "ACCOMPANIMENT"),
    )
    with pytest.raises(RhythmSectionTimingReportError, match="EMPTY_EME_POPULATION"):
        RhythmSectionTimingReportService(EmptyPipeline).build(sources, **AUTHORITY)
