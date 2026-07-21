from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.services.beat_reference_builder import BeatReferenceBuilder


def test_build_beat_references():

    events = (
        ElementaryMetricEvent(
            id=uuid4(),
            contributor_id=uuid4(),
            timestamp=0.000,
            confidence=1.0,
            created_at=datetime.now(),
        ),
        ElementaryMetricEvent(
            id=uuid4(),
            contributor_id=uuid4(),
            timestamp=1.000,
            confidence=1.0,
            created_at=datetime.now(),
        ),
    )

    beats = BeatReferenceBuilder().build(events)

    assert len(beats) == 2
    assert isinstance(beats[0], BeatReference)
    assert beats[0].index == 0
    assert beats[1].index == 1
