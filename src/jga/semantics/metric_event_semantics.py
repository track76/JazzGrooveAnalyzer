"""
Metric Event Semantics.
"""

from dataclasses import dataclass

from jga.semantics.contribution_type import ContributionType
from jga.semantics.metric_role import MetricRole
from jga.semantics.timing_behaviour import TimingBehaviour


@dataclass(frozen=True, slots=True)
class MetricEventSemantics:
    """
    Scientific semantics associated with a Metric Event.
    """

    contribution_type: ContributionType = (
        ContributionType.UNKNOWN
    )

    timing_behaviour: TimingBehaviour = (
        TimingBehaviour.UNKNOWN
    )

    metric_role: MetricRole = (
        MetricRole.UNKNOWN
    )
