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
