from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import (
    BeatReference,
)

from jga.reporting.builders.analytical_beat_builder import (
    AnalyticalBeatBuilder,
)


def test_build_from_beat_reference_preserves_temporal_reference():

    reference = BeatReference(

        id=uuid4(),

        index=3,

        timestamp=1.5,

        created_at=datetime.now(),

    )

    builder = AnalyticalBeatBuilder()

    beat = builder.build_from_reference(
        reference
    )

    assert beat.number == 3

    assert beat.timestamp_seconds == 1.5

    assert beat.cells == ()


def test_build_assigns_local_beat_number():

    from datetime import datetime
    from uuid import uuid4

    from jga.domain.beat_reference import (
        BeatReference,
    )


    reference = BeatReference(

        id=uuid4(),

        index=17,

        timestamp=5.0,

        created_at=datetime.now(),

    )


    builder = AnalyticalBeatBuilder()


    beat = builder.build(

        reference,

        number=2,

    )


    assert beat.number == 2

    assert beat.timestamp_seconds == 5.0


def test_build_populates_cells_from_metric_cluster():

    from datetime import datetime
    from uuid import uuid4

    from jga.domain.beat_reference import (
        BeatReference,
    )

    from jga.domain.elementary_metric_event import (
        ElementaryMetricEvent,
    )

    from jga.domain.metric_cluster import (
        MetricCluster,
    )

    from jga.reporting.builders.analytical_beat_builder import (
        AnalyticalBeatBuilder,
    )


    beat_reference = BeatReference(

        id=uuid4(),

        index=2,

        timestamp=1.0,

        created_at=datetime.now(),

    )


    event = ElementaryMetricEvent(

        id=uuid4(),

        contributor_id=uuid4(),

        timestamp=1.010,

        confidence=1.0,

        created_at=datetime.now(),

    )


    cluster = MetricCluster(

        id=uuid4(),

        beat_reference=beat_reference,

        events=(event,),

        created_at=datetime.now(),

    )


    builder = AnalyticalBeatBuilder()


    beat = builder.build(

        reference=beat_reference,

        number=3,

        metric_cluster=cluster,

    )


    assert beat.number == 3

    assert len(beat.cells) == 1

    assert (
        beat.cells[0]
        .absolute_time_seconds
        == 1.010
    )
