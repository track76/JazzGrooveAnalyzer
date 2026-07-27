from datetime import datetime
from uuid import uuid4

from jga.core.stability_curve import StabilityCurve
from jga.core.stability_point import StabilityPoint

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.metric_cluster import MetricCluster

from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.engines.scientific_behaviour_geometry_engine_runner import (
    ScientificBehaviourGeometryEngineRunner,
)


def test_runner_populates_analysis_context_geometry():

    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=1.010,
        confidence=1.0,
        created_at=datetime.now(),
    )

    beat = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=1.000,
        created_at=datetime.now(),
    )

    cluster = MetricCluster(
        id=uuid4(),
        beat_reference=beat,
        events=(event,),
        created_at=datetime.now(),
    )

    context = AnalysisContext(
        audio=None,
        metric_clusters=(cluster,),
        stability_curve=StabilityCurve(
            points=[
                StabilityPoint(
                    time=1.000,
                    score=0.90,
                    window_size=10,
                )
            ]
        ),
    )

    runner = ScientificBehaviourGeometryEngineRunner()

    runner.run(context)

    assert context.scientific_geometric_plane is not None

    assert (
        context.scientific_geometric_plane.size
        == 1
    )
