from collections import Counter
from decimal import Decimal

import pytest

from jga.domain.declared_metric_reference import (
    DeclaredMetricReference,
    MetricReferenceProvenance,
)
from jga.domain.declared_metric_timeline import (
    DeclaredAnalysisScope,
    DeclaredQuarterPhaseOrigin,
)
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline


MUSICXML_SHA256 = "809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778"
SCOPE_END = Decimal(1865728) / Decimal(44100)
SOURCES = (
    ("drums.wav", "d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd", 63, 2),
    ("piano.wav", "26fa1158f375598cc7c01e04379c00547ef1787f6862eb2f29a36aafd9007c7e", 49, 3),
    ("double_bass.wav", "31d6f2e34d360c6f8f75362187433f2a2c1f5eb5cbbfe627305e99d07d8be6c5", 27, 2),
    ("tenor_sax.wav", "89dd7e5c6063d3c4d5e4ac59c9119c265df4257dfb1b4a1e01b5f117ee87182e", 16, 3),
)


def analyze(filename: str, checksum: str):
    tempo_provenance = MetricReferenceProvenance(
        "GT-VAL-001-v1",
        "authoritative controlled-source MusicXML",
        MUSICXML_SHA256,
        "complete controlled performance",
    )
    asset_provenance = MetricReferenceProvenance(
        f"CED-VAL-001-{filename}",
        "authoritative controlled audio asset",
        checksum,
        "complete controlled performance",
    )
    return AnalysisPipeline().analyze(
        f"recordings/validation/stems/{filename}",
        declared_metric_reference=DeclaredMetricReference(
            Decimal("78"), "quarter", tempo_provenance
        ),
        declared_quarter_phase_origin=DeclaredQuarterPhaseOrigin(
            Decimal("0"), asset_provenance
        ),
        declared_analysis_scope=DeclaredAnalysisScope(
            Decimal("0"), SCOPE_END, checksum, asset_provenance
        ),
    )


@pytest.mark.parametrize("filename,checksum,event_count,max_per_interval", SOURCES)
def test_metric_localization_preserves_complete_source_event_population(
    filename,
    checksum,
    event_count,
    max_per_interval,
):
    first = analyze(filename, checksum)
    second = analyze(filename, checksum)
    events = first.elementary_metric_events
    associations = first.elementary_metric_event_associations
    points = (
        first.representation_result.metric_landscape.metric_trajectory.metric_points
    )
    counts = Counter(item.beat_reference_id for item in associations)

    assert len(first.domain_pulse_candidates) == event_count
    assert len(events) == event_count
    assert len(associations) == event_count
    assert len(points) == event_count
    assert all(item.outcome == "ASSOCIATED" for item in associations)
    assert len({item.elementary_metric_event_id for item in associations}) == event_count
    assert len({point.event.id for point in points}) == event_count
    assert max(counts.values()) == max_per_interval
    assert all(0.0 <= item.normalized_phase < 1.0 for item in associations)
    assert tuple(item.id for item in events) == tuple(
        item.id for item in second.elementary_metric_events
    )
    assert tuple(item.normalized_phase for item in associations) == tuple(
        item.normalized_phase
        for item in second.elementary_metric_event_associations
    )
    assert all(len(item.supporting_pulse_candidate_ids) == 1 for item in events)
    assert all(item.source_asset_sha256 == checksum for item in events)
