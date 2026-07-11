from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.metric_cluster import MetricCluster


class MetricClusterBuilder:
    """
    Builds MetricCluster objects by assigning
    ElementaryMetricEvents to BeatReferences.
    """

    def __init__(
        self,
        cluster_window: float = 0.010,
    ):
        self.cluster_window = cluster_window

    def build(
        self,
        beat_references: tuple[BeatReference, ...],
        events: tuple[ElementaryMetricEvent, ...],
    ) -> tuple[MetricCluster, ...]:

        if not beat_references or not events:
            return ()

        clusters = []

        for beat in beat_references:

            assigned_events = tuple(
                event
                for event in events
                if abs(event.timestamp - beat.timestamp)
                <= self.cluster_window
            )

            if assigned_events:
                clusters.append(
                    MetricCluster(
                        id=uuid4(),
                        beat_reference=beat,
                        events=assigned_events,
                        created_at=datetime.now(),
                    )
                )

        return tuple(clusters)