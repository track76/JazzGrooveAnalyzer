from datetime import datetime
from uuid import uuid4

from jga.domain.metric_cluster import MetricCluster
from jga.domain.pulse import Pulse


class PulseBuilder:
    """
    Builds Pulse objects from MetricCluster objects.
    """

    def build(
        self,
        clusters: tuple[MetricCluster, ...],
    ) -> tuple[Pulse, ...]:

        if not clusters:
            return ()

        pulses = []

        for cluster in clusters:

            pulses.append(
                Pulse(
                    id=uuid4(),
                    index=cluster.beat_reference.index,
                    cluster=cluster,
                    timestamp=cluster.beat_reference.timestamp,
                    created_at=datetime.now(),
                )
            )

        return tuple(pulses)