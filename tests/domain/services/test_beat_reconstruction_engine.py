import pytest

from jga.domain.services.beat_reconstruction_engine import (
    BeatReconstructionEngine,
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
