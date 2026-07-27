from jga.geometry.projections import (
    DefaultMetricBehaviourProjection,
)

from jga.core.stability_curve import (
    StabilityCurve,
)

from jga.core.stability_point import (
    StabilityPoint,
)

from jga.domain.beat_reference import (
    BeatReference,
)

from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)

from datetime import datetime
from uuid import uuid4


def test_metric_behaviour_projection_creates_xy_input():

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

    curve = StabilityCurve(
        points=[
            StabilityPoint(
                time=1.000,
                score=0.90,
                window_size=10,
            )
        ]
    )

    projection = DefaultMetricBehaviourProjection()

    result = projection.project(
        event,
        beat,
        curve,
    )

    assert len(result.coordinates) == 2

    assert result.coordinates[0].name == "Metric Offset"
    assert round(result.coordinates[0].value, 6) == 10.0

    assert result.coordinates[1].name == "Metric Stability"
    assert result.coordinates[1].value == 0.90
