from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.internal_metric_timeline import InternalMetricTimeline
from jga.domain.metric_cluster import MetricCluster
from jga.domain.pulse import Pulse
from jga.visualization.domain_metric_projector import (
    DomainMetricProjector,
)
from jga.visualization.metric_visualization_series import (
    MetricVisualizationSeries,
)


def test_projects_internal_metric_timeline_into_visualization_series():
    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=1.25,
        confidence=0.82,
        created_at=datetime.now(),
    )

    beat = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=1.25,
        created_at=datetime.now(),
    )

    cluster = MetricCluster(
        id=uuid4(),
        beat_reference=beat,
        events=(event,),
        created_at=datetime.now(),
    )

    pulse = Pulse(
        id=uuid4(),
        index=0,
        cluster=cluster,
        timestamp=1.25,
        created_at=datetime.now(),
    )

    timeline = InternalMetricTimeline(
        id=uuid4(),
        pulses=(pulse,),
        created_at=datetime.now(),
    )

    projector = DomainMetricProjector()

    series = projector.project(timeline)

    assert isinstance(
        series,
        MetricVisualizationSeries,
    )

    assert len(series.points) == 1

    point = series.points[0]

    assert point.time == 1.25
    assert point.value == 0.82
