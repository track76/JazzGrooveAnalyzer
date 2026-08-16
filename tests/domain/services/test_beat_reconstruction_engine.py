import pytest
from decimal import Decimal

from jga.domain.services.beat_reconstruction_engine import (
    BeatReconstructionEngine,
)
from jga.domain.declared_metric_reference import (
    DeclaredMetricReference,
    MetricReferenceProvenance,
)


def test_engine_can_be_instantiated():
    assert BeatReconstructionEngine() is not None


def test_build_requires_events():
    engine = BeatReconstructionEngine()

    with pytest.raises(TypeError):
        engine.reconstruct()


def test_empty_events_return_empty_tuple():
    engine = BeatReconstructionEngine()

    assert engine.reconstruct(()) == ()


def declared_reference(bpm: str = "78") -> DeclaredMetricReference:
    return DeclaredMetricReference(
        beats_per_minute=Decimal(bpm),
        beat_unit="quarter",
        provenance=MetricReferenceProvenance(
            source_id="GT-VAL-001-v1",
            source_kind="authoritative controlled-source context",
            source_sha256=(
                "809a6ef276c4c3b9042c71d40a71763d"
                "cbf90d47e654e784af371eb53d073778"
            ),
            temporal_scope="complete controlled performance",
        ),
    )


from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent


def test_single_event_reconstructs_single_beat_reference():

    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=1.25,
        confidence=1.0,
        created_at=datetime.now(),
    )

    beats = BeatReconstructionEngine().reconstruct(
        (event,),
    )

    assert len(beats) == 1

    assert isinstance(
        beats[0],
        BeatReference,
    )

    assert beats[0].timestamp == 1.25

from jga.domain.services.beat_reference_builder import (
    BeatReferenceBuilder,
)


def test_engine_matches_current_builder():

    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=1.25,
        confidence=1.0,
        created_at=datetime.now(),
    )

    builder_beats = BeatReferenceBuilder().build(
        (event,),
    )

    engine_beats = BeatReconstructionEngine().reconstruct(
        (event,),
    )

    assert len(engine_beats) == len(builder_beats)

    assert engine_beats[0].index == builder_beats[0].index
    assert engine_beats[0].timestamp == builder_beats[0].timestamp


def test_each_event_generates_one_initial_beat():

    events = (
        ElementaryMetricEvent(
            id=uuid4(),
            contributor_id=uuid4(),
            timestamp=1.0,
            confidence=1.0,
            created_at=datetime.now(),
        ),
        ElementaryMetricEvent(
            id=uuid4(),
            contributor_id=uuid4(),
            timestamp=2.0,
            confidence=1.0,
            created_at=datetime.now(),
        ),
        ElementaryMetricEvent(
            id=uuid4(),
            contributor_id=uuid4(),
            timestamp=3.0,
            confidence=1.0,
            created_at=datetime.now(),
        ),
    )

    beats = BeatReconstructionEngine().reconstruct(events)

    assert len(beats) == len(events)


def test_declared_metric_reference_controls_period_but_not_observed_origin():
    events = tuple(
        ElementaryMetricEvent(
            id=uuid4(),
            contributor_id=uuid4(),
            timestamp=timestamp,
            confidence=1.0,
            created_at=datetime.now(),
        )
        for timestamp in (1.25, 1.9, 2.7)
    )

    beats = BeatReconstructionEngine().reconstruct(
        events,
        declared_metric_reference=declared_reference(),
    )

    expected_period = 60.0 / 78.0
    assert beats[0].timestamp == 1.25
    assert beats[1].timestamp == pytest.approx(1.25 + expected_period)
    assert beats[2].timestamp == pytest.approx(1.25 + 2 * expected_period)


from jga.domain.services.beat_period_estimator import (
    BeatPeriodEstimator,
)


def test_engine_uses_period_estimator():

    engine = BeatReconstructionEngine()

    assert isinstance(
        engine._period_estimator,
        BeatPeriodEstimator,
    )


from jga.domain.services.beat_grid_reconstructor import (
    BeatGridReconstructor,
)


def test_engine_uses_grid_reconstructor():

    engine = BeatReconstructionEngine()

    assert isinstance(
        engine._grid_reconstructor,
        BeatGridReconstructor,
    )
