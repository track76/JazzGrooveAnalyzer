from decimal import Decimal

import pytest

from jga.domain.declared_meter import DeclaredMeter
from jga.domain.declared_metric_reference import (
    DeclaredMetricReference,
    MetricReferenceProvenance,
)
from jga.domain.declared_metric_timeline import (
    DeclaredAnalysisScope,
    DeclaredQuarterPhaseOrigin,
)
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline


MP3_PATH = "recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3"
SOURCE_SHA256 = "809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778"


def declared_context():
    provenance = MetricReferenceProvenance(
        source_id="GT-VAL-001-v1",
        source_kind="authoritative controlled-source context",
        source_sha256=SOURCE_SHA256,
        temporal_scope="complete controlled performance",
    )
    return (
        DeclaredMetricReference(Decimal("78"), "quarter", provenance),
        DeclaredMeter(4, 4, provenance),
        DeclaredQuarterPhaseOrigin(Decimal("0"), provenance),
        DeclaredAnalysisScope(
            Decimal("0"), Decimal("42.24"), SOURCE_SHA256, provenance
        ),
    )


def analyze_declared():
    metric_reference, meter, phase, scope = declared_context()
    return AnalysisPipeline().analyze(
        MP3_PATH,
        declared_metric_reference=metric_reference,
        declared_quarter_phase_origin=phase,
        declared_analysis_scope=scope,
        declared_meter=meter,
    )


@pytest.fixture(scope="module")
def controlled_analyses():
    return AnalysisPipeline().analyze(MP3_PATH), analyze_declared(), analyze_declared()


def projected_events(context):
    return tuple(
        event
        for cluster in context.metric_clusters
        for event in cluster.events
    )


def projection_signature(context):
    return tuple(
        (
            event.timestamp,
            cluster.beat_reference.timestamp,
            (event.timestamp - cluster.beat_reference.timestamp) * 1000.0,
        )
        for cluster in context.metric_clusters
        for event in cluster.events
    )


def test_controlled_source_preserves_all_observations_and_projects_each_eme_once(
    controlled_analyses,
):
    _, declared, _ = controlled_analyses
    projected = projected_events(declared)

    assert len(declared.domain_pulse_candidates) == 77
    assert len(projected) == len(declared.elementary_metric_events)
    assert len({event.id for event in projected}) == len(projected)
    assert {event.id for event in projected} == {
        event.id for event in declared.elementary_metric_events
    }
    assert sum(
        len(item.supporting_pulse_candidate_ids)
        for item in declared.elementary_metric_event_associations
    ) == 77
    assert all(
        item.outcome in {"ASSOCIATED", "AMBIGUOUS"}
        for item in declared.elementary_metric_event_associations
    )


def test_projection_preserves_event_identity_timestamp_and_contributor_provenance(
    controlled_analyses,
):
    _, declared, _ = controlled_analyses
    input_by_id = {event.id: event for event in declared.elementary_metric_events}

    for event in projected_events(declared):
        original = input_by_id[event.id]
        assert event is original
        assert event.timestamp == original.timestamp
        assert event.contributor_id == original.contributor_id

    points = declared.representation_result.metric_landscape.metric_trajectory.metric_points
    assert len(points) == len(input_by_id)
    assert {point.event.id for point in points} == set(input_by_id)
    assert all(
        point.offset_ms
        == pytest.approx(
            (point.event.timestamp - point.beat_reference.timestamp) * 1000.0
        )
        for point in points
    )


def test_projection_replay_is_deterministic(controlled_analyses):
    _, first, second = controlled_analyses

    assert projection_signature(first) == projection_signature(second)


def test_declared_context_does_not_change_core_observations(controlled_analyses):
    observed_only, declared, _ = controlled_analyses

    assert declared.pulse_candidates == observed_only.pulse_candidates
    assert (
        declared.candidate_period_population
        == observed_only.candidate_period_population
    )
