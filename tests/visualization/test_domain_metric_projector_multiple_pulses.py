from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.internal_metric_timeline import InternalMetricTimeline
from jga.domain.metric_cluster import MetricCluster
from jga.domain.pulse import Pulse
from jga.visualization.domain_metric_projector import DomainMetricProjector


def make_pulse(index: int, timestamp: float, confidence: float) -> Pulse:
    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=timestamp,
        confidence=confidence,
        created_at=datetime.now(),
    )

    beat = BeatReference(
        id=uuid4(),
        index=index,
        timestamp=timestamp,
        created_at=datetime.now(),
    )

    cluster = MetricCluster(
        id=uuid4(),
        beat_reference=beat,
        events=(event,),
        created_at=datetime.now(),
    )

    return Pulse(
        id=uuid4(),
        index=index,
        cluster=cluster,
        timestamp=timestamp,
        created_at=datetime.now(),
    )


def test_projects_multiple_pulses_in_order():
    timeline = InternalMetricTimeline(
        id=uuid4(),
        pulses=(
            make_pulse(0, 1.0, 0.90),
            make_pulse(1, 2.0, 0.80),
            make_pulse(2, 3.0, 0.70),
        ),
        created_at=datetime.now(),
    )

    series = DomainMetricProjector().project(timeline)

    assert len(series.points) == 3

    assert [p.time for p in series.points] == [1.0, 2.0, 3.0]
    assert [p.value for p in series.points] == [0.90, 0.80, 0.70]
