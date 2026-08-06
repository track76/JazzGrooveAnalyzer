from jga.semantics.contribution_type import (
    ContributionType,
)
from jga.semantics.metric_event_semantics import (
    MetricEventSemantics,
)
from jga.semantics.metric_role import (
    MetricRole,
)
from jga.semantics.timing_behaviour import (
    TimingBehaviour,
)


def test_default_semantics():

    semantics = MetricEventSemantics()

    assert (
        semantics.contribution_type
        is ContributionType.UNKNOWN
    )

    assert (
        semantics.timing_behaviour
        is TimingBehaviour.UNKNOWN
    )

    assert (
        semantics.metric_role
        is MetricRole.UNKNOWN
    )
